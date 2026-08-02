#!/usr/bin/env python3
"""House rules for every __manifest__.py in this repository.

Run it locally before committing, or let CI run it for you:

    python3 tools/check_manifests.py

Exit code 0 means every module follows the standard. Anything else prints
what is wrong and where.
"""
import ast
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTHOR = "MBA Consultings, Brooks Gonzalez"
WEBSITE = "https://mbaconsultings.com"
LICENSES = {"LGPL-3", "AGPL-3", "OPL-1"}
VERSION_RE = re.compile(r"^18\.0\.\d+\.\d+\.\d+$")

# Canonical key order. Keys not listed here are allowed, but the ones that
# are listed must appear in this relative order.
KEY_ORDER = [
    "name",
    "version",
    "category",
    "summary",
    "description",
    "author",
    "website",
    "depends",
    "data",
    "demo",
    "installable",
    "application",
    "license",
]
REQUIRED = set(KEY_ORDER)


def module_dirs():
    for entry in sorted(os.listdir(ROOT)):
        path = os.path.join(ROOT, entry)
        if os.path.isfile(os.path.join(path, "__manifest__.py")):
            yield entry, path


def ordered_keys(source):
    """Keys in the order they appear in the source, via the AST."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            return [k.value for k in node.keys if isinstance(k, ast.Constant)]
    return []


def check(module, path):
    errors = []
    manifest_path = os.path.join(path, "__manifest__.py")
    source = open(manifest_path, encoding="utf-8").read()

    try:
        manifest = ast.literal_eval(source)
    except (SyntaxError, ValueError) as exc:
        return ["%s: manifest is not a literal dict (%s)" % (module, exc)]

    missing = REQUIRED - set(manifest)
    if missing:
        errors.append("%s: missing keys %s" % (module, sorted(missing)))

    if manifest.get("author") != AUTHOR:
        errors.append(
            "%s: author must be %r, found %r"
            % (module, AUTHOR, manifest.get("author"))
        )

    if manifest.get("website") != WEBSITE:
        errors.append(
            "%s: website must be %r, found %r"
            % (module, WEBSITE, manifest.get("website"))
        )

    if manifest.get("license") not in LICENSES:
        errors.append(
            "%s: license must be one of %s, found %r"
            % (module, sorted(LICENSES), manifest.get("license"))
        )

    version = manifest.get("version", "")
    if not VERSION_RE.match(str(version)):
        errors.append(
            "%s: version must look like 18.0.1.0.0, found %r" % (module, version)
        )

    if manifest.get("installable") is not True:
        errors.append("%s: installable must be True" % module)

    present = [k for k in ordered_keys(source) if k in KEY_ORDER]
    expected = [k for k in KEY_ORDER if k in present]
    if present != expected:
        errors.append(
            "%s: keys out of order\n     found:    %s\n     expected: %s"
            % (module, present, expected)
        )

    if '"' in source.split("{", 1)[-1].split(":")[0]:
        errors.append("%s: use single quotes for manifest keys" % module)

    for data_file in manifest.get("data", []) + manifest.get("demo", []):
        if not os.path.exists(os.path.join(path, data_file)):
            errors.append("%s: data file not found -> %s" % (module, data_file))

    if not os.path.exists(os.path.join(path, "README.md")):
        errors.append("%s: missing README.md" % module)

    icon = os.path.join(path, "static", "description", "icon.png")
    if not os.path.exists(icon):
        errors.append("%s: missing static/description/icon.png" % module)

    return errors


def main():
    modules = list(module_dirs())
    if not modules:
        print("No modules found under %s" % ROOT)
        return 1

    all_errors = []
    for module, path in modules:
        errors = check(module, path)
        status = "ok" if not errors else "FAIL"
        print("[%s] %s" % (status, module))
        all_errors.extend(errors)

    if all_errors:
        print("\n%d problem(s):\n" % len(all_errors))
        for err in all_errors:
            print("  - %s" % err)
        return 1

    print("\n%d module(s) follow the standard." % len(modules))
    return 0


if __name__ == "__main__":
    sys.exit(main())
