"""Repository inspection for doctrine setup (offline, mechanical)."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field


@dataclass
class InspectionReport:
    languages: list[str] = field(default_factory=list)
    rust_workspace: bool = False
    workspace_members: list[str] = field(default_factory=list)
    crate_roots: list[str] = field(default_factory=list)
    readme_excerpt: str = ""
    architecture_docs: list[str] = field(default_factory=list)
    candidate_components: list[tuple[str, str]] = field(default_factory=list)  # id, glob


def _read_excerpt(path: str, limit: int = 400) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read(limit)
        return " ".join(text.split())[:300]
    except OSError:
        return ""


def inspect_repository(project_root: str) -> InspectionReport:
    root = os.path.abspath(project_root)
    report = InspectionReport()

    readme = os.path.join(root, "README.md")
    if os.path.isfile(readme):
        report.readme_excerpt = _read_excerpt(readme)

    cargo = os.path.join(root, "Cargo.toml")
    if os.path.isfile(cargo):
        report.languages.append("rust")
        try:
            with open(cargo, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            text = ""
        if "[workspace]" in text:
            report.rust_workspace = True
            for m in re.finditer(r'^\s*members\s*=\s*\[(.*?)\]', text, re.MULTILINE | re.DOTALL):
                inner = m.group(1)
                for part in re.findall(r'"([^"]+)"', inner):
                    report.workspace_members.append(part)
                    member_path = os.path.join(root, part.replace("\\", "/"))
                    if os.path.isdir(member_path):
                        report.candidate_components.append(
                            (_slug(part), f"{part.strip('/')}/**")
                        )
        else:
            report.candidate_components.append(("crate-root", "src/**"))
            report.crate_roots.append(".")

    for docs_path in ("docs/architecture.md", "doc/architecture.md", "ARCHITECTURE.md"):
        p = os.path.join(root, docs_path)
        if os.path.isfile(p):
            report.architecture_docs.append(docs_path)

    src = os.path.join(root, "src")
    if os.path.isdir(src) and not report.rust_workspace:
        if ("crate-root", "src/**") not in report.candidate_components:
            report.candidate_components.append(("crate-root", "src/**"))

    # Dedupe candidates by pattern
    seen: set[str] = set()
    uniq: list[tuple[str, str]] = []
    for cid, pat in report.candidate_components:
        if pat in seen:
            continue
        seen.add(pat)
        uniq.append((cid, pat))
    report.candidate_components = uniq
    return report


def _slug(path: str) -> str:
    base = os.path.basename(path.rstrip("/"))
    return re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-") or "component"


def scan_component_hints(root: str, pattern: str) -> dict[str, int]:
    """Lightweight text scan under matched paths (suggestion only)."""
    counts = {
        "atomic": 0,
        "mutex": 0,
        "serde": 0,
        "network": 0,
        "arch": 0,
    }
    prefix = pattern.split("/**")[0].split("*")[0].rstrip("/")
    base = os.path.join(root, prefix)
    if not os.path.isdir(base):
        return counts
    for dirpath, _, files in os.walk(base):
        for fn in files:
            if not fn.endswith((".rs", ".py", ".go", ".ts", ".tsx", ".js")):
                continue
            try:
                with open(os.path.join(dirpath, fn), encoding="utf-8", errors="ignore") as f:
                    body = f.read()
            except OSError:
                continue
            if re.search(r"\bAtomic\w*", body):
                counts["atomic"] += len(re.findall(r"\bAtomic\w*", body))
            if re.search(r"\b(Mutex|RwLock)\b", body):
                counts["mutex"] += len(re.findall(r"\b(Mutex|RwLock)\b", body))
            if "serde" in body:
                counts["serde"] += body.count("serde")
            if re.search(r"\b(TcpStream|UdpSocket|tokio::net)\b", body):
                counts["network"] += 1
            if "std::arch" in body or "#[target_feature" in body:
                counts["arch"] += 1
    return counts
