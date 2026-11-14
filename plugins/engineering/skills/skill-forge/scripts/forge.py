#!/usr/bin/env python3
"""skill-forge: find, fetch, scaffold and validate skills for the claudeskills repo.

Commands (run from anywhere inside the repo):
  search <words...>                 rank existing local skills and catalog entries
  show <catalog-name>               print one catalog entry
  fetch <catalog-name> [--out DIR]  download an entry's upstream files at the pinned commit
  scaffold <plugin> <skill-name> --description TEXT [--from CATALOG-NAME]
                                    create plugins/<plugin>/skills/<skill-name>/ with SKILL.md;
                                    with --from, upstream files go to references/ with attribution
  validate [PATH ...] [--all]       check skill folders against repo conventions (exit 1 on error)
  refresh-catalog <ecc-checkout>    rebuild catalog/ecc-catalog.json from a local ECC clone

Standard library only, so it runs on any machine with Python 3.9+.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
CATALOG = SKILL_DIR / "catalog" / "ecc-catalog.json"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
STOP = {"a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "with", "skill", "use", "when", "how"}


def repo_root() -> pathlib.Path:
    p = SKILL_DIR
    while p != p.parent:
        if (p / ".claude-plugin" / "marketplace.json").exists():
            return p
        p = p.parent
    sys.exit("error: not inside the claudeskills repo (no .claude-plugin/marketplace.json found)")


# ---------- frontmatter ----------

def frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter reader: scalar keys and folded/literal blocks."""
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out, key, block = {}, None, []
    for line in m.group(1).splitlines():
        top = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if top and not line.startswith(" "):
            if key and block:
                out[key] = " ".join(s.strip() for s in block).strip()
            key, val = top.group(1), top.group(2).strip()
            block = []
            if val in (">", "|", ">-", "|-", ""):
                out[key] = ""
            else:
                out[key] = val.strip("'\"")
                key = None
        elif key is not None:
            block.append(line)
    if key and block:
        out[key] = " ".join(s.strip() for s in block).strip()
    return out


# ---------- search ----------

def tokens(s: str):
    return [t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in STOP]


def score(query, name, desc) -> int:
    n, d = set(tokens(name.replace("-", " "))), tokens(desc)
    return sum(3 * (q in n) + min(d.count(q), 3) for q in query)


def local_skills(root):
    for f in sorted(root.glob("plugins/*/skills/*/SKILL.md")):
        fm = frontmatter(f.read_text(errors="replace"))
        plugin = f.parts[-4]
        yield {"name": fm.get("name", f.parent.name), "plugin": plugin,
               "description": fm.get("description", ""), "path": str(f.parent.relative_to(root))}
    for f in sorted(root.glob("plugins/*/skills/*/references/*.md")):
        head = f.read_text(errors="replace")[:6000]
        title = re.search(r"^#\s+(.+)$", head, re.M)
        yield {"name": f.stem, "plugin": f.parts[-5], "kind": "reference",
               "description": title.group(1) if title else "", "path": str(f.relative_to(root))}


def load_catalog():
    if not CATALOG.exists():
        sys.exit(f"error: catalog missing at {CATALOG}. Run refresh-catalog.")
    return json.loads(CATALOG.read_text())


def cmd_search(a):
    root, q = repo_root(), tokens(" ".join(a.words))
    if not q:
        sys.exit("error: give some search words")
    loc = sorted(((score(q, s["name"], s["description"]), s) for s in local_skills(root)),
                 key=lambda x: -x[0])
    cat = load_catalog()
    rem = sorted(((score(q, e["name"], e["description"]), e) for e in cat["entries"]),
                 key=lambda x: -x[0])
    print("LOCAL (already in this repo — prefer these):")
    hits = [x for x in loc if x[0] > 0][: a.limit]
    for s, e in hits:
        kind = e.get("kind", "skill")
        print(f"  [{s:2}] {e['plugin']}:{e['name']} ({kind})  {e['path']}\n       {e['description'][:150]}")
    if not hits:
        print("  (none)")
    print(f"\nCATALOG ({cat['source']} @ {cat['commit'][:7]}):")
    hits = [x for x in rem if x[0] > 0][: a.limit]
    for s, e in hits:
        merged = f"  [merged → {e['merged_into']}]" if e.get("merged_into") else ""
        print(f"  [{s:2}] {e['name']} ({e['kind']}){merged}\n       {e['description'][:150]}")
    if not hits:
        print("  (none) — build from official docs instead (see SKILL.md, source ladder step 3)")


