import { readdirSync, existsSync, readFileSync, statSync } from "node:fs";
import { join, basename, dirname } from "node:path";
import { Logger } from "pino";

import {
  TestCaseDefinition,
  TestCaseType,
  UnexecutedReason,
  UnexecutedReasonCode,
} from "./models.js";

import { parseFile, isInXML, TestCase } from "./parser.js";

export interface findResult {
  tests: TestCase[];
  unexecuted: Record<string, UnexecutedReason>;
}

export function findTestCases(testsDir: string, recursive: boolean, logger: Logger): findResult {
  const tests: TestCase[] = [];
  const unexecuted: Record<string, UnexecutedReason> = {};

  logger.info("Trying to find files in: %s", testsDir)
  const testFiles = findFiles(testsDir, recursive);
  logger.info("Discovered %d .test file(s)", testFiles.length);

  for (const testPath of testFiles) {
    const fileName = basename(testPath);
    const name = fileName.replace(/\.test$/, "");
    const dir = dirname(testPath);

    // .in and .out existence
    const inPath = join(dir, name + ".in");
    const stdinFile = existsSync(inPath) ? inPath : null;

    const outPath = join(dir, name + ".out");
    const expectedStdout = existsSync(outPath) ? readFileSync(outPath, "utf8") : null;

    // parse the file itself
    let parsed;

    try {
      const raw = readFileSync(testPath, "utf8");
      parsed = parseFile(raw);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);

      unexecuted[name] = new UnexecutedReason(
        UnexecutedReasonCode.MALFORMED_TEST_CASE_FILE,
        `Could not read or parse file: ${msg}`
      );

      continue;
    }

    // validate required
    if (!parsed.category) {
      unexecuted[name] = new UnexecutedReason(
        UnexecutedReasonCode.MALFORMED_TEST_CASE_FILE,
        "Missing required '+++' category tag"
      );

      continue;
    }

    if (parsed.points === null) {
      unexecuted[name] = new UnexecutedReason(
        UnexecutedReasonCode.MALFORMED_TEST_CASE_FILE,
        "Missing required '>>>' points tag"
      );

      continue;
    }

    if (parsed.source == null) {
      unexecuted[name] = new UnexecutedReason(
        UnexecutedReasonCode.MALFORMED_TEST_CASE_FILE,
        "Missing required source code"
      );

      continue;
    }

    const hasParserCodes = parsed.parserExitCodes.length > 0;
    const hasInterpreterCodes = parsed.interpreterExitCodes.length > 0;
    const xmlSource = isInXML(parsed.source);

    const testType = determineTestType(hasParserCodes, hasInterpreterCodes, xmlSource);

    if (testType === null) {
      unexecuted[name] = new UnexecutedReason(
        UnexecutedReasonCode.CANNOT_DETERMINE_TYPE,
        `Cannot determine test type`
      );

      continue;
    }

    let definition: TestCaseDefinition;

    // try because of validateExitCodes()
    try {
      definition = new TestCaseDefinition({
        name: name,
        test_source_path: testPath,
        stdin_file: stdinFile,
        expected_stdout_file: expectedStdout !== null ? outPath : null,

        test_type: testType,
        description: parsed.description,
        category: parsed.category,
        points: parsed.points,
        expected_parser_exit_codes: hasParserCodes ? parsed.parserExitCodes : null,

        expected_interpreter_exit_codes: hasInterpreterCodes ? parsed.interpreterExitCodes : null,
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);

      unexecuted[name] = new UnexecutedReason(UnexecutedReasonCode.MALFORMED_TEST_CASE_FILE, msg);

      continue;
    }

    const testUnit: TestCase = {
      definition,
      sourceCode: parsed.source,
      expectedStdout,
    };

    tests.push(testUnit);
  }

  return { tests, unexecuted };
}

function findFiles(dir: string, recursive: boolean): string[] {
  const results: string[] = [];

  for (const entry of readdirSync(dir)) {

    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);

    if (stat.isDirectory() && recursive) {
      results.push(...findFiles(fullPath, recursive));
    } else if (stat.isFile() && entry.endsWith(".test")) {
      results.push(fullPath);
    }
  }

  return results;
}

function determineTestType(
  hasParserCodes: boolean,
  hasInterpreterCodes: boolean,
  isXml: boolean
): TestCaseType | null {
  if (hasParserCodes && !hasInterpreterCodes) {
    return TestCaseType.PARSE_ONLY;
  }

  if (!hasParserCodes && hasInterpreterCodes && isXml) {
    return TestCaseType.EXECUTE_ONLY;
  }

  if (hasInterpreterCodes && !isXml) {
    return TestCaseType.COMBINED;
  }

  return null;
}
