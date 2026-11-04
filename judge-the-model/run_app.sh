#!/usr/bin/env bash
# Start the Streamlit app on this computer only (this does not publish anything; see SETUP.md).
#
#   bash run_app.sh        then open http://localhost:8501 ; stop with Ctrl+C
#
# It installs nothing and never runs git. If a prerequisite is missing it says what to do.

set -euo pipefail

PORT=8501

# 1. Work from the folder this script lives in, wherever it is run from.
cd "$(dirname "${BASH_SOURCE[0]}")"

stop() {
  echo "Cannot start the app: $1" >&2
  exit 1
}

# 2. Find the project's Python: .venv first (Mac/Linux, then Windows), else the active python.
if [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
elif [ -x ".venv/Scripts/python.exe" ]; then
  PY=".venv/Scripts/python.exe"
elif command -v python3 >/dev/null 2>&1; then
  PY="python3"
  echo "Note: no .venv found; using the active python3."
elif command -v python >/dev/null 2>&1; then
  PY="python"
  echo "Note: no .venv found; using the active python."
else
  stop "no Python found. Create the environment first: uv venv, then uv pip install -r requirements.txt"
fi

# 3. Check the prerequisites.
[ -f "streamlit_app.py" ] || stop "streamlit_app.py is missing from $(pwd)."
[ -f "m11.py" ] || stop "m11.py is missing from $(pwd); restore it from the starter."
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' \
  || stop "$("$PY" --version 2>&1) is too old; the project needs Python 3.11 or newer (recreate .venv with uv)."
"$PY" -c 'import streamlit, pandas' 2>/dev/null \
  || stop "Streamlit or pandas is not installed for $PY. Run: uv pip install -r requirements.txt"
[ -d "results" ] || echo "Note: results/ is missing; the app will have nothing to show until you run python -m analysis."

# 4. Start the app. exec hands the terminal to Streamlit, so Ctrl+C stops it directly.
echo "Starting Judge the Model with $PY"
echo "Open this address in your browser:  http://localhost:$PORT"
echo "Stop the app with Ctrl+C."
exec "$PY" -m streamlit run streamlit_app.py \
  --server.port "$PORT" \
  --server.headless true \
  --browser.gatherUsageStats false