def find_entry(name):
    cat = load_catalog()
    for e in cat["entries"]:
        if e["name"] == name or e["id"] == name:
            return cat, e
    sys.exit(f"error: '{name}' not in catalog. Try: forge.py search {name}")


def cmd_show(a):
    cat, e = find_entry(a.name)
    print(json.dumps(e, indent=2))


# ---------- fetch ----------

def raw_url(cat, path):
    return f"https://raw.githubusercontent.com/{cat['repo']}/{cat['commit']}/{path}"


def download(cat, e, out: pathlib.Path):
    out.mkdir(parents=True, exist_ok=True)
    got = []
    for rel in e["files"]:
        url = raw_url(cat, rel)
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = r.read()
        except Exception as ex:  # network blocked, file moved, etc.
            sys.exit(f"error: could not download {url}: {ex}\n"
                     f"Fallback: git clone https://github.com/{cat['repo']} && "
                     f"git -C <clone> checkout {cat['commit']} && copy {rel} by hand.")
        dest = out / pathlib.Path(rel).relative_to(e["base"]) if e["base"] else out / pathlib.Path(rel).name
        if dest.name == "SKILL.md":  # never nest a second SKILL.md inside a skill
            dest = dest.with_name(f"upstream-{e['name']}.md")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        got.append(dest)
    return got


def cmd_fetch(a):
    cat, e = find_entry(a.name)
    out = pathlib.Path(a.out or f"./forge-{e['name']}")
    for f in download(cat, e, out):
        print(f)


# ---------- scaffold ----------

SKILL_TMPL = """---
name: {name}
description: {description}
---

# {title}

<!-- skill-forge scaffold. Replace every section below with real content, then run:
     python3 plugins/engineering/skills/skill-forge/scripts/forge.py validate {path} -->

## When to use

## How to do it

## iCareerOS stack notes

## Failure modes to avoid
{refs}"""


def cmd_scaffold(a):
    root = repo_root()
    if not NAME_RE.match(a.skill):
        sys.exit("error: skill name must be kebab-case (a-z, 0-9, hyphens)")
    plugin_dir = root / "plugins" / a.plugin
    if not (plugin_dir / ".claude-plugin" / "plugin.json").exists():
        plugins = sorted(p.parent.parent.name for p in root.glob("plugins/*/.claude-plugin/plugin.json"))
        sys.exit(f"error: no plugin '{a.plugin}'. Existing: {', '.join(plugins)}")
    for s in local_skills(root):
        if s.get("kind") != "reference" and s["name"] == a.skill:
            sys.exit(f"error: a skill named '{a.skill}' already exists at {s['path']}")
    dest = plugin_dir / "skills" / a.skill
    if dest.exists():
        sys.exit(f"error: {dest} already exists")
    desc = " ".join(a.description.split())
    refs = ""
    if a.source:
        cat, e = find_entry(a.source)
        files = download(cat, e, dest / "references")
        credit = (f"Adapted from Everything Claude Code (MIT, (c) Affaan Mustafa) — "
                  f"`{e['path']}` @ {cat['commit'][:7]}. See NOTICE.")
        lines = []
        for f in files:
            if f.suffix == ".md":
                t = f.read_text(errors="replace")
                t = re.sub(r"\A---\n.*?\n---\n", "", t, count=1, flags=re.S).lstrip()
                f.write_text(f"<!-- {credit} -->\n\n{t}")
            lines.append(f"- `{f.relative_to(dest)}` — upstream source material ({e['kind']} `{e['name']}`)")
        refs = "\n## References\n\n" + "\n".join(lines) + "\n"
    rel = dest.relative_to(root)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "SKILL.md").write_text(SKILL_TMPL.format(
        name=a.skill, description=desc, title=a.skill.replace("-", " ").capitalize(), path=rel, refs=refs))
    print(f"created {rel}/SKILL.md")
    if refs:
        print(refs.strip())


# ---------- validate ----------

