set -e

black --check --diff fmpsdk/ tests/
isort --check-only --diff fmpsdk/ tests/
# stop the build if there are Python syntax errors or undefined names
flake8 fmpsdk/ --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
flake8 fmpsdk/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
mypy fmpsdk/ --ignore-missing-imports --no-strict-optional
pytest