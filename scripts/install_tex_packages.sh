#!/bin/bash
# Install missing TinyTeX packages required by Phase 2.
TLMGR="${TLMGR:-tlmgr}"
REPO="https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2021/tlnet-final"
"$TLMGR" --repository "$REPO" install amsthm makecell caption listings microtype parskip xurl upquote footnotehyper pdflscape 2>&1
echo "---"
echo "Verifying installs..."
for pkg in amsthm makecell caption listings microtype parskip xurl upquote footnotehyper natbib lscape pdflscape rotating; do
  out=$(kpsewhich $pkg.sty 2>&1)
  if [ -z "$out" ]; then
    echo "MISSING: $pkg"
  else
    echo "OK: $pkg -> $out"
  fi
done
