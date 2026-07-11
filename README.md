# example


# build book

## Docker

```bash
$ make pdf
```

## native
```bash
$ sudo sh install-tools.sh
$ uv sync
$ uv run make latexpdfja
```

# start new project
```bash
$ uv run startproject 
==================================================
Book Template - Start Project
==================================================

Project name: example
Book title [example タイトル]: タイトル入力例
Author(s) [著者名]: user
Copyright year [2019]: 2026

Summary:
  Project name : example
  Safe name    : example
  Title        : 時報生成器の本
  Author(s)    : user
  Year         : 2026

Proceed? [Y/n]: y

  Updated /home/user/example/source/conf.py
  Updated /home/user/example/Makefile
  Updated /home/user/example/.github/workflows/pdf.yml
  Updated /home/user/example/pyproject.toml
  Updated /home/user/example/README.md
  Updated /home/user/example/source/00-maegaki.rst
  Updated /home/user/example/source/post.rst

Project initialized successfully!

Next steps:
  1. Edit source/conf.py to fine-tune PDF/LaTeX settings
  2. Replace the sample chapters in source/
  3. Update the cover/colophon images in illustrator/
  4. Build: make pdf
```