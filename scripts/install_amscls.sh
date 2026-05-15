#!/bin/bash
TLMGR="${TLMGR:-tlmgr}"
REPO="https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2021/tlnet-final"
"$TLMGR" --repository "$REPO" install amscls 2>&1
echo "---"
kpsewhich amsthm.sty
