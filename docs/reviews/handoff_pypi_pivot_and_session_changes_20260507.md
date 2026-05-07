# Handoff: PyPI pivot and major changes from session 2026-05-07

For the main research instance and any other agent picking up Beyond Recall paper work after this session.

## TL;DR

Three load-bearing changes that affect how the paper is distributed and how readers install the cited code:

1. **PyPI is off the table.** The `baselayer` name is held by an unrelated project. Plan changed from "publish 0.2.0 to PyPI" to "vendor 0.2.0 source into the study repo and use git-install."
2. **Base Layer 0.2.0 source is now vendored** at `memory-study-repo/baselayer/`. Paper readers clone the study repo and `pip install -e ./baselayer`.
3. **Base Layer 0.3.0 (partial-serving MCP) shipped on the live BaseLayer repo.** The paper still cites 0.2.0; 0.3.0 is forward development, not paper material.

## What changed in detail

### 1. PyPI publish was abandoned

The `baselayer` package name on PyPI (https://pypi.org/project/baselayer/) is held by Stéfan van der Walt (stefanv@berkeley.edu), almost certainly the SkyPortal `baselayer` web framework. They uploaded a 0.0.0 placeholder in 2025 with summary "PyPi version coming soon; see GH for existing releases." The name is not realistically reclaimable on a paper-distribution timeline.

**Practical consequence:** any documentation, recipe, or paper passage that says `pip install baselayer` or `pip install baselayer==X.Y.Z` is wrong and will fail. The current paper drafts (v11.8, v11) do not contain such references; this is documented for future-proofing.

### 2. The vendor approach replaced PyPI for paper reproducibility

A frozen copy of Base Layer at v0.2.0 is now committed in the study repo at `./baselayer/`. The vendored copy:

- Has its own pyproject.toml with `version = "0.2.0"`
- Has `VENDORED_README.md` documenting the frozen-version status and pointing readers at the active development repo
- Will not drift; updates to Base Layer 0.3.0+ on the live repo do not affect this directory
- Is referenced in `REPRODUCE.md` section 1.1 with the install command `pip install -e ./baselayer`

The vendor was committed in `acb3718 Vendor Base Layer v0.2.0 source for paper reproducibility` on master.

### 3. v0.2.0 git tag was retroactively cleaned

The tag previously pointed at commit `fc09777`, which had pyproject `version = "0.1.0"` (the pyproject bump from 0.1.0 to 0.2.0 was never committed in the live repo's history; it lived only in the working tree). The tag now points at a clean commit (`67610ea`) where pyproject correctly reads `version = "0.2.0"`. This was fast-changed before any external reader could have cloned the previous tag value.

Install the paper-cited version directly:

```bash
pip install git+https://github.com/agulaya24/BaseLayer.git@v0.2.0
```

This is documented in the live repo's README, AGENTS.md, llms.txt, CHANGELOG.md, and recipes.

### 4. Base Layer 0.3.0 shipped on the live repo (NOT paper material)

The live BaseLayer repo's main branch is now at version 0.3.0, which introduced a partial-serving MCP design:

- The always-on `memory://specification` resource returns the CORE layer (~2,500 tokens) plus a manifest of additional tools
- ANCHORS, PREDICTIONS, and the unified brief are now model-controlled tools (`get_anchors()`, `get_predictions()`, `get_brief()`) that the model fetches on demand
- A new `get_call_log()` tool returns recent MCP calls in-process
- All resource reads and tool invocations log to stderr in format `[base-layer] INFO: mcp_call name=<n> [k=v ...]`
- Manifest fetch-trigger language is grounded in the Beyond Recall finding that interpretation-heavy questions (not literal recall) are where additional layers add the most value

The paper does not cite 0.3.0. The paper-citable version is 0.2.0, vendored in this repo. 0.3.0 is described in the live repo's CHANGELOG but should not be referenced in the paper.

### 5. Documentation across the live repo was updated

`agulaya24/BaseLayer` main now has consistent documentation reflecting both the partial-serving MCP and the no-PyPI install path:

- `README.md`: Quick Start uses git-install; Reproducibility section covers v0.2.0 tag and the vendored copy in this repo
- `AGENTS.md`: Setup section uses git-install; MCP section describes partial-serving with all six layer-and-monitoring tools
- `CLAUDE.md`: same MCP section, plus partial-serving rationale and link to the spec-loading workflow
- `llms.txt`: reproducibility paragraph updated
- `CHANGELOG.md`: 0.3.0 entry with the resource shape change, 0.2.0 reproducibility note revised
- `pyproject.toml`: version 0.3.0
- `docs/core/ARCHITECTURE.md`: Serving Layer section now describes partial-serving as shipped in 0.3.0; activation matching noted as future direction
- `docs/core/FLOW_GUIDE.md`, `docs/core/MCP_REGISTRY_SUBMISSIONS.md`: install instructions updated
- `recipes/run_pipeline_on_chatgpt_export.md`, `recipes/serve_specification_via_mcp.md`: prerequisites and goal text updated

Two exceptions left untouched (deliberate):
- `CHANGELOG.md` historical entries describing prior `pip install baselayer` behavior. Accurate as history.
- `docs/core/DECISIONS.md` references `pip install baselayer` in decision rationale describing a past problem statement. Editing would be revisionist.

### 6. Personal CORE injection (Aarik's local environment only)

`~/.claude/CLAUDE.md` was created with Aarik's CORE layer wrapped in clearly-delimited markers. This is global to all his Claude Code sessions, independent of any project. It is not committed anywhere. New Claude Code sessions read this file at startup and treat the content as system context.

This is local to Aarik's machine and is not relevant to public repos or the paper.

### 7. MCP server registered locally

`base-layer` is now registered with Aarik's Claude Code via `claude mcp add --transport stdio base-layer -- baselayer-mcp`. Health check shows connected. Will activate on his next Claude Code restart (open a new session).

This too is local to Aarik's machine.

## Action items for the research instance

If picking up paper work after this session, here is what is worth knowing:

1. **Do not write `pip install baselayer` or `pip install baselayer==X.Y.Z` anywhere.** Both will fail. Use:
   - `pip install git+https://github.com/agulaya24/BaseLayer.git@v0.2.0` (paper version), or
   - `pip install -e ./baselayer` (when working from a memory-study-repo clone)

2. **The paper currently has no PyPI references** (grep confirmed across v11_8 and v11 drafts). This handoff is preventive: do not reintroduce them in any new section, abstract, or supplementary material.

3. **`v0.2.0` is the canonical paper-version tag.** The previous plan's tag name (`v0.2-paper-2026`) was not used; the simpler `v0.2.0` was chosen. Memory and references that say `v0.2-paper-2026` are stale.

4. **The vendored copy at `./baselayer/` is intentionally frozen.** Do not update it from the live BaseLayer repo. If a critical fix is needed for the cited version, decide deliberately (it would change the paper's reproduced numbers).

5. **0.3.0 partial-serving MCP is forward development.** It is not paper material. If readers ask about MCP usage, the paper-relevant install is the vendored copy or `v0.2.0` tag. The live repo's MCP server is 0.3.0 partial-serving.

## References

- Live BaseLayer repo: https://github.com/agulaya24/BaseLayer
- Live tag for paper version: https://github.com/agulaya24/BaseLayer/releases/tag/v0.2.0
- Vendored copy in this repo: `./baselayer/`, see `./baselayer/VENDORED_README.md`
- Memory note (Aarik's auto-memory): `~/.claude/projects/C--Users-Aarik-Anthropic/memory/reference_pypi_unavailable.md`
- 0.3.0 release notes: live repo `CHANGELOG.md` line 1+
- MCP partial-serving design review: live repo `docs/internal/reviews/mcp_design_review_20260507_090612.md` (gitignored from public repo, available locally)
- Spec-loading workflow doc: live repo `docs/internal/spec_loading_workflow.md` (gitignored from public repo, available locally)

## Pushed commits from this session

Live BaseLayer repo (`agulaya24/BaseLayer`, main):

- `c619994` Partial-serving MCP: CORE on resource, layers via tools (0.3.0)
- `e1b344c` Replace PyPI install instructions with git-install (PyPI name unavailable)
- `e3247f9` Update serving-layer descriptions to reflect 0.3.0 partial-serving

Tags pushed: `v0.2.0` (paper baseline), `v0.3.0` (partial-serving release).

Study repo (`agulaya24/beyond-recall`, master):

- `acb3718` Vendor Base Layer v0.2.0 source for paper reproducibility
