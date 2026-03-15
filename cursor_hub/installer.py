"""
Install logic for Cursor packs: find hub root, resolve packs, merge into target.
Used by both tools/install.py and the cursor-hub CLI.
"""
from __future__ import annotations

import os
import shutil
import sys

PACKS_ROOT = "packs"
CURSOR_DIR = ".cursor"
PACK_YML = "pack.yml"
RULES = "rules"
COMMANDS = "commands"
AGENTS = "agents"
TOOLS_DIR = "tools"
DESIGN_LOG_DIR = "design-log"
SHARED_PACK = "_shared"

ALL_RUST_PACKS = [
    "design-log",
    "rust-design-review",
    "rust-implementation",
    "rust-testing",
    "rust-bugfix",
    "rust-review",
    "documentation",
    "security",
]
ALL_PYTHON_PACKS = [
    "design-log",
    "python-design-review",
    "python-implementation",
    "python-testing",
    "python-bugfix",
    "python-review",
    "documentation",
    "security",
]
ALL_JS_TS_PACKS = [
    "design-log",
    "js-ts-design-review",
    "js-ts-implementation",
    "js-ts-testing",
    "js-ts-bugfix",
    "js-ts-review",
    "documentation",
    "security",
]
ALL_TERRAFORM_PACKS = [
    "design-log",
    "terraform-design-review",
    "terraform-implementation",
    "terraform-testing",
    "terraform-bugfix",
    "terraform-review",
    "documentation",
    "security",
]
LANGUAGE_PACK_SETS: dict[str, list[str]] = {
    "rust": ALL_RUST_PACKS,
    "python": ALL_PYTHON_PACKS,
    "js-ts": ALL_JS_TS_PACKS,
    "terraform": ALL_TERRAFORM_PACKS,
}

DESIGN_LOG_README = """# Design Log

Design decisions and implementation notes live here as `NNN-short-name.md`.
Create new entries from the project root:

    python .cursor/tools/new_design_log.py --slug <short-name>

Use `--dir` to target a different directory (e.g. another repo).
"""


def find_repo_root(start: str) -> str | None:
    """Walk up from start to find a directory containing packs/cursor/_shared."""
    current = os.path.abspath(start)
    while current and current != os.path.dirname(current):
        check = os.path.join(current, PACKS_ROOT, "cursor", SHARED_PACK)
        if os.path.isdir(check):
            return current
        current = os.path.dirname(current)
    return None


def get_hub_root(start: str | None = None) -> str | None:
    """Find cursor-hub root: optional start path, then cwd, then script/package location."""
    if start:
        root = find_repo_root(start)
        if root:
            return root
    root = find_repo_root(os.getcwd())
    if root:
        return root
    # Fallback: parent of this package (when running as cursor-hub CLI from repo)
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.normpath(os.path.join(pkg_dir, ".."))
    if os.path.isdir(os.path.join(candidate, PACKS_ROOT, "cursor", SHARED_PACK)):
        return candidate
    return None


def get_pack_dirs(repo_root: str, pack_names: list[str]) -> list[str]:
    """Resolve pack names to full paths by scanning for pack.yml files."""
    cursor_root = os.path.join(repo_root, PACKS_ROOT, "cursor")
    if not os.path.isdir(cursor_root):
        raise FileNotFoundError(f"Cursor packs root not found at {cursor_root}")

    index: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(cursor_root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        if PACK_YML not in filenames:
            continue
        pack_path = dirpath
        pack_name = os.path.basename(pack_path)
        pack_yml = os.path.join(pack_path, PACK_YML)
        explicit_name: str | None = None
        try:
            with open(pack_yml, "r", encoding="utf-8") as f:
                for raw in f:
                    line = raw.strip()
                    if line.startswith("name:") and ":" in line:
                        val = line.split(":", 1)[1].strip().strip("'\"")
                        if val:
                            explicit_name = val
                        break
        except OSError:
            pass
        key = explicit_name or pack_name
        index[key] = pack_path

    ordered = [SHARED_PACK] + [p for p in pack_names if p != SHARED_PACK]
    seen: set[str] = set()
    out: list[str] = []
    for name in ordered:
        if name in seen:
            continue
        if name not in index:
            raise FileNotFoundError(f"Pack not found: {name}")
        out.append(index[name])
        seen.add(name)
    return out


def merge_cursor_dir(src: str, dst: str, overwrite: bool, dry_run: bool) -> tuple[int, int, int]:
    """Copy contents of src/.cursor/* into dst/.cursor/*."""
    src_cursor = os.path.join(src, CURSOR_DIR)
    r, c, a = 0, 0, 0
    if not os.path.isdir(src_cursor):
        return (r, c, a)
    for sub in (RULES, COMMANDS, AGENTS):
        src_sub = os.path.join(src_cursor, sub)
        if not os.path.isdir(src_sub):
            continue
        dst_sub = os.path.join(dst, CURSOR_DIR, sub)
        if dry_run:
            for name in os.listdir(src_sub):
                f = os.path.join(src_sub, name)
                if os.path.isfile(f):
                    print(f"[dry-run] would add {os.path.join(CURSOR_DIR, sub, name)}")
            continue
        os.makedirs(dst_sub, exist_ok=True)
        for name in os.listdir(src_sub):
            src_file = os.path.join(src_sub, name)
            if not os.path.isfile(src_file):
                continue
            dst_file = os.path.join(dst_sub, name)
            if overwrite or not os.path.exists(dst_file):
                shutil.copy2(src_file, dst_file)
                if sub == RULES:
                    r += 1
                elif sub == COMMANDS:
                    c += 1
                else:
                    a += 1
    return (r, c, a)


def read_pack_version(pack_dir: str) -> str | None:
    """Read version from pack.yml if present."""
    path = os.path.join(pack_dir, PACK_YML)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("version:") and ":" in line:
                    val = line.split(":", 1)[1].strip().strip("'\"")
                    return val if val else None
    except OSError:
        pass
    return None


def copy_tools(repo_root: str, target: str, dry_run: bool) -> None:
    """Copy hub tools/ into target/.cursor/tools/."""
    src = os.path.join(repo_root, "tools")
    dst = os.path.join(target, CURSOR_DIR, TOOLS_DIR)
    if not os.path.isdir(src):
        return
    if dry_run:
        print(f"[dry-run] would copy tools/ into {CURSOR_DIR}/{TOOLS_DIR}/")
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"  Copied tools into {CURSOR_DIR}/{TOOLS_DIR}/ (run from project root: python {CURSOR_DIR}/{TOOLS_DIR}/new_design_log.py --slug <name>).")


