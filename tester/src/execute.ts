
import { spawnSync } from "node:child_process";
import { writeFileSync, existsSync, unlinkSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { randomBytes } from "node:crypto";
import { Logger } from "pino";

import {
  TestCaseType,
  TestCaseReport,
  TestResult,
  UnexecutedReason,
  UnexecutedReasonCode,
} from "./models.js";
import { TestCase } from "./parser.js";


export interface ExecutorConfig {
    parserBin:      string;
    interpreterBin: string;
    logger:         Logger;
}

interface ProcessResult {
    exitCode: number;
    stdout:   string;
    stderr:   string;
    failed:   boolean;
}

function runProcess(
    bin:       string,
    args:      string[],
    logger:    Logger
    ): ProcessResult {

    logger.debug("Running: %s %s", bin, args.join(" "));

    const result = spawnSync(bin, args, {
        encoding:  "utf8",
        maxBuffer: 8 * 1024 * 1024,
    });

    if (result.error) {
        logger.warn("Failed to spawn %s: %s", bin, result.error.message);
        return { exitCode: -1, stdout: "", stderr: result.error.message, failed: true };
    }

    return {
        exitCode: result.status ?? -1,
        stdout:   result.stdout ?? "",
        stderr:   result.stderr ?? "",
        failed:   false,
    };
}


function writeTempFile(content: string, suffix: string): string {

    const path = join(tmpdir(), `sol26_${randomBytes(6).toString("hex")}${suffix}`);
    writeFileSync(path, content, "utf8");

    return path;
}


function diffStrings(expected: string, actual: string): string | null {

    const expectedFile = writeTempFile(expected, "_expected");
    const actualFile   = writeTempFile(actual,   "_actual");

    try {
        const result = spawnSync("diff", [expectedFile, actualFile], { encoding: "utf8" });

        if (result.status === 0) return null;
        
        return result.stdout || result.stderr || "(diff returned non-zero with no output)";
    }
    
    finally {
        if (existsSync(expectedFile)) unlinkSync(expectedFile);
        if (existsSync(actualFile))   unlinkSync(actualFile);
    }
}


function executeParseOnly(
    tc:     TestCase,
    config: ExecutorConfig
    ): TestCaseReport | UnexecutedReason {

    const sourceFile = writeTempFile(tc.sourceCode, ".sol");

    try {
        const r = runProcess(config.parserBin, [sourceFile, ">temp.xml"], config.logger);

        if (r.failed)
            return new UnexecutedReason(UnexecutedReasonCode.CANNOT_EXECUTE, `Parser could not be executed: ${r.stderr}`);

        if (!tc.definition.expected_parser_exit_codes!.includes(r.exitCode))
            return new TestCaseReport(TestResult.UNEXPECTED_PARSER_EXIT_CODE, r.exitCode, null, r.stdout, r.stderr);

        return new TestCaseReport(TestResult.PASSED, r.exitCode, null, r.stdout, r.stderr);
    }
    
    finally {
        if (existsSync(sourceFile)) unlinkSync(sourceFile);
    }
}

function executeInterpretOnly(
    tc:     TestCase,
    config: ExecutorConfig
    ): TestCaseReport | UnexecutedReason {

    const sourceFile = writeTempFile(tc.sourceCode, ".xml");

    try {
        const r = runProcess(config.interpreterBin, ["--source", sourceFile], config.logger);

        if (r.failed)
            return new UnexecutedReason(UnexecutedReasonCode.CANNOT_EXECUTE, `Interpreter could not be executed: ${r.stderr}`);

        if (!tc.definition.expected_interpreter_exit_codes!.includes(r.exitCode))
            return new TestCaseReport(TestResult.UNEXPECTED_INTERPRETER_EXIT_CODE, null, r.exitCode, null, null, r.stdout, r.stderr);

        if (r.exitCode === 0 && tc.expectedStdout !== null) {
            const diff = diffStrings(tc.expectedStdout, r.stdout);
            if (diff !== null)
                return new TestCaseReport(TestResult.INTERPRETER_RESULT_DIFFERS, null, r.exitCode, null, null, r.stdout, r.stderr, diff);
        }

        return new TestCaseReport(TestResult.PASSED, null, r.exitCode, null, null, r.stdout, r.stderr);
    }
    
    finally {
        if (existsSync(sourceFile)) unlinkSync(sourceFile);
    }
}

function executeCombined(
    tc:     TestCase,
    config: ExecutorConfig
    ): TestCaseReport | UnexecutedReason {

    let parser_cli: string[] = [tc.sourceCode, ">temp.xml"];

    
    // SOL to XML

    const pr = runProcess(config.parserBin, parser_cli, config.logger);

    if (pr.failed)
        return new UnexecutedReason(UnexecutedReasonCode.CANNOT_EXECUTE, `Parser could not be executed: ${pr.stderr}`);

    if (pr.exitCode !== 0)
        return new TestCaseReport(TestResult.UNEXPECTED_PARSER_EXIT_CODE, pr.exitCode, null, pr.stdout, pr.stderr);

    // XML to Output
    let interpreter_cli: string [] = ["--source", "temp.xml"];

    if (tc.definition.stdin_file != null) {
        parser_cli.push("--input", tc.definition.stdin_file);
    }

    const ir = runProcess(config.interpreterBin, interpreter_cli, config.logger);

    if (ir.failed)
        return new UnexecutedReason(UnexecutedReasonCode.CANNOT_EXECUTE, `Interpreter could not be executed: ${ir.stderr}`);

    if (!tc.definition.expected_interpreter_exit_codes!.includes(ir.exitCode))
        return new TestCaseReport(TestResult.UNEXPECTED_INTERPRETER_EXIT_CODE, pr.exitCode, ir.exitCode, pr.stdout, pr.stderr, ir.stdout, ir.stderr);

    if (ir.exitCode === 0 && tc.expectedStdout !== null) {
        const diff = diffStrings(tc.expectedStdout, ir.stdout);

        if (diff !== null)
            return new TestCaseReport(TestResult.INTERPRETER_RESULT_DIFFERS, pr.exitCode, ir.exitCode, pr.stdout, pr.stderr, ir.stdout, ir.stderr, diff);
    }

    return new TestCaseReport(TestResult.PASSED, pr.exitCode, ir.exitCode, pr.stdout, pr.stderr, ir.stdout, ir.stderr); 
}

/**
 * Executes a single LoadedTestCase and returns either a TestCaseReport
 * (the test ran, pass or fail) or an UnexecutedReason (it could not run).
 *
 * No file reads are performed here. All content comes from `tc`.
 */
export function executeTestCase(
    tc:     TestCase,
    config: ExecutorConfig
    ): TestCaseReport | UnexecutedReason {

    switch (tc.definition.test_type) {
        case TestCaseType.PARSE_ONLY:    return executeParseOnly(tc, config);

        case TestCaseType.EXECUTE_ONLY:  return executeInterpretOnly(tc, config);

        case TestCaseType.COMBINED:      return executeCombined(tc, config);
        
        // default: throw new Error(`Unknown test type: ${tc.definition.test_type}`);
    }
}