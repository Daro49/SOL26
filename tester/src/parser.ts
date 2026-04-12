
import type { TestCaseDefinition } from "./models.js";

export interface TestCase {
  definition: TestCaseDefinition;
  sourceCode: string;
  expectedStdout: string | null;
}

export interface ParsedTest {
    description: string | null;
    category: string | null;
    points: number | null;
    parserExitCodes: number[] | [];
    interpreterExitCodes: number[] | [],
    source: string | null
}

export function isInXML(source: string): boolean {
    return source.trimStart().startsWith("<");
}

export function parseFile(file: string): ParsedTest {

    const lines = file.split("\n");

    let description: string | null = null;
    let category: string | null = null;
    const parserExitCodes: number[] = [];
    const interpreterExitCodes: number[] = [];
    let points: number | null = null;

    let sourceStart = 0;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        

        if (line?.trim() === "") {
            sourceStart = i;
            break;
        }

        if (line?.startsWith("***")) {
            description = line.slice(3).trim();
        }

        else if (line?.startsWith("+++")) {
            category = line.slice(3).trim();
        }

        else if (line?.startsWith(">>>")) {
            const _number = parseInt(line.slice(3).trim());
            if (!isNaN(_number)) points = _number;
        }

        else if (line?.startsWith("!C!")) {
            const _number = parseInt(line.slice(3).trim());
            if (!isNaN(_number)) parserExitCodes.push(_number);
        }

        else if (line?.startsWith("!I!")) {
            const _number = parseInt(line.slice(3).trim());
            if (!isNaN(_number)) interpreterExitCodes.push(_number);
        }
    }

    const sourceLines = sourceStart > 0 ? lines.slice(sourceStart) : [];

    return {
        description,
        category,
        points,
        parserExitCodes,
        interpreterExitCodes,
        source: sourceLines.join("\n")
    }
}