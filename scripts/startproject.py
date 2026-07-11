#!/usr/bin/env python3
"""
Django-style startproject command for the book template.

Usage:
    uv run startproject        # Interactive mode
    uv run startproject NAME   # Non-interactive with defaults
"""

import argparse
import datetime
import os
import re
import sys


def prompt(label, default="", required=True):
    """Prompt user for input."""
    while True:
        if default:
            value = input(f"{label} [{default}]: ").strip()
            if not value:
                value = default
        else:
            value = input(f"{label}: ").strip()
        if value or not required:
            return value
        print("  This field is required. Please enter a value.")


def replace_in_file(path, replacements, dry_run=False):
    """Replace strings in a file."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    for old, new in replacements:
        content = content.replace(old, new)

    if content == original:
        print(f"  (no changes in {path})")
        return

    if dry_run:
        print(f"  [dry-run] Would update {path}")
        return

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Updated {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new book project from this template.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run startproject          # Interactive prompts
  uv run startproject mybook   # Quick start with defaults
        """,
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Project name (used for file names, package name, etc.)",
    )
    parser.add_argument(
        "--author",
        help="Author name(s)",
    )
    parser.add_argument(
        "--title",
        help="Book title (used in PDF metadata)",
    )
    parser.add_argument(
        "--year",
        help="Copyright year",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    args = parser.parse_args()

    print("=" * 50)
    print("Book Template - Start Project")
    print("=" * 50)
    print()

    # Gather inputs
    if args.name:
        project_name = args.name
        print(f"Project name: {project_name}")
    else:
        project_name = prompt("Project name", required=True)

    # Derive safe name for filenames (alphanumeric + underscore + hyphen)
    safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "", project_name)
    if not safe_name:
        safe_name = "project"

    default_title = f"{project_name} タイトル"
    title = args.title or prompt("Book title", default=default_title)

    default_author = "著者名"
    author = args.author or prompt("Author(s)", default=default_author)

    default_year = str(datetime.datetime.now().year)
    year = args.year or prompt("Copyright year", default=default_year)

    print()
    print("Summary:")
    print(f"  Project name : {project_name}")
    print(f"  Safe name    : {safe_name}")
    print(f"  Title        : {title}")
    print(f"  Author(s)    : {author}")
    print(f"  Year         : {year}")
    print()

    if not args.dry_run:
        confirm = input("Proceed? [Y/n]: ").strip().lower()
        if confirm and confirm not in ("y", "yes"):
            print("Aborted.")
            sys.exit(1)
        print()

    # Define replacements for each file
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # source/conf.py
    conf_py = os.path.join(root, "source", "conf.py")
    replace_in_file(
        conf_py,
        [
            ("project = u'gps-ntp'", f"project = u'{project_name}'"),
            ("author = u'chibiegg, homelith, misodengaku, notchi'", f"author = u'{author}'"),
            ("copyright = u'2019, chibiegg, homelith, misodengaku, notchi'", f"copyright = u'{year}, {author}'"),
            ("htmlhelp_basename = 'CHANGEME'", f"htmlhelp_basename = '{safe_name}'"),
            (
                "(master_doc, 'CHANGEME.tex', 'CHANGEME タイトル CHANGEME',\n     'author, 著者', 'manual')",
                f"(master_doc, '{safe_name}.tex', '{title}',\n     '{author}', 'manual')",
            ),
            (
                "(master_doc, 'CHANGEME', 'CHANGEME タイトル CHANGEME',\n     [author], 1)",
                f"(master_doc, '{safe_name}', '{title}',\n     [author], 1)",
            ),
            (
                "(master_doc, 'CHANGEME', 'CHANGEME タイトル CHANGEME',\n     author, 'CHANGEME', 'One line description of project.',\n     'Miscellaneous')",
                f"(master_doc, '{safe_name}', '{title}',\n     author, '{safe_name}', 'One line description of project.',\n     'Miscellaneous')",
            ),
        ],
        dry_run=args.dry_run,
    )

    # Makefile
    makefile = os.path.join(root, "Makefile")
    replace_in_file(
        makefile,
        [
            ("$(BUILDDIR)/latex/output.pdf", f"$(BUILDDIR)/latex/{safe_name}.pdf"),
            ("cp $(BUILDDIR)/latex/*.pdf output/", f"cp $(BUILDDIR)/latex/{safe_name}.pdf output/"),
            ('"output.tex"', f'"{safe_name}.tex"'),
            ("output.dvi", f"{safe_name}.dvi"),
        ],
        dry_run=args.dry_run,
    )

    # GitHub workflow
    workflow = os.path.join(root, ".github", "workflows", "pdf.yml")
    replace_in_file(
        workflow,
        [
            ("FILENAME: CHANGEME.pdf", f"FILENAME: {safe_name}.pdf"),
        ],
        dry_run=args.dry_run,
    )

    # pyproject.toml
    pyproject = os.path.join(root, "pyproject.toml")
    replace_in_file(
        pyproject,
        [
            ('name = "usui-book-template"', f'name = "{safe_name}"'),
        ],
        dry_run=args.dry_run,
    )

    # README.md
    readme = os.path.join(root, "README.md")
    replace_in_file(
        readme,
        [
            ("# book-template", f"# {project_name}"),
        ],
        dry_run=args.dry_run,
    )

    # RST source files
    maegaki = os.path.join(root, "source", "00-maegaki.rst")
    replace_in_file(
        maegaki,
        [
            ("Author : 著者名", f"Author : {author}"),
        ],
        dry_run=args.dry_run,
    )

    post = os.path.join(root, "source", "post.rst")
    replace_in_file(
        post,
        [
            ("Author : 著者名", f"Author : {author}"),
        ],
        dry_run=args.dry_run,
    )

    print()
    if args.dry_run:
        print("Dry run complete. No files were modified.")
    else:
        print("Project initialized successfully!")
        print()
        print("Next steps:")
        print("  1. Edit source/conf.py to fine-tune PDF/LaTeX settings")
        print("  2. Replace the sample chapters in source/")
        print("  3. Update the cover/colophon images in illustrator/")
        print("  4. Build: make pdf")


if __name__ == "__main__":
    main()
