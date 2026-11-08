#!/usr/bin/env bash
# Run the test suite and build a single-file Allure report.
#
# Usage:
#   ./run_test.sh                      # run all tests, build report, open it
#   ./run_test.sh --headed             # extra args are passed to pytest
#   ./run_test.sh -m guest             # only tests marked "guest"
#   ./run_test.sh -k GD02              # filter by test name
#   ./run_test.sh --no-open            # build report but do not open it (CI)
#   ./run_test.sh --no-report          # run tests only
#   ./run_test.sh --report-only        # rebuild report from existing allure-results

set -uo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

RESULTS_DIR="allure-results"
REPORT_DIR="allure-report"
OPEN_REPORT=1
BUILD_REPORT=1
RUN_TESTS=1
PYTEST_ARGS=()

for arg in "$@"; do
  case "$arg" in
    --no-open)     OPEN_REPORT=0 ;;
    --no-report)   BUILD_REPORT=0; OPEN_REPORT=0 ;;
    --report-only) RUN_TESTS=0 ;;
    -h|--help)     sed -n '2,12p' "$0"; exit 0 ;;
    *)             PYTEST_ARGS+=("$arg") ;;
  esac
done

# --- pre-checks --------------------------------------------------------------
if [[ ! -f .env ]]; then
  echo "❌ .env not found. Run: cp .env.example .env  and fill in the credentials."
  exit 2
fi

if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
PYTHON="${PYTHON:-$(command -v python3 || command -v python)}"

# --- run tests ---------------------------------------------------------------
TEST_STATUS=0
if [[ $RUN_TESTS -eq 1 ]]; then
  echo "▶ Running pytest ${PYTEST_ARGS[*]:-}"
  "$PYTHON" -m pytest --alluredir="$RESULTS_DIR" --clean-alluredir ${PYTEST_ARGS[@]+"${PYTEST_ARGS[@]}"}
  TEST_STATUS=$?
fi

# --- build report ------------------------------------------------------------
if [[ $BUILD_REPORT -eq 1 ]]; then
  if ! command -v allure >/dev/null 2>&1; then
    echo "⚠ Allure CLI not found (macOS: brew install allure). Skipping report."
    exit $TEST_STATUS
  fi
  echo "▶ Generating single-file Allure report → $REPORT_DIR/index.html"
  allure generate "$RESULTS_DIR" --clean --single-file -o "$REPORT_DIR" || exit 1

  if [[ $OPEN_REPORT -eq 1 ]]; then
    if command -v open >/dev/null 2>&1; then
      open "$REPORT_DIR/index.html"            # macOS
    elif command -v xdg-open >/dev/null 2>&1; then
      xdg-open "$REPORT_DIR/index.html"        # Linux
    else
      echo "Open $ROOT_DIR/$REPORT_DIR/index.html in your browser."
    fi
  fi
fi

exit $TEST_STATUS
