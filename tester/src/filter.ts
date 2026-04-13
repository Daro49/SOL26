import { TestCaseDefinition, UnexecutedReason, UnexecutedReasonCode } from "./models.js";
import { TestCase } from "./parser.js";

export interface FilterCriteria {
  include: string[] | null;
  include_category: string[] | null;
  include_test: string[] | null;
  exclude: string[] | null;
  exclude_category: string[] | null;
  exclude_test: string[] | null;
  regex: boolean;
}

export interface FilterResult {
  include: TestCase[];
  exclude: Record<string, UnexecutedReason>;
}

export function filterTestCases(testCase: TestCase[], criteria: FilterCriteria): FilterResult {
  const included: TestCase[] = [];
  const filteredOut: Record<string, UnexecutedReason> = {};

  for (const test of testCase) {
    if (shouldInclude(test.definition, criteria)) {
      included.push(test);
    } else {
      filteredOut[test.definition.name] = new UnexecutedReason(
        UnexecutedReasonCode.FILTERED_OUT,
        "Test case was excluded by the provided filter criteria."
      );
    }
  }

  return { include: included, exclude: filteredOut };
}

function matches(value: string, patterns: string[], useRegex: boolean): boolean {
  if (useRegex) {
    return patterns.some((p) => new RegExp(p).test(value));
  }

  return patterns.includes(value);
}

function shouldInclude(def: TestCaseDefinition, criteria: FilterCriteria): boolean {
  const { regex } = criteria;

  const isMatch = (val: string, patterns: string[] | null) =>
    patterns ? matches(val, patterns, regex) : false;

  // Exclude
  const excludeRules = [
    () => isMatch(def.name, criteria.exclude),
    () => isMatch(def.category, criteria.exclude),
    () => isMatch(def.category, criteria.exclude_category),
    () => isMatch(def.name, criteria.exclude_test),
  ];

  if (excludeRules.some((rule) => rule())) {
    return false;
  }

  const hasInclusionFilters =
    criteria.include || criteria.include_category || criteria.include_test;

  if (!hasInclusionFilters) {
    return true;
  }

  // Include
  const includeRules = [
    () => isMatch(def.name, criteria.include),
    () => isMatch(def.category, criteria.include),
    () => isMatch(def.category, criteria.include_category),
    () => isMatch(def.name, criteria.include_test),
  ];

  return includeRules.some((rule) => rule());
}
