# Agent Skills specification (agentskills.io)

Source: [Specification](https://agentskills.io/specification). Every claim below
traces to that page unless noted otherwise.

This is the vendor-neutral specification that underlies the skill-packaging shape
used across agent ecosystems: a directory with a required `SKILL.md` plus
optional supporting content. It's the shared foundation summarized in this
skill's `SKILL.md`; this file carries the full field-by-field detail.

## Directory structure

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # required: metadata + instructions
├── scripts/          # optional: executable code
├── references/       # optional: documentation
├── assets/           # optional: templates, resources
└── ...               # any additional files or directories
```

## `SKILL.md` format

`SKILL.md` must contain YAML frontmatter followed by Markdown content.

### Frontmatter fields

| Field | Required | Constraints |
| --- | --- | --- |
| `name` | Yes | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. |
| `description` | Yes | Max 1024 characters. Non-empty. Describes what the skill does and when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
| `metadata` | No | Arbitrary key-value mapping for additional metadata (a map from string keys to string values). |
| `allowed-tools` | No | Space-separated string of pre-approved tools the skill may use. Experimental. |

Minimal example:

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

Example with optional fields:

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

### `name` field rules

The required `name` field:

- Must be 1-64 characters.
- May only contain unicode lowercase alphanumeric characters (`a-z`, `0-9`) and
  hyphens (`-`).
- Must not start or end with a hyphen (`-`).
- Must not contain consecutive hyphens (`--`).
- Must match the parent directory name.

Valid: `pdf-processing`, `data-analysis`, `code-review`. Invalid: `PDF-Processing`
(uppercase not allowed), `-pdf` (can't start with a hyphen), `pdf--processing`
(consecutive hyphens not allowed).

### `description` field rules

The required `description` field must be 1-1024 characters, should describe both
what the skill does and when to use it, and should include specific keywords
that help agents identify relevant tasks. The specification contrasts a good
example (`Extracts text and tables from PDF files, fills PDF forms, and merges
multiple PDFs. Use when working with PDF documents or when the user mentions
PDFs, forms, or document extraction.`) with a poor one (`Helps with PDFs.`).

### `license` field

The optional `license` field specifies the license applied to the skill; the
specification recommends keeping it short — either the name of a license or the
name of a bundled license file, for example `Proprietary. LICENSE.txt has
complete terms`.

### `compatibility` field

The optional `compatibility` field must be 1-500 characters if provided, and
should only be included if a skill has specific environment requirements — it
can indicate intended product, required system packages, or network access
needs, for example `Designed for Claude Code (or similar products)` or `Requires
git, docker, jq, and access to the internet`. The specification notes that most
skills don't need this field.

### `metadata` field

The optional `metadata` field is a map from string keys to string values that
clients can use to store additional properties not defined by the specification;
it recommends making key names reasonably unique to avoid accidental conflicts.

### `allowed-tools` field

The optional `allowed-tools` field is a space-separated string of tools that are
pre-approved to run, for example `Bash(git:*) Bash(jq:*) Read`. The
specification marks this field experimental, noting support may vary between
agent implementations.

### Body content

The Markdown body after the frontmatter contains the skill instructions, with no
format restrictions. Recommended sections are step-by-step instructions,
examples of inputs and outputs, and common edge cases. The agent loads this
entire file once it decides to activate a skill, so the specification suggests
splitting longer `SKILL.md` content into referenced files.

## Optional directories

A skill directory may contain any files and directories beyond the required
`SKILL.md`. These conventions are recommendations, not requirements, for
organizing common content types:

- **`scripts/`** — executable code agents can run. Scripts should be
  self-contained or clearly document dependencies, include helpful error
  messages, and handle edge cases gracefully. Supported languages depend on the
  agent implementation; common options include Python, Bash, and JavaScript.
- **`references/`** — additional documentation agents can read when needed, for
  example `REFERENCE.md` (detailed technical reference), `FORMS.md` (form
  templates or structured data formats), or domain-specific files such as
  `finance.md` or `legal.md`. The specification recommends keeping individual
  reference files focused, since agents load them on demand and smaller files
  mean less context use.
- **`assets/`** — static resources such as templates (document or configuration
  templates), images (diagrams, examples), or data files (lookup tables,
  schemas).

## Progressive disclosure

Agents load skills progressively, pulling in more detail only as a task calls
for it:

1. **Metadata** (~100 tokens): the `name` and `description` fields load at
   startup for all skills.
2. **Instructions** (< 5000 tokens recommended): the full `SKILL.md` body loads
   when the skill activates.
3. **Resources** (as needed): files in `scripts/`, `references/`, or `assets/`
   load only when required.

The specification recommends keeping the main `SKILL.md` under 500 lines and
moving detailed reference material to separate files.

## File references

References to other files inside a skill use relative paths from the skill
root, for example:

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

The specification recommends keeping file references one level deep from
`SKILL.md` and avoiding deeply nested reference chains.

## Validation

The [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)
reference library validates skills against the specification:

```bash
skills-ref validate ./my-skill
```

This checks that a skill's `SKILL.md` frontmatter is valid and follows all
naming conventions.
