#!/bin/bash

INSTALL_DIR="/usr/local/bin"
TOOL_NAME="bioutils"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$SCRIPT_DIR/.venv/" ]; then
    python3 -m virtualenv "$SCRIPT_DIR/.venv"
fi

source "$SCRIPT_DIR/.venv/bin/activate"

pip install matplotlib streamlit mpld3 pandas

deactivate

WRAPPER_SCRIPT="$INSTALL_DIR/$TOOL_NAME"
cat <<EOL > "$WRAPPER_SCRIPT"
#!/bin/bash
cd "$SCRIPT_DIR"
source .venv/bin/activate
python3 cli.py "\$@"
deactivate
EOL

chmod +x "$WRAPPER_SCRIPT"

echo "Installation complete. You can run the tool using '$TOOL_NAME'."
