import json
import os
import re
import subprocess
import sys

# Usage: python verify_structure.py [project root]
# Fails loudly (exit 1) when the project is missing any folder or file the template provides (exact letter case), when a template placeholder was left unfilled, when the ledger or decision log lost its header, when a record holds an em or en dash outside a quotation, or when git is not on a working branch.
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MANIFEST = os.path.join(ROOT, "template.json")
RECORD_EXT = {".md", ".txt", ".rst"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "Library", "Binaries", "Intermediate", "Saved", "DerivedDataCache", "dist", "build", "obj", "bin", ".vs", "Temp", "Logs"}
DASH = re.compile("[" + chr(0x2013) + chr(0x2014) + "]")
QUOTED = re.compile("\"[^\"\n]*\"|" + chr(0x201C) + "[^" + chr(0x201D) + "\n]*" + chr(0x201D))
failures = []


def check(ok, what):
    print(f"  {'ok  ' if ok else 'FAIL'} {what}")
    if not ok:
        failures.append(what)


def exists_exact(rel):
    # Returns True when every component of the relative path exists with exactly this letter case.
    cur = ROOT
    for part in rel.replace("\\", "/").split("/"):
        if not os.path.isdir(cur) or part not in os.listdir(cur):
            return False
        cur = os.path.join(cur, part)
    return True


manifest = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else None
check(manifest is not None, "template.json present")
for rel in (manifest or {}).get("required", []):
    check(exists_exact(rel), f"{rel} present (exact letter case)")
for rel in (manifest or {}).get("substituted", []):
    path = os.path.join(ROOT, rel)
    if os.path.exists(path):
        text = open(path, encoding="utf-8").read()
        check(not re.search(r"\{\{[A-Z_]+\}\}", text), f"{rel} has no unfilled placeholder")
for rel, header in (("approved/LEDGER.md", "| Date | JP's words | File | SHA-256 (first 16) | What is approved |"), ("docs/DECISIONS.md", "| Date | JP's words | Ruling taken | Status |"), ("docs/PROPOSALS.md", "| Raised | Question | Options, each with its standard | Consequence | Status |")):
    path = os.path.join(ROOT, rel)
    check(os.path.exists(path) and header in open(path, encoding="utf-8").read(), f"{rel} keeps its table header")
# Every record file in the project (paths in template.json record_check_exclusions and review/unsure excluded); a dash inside a quotation is a verbatim quote and is allowed.
skip_rel = {p.replace("\\", "/").strip("/") for p in (manifest or {}).get("record_check_exclusions", [])} | {"review/unsure"}
dashed, scanned = [], 0
for dp, dns, fns in os.walk(ROOT):
    rel_dir = os.path.relpath(dp, ROOT).replace("\\", "/")
    dns[:] = [d for d in dns if d not in SKIP_DIRS and (rel_dir + "/" + d if rel_dir != "." else d) not in skip_rel]
    for fn in fns:
        if os.path.splitext(fn)[1].lower() not in RECORD_EXT:
            continue
        rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace("\\", "/")
        if rel in skip_rel:
            continue
        scanned += 1
        lines = [n for n, line in enumerate(open(os.path.join(dp, fn), encoding="utf-8", errors="replace"), 1) if DASH.search(QUOTED.sub("", line))]
        if lines:
            dashed.append(f"{rel} ({len(lines)} lines, first {lines[0]})")
check(not dashed, f"no em or en dashes outside quotations in the {scanned} record files" + (": " + "; ".join(dashed[:20]) + (f"; and {len(dashed) - 20} more files" if len(dashed) > 20 else "") if dashed else ""))
try:
    branch = subprocess.run(["git", "-C", ROOT, "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    check(branch not in ("main", "master", "release"), f"git is on a working branch (found {branch})")
except (subprocess.CalledProcessError, FileNotFoundError):
    check(False, "git repository present")
print(f"STRUCTURE {'PASS' if not failures else 'FAIL'} | {len(failures)} failed | {ROOT}")
sys.exit(1 if failures else 0)
