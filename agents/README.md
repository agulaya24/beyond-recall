# `agents/` — Instructions for AI agents working on this repo

**What's in this folder:** Guidance documents for AI tools (like Claude Code) so they can navigate the study repo, verify paper claims, and avoid common mistakes.

## Contents

- `study-guide.md`: The primary navigation document for an AI agent. Explains what the study is, where each kind of file lives, how to verify any claim in the paper, and how to report problems. If an AI is asked "what is this repo?", it should read this file first.
- `STUDY_MEMORY.md`: Persistent memory for AI sessions working on the study. Holds the load-bearing constants (N=14 subjects, 5-judge primary panel, condition naming, framing rules) and a log of methodology changes by session (S114, etc). Think of it as the rolling context the study carries between sessions.

## How naming works here

Files are plain Markdown. Filenames describe their role directly. No coded conventions. The top-level `AGENTS.md` in the repo root is a separate, shorter agent entry point that points here for detail.

## Where these files come from / go to

Hand-maintained. They are updated whenever a methodology constant changes (for example, when the primary judge panel moved from 7 judges to 5 judges in S114). Any AI agent reading the repo should check these files before proceeding.

## Caveats worth knowing

- `STUDY_MEMORY.md` is scoped to the "Beyond Recall" study only. It is not the broader Base Layer project memory.
- If numbers in `STUDY_MEMORY.md` disagree with `docs/DATA_REFERENCE.md`, `DATA_REFERENCE.md` wins for S113 sensitivity numbers and `docs/research/recompute_5judge_primary.md` wins for S114 primary numbers. The study guide and memory both say this explicitly.
- Session tags like "S114" refer to working sessions in the paper's lifecycle. S114 is the active session as of 2026-04-21.