def ensure_design_log_dir(target: str, dry_run: bool) -> None:
    """Create target/.cursor/design-log/ and README.md if missing."""
    log_dir = os.path.join(target, CURSOR_DIR, DESIGN_LOG_DIR)
    readme = os.path.join(log_dir, "README.md")
    if os.path.isfile(readme):
        return
    if dry_run:
        print(f"[dry-run] would create {CURSOR_DIR}/{DESIGN_LOG_DIR}/README.md")
        return
    os.makedirs(log_dir, exist_ok=True)
    with open(readme, "w", encoding="utf-8") as f:
        f.write(DESIGN_LOG_README)


def run_install(
    repo_root: str,
    target: str,
    pack_names: list[str],
    *,
    overwrite: bool = False,
    dry_run: bool = False,
) -> int:
    """
    Install the given packs from repo_root into target.
    Returns 0 on success, 1 on error.
    """
    repo_root = os.path.normpath(os.path.abspath(repo_root))
    target = os.path.normpath(os.path.abspath(target))

    if target == repo_root or target.startswith(repo_root + os.sep):
        print("Error: Target is inside the hub repo.", file=sys.stderr)
        print(f"  Target: {target}", file=sys.stderr)
        print(f"  Hub:    {repo_root}", file=sys.stderr)
        print("  Use a target outside the hub (e.g. ../my-project).", file=sys.stderr)
        return 1

    try:
        pack_dirs = get_pack_dirs(repo_root, pack_names)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"Target: {target}")

    if not dry_run:
        os.makedirs(os.path.join(target, CURSOR_DIR), exist_ok=True)

    total_r, total_c, total_a = 0, 0, 0
    for pack_dir in pack_dirs:
        r, c, a = merge_cursor_dir(pack_dir, target, overwrite, dry_run)
        total_r += r
        total_c += c
        total_a += a

    ensure_design_log_dir(target, dry_run)
    copy_tools(repo_root, target, dry_run)

    if dry_run:
        print("Dry run complete. No files written.")
    else:
        print(f"Installed into: {target}")
        print(f"  Packs: _shared, {', '.join(pack_names)}")
        versions = []
        for pack_dir in pack_dirs:
            pack_name = os.path.basename(pack_dir)
            ver = read_pack_version(pack_dir)
            if ver:
                versions.append(f"{pack_name}={ver}")
        if versions:
            print(f"  Versions: {' '.join(versions)}")
        if total_r or total_c or total_a:
            print(f"  Added: {total_r} rules, {total_c} commands, {total_a} agents")
        else:
            print("  (No new files; target already had these. Use --overwrite to replace.)")
        print(f"  {CURSOR_DIR}/{DESIGN_LOG_DIR}/ created if missing.")
        cursor_dir = os.path.join(target, CURSOR_DIR)
        if os.path.isdir(cursor_dir):
            for sub in (RULES, COMMANDS, AGENTS, DESIGN_LOG_DIR, TOOLS_DIR):
                subpath = os.path.join(cursor_dir, sub)
                if os.path.isdir(subpath):
                    n = len([f for f in os.listdir(subpath) if os.path.isfile(os.path.join(subpath, f))])
                    print(f"  -> {os.path.join(target, CURSOR_DIR, sub)} ({n} files)")
    return 0


def expand_pack_names(
    pack_names: list[str],
    lang: list[str] | None,
) -> list[str]:
    """Expand 'all', 'rust', and --lang into full pack lists. Dedupe, preserve order."""
    expanded: list[str] = []
    if lang:
        for l in lang:
            packs_for_lang = LANGUAGE_PACK_SETS.get(l)
            if not packs_for_lang:
                known = ", ".join(sorted(LANGUAGE_PACK_SETS))
                print(f"Warning: unknown language '{l}' (known: {known})")
                continue
            expanded.extend(packs_for_lang)
    for p in pack_names:
        if p == "all":
            if lang:
                expanded.extend(LANGUAGE_PACK_SETS.get(lang[0], ALL_RUST_PACKS))
            else:
                expanded.extend(ALL_RUST_PACKS)
        elif p == "rust":
            expanded.extend(ALL_RUST_PACKS)
        else:
            expanded.append(p)
    seen: set[str] = set()
    return [x for x in expanded if x not in seen and not seen.add(x)]
