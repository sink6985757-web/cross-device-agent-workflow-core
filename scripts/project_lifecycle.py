#!/usr/bin/env python3
"""Validate portable lifecycle manifests and classify a project's Git state.

This helper is intentionally read-only. It never clones, pulls, commits, pushes,
merges, rebases, switches branches, creates repositories, or changes remotes.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REVISION_RE = re.compile(
    r"^(?:[0-9A-Fa-f]{40}|v?[0-9]+(?:\.[0-9]+){1,3}(?:[-+][0-9A-Za-z.-]+)?)$"
)
REMOTE_RE = re.compile(r"^[A-Za-z0-9._-]+$")
FORBIDDEN_ACTIONS = {
    "create-repository",
    "force-push",
    "auto-merge-or-rebase",
    "tag-or-release",
    "merge-pull-request",
    "delete-or-archive",
    "change-permissions",
}


def portable_path(value: Any, *, allow_dot: bool = False) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if value == ".":
        return allow_dot
    if value.startswith(("/", "~", "//")) or re.match(r"^[A-Za-z]:", value):
        return False
    if "\\" in value or "//" in value:
        return False
    parts = value.split("/")
    return all(part not in ("", ".", "..") for part in parts)


def _require_mapping(value: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return {}
    return value


def _require_exact_keys(
    value: dict[str, Any], expected: set[str], path: str, errors: list[str]
) -> None:
    missing = expected - set(value)
    extra = set(value) - expected
    if missing:
        errors.append(f"{path} missing: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{path} has unknown keys: {', '.join(sorted(extra))}")


def validate_manifest(payload: Any) -> list[str]:
    errors: list[str] = []
    root = _require_mapping(payload, "manifest", errors)
    expected_root = {
        "schema_version",
        "profile",
        "authority",
        "routing",
        "project",
        "paths",
        "content",
        "checkpoint",
        "device_binding",
        "rollback",
    }
    _require_exact_keys(root, expected_root, "manifest", errors)

    if root.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if root.get("profile") not in {"lite", "full"}:
        errors.append("profile must be lite or full")

    authority = _require_mapping(root.get("authority"), "authority", errors)
    _require_exact_keys(authority, {"core", "lifecycle", "readygate"}, "authority", errors)
    for name in ("core", "lifecycle", "readygate"):
        source = _require_mapping(authority.get(name), f"authority.{name}", errors)
        _require_exact_keys(source, {"repository", "revision"}, f"authority.{name}", errors)
        if not REPOSITORY_RE.fullmatch(str(source.get("repository", ""))):
            errors.append(f"authority.{name}.repository must be owner/repository")
        if not REVISION_RE.fullmatch(str(source.get("revision", ""))):
            errors.append(f"authority.{name}.revision must be an immutable tag or 40-character commit")

    routing = _require_mapping(root.get("routing"), "routing", errors)
    _require_exact_keys(routing, {"part", "project", "project_root"}, "routing", errors)
    for name in ("part", "project"):
        if not isinstance(routing.get(name), str) or not routing.get(name):
            errors.append(f"routing.{name} must be a non-empty string")
    if routing.get("project_root") != ".":
        errors.append("routing.project_root must be '.'; Part routing is not a Git boundary")

    project = _require_mapping(root.get("project"), "project", errors)
    _require_exact_keys(
        project,
        {"github_repository", "remote", "default_branch", "project_kind"},
        "project",
        errors,
    )
    if not REPOSITORY_RE.fullmatch(str(project.get("github_repository", ""))):
        errors.append("project.github_repository must be owner/repository")
    if not REMOTE_RE.fullmatch(str(project.get("remote", ""))):
        errors.append("project.remote is invalid")
    branch = project.get("default_branch")
    if not isinstance(branch, str) or not branch or any(
        token in branch for token in (" ", "..", "~", "^", ":", "?", "*", "[", "\\")
    ) or branch.startswith((".", "/")) or branch.endswith(("/", ".", ".lock")):
        errors.append("project.default_branch is invalid")
    if project.get("project_kind") not in {"code", "data", "docs", "mixed"}:
        errors.append("project.project_kind is invalid")

    paths = _require_mapping(root.get("paths"), "paths", errors)
    _require_exact_keys(paths, {"agents", "readme", "changelog", "handoff", "manifest"}, "paths", errors)
    for name in ("agents", "readme", "changelog", "handoff", "manifest"):
        if not portable_path(paths.get(name)):
            errors.append(f"paths.{name} must be a portable project-relative path")
    if paths.get("manifest") != ".agents/project-lifecycle.json":
        errors.append("paths.manifest must be .agents/project-lifecycle.json")

    content = _require_mapping(root.get("content"), "content", errors)
    _require_exact_keys(content, {"tracked_roots", "excluded_roots", "large_file_policy"}, "content", errors)
    for name, allow_dot in (("tracked_roots", True), ("excluded_roots", False)):
        values = content.get(name)
        if not isinstance(values, list) or (name == "tracked_roots" and not values):
            errors.append(f"content.{name} must be a non-empty array" if name == "tracked_roots" else f"content.{name} must be an array")
        elif not all(isinstance(v, str) for v in values) or len(values) != len(set(values)) or not all(portable_path(v, allow_dot=allow_dot) for v in values):
            errors.append(f"content.{name} must contain unique portable relative paths")
    if content.get("large_file_policy") not in {"repository-default", "git-lfs", "manifest-only", "exclude"}:
        errors.append("content.large_file_policy is invalid")

    checkpoint = _require_mapping(root.get("checkpoint"), "checkpoint", errors)
    checkpoint_keys = {
        "mode",
        "initial",
        "startup",
        "shutdown",
        "branch_policy",
        "readback",
        "force_push",
        "pull_mode",
        "unknown_untracked",
        "allow_paths",
        "forbidden_actions",
    }
    _require_exact_keys(checkpoint, checkpoint_keys, "checkpoint", errors)
    constants = {
        "initial": "push-bootstrap",
        "startup": "fetch-and-verify",
        "shutdown": "commit-and-push-current-branch",
        "branch_policy": "current-work-branch",
        "readback": "remote-sha",
        "force_push": False,
        "pull_mode": "ff-only",
        "unknown_untracked": "stop",
    }
    if checkpoint.get("mode") not in {"manual", "standing_scoped"}:
        errors.append("checkpoint.mode must be manual or standing_scoped")
    for name, expected in constants.items():
        if checkpoint.get(name) != expected:
            errors.append(f"checkpoint.{name} must be {expected!r}")
    allow_paths = checkpoint.get("allow_paths")
    if not isinstance(allow_paths, list) or not allow_paths or not all(isinstance(v, str) for v in allow_paths) or len(allow_paths) != len(set(allow_paths)) or not all(portable_path(v) for v in allow_paths):
        errors.append("checkpoint.allow_paths must contain unique portable project-relative paths")
    forbidden = checkpoint.get("forbidden_actions")
    if not isinstance(forbidden, list) or not all(isinstance(v, str) for v in forbidden) or set(forbidden) != FORBIDDEN_ACTIONS:
        errors.append("checkpoint.forbidden_actions must contain the complete fixed denylist")

    device = _require_mapping(root.get("device_binding"), "device_binding", errors)
    _require_exact_keys(device, {"mode", "local_policy"}, "device_binding", errors)
    if device.get("mode") != "runtime-only" or device.get("local_policy") != "policy.local.yaml":
        errors.append("device_binding must stay runtime-only in ignored policy.local.yaml")

    rollback = _require_mapping(root.get("rollback"), "rollback", errors)
    rollback_expected = {
        "published_change": "git-revert",
        "inspect_old_revision": "restore-branch",
        "behind_clean": "pull-ff-only",
        "diverged": "stop-preserve-refs",
        "clone_target": "empty-directory-only",
    }
    _require_exact_keys(rollback, set(rollback_expected), "rollback", errors)
    for name, expected in rollback_expected.items():
        if rollback.get(name) != expected:
            errors.append(f"rollback.{name} must be {expected}")

    return errors


def normalize_remote(value: str) -> str | None:
    text = value.strip().rstrip("/")
    patterns = (
        r"^https://github\.com/([^/]+/[^/]+?)(?:\.git)?$",
        r"^git@github\.com:([^/]+/[^/]+?)(?:\.git)?$",
        r"^ssh://git@github\.com/([^/]+/[^/]+?)(?:\.git)?$",
    )
    for pattern in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).lower()
    return None


def classify_state(
    *,
    remote_matches: bool,
    detached: bool,
    has_upstream: bool,
    dirty: bool,
    ahead: int,
    behind: int,
) -> str:
    if not remote_matches:
        return "WRONG_REMOTE"
    if detached:
        return "DETACHED_HEAD"
    if not has_upstream:
        return "NO_UPSTREAM"
    if ahead and behind:
        return "DIVERGED"
    if dirty:
        return "DIRTY"
    if ahead:
        return "AHEAD"
    if behind:
        return "BEHIND"
    return "CLEAN_SYNCED"


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def classify_git(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    top = _git(root, "rev-parse", "--show-toplevel", check=False)
    if top.returncode != 0:
        return {"state": "NOT_GIT_REPOSITORY", "project_root": str(root)}
    git_root = Path(top.stdout.strip()).resolve()
    if git_root != root.resolve():
        return {"state": "WRONG_GIT_ROOT", "project_root": str(root), "git_root": str(git_root)}

    project = manifest["project"]
    remote_name = project["remote"]
    remote = _git(root, "remote", "get-url", remote_name, check=False)
    if remote.returncode != 0:
        return {"state": "NO_REMOTE", "git_root": str(git_root), "remote": remote_name}
    remote_url = remote.stdout.strip()
    expected = project["github_repository"].lower()
    actual = normalize_remote(remote_url)
    remote_matches = actual == expected

    branch_result = _git(root, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    detached = branch_result.returncode != 0
    branch = branch_result.stdout.strip() if not detached else None
    upstream_result = _git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
    has_upstream = upstream_result.returncode == 0
    upstream = upstream_result.stdout.strip() if has_upstream else None
    dirty = bool(_git(root, "status", "--porcelain=v1").stdout.strip())
    ahead = behind = 0
    if has_upstream:
        counts = _git(root, "rev-list", "--left-right", "--count", "HEAD...@{u}", check=False)
        if counts.returncode == 0:
            fields = counts.stdout.split()
            if len(fields) == 2:
                ahead, behind = map(int, fields)
    state = classify_state(
        remote_matches=remote_matches,
        detached=detached,
        has_upstream=has_upstream,
        dirty=dirty,
        ahead=ahead,
        behind=behind,
    )
    return {
        "state": state,
        "git_root": str(git_root),
        "branch": branch,
        "upstream": upstream,
        "dirty": dirty,
        "ahead": ahead,
        "behind": behind,
        "remote": remote_name,
        "remote_url": remote_url,
        "expected_repository": project["github_repository"],
        "remote_matches": remote_matches,
    }


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate-manifest")
    validate.add_argument("manifest", type=Path)
    classify = subparsers.add_parser("classify-git")
    classify.add_argument("manifest", type=Path)
    classify.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    try:
        payload = load_manifest(args.manifest)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 1
    errors = validate_manifest(payload)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    if args.command == "validate-manifest":
        print(json.dumps({"valid": True, "manifest": str(args.manifest)}, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps(classify_git(args.project_root, payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
