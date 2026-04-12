
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


export function filterTestCases(
    testCase: TestCase[],
    criteria: FilterCriteria
    ): FilterResult {

    const included: TestCase[] = [];
    const filteredOut: Record<string, UnexecutedReason> = {};

    for (const test of testCase) {
        
        if (shouldInclude(test.definition, criteria)) {
            included.push(test);
        }
        
        else {
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
    
    const { include, include_category, include_test, exclude, exclude_category, exclude_test, regex } = criteria;

    // exclude first
    if (exclude !== null) {
        if (matches(def.name, exclude, regex) ||
            matches(def.category, exclude, regex)) {
        
            return false;
        }
    }

    if (exclude_category !== null && matches(def.category, exclude_category, regex)) {
        return false;
    }

    if (exclude_test !== null && matches(def.name, exclude_test, regex)) {
        return false;
    }

    // then include
    const hasInclusionFilter = include !== null || include_category !== null || include_test !== null;

    if (!hasInclusionFilter) {
        return true;
    }

    if (include !== null) {
        if (matches(def.name, include, regex) ||
            matches(def.category, include, regex)) {

        return true;
        }
    }

    if (include_category !== null && matches(def.category, include_category, regex)) {
        return true;
    }

    if (include_test !== null && matches(def.name, include_test, regex)) {
        return true;
    }

    return false;
}