#!/usr/bin/env python3
"""
Render a JSON Resume to HTML using a Jinja2 template.

Usage:
    python render_resume.py resume.json
    python render_resume.py resume.json -o output.html
    python render_resume.py resume.json -t custom_template.html.j2
"""

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


def load_resume(resume_path: Path) -> dict:
    """Load and parse a JSON Resume file."""
    with open(resume_path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_resume(resume_data: dict, template_path: Path) -> str:
    """Render the resume data using the Jinja2 template."""
    template_dir = template_path.parent
    template_name = template_path.name

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(template_name)
    return template.render(**resume_data)


def main():
    parser = argparse.ArgumentParser(
        description="Render a JSON Resume to HTML using a Jinja2 template."
    )
    parser.add_argument(
        "resume",
        type=Path,
        help="Path to the JSON Resume file",
    )
    parser.add_argument(
        "-t",
        "--template",
        type=Path,
        default=None,
        help="Path to the Jinja2 template (default: frontend/resume.html.j2)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output HTML file path (default: frontend/index.html)",
    )

    args = parser.parse_args()

    # Determine paths relative to script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    template_path = args.template or project_root / "scripts" / "resume.html.j2"
    output_path = args.output or project_root / "frontend" / "index.html"

    # Validate inputs
    if not args.resume.exists():
        print(f"Error: Resume file not found: {args.resume}", file=sys.stderr)
        sys.exit(1)

    if not template_path.exists():
        print(f"Error: Template file not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    # Load and render
    try:
        resume_data = load_resume(args.resume)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in resume file: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        html_output = render_resume(resume_data, template_path)
    except TemplateNotFound as e:
        print(f"Error: Template not found: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"Resume rendered successfully to: {output_path}")


if __name__ == "__main__":
    main()
