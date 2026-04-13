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
  parserExitCodes: number[];
  interpreterExitCodes: number[];
  source: string | null;
}

export function isInXML(source: string): boolean {
  return source.trimStart().startsWith("<");
}

export function parseFile(file: string): ParsedTest {
  const lines = file.split("\n");
  const headerEndIndex = lines.findIndex((line) => line.trim() === "");

  const headerLines = headerEndIndex === -1 ? lines : lines.slice(0, headerEndIndex);
  const sourceLines = headerEndIndex === -1 ? [] : lines.slice(headerEndIndex + 1);

  const result: ParsedTest = {
    description: null,
    category: null,
    points: null,
    parserExitCodes: [],
    interpreterExitCodes: [],
    source: sourceLines.join("\n"),
  };

  const handlers: Record<string, (val: string) => void> = {
    "***": (v) => (result.description = v),
    "+++": (v) => (result.category = v),
    ">>>": (v) => {
      const n = parseInt(v);
      if (!isNaN(n)) result.points = n;
    },
    "!C!": (v) => {
      const n = parseInt(v);
      if (!isNaN(n)) result.parserExitCodes.push(n);
    },
    "!I!": (v) => {
      const n = parseInt(v);
      if (!isNaN(n)) result.interpreterExitCodes.push(n);
    },
  };

  for (const line of headerLines) {
    const prefix = line.slice(0, 3);
    const content = line.slice(3).trim();
    handlers[prefix]?.(content);
  }

  return result;
}
