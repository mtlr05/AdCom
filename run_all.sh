#!/usr/bin/env bash
# Rebuild everything offline from data/: cur -> final -> report -> charts -> consistency check.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/data"
export PYTHONPATH="$HERE/scripts" ADCOM_SCRIPTS="$HERE/scripts" CHART_DIR="$HERE/charts"
python3 "$HERE/scripts/cur.py"
python3 "$HERE/scripts/final.py"
python3 "$HERE/scripts/report.py"
python3 "$HERE/scripts/four.py"
python3 "$HERE/scripts/four_pct.py"
python3 "$HERE/scripts/four_cgt.py"
python3 "$HERE/scripts/cgt_tables.py"
python3 "$HERE/tests/check_consistency.py"
echo "run_all.sh: OK"
