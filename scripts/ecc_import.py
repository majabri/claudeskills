#!/usr/bin/env python3
"""One-time import of selected Everything Claude Code (ECC) material into this repo.

Usage: python3 scripts/ecc_import.py /path/to/ecc-checkout [--force]

Copies each mapped source file, strips its YAML frontmatter when it becomes a
reference file, and stamps an attribution header (ECC is MIT-licensed).
Agents and commands keep their frontmatter.

The imported files were then edited by hand (ECC-only tooling removed, iCareerOS
stack notes added). Existing targets are skipped unless --force is given, which
would discard those edits. skill-forge reads MAP to mark catalog entries as merged.
"""
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
ENG = REPO / "plugins" / "engineering"
SK = ENG / "skills"

# source path in ECC -> (target path, kind)  kind: ref | agent | command
MAP = {
    # L0 debug
    "agents/build-error-resolver.md": (SK / "software-l0-debug/references/build-errors.md", "ref"),
    "agents/silent-failure-hunter.md": (SK / "software-l0-debug/references/silent-failures.md", "ref"),
    # L1 operate
    "skills/verification-loop/SKILL.md": (SK / "software-l2-build/references/verification-loop.md", "ref"),
    # L2 build
    "skills/react-patterns/SKILL.md": (SK / "software-l2-build/references/react-patterns.md", "ref"),
    "skills/typescript-patterns/SKILL.md": (SK / "software-l2-build/references/typescript-patterns.md", "ref"),
    "skills/nextjs-turbopack/SKILL.md": (SK / "software-l2-build/references/nextjs.md", "ref"),
    "skills/tdd-workflow/SKILL.md": (SK / "software-l2-build/references/tdd-workflow.md", "ref"),
    "agents/typescript-reviewer.md": (SK / "software-l2-build/references/review-typescript.md", "ref"),
    "agents/react-reviewer.md": (SK / "software-l2-build/references/review-react.md", "ref"),
    # L3 architect
    "skills/postgres-patterns/SKILL.md": (SK / "software-l3-architect/references/postgres-patterns.md", "ref"),
    "skills/database-migrations/SKILL.md": (SK / "software-l3-architect/references/database-migrations.md", "ref"),
    "skills/architecture-decision-records/SKILL.md": (SK / "software-l3-architect/references/adr.md", "ref"),
    "skills/api-design/SKILL.md": (SK / "software-l3-architect/references/api-design.md", "ref"),
    # AI architect
    "skills/cost-aware-llm-pipeline/SKILL.md": (SK / "ai-architect/references/llm-cost.md", "ref"),
    "skills/prompt-caching-strategy/SKILL.md": (SK / "ai-architect/references/prompt-caching.md", "ref"),
    "agents/rag-pipeline-reviewer.md": (SK / "ai-architect/references/rag-review.md", "ref"),
    # UI tester
    "skills/e2e-testing/SKILL.md": (SK / "ui-tester/references/playwright-e2e.md", "ref"),
    "agents/e2e-runner.md": (SK / "ui-tester/references/e2e-runner.md", "ref"),
    # New security-review skill (SKILL.md written by hand; these are its references)
    "skills/security-review/SKILL.md": (SK / "security-review/references/checklist.md", "ref"),
    "skills/security-review/cloud-infrastructure-security.md": (SK / "security-review/references/cloud-infra.md", "ref"),
    "agents/security-reviewer.md": (SK / "security-review/references/reviewer-procedure.md", "ref"),
    # Subagents
    "agents/planner.md": (ENG / "agents/planner.md", "agent"),
    "agents/code-reviewer.md": (ENG / "agents/code-reviewer.md", "agent"),
    "agents/security-reviewer.md#agent": (ENG / "agents/security-reviewer.md", "agent"),
    "agents/database-reviewer.md": (ENG / "agents/database-reviewer.md", "agent"),
    # Commands (security-scan and quality-gate are written by hand: ECC versions need ECC hooks / an npm scanner)
    "commands/plan.md": (ENG / "commands/plan.md", "command"),
    "commands/code-review.md": (ENG / "commands/code-review.md", "command"),
}

FM = re.compile(r"\A---\n.*?\n---\n", re.S)


def main(ecc: pathlib.Path, force: bool = False) -> None:
    sha = subprocess.check_output(["git", "-C", str(ecc), "rev-parse", "HEAD"], text=True).strip()
    for src, (dst, kind) in MAP.items():
        src_path = ecc / src.split("#")[0]
        text = src_path.read_text()
        credit = f"Adapted from Everything Claude Code (MIT, (c) Affaan Mustafa) — `{src.split('#')[0]}` @ {sha[:7]}. See NOTICE."
        if kind == "ref":
            text = FM.sub("", text, count=1).lstrip()
            text = f"<!-- {credit} -->\n\n{text}"
        else:
            m = FM.match(text)
            head, body = (text[: m.end()], text[m.end():]) if m else ("", text)
            text = f"{head}\n<!-- {credit} -->\n{body}"
        if dst.exists() and not force:
            print(f"skip     {dst.relative_to(REPO)} (exists; --force to overwrite)")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text)
        print(f"{kind:8} {src} -> {dst.relative_to(REPO)}")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]).resolve(), force="--force" in sys.argv[2:])
