# Base Layer (vendored, v0.2.0)

This directory contains a frozen copy of Base Layer at version 0.2.0, the snapshot referenced by the Beyond Recall paper. It is bundled here so that paper readers can reproduce the pipeline without depending on a separate repository or package registry.

This copy is intentionally not synced with active Base Layer development. For the latest version, ongoing changes, issues, and discussion, see:

- Active repository: https://github.com/agulaya24/BaseLayer
- Live version (0.3.0+): includes a partial-serving MCP design and other refinements that postdate the paper

## Installing this vendored copy

From the root of the study repository:

```
pip install -e ./baselayer
```

This installs Base Layer 0.2.0 in editable mode. After install, the `baselayer` CLI and `baselayer-mcp` server are on your PATH and read from this directory.

## Why a vendored copy

1. The paper cites a specific version of the pipeline. Bundling that version in the same repository as the paper, data, and analysis scripts means readers do one clone and have everything.
2. PyPI registration of the `baselayer` name is held by an unrelated project. A vendored copy sidesteps the name conflict.
3. Active Base Layer development continues at the URL above. Pinning the paper-cited version in this repository protects against drift.

## Authoritative reference

The original `README.md` and `AGENTS.md` files in this directory describe Base Layer's architecture and usage at version 0.2.0. They are accurate for the paper-cited functionality. For documentation that reflects later versions, consult the active repository.
