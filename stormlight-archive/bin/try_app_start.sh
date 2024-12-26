#!/usr/bin/env bash

set -x
# setup direnv based venv use.
eval "$(direnv export bash)"

# startup server-tasks...

# glowforge logging. Output will come back to this pty, which also goes to balena OR
# to a logged in user if starting from an ssh-in for development.
gfl_server&


PBB_CMD='eval "$(direnv export bash)"; python display/tui_entry.py'
uxterm -fullscreen -e "$PBB_CMD ; sleep 10"

# If we come back, nuke gfl so we can restart cleanly.
kill %1
