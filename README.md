# Markdown & Mermaid Viewer

A lightweight viewer collection for markdown files and Mermaid diagrams, with GitHub-like styling. Available in both GUI (Tkinter) and terminal (Rich) versions.

## Features

### Markdown GUI Version (Tkinter)
- **GitHub-like styling** - Clean, professional rendering that matches GitHub's markdown display
- **Rich markdown support** - Headers, bold, italic, code blocks, lists, blockquotes, tables, and more
- **ASCII art rendering** - Properly displays ASCII diagrams and box-drawing characters without wrapping or spacing issues
- **Syntax-aware code blocks** - Monospace font with gray background for code snippets
- **Horizontal scrolling** - Long lines don't wrap, maintaining formatting integrity
- **Desktop window** - Resizable GUI window with scrollbars

### Terminal Version (Rich)
- **Flexible output** - Direct stdout output or pipe to any pager
- **GitHub-like styling** - Professional rendering with colors and formatting
- **Syntax highlighting** - Automatic code syntax highlighting in blocks
- **Auto-width detection** - Adapts to terminal width automatically
- **Pager integration** - Launcher script automatically uses `less -R` when available
- **Pipe-friendly** - Works with any pager (less, more, most, etc.)
- **Lightweight** - Pure Python with minimal dependencies

### Mermaid Diagram Viewer - GUI (Tkinter)
- **Click and view** - Double-click `.mmd` files to instantly view diagrams
- **Auto-download** - Fetches rendered diagram from mermaid.ink automatically
- **Scrollable canvas** - View large diagrams with horizontal and vertical scrolling
- **All diagram types** - Supports flowcharts, sequence diagrams, class diagrams, state diagrams, Gantt charts, and more
- **Simple and fast** - Opens in seconds, no complex setup required

### Mermaid Diagram Viewer - Terminal (Rich)
- **Syntax highlighting** - Colorized Mermaid source code display
- **Online rendering** - Generates URLs for viewing diagrams via mermaid.ink
- **Multiple formats** - Provides both PNG and SVG URLs
- **Download instructions** - Built-in curl commands for saving diagrams
- **All diagram types** - Supports flowcharts, sequence diagrams, class diagrams, state diagrams, Gantt charts, and more
- **Pure Python** - No Node.js or external binaries required

## Installation

### Requirements

- Python 3.6+
- Tkinter (usually included with Python) - for GUI versions
- markdown library - for markdown rendering
- rich library - for terminal versions
- mermaid-py library - for Mermaid diagram viewers
- Pillow (PIL) library - for Mermaid GUI viewer image display

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Make the launcher scripts executable (optional)
chmod +x markdown-viewer
chmod +x markdown-viewer-term
chmod +x mermaid-viewer
chmod +x mermaid-viewer-term
```

## Usage

### GUI Version

```bash
# Using Python directly
python3 markdown_viewer.py <filename.md>

# Using the launcher script
./markdown-viewer <filename.md>

# Example
python3 markdown_viewer.py sample_files/README.md
```

### Terminal Version

```bash
# Using Python directly (outputs to stdout)
python3 markdown_viewer_term.py <filename.md>

# Using the launcher script (automatically pipes to less if available)
./markdown-viewer-term <filename.md>

# Manually pipe to your preferred pager
python3 markdown_viewer_term.py <filename.md> | less -R
python3 markdown_viewer_term.py <filename.md> | more

# Example
./markdown-viewer-term sample_files/CHAT_PIPELINE_ARCHITECTURE.md
```

**Terminal Navigation (when using a pager):**
- Use arrow keys, Page Up/Down, or Space to scroll
- Press `q` to quit (in less)
- The launcher script automatically uses `less -R` if available and output is not piped

### Mermaid Diagram Viewer - GUI

```bash
# Using Python directly
python3 mermaid_viewer_gui.py <filename.mmd>

# Using the launcher script
./mermaid-viewer <filename.mmd>

# Examples
./mermaid-viewer sample_files/sample_flowchart.mmd
./mermaid-viewer sample_files/sample_sequence.mmd
```

**What happens:**
1. Window opens with "Loading diagram..." message
2. Diagram is fetched from mermaid.ink and displayed
3. Scroll to view large diagrams
4. Close window when done

**Perfect for:**
- Quick viewing of `.mmd` files
- File manager integration (double-click to view)
- Presentations and documentation review

### Mermaid Diagram Viewer - Terminal

```bash
# Using Python directly (outputs to stdout)
python3 mermaid_viewer_term.py <filename.mmd>

# Using the launcher script (automatically pipes to less if available)
./mermaid-viewer-term <filename.mmd>

