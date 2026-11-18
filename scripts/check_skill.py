#!/usr/bin/env python3
"""Check the local skill structure and reference links without network access."""

import argparse
import json
import re
from pathlib import Path


def slug(text):
    text = text.strip().lower().replace("`", "")
    return re.sub(r"[^\w\s-]", "", text).replace(" ", "-")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parent.parent))
    root = Path(parser.parse_args().root).resolve()
    errors = []
    main_path = root / "SKILL.md"
    if not main_path.is_file():
        print(json.dumps({"ok": False, "errors": ["SKILL.md is missing"]}))
        return 2
    main_text = main_path.read_text(encoding="utf-8")
    parts = main_text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        errors.append("SKILL.md needs opening YAML frontmatter")
        fields = {}
    else:
        fields = {}
        for line in parts[1].splitlines():
            if line.strip():
                key, separator, value = line.partition(":")
                if not separator or not value.strip():
                    errors.append("Frontmatter must use nonempty one-line fields")
                fields[key.strip()] = value.strip()
        if set(fields) != {"name", "description"}:
            errors.append("Frontmatter must contain only name and description")
    name = fields.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Skill name must be lowercase hyphen-case, at most 64 characters")
    if len(main_text.splitlines()) > 500:
        errors.append("SKILL.md exceeds the 500-line entrypoint budget")
    if "[TODO" in main_text:
        errors.append("SKILL.md still contains initializer placeholders")

    required = ["agents/openai.yaml", "scripts/speech_preflight.py", "scripts/test_speech_preflight.py"]
    for relative in required:
        if not (root / relative).is_file():
            errors.append("Missing " + relative)
    metadata_path = root / "agents/openai.yaml"
    if metadata_path.is_file():
        metadata = metadata_path.read_text(encoding="utf-8")
        if "$" + name not in metadata:
            errors.append("Agent default_prompt must name this skill")
        for key in ("display_name", "short_description", "default_prompt"):
            if not re.search(r'^\s+' + key + r': ".+"$', metadata, re.M):
                errors.append("Missing quoted agent interface field: " + key)

    markdown = sorted(root.glob("*.md")) + sorted((root / "references").glob("*.md"))
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(root))
        if chr(0x2014) in text:
            errors.append(relative + " contains prohibited punctuation")
        if path != main_path and len(text.splitlines()) > 100 and "## Contents" not in text:
            errors.append(relative + " needs a contents list for navigation")
        for destination in re.findall(r"\]\(([^)]+)\)", text):
            if re.match(r"(?:https?://|mailto:)", destination):
                continue
            filename, _, anchor = destination.partition("#")
            target = (path.parent / filename).resolve() if filename else path
            if not target.is_file():
                errors.append(relative + " has a missing local link: " + destination)
                continue
            if anchor and target.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", target.read_text(encoding="utf-8"), re.M)
                if anchor not in {slug(heading) for heading in headings}:
                    errors.append(relative + " has a missing heading: " + destination)
    result = {"ok": not errors, "errors": errors, "markdown_files": len(markdown),
              "entrypoint_words": len(main_text.split()), "entrypoint_lines": len(main_text.splitlines())}
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
