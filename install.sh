#!/usr/bin/env bash
# Install the `pycoach` command by linking bin/pycoach onto your PATH.
#
#   ./install.sh
#
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Prefer a bin folder that is already on your PATH.
if [ -n "${PREFIX:-}" ] && [ -d "$PREFIX/bin" ]; then
    BIN="$PREFIX/bin"
elif [ -d "$HOME/.local/bin" ]; then
    BIN="$HOME/.local/bin"
else
    BIN="$HOME/bin"
    mkdir -p "$BIN"
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 was not found on your PATH."
    echo "Termux: run 'pkg install python' and try again."
    exit 1
fi

chmod +x "$HERE/bin/pycoach" "$HERE/pycoach.py" "$HERE/_runner.py" 2>/dev/null || true
ln -sf "$HERE/bin/pycoach" "$BIN/pycoach"

echo "Installed: $BIN/pycoach"
echo "           -> $HERE/bin/pycoach"
echo

case ":$PATH:" in
    *":$BIN:"*) ;;
    *)
        echo "One more thing - $BIN is not on your PATH yet."
        echo "Add this line to ~/.bashrc and restart your shell:"
        echo
        echo "    export PATH=\"$BIN:\$PATH\""
        echo
        ;;
esac

echo "Start it with:  pycoach"
