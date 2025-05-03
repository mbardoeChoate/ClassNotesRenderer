# Renderer: Markdown-to-PDF Tool for Handouts

This tool is designed to help teachers efficiently convert Markdown-based handouts into PDF files using Pandoc. It looks for Markdown files with special comment-based commands and creates PDFs based on those instructions.

---

## Folder Structure

The `render.py` script should live inside a `tools/` subdirectory, while your handouts are organized in sibling directories like this:

```
/MyCourse
├── Week01
│   ├── HW1.md
│   └── pdf/
├── Week02
│   ├── Notes.md
│   └── pdf/
├── tools
│   ├── render.py
│   └── grid-header.tex
```

Each content folder (`Week01`, `Week02`, etc.) should contain:
- One or more `.md` files
- A `pdf/` subfolder for generated output

The `tools/` directory contains:
- `render.py` — the script
- `grid-header.tex` — optional background for handouts using the `grid` command

---

## How It Works

1. The script searches **one level up** from the `tools/` directory.
2. It finds subdirectories that contain a `pdf/` folder.
3. It scans for `.md` files in those directories.
4. If a Markdown file contains the command `<!-- command: render -->`, it is converted to a PDF using Pandoc.
5. The PDF is saved to the same directory’s `pdf/` subfolder.

---

## Supported Commands

Place these in your `.md` file using HTML-style comments:

Commands:

| Command (Version 1)    | Command (Version 2)           | Description                                                     |
|------------------------|-------------------------------|-----------------------------------------------------------------|
| `[comment:] render`    | `<!-- command: render -->`    | Required for the file to be processed and turned into a PDF     |
| `[comment:] grid`      | `<!-- command: grid -->`      | Adds a grid background (requires `grid-header.tex` in `tools/`) |
| `[comment:] landscape` | `<!-- command: landscape -->` | Renders the PDF in landscape orientation instead of portrait    |

You can combine commands in any file.

---

## `grid-header.tex` Location

If you use the `grid` command, make sure the file `grid-header.tex` is located inside the `tools/` directory next to `render.py`. The script is configured to include it using an absolute path relative to its own location.

---

## Image Support

Your Markdown files can include images using relative paths (e.g., `![Diagram](images/plot.png)`). As long as the image paths are valid **from the location of the `.md` file**, they will render correctly. This is handled by Pandoc's `--resource-path`.

---

## How to Run

From the **top-level directory of your course**, run the script like this:

```bash
python tools/render.py
```

The script will:
- Search all subdirectories one level above `tools/`
- Process any `.md` files with the appropriate command
- Save PDFs into the correct `pdf/` subfolders

---

## Requirements

- Python 3.6+
- [Pandoc](https://pandoc.org/)
- A LaTeX engine (e.g., `pdflatex`)
- Optional: `grid-header.tex` in `tools/` for grid-style backgrounds

---

## Example

A simple Markdown file that will be rendered:

```markdown
<!-- command: render -->
<!-- command: landscape -->
<!-- command: grid -->

# Homework 5

Here are some problems for today.

1. Let $f(x) = 3x + 2$. Find $f^{-1}(x)$.
```

---

## Notes

- The script avoids changing the working directory to preserve relative image paths.
- Output is verbose to show progress while running.
- You can easily add new command types by editing the `process_file` method in `render.py`.
