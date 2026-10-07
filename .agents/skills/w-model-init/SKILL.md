---
name: w-model-init
description: Add the W-Model development guidance to a repository's root AGENTS.md safely from its dedicated template.
---

# W-Model Repository Setup

Use this skill when adding W-Model guidance to a repository. The dedicated source is `.agents/templates/w-model/AGENTS.md.template`; do not change `.agents/templates/AGENTS.md.template`, which is owned by `aide-init`.

## Run

From the target repository root, inspect the repository and template, then run:

```sh
python3 .agents/skills/w-model-init/scripts/init.py
```

An optional positional argument selects another existing target repository root:

```sh
python3 .agents/skills/w-model-init/scripts/init.py /path/to/repository
```

The target repository must contain the template and this setup script. Review the template and the target `AGENTS.md` before accepting changes. The script prints a unified diff before writing. It never merges or overwrites a conflicting or edited W-Model section; resolve such cases manually and rerun only when the existing section exactly matches the template.

## Safety and update rules

- Require a real directory root and ordinary, non-symlink `.agents`, `.agents/templates`, template, and root `AGENTS.md` paths. Reject missing/non-directory parents, symlinks, special files, unreadable files, invalid UTF-8, and malformed or unsafe template links without writing.
- The template must be exactly one Markdown section rooted at `## W-Model 開発案内`. Its child heading levels are shifted to fit the target document; an ambiguous heading structure or level beyond six is rejected.
- Append the section without changing existing bytes other than adding a separator newline if required. Existing document headings determine the inserted heading depth: use depth 2 if the shallowest existing heading is level 1, otherwise use that shallowest depth; use depth 1 when there are no headings.
- A single existing `W-Model 開発案内` section is a no-op only when its normalized content matches the rendered template. Duplicate, edited, or unrelated sections with the same heading are conflicts: show the diff and stop without writing.
- If `AGENTS.md` is absent, show and write a new file containing the rendered section. Re-running after a successful setup is idempotent.
- Validate every relative Markdown link in the template against an existing regular file within the target root. Do not follow symlinks while validating paths; reject encoded or ambiguous local destinations rather than guessing how Markdown will resolve them.

## Verification

Run the unit tests from the repository root:

```sh
python3 -m unittest discover -s .agents/skills/w-model-init/tests -v
```

After setup, read back `AGENTS.md`, confirm the section and all linked files, and report whether a file was created, updated, or already current. Never claim a write succeeded without reading the result back.