# Example
./mermaid-viewer-term sample_files/sample_flowchart.mmd
```

**What you get:**
- Syntax-highlighted Mermaid source code
- PNG and SVG URLs for viewing the rendered diagram
- Ready-to-use curl commands for downloading diagrams

**To view the diagram:**
1. Copy the PNG or SVG URL and open in a browser
2. Or use the provided curl command to download the image
3. Diagrams are rendered via mermaid.ink (online service)

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

### GUI Version

**Font Configuration:**
- **Body text**: DejaVu Sans, size 11
- **Code/monospace**: DejaVu Sans Mono, size 10
- **Headers**: Sized from 11pt (H6) to 24pt (H1)

**Text Widget Settings:**
- **Wrap mode**: NONE - Prevents text wrapping that would break ASCII art
- **Horizontal scrolling**: Enabled for long lines
- **Background**: White (#ffffff)
- **Foreground**: GitHub dark gray (#24292e)

**Markdown Extensions:**
- `extra` - Adds support for tables, fenced code, and more
- `tables` - Table rendering
- `fenced_code` - Triple-backtick code blocks

**Note**: The `codehilite` extension is intentionally NOT used as it breaks ASCII art rendering by inserting HTML spans.

### Terminal Version

**Rendering:**
- Uses Rich library's built-in Markdown renderer
- Automatic syntax highlighting for code blocks
- Auto-detects terminal width for optimal display
- Pager mode with standard keyboard controls

**Terminal Compatibility:**
- Full color support on modern terminals
- Graceful fallback for limited terminals
- Unicode box-drawing character support

### Mermaid Diagram Viewer

**Rendering:**
- Uses mermaid-py library to generate mermaid.ink URLs
- Syntax highlighting for Mermaid source code via Rich
- Online rendering via mermaid.ink service (no local rendering)
- Supports all Mermaid diagram types

**Output:**
- Displays formatted source code with line numbers
- Provides PNG and SVG URLs for browser viewing
- Includes ready-to-use curl download commands
- No external binaries or Node.js required

## Testing

Sample markdown files are provided in the `sample_files/` directory for testing various rendering scenarios, including:
- Simple markdown documents
- Complex ASCII art diagrams
- Technical documentation
- Scientific papers

Sample Mermaid diagram files (`.mmd`) are also included:
- Flowcharts (`sample_flowchart.mmd`)
- Sequence diagrams (`sample_sequence.mmd`)

## Known Limitations

### GUI Version
- Read-only display (no editing capability)
- No dark mode
- No file browser UI (must specify file via command line)
- Links are styled but not clickable
- Images are not rendered

### Terminal Version
- Read-only display (no editing capability)
- Links are styled but not clickable
- Images are not rendered
- Requires terminal with Unicode support for best experience

### Mermaid GUI Viewer
- Requires internet connection (uses mermaid.ink service)
- Diagrams rendered by external service
- No offline viewing capability
- Read-only display

## File Association (Double-Click to Open)

### Linux (GNOME/Nautilus)

To make `.mmd` files open with the Mermaid GUI viewer when double-clicked:

1. **Right-click any `.mmd` file** → **Properties**
2. **Open With** tab → **Add Application**
3. **Use a custom command:**
   ```
   /full/path/to/markdown_viewer/mermaid-viewer %f
   ```
   Replace `/full/path/to/` with your actual path
4. **Set as default** and click OK

**Or create a .desktop file:**

```bash
mkdir -p ~/.local/share/applications

cat > ~/.local/share/applications/mermaid-viewer.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Mermaid Diagram Viewer
Comment=View Mermaid diagrams
Exec=/full/path/to/markdown_viewer/mermaid-viewer %f
Terminal=false
Categories=Graphics;Viewer;
MimeType=text/plain;
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications
```

### Linux (KDE/Dolphin)

1. **Right-click `.mmd` file** → **Properties**
2. **File Association** → **Add**
3. Browse to `mermaid-viewer` script
4. Set as default

### macOS

Create a simple AppleScript application:

```applescript
on run {input}
    do shell script "/full/path/to/markdown_viewer/mermaid-viewer " & quoted form of POSIX path of (item 1 of input)
end run
```

Save as Application, then right-click `.mmd` file → Get Info → Open with → Select your app

## Project Structure

```
markdown_viewer/
├── markdown_viewer.py      # Markdown GUI application (Tkinter)
├── markdown_viewer_term.py # Markdown terminal viewer (Rich)
├── mermaid_viewer_gui.py   # Mermaid GUI viewer (Tkinter)
├── mermaid_viewer_term.py  # Mermaid terminal viewer (Rich)
├── markdown-viewer         # Markdown GUI launcher script
├── markdown-viewer-term    # Markdown terminal launcher script
├── mermaid-viewer          # Mermaid GUI launcher script
├── mermaid-viewer-term     # Mermaid terminal launcher script
├── markdown-viewer.spec    # PyInstaller configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── DEVELOPMENT_NOTES.md   # Technical implementation notes
├── TERMINAL_VIEWER_IMPLEMENTATION_PLAN.md
├── PROJECT_CHECKPOINT.md  # Project state for resumption
├── sample_files/          # Test markdown and Mermaid files
│   ├── *.md               # Markdown test files
│   └── *.mmd              # Mermaid diagram files
├── build/                 # PyInstaller build artifacts
└── dist/                  # Compiled binaries
```

## License

This project is provided as-is for educational and personal use.

## Contributing

When working on this project, please refer to `DEVELOPMENT_NOTES.md` for technical details about the implementation and common issues.