def validate_dir(d: pathlib.Path, root: pathlib.Path):
    errs, warns = [], []
    f = d / "SKILL.md"
    if not f.exists():
        return [f"{d}: missing SKILL.md"], []
    text = f.read_text(errors="replace")
    fm = frontmatter(text)
    rel = d.relative_to(root) if d.is_relative_to(root) else d
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        errs.append(f"{rel}: frontmatter has no name")
    elif name != d.name:
        errs.append(f"{rel}: name '{name}' does not match folder '{d.name}'")
    elif not NAME_RE.match(name) or len(name) > 64:
        errs.append(f"{rel}: name must be kebab-case, max 64 chars")
    if not desc:
        errs.append(f"{rel}: frontmatter has no description")
    elif len(desc) > 1024:
        errs.append(f"{rel}: description is {len(desc)} chars (max 1024)")
    if "skill-forge scaffold" in text:
        errs.append(f"{rel}: still contains the unfilled scaffold marker")
    body = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    if body.count("\n") > 500:
        warns.append(f"{rel}: SKILL.md body is {body.count(chr(10))} lines; move depth into references/")
    for ref in re.findall(r"`(references/[^`\s\[\]<>{}…*]+\.\w+)`", text):
        if not (d / ref).exists():
            errs.append(f"{rel}: points to missing file {ref}")
    return errs, warns


def cmd_validate(a):
    root = repo_root()
    dirs = ([p.parent for p in sorted(root.glob("plugins/*/skills/*/SKILL.md"))] if a.all or not a.paths
            else [pathlib.Path(p).resolve() for p in a.paths])
    errs, warns = [], []
    for d in dirs:
        e, w = validate_dir(d, root)
        errs += e
        warns += w
    for w in warns:
        print("warn: ", w)
    for e in errs:
        print("ERROR:", e)
    print(f"{len(dirs)} skill(s) checked, {len(errs)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errs else 0)


# ---------- catalog ----------

def merged_map():
    """Upstream paths already merged into this repo (from scripts/ecc_import.py)."""
    imp = repo_root() / "scripts" / "ecc_import.py"
    out = {}
    if imp.exists():
        for src, dst in re.findall(r'"([^"#]+)(?:#\w+)?":\s*\(([^,]+),', imp.read_text()):
            out[src] = re.sub(r'[\s"]', "", dst).replace("SK/", "engineering/skills/").replace("ENG/", "engineering/")
    return out


def cmd_refresh(a):
    ecc = pathlib.Path(a.ecc).resolve()
    sha = subprocess.check_output(["git", "-C", str(ecc), "rev-parse", "HEAD"], text=True).strip()
    merged = merged_map()
    entries = []

    def add(kind, name, path, base, files):
        fm = frontmatter((ecc / path).read_text(errors="replace"))
        e = {"id": f"{kind}:{name}", "name": name, "kind": kind,
             "description": " ".join(fm.get("description", "").split())[:600],
             "path": path, "base": base, "files": files}
        if path in merged:
            e["merged_into"] = merged[path]
        entries.append(e)

    for f in sorted((ecc / "skills").glob("*/SKILL.md")):
        base = str(f.parent.relative_to(ecc))
        files = sorted(str(p.relative_to(ecc)) for p in f.parent.rglob("*")
                       if p.is_file() and p.stat().st_size < 200_000)
        add("skill", f.parent.name, str(f.relative_to(ecc)), base, files)
    for kind, folder in (("agent", "agents"), ("command", "commands")):
        for f in sorted((ecc / folder).glob("*.md")):
            rel = str(f.relative_to(ecc))
            add(kind, f.stem, rel, "", [rel])
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(json.dumps({
        "source": "Everything Claude Code (MIT, (c) Affaan Mustafa)",
        "repo": "affaan-m/everything-claude-code", "commit": sha,
        "entries": entries}, indent=1) + "\n")
    m = sum(1 for e in entries if e.get("merged_into"))
    print(f"wrote {CATALOG.relative_to(repo_root())}: {len(entries)} entries ({m} already merged) @ {sha[:7]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("search"); p.add_argument("words", nargs="+"); p.add_argument("--limit", type=int, default=8)
    p.set_defaults(fn=cmd_search)
    p = sub.add_parser("show"); p.add_argument("name"); p.set_defaults(fn=cmd_show)
    p = sub.add_parser("fetch"); p.add_argument("name"); p.add_argument("--out"); p.set_defaults(fn=cmd_fetch)
    p = sub.add_parser("scaffold"); p.add_argument("plugin"); p.add_argument("skill")
    p.add_argument("--description", required=True); p.add_argument("--from", dest="source")
    p.set_defaults(fn=cmd_scaffold)
    p = sub.add_parser("validate"); p.add_argument("paths", nargs="*"); p.add_argument("--all", action="store_true")
    p.set_defaults(fn=cmd_validate)
    p = sub.add_parser("refresh-catalog"); p.add_argument("ecc"); p.set_defaults(fn=cmd_refresh)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
