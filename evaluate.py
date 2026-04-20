#!/usr/bin/env python3
import json
import sys
import os

# Farby pre terminál
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def evaluate_json(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {filepath} is not a valid JSON.")
            return

    file_basename = os.path.basename(filepath)
    print(f"\n{BOLD}REPORT SUMMARY: {file_basename}{RESET}")
    print("=" * 70)
    print(f"{'CATEGORY':<15} | {'TEST NAME':<35} | {'STATUS':<15}")
    print("-" * 70)

    total_pts = 0
    passed_pts = 0

    # 1. Spracovanie výsledkov podľa kategórií
    results = data.get('results', {})
    if results:
        for cat_name, cat_data in results.items():
            total_pts += cat_data.get('total_points', 0)
            passed_pts += cat_data.get('passed_points', 0)
            
            for test_name, test_info in cat_data.get('test_results', {}).items():
                res = test_info.get('result')
                
                if res == "passed":
                    status = f"{GREEN}✅ PASSED{RESET}"
                elif res == "diff_fail":
                    status = f"{RED}❌ DIFF FAIL{RESET}"
                elif res == "int_fail":
                    status = f"{RED}❌ INT FAIL{RESET}"
                elif res == "parse_fail":
                    status = f"{RED}❌ PARSE FAIL{RESET}"
                else:
                    status = f"{YELLOW}❓ {res.upper()}{RESET}"

                print(f"{cat_name[:15]:<15} | {test_name[:35]:<35} | {status}")

    # 2. Spracovanie nespustených testov (Unexecuted)
    unexecuted = data.get('unexecuted', {})
    if unexecuted:
        for test_name, reason_obj in unexecuted.items():
            reason = reason_obj.get('reason', 'UNKNOWN ERROR')
            print(f"{'ERROR':<15} | {test_name[:35]:<35} | {RED}🚫 {reason}{RESET}")

    print("-" * 70)
    
    # Percentuálna úspešnosť
    score_str = f"{passed_pts}/{total_pts}"
    percent = (passed_pts / total_pts * 100) if total_pts > 0 else 0
    
    color = GREEN if percent == 100 else (YELLOW if percent > 0 else RED)
    print(f"{BOLD}FINAL SCORE: {color}{score_str} points ({percent:.1f}%){RESET}")
    print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Ak nie je zadaný súbor, skús spracovať všetky report_*.json v aktuálnom priečinku
        import glob
        files = glob.glob("report_*.json")
        if not files:
            print("Usage: python3 evaluate.py <report.json> alebo report_*.json súbory v priečinku.")
        else:
            for f in sorted(files):
                evaluate_json(f)
    else:
        evaluate_json(sys.argv[1])