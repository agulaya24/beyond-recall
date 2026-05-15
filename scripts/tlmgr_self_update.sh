#!/bin/bash
TLMGR="${TLMGR:-tlmgr}"
REPO="https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2021/tlnet-final"
LOG="/tmp/tlmgr_self.log"
"$TLMGR" --repository "$REPO" update --self > "$LOG" 2>&1
echo "exit=$?"
tail -50 "$LOG"
