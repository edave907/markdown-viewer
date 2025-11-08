# Markdown Viewer

A lightweight, desktop markdown viewer with GitHub-like styling built using Python and Tkinter.

## Features

- **GitHub-like styling** - Clean, professional rendering that matches GitHub's markdown display
- **Rich markdown support** - Headers, bold, italic, code blocks, lists, blockquotes, tables, and more
- **ASCII art rendering** - Properly displays ASCII diagrams and box-drawing characters without wrapping or spacing issues
- **Syntax-aware code blocks** - Monospace font with gray background for code snippets
- **Horizontal scrolling** - Long lines don't wrap, maintaining formatting integrity
- **Lightweight** - Pure Python with minimal dependencies

## Installation

### Requirements

- Python 3.6+
- Tkinter (usually included with Python)
- markdown library

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Make the launcher executable (optional)
chmod +x markdown-viewer
```

## Usage

### Command Line

```bash
# Using Python directly
python3 markdown_viewer.py <filename.md>

# Using the launcher script
./markdown-viewer <filename.md>

# Example
python3 markdown_viewer.py sample_files/README.md
```

### Compiled Binary

If you've built the standalone binary:

```bash
./dist/markdown-viewer <filename.md>
```

## Building Standalone Binary

To create a standalone executable using PyInstaller:

```bash
pip install pyinstaller
pyinstaller markdown-viewer.spec
```

The compiled binary will be in the `dist/` directory.

## Supported Markdown Features

### Text Formatting
- **Bold** - `**text**` or `__text__`
- *Italic* - `*text*` or `_text_`
- `Inline code` - `` `code` ``

### Headers
- H1 through H6 - `# Header` to `###### Header`

### Lists
- Unordered lists with bullets
- Nested lists with proper indentation

### Code Blocks
- Fenced code blocks with triple backticks
- Proper monospace rendering
- ASCII art and diagrams display correctly

### Other Elements
- Blockquotes
- Horizontal rules
- Tables
- Links (displayed with blue color and underline)

## Technical Details

### Font Configuration

- **Body text**: DejaVu Sans, size 11
- **Code/monospace**: DejaVu Sans Mono, size 10
- **Headers**: Sized from 11pt (H6) to 24pt (H1)

### Text Widget Settings

- **Wrap mode**: NONE - Prevents text wrapping that would break ASCII art
- **Horizontal scrolling**: Enabled for long lines
- **Background**: White (#ffffff)
- **Foreground**: GitHub dark gray (#24292e)

### Markdown Extensions

The viewer uses the following Python markdown extensions:
- `extra` - Adds support for tables, fenced code, and more
- `tables` - Table rendering
- `fenced_code` - Triple-backtick code blocks

**Note**: The `codehilite` extension is intentionally NOT used as it breaks ASCII art rendering by inserting HTML spans.

## Testing

Sample markdown files are provided in the `sample_files/` directory for testing various rendering scenarios, including:
- Simple markdown documents
- Complex ASCII art diagrams
- Technical documentation
- Scientific papers

## Known Limitations

- Read-only display (no editing capability)
- No dark mode
- No file browser UI (must specify file via command line)
- Links are styled but not clickable
- Images are not rendered

## Project Structure

```
markdown_viewer/
├── markdown_viewer.py      # Main application
├── markdown-viewer         # Launcher script
├── markdown-viewer.spec    # PyInstaller configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── DEVELOPMENT_NOTES.md   # Technical implementation notes
├── sample_files/          # Test markdown files
├── build/                 # PyInstaller build artifacts
└── dist/                  # Compiled binaries
```

## License

This project is provided as-is for educational and personal use.

## Contributing

When working on this project, please refer to `DEVELOPMENT_NOTES.md` for technical details about the implementation and common issues.
