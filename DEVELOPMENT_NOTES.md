# Development Notes - Markdown Viewer

Technical documentation for developers and AI assistants working on the markdown viewer project.

**Last Updated**: 2025-11-20

---

## Project Versions

This project includes two versions of the markdown viewer:

1. **GUI Version** (`markdown_viewer.py`) - Tkinter-based desktop application
2. **Terminal Version** (`markdown_viewer_term.py`) - Rich-based terminal pager

## Architecture Overview

### GUI Version (Tkinter)

The GUI markdown viewer is built using three main components:

1. **Markdown to HTML Conversion** - Uses the Python `markdown` library to convert markdown text to HTML
2. **HTML Parser** - Custom `MarkdownRenderer` class extends `HTMLParser` to parse the generated HTML
3. **Tkinter Text Widget** - Displays the parsed content with styled tags

**Data Flow:**
```
Markdown File → markdown.markdown() → HTML → MarkdownRenderer → Tkinter Text Widget
```

### Terminal Version (Rich)

The terminal markdown viewer uses a simpler architecture:

1. **Markdown Parsing** - Rich library's built-in `Markdown` class handles parsing and rendering
2. **Console Output** - `Console` with pager mode for scrollable display
3. **Auto-width Detection** - Automatically adapts to terminal width

**Data Flow:**
```
Markdown File → Rich Markdown → Console.pager() → Terminal Display
```

## Key Implementation Details

### GUI Version Implementation

#### MarkdownRenderer Class

The `MarkdownRenderer` class (markdown_viewer.py:15-122) is a custom HTML parser that:
- Tracks parsing state (current tags, list levels, code block status)
- Converts HTML tags to Tkinter text widget tags
- Buffers code block content for batch insertion
- Handles nested structures (lists, blockquotes, tables)

**Important State Variables:**
- `current_tags` - Stack of active formatting tags
- `list_level` - Depth of nested lists
- `in_code_block` - Flag for code block processing
- `code_buffer` - Accumulates code block content before insertion

#### Text Widget Configuration

The Tkinter `ScrolledText` widget is configured with specific settings critical for proper rendering:

```python
wrap=tk.NONE  # CRITICAL: Prevents word wrapping
```

**Why NONE wrapping is essential:**
- ASCII art and diagrams require exact character positioning
- Word wrapping breaks box-drawing characters (┌─┐│└┘)
- Long lines get horizontal scrollbars instead of wrapping

### Terminal Version Implementation

#### Rich Library Integration

The terminal version uses Rich library's built-in capabilities:

**Console Configuration:**
```python
console = Console(force_terminal=True)  # Auto-detects terminal width, forces color output
```

**Direct Output (No Built-in Pager):**
```python
console.print(md)  # Prints to stdout
```

**Key Design Decisions:**
- **No built-in pager** - Output goes directly to stdout
- **User choice** - Users can pipe to their preferred pager (less, more, most, etc.)
- **Automatic paging** - Launcher script automatically pipes to `less -R` when available
- **force_terminal=True** - Ensures ANSI color codes are output even when piped
- Syntax highlighting for code blocks (automatic)
- No custom HTML parsing needed - Rich handles everything

**Launcher Script Behavior:**
- Detects if output is to a terminal (`-t 1` test)
- If to terminal and `less` is available: automatically pipes to `less -R`
- If output is piped: passes through without modification
- Users can override by manually piping to any pager

**Error Handling:**
- File not found errors with styled output to stderr
- Generic exception handling with user-friendly messages
- Exit codes (0 for success, 1 for errors)

## ASCII Art Rendering - Critical Fixes

### Problem History

The viewer initially had issues rendering ASCII art diagrams with box-drawing characters. The problems were:

1. **Blank lines appearing within boxes** - Breaking visual continuity
2. **Extra spaces in the middle of boxes** - Disrupting alignment

### Root Causes Identified

#### Issue #1: codehilite Extension
**Problem**: The `codehilite` markdown extension was breaking ASCII art into syntax-highlighted HTML spans.

**Example HTML Output**:
```html
<span class="err">┌─────┐</span>
<span class="err">│</span><span class="w"> Text </span><span class="err">│</span>
```

**Impact**: Each span caused the HTML parser to make separate `handle_data()` calls, inserting text in chunks and creating visual breaks.

**Fix**: Removed `'codehilite'` from the extensions list (line 194):
```python
# Before
extensions=['extra', 'codehilite', 'tables', 'fenced_code']

# After
extensions=['extra', 'tables', 'fenced_code']
```

#### Issue #2: Tag Spacing Parameters
**Problem**: The `code_block` tag had `spacing1` and `spacing3` parameters that added vertical spacing.

**Impact**: In Tkinter, these spacing parameters can affect line rendering within code blocks, potentially adding unwanted space.

**Fix**: Removed all spacing parameters from code_block tag (lines 178-179):
```python
# Before
self.text.tag_configure('code_block', font=code_font, background='#f6f8fa',
                        foreground='#24292e', lmargin1=10, lmargin2=10,
                        rmargin=10, spacing1=10, spacing3=10)

# After
self.text.tag_configure('code_block', font=code_font, background='#f6f8fa',
                        foreground='#24292e', lmargin1=10, lmargin2=10, rmargin=10)
```

#### Issue #3: Text Wrapping
**Problem**: The text widget was configured with `wrap=tk.WORD`, causing long ASCII art lines to wrap at word boundaries.

**Impact**: Box-drawing characters would wrap mid-line, creating gaps and misalignment.

**Fix**: Changed wrap mode to NONE (line 137):
```python
# Before
wrap=tk.WORD

# After
wrap=tk.NONE
```

### Verification

After all three fixes, ASCII art renders correctly:
- No blank lines within boxes
- No extra spaces from wrapping
- Box-drawing characters maintain alignment
- Long lines show horizontal scrollbar

## Tag Configuration Reference

### Font Definitions (lines 148-158)

```python
default_font = Font(family='DejaVu Sans', size=11)
code_font = Font(family='DejaVu Sans Mono', size=10)
bold_font = Font(family='DejaVu Sans', size=11, weight='bold')
italic_font = Font(family='DejaVu Sans', size=11, slant='italic')
h1_font = Font(family='DejaVu Sans', size=24, weight='bold')
h2_font = Font(family='DejaVu Sans', size=20, weight='bold')
h3_font = Font(family='DejaVu Sans', size=16, weight='bold')
h4_font = Font(family='DejaVu Sans', size=14, weight='bold')
h5_font = Font(family='DejaVu Sans', size=12, weight='bold')
h6_font = Font(family='DejaVu Sans', size=11, weight='bold')
```

### Color Scheme (GitHub-inspired)

- **Background**: `#ffffff` (white)
- **Text**: `#24292e` (dark gray)
- **Code background**: `#f6f8fa` (light gray)
- **Inline code**: `#e83e8c` (pink/magenta)
- **Links**: `#0366d6` (blue)
- **Blockquote**: `#6a737d` (medium gray)
- **Bullets**: `#0366d6` (blue)
- **H6**: `#6a737d` (medium gray)
- **HR**: `#e1e4e8` (very light gray)

## Code Block Processing

### How Code Blocks are Handled

1. **Markdown conversion** creates `<pre><code>` HTML tags
2. **Parser detects** `<pre>` start tag, sets `in_code_block = True`
3. **Content buffering** - All data within `<code>` tags goes into `code_buffer`
4. **Batch insertion** - On `</pre>` end tag, entire buffer is joined and inserted as single chunk with `code_block` tag
5. **Newline preservation** - Code content maintains original newline characters

### Why Buffering is Important

```python
def handle_endtag(self, tag):
    if tag == 'pre':
        if self.code_buffer:
            code_text = ''.join(self.code_buffer)  # Join all chunks
            self.text.insert(tk.END, code_text, 'code_block')
            self.text.insert(tk.END, '\n')
        self.in_code_block = False
        self.code_buffer = []
```

If we inserted each chunk separately, we would lose the ability to apply the `code_block` tag uniformly and might create rendering artifacts.

## Markdown Extensions Explained

### Extensions Used

1. **extra** - Meta-extension that includes:
   - Fenced code blocks
   - Tables
   - Footnotes
   - Attribute lists
   - Definition lists
   - Abbreviations

2. **tables** - Explicit table support (also included in `extra`)

3. **fenced_code** - Triple-backtick code blocks (also included in `extra`)

### Why codehilite is NOT Used

The `codehilite` extension provides syntax highlighting by wrapping code in `<span>` tags with CSS classes. For a Tkinter text widget:

**Problems**:
- Creates multiple `handle_data()` calls per line
- Breaks ASCII art into fragments
- Requires complex span-to-tag mapping
- Adds unnecessary complexity

**Alternative**: If syntax highlighting is desired in the future, it should be implemented in the `MarkdownRenderer` directly using Tkinter tags, not HTML spans.

## Testing Recommendations

### Test Cases for ASCII Art

When modifying the renderer, always test with:
1. **Box-drawing characters**: ┌─┐│└┘├┤┬┴┼
2. **Long lines**: Lines exceeding 80 characters
3. **Nested boxes**: Boxes within boxes
4. **Arrow characters**: →←↑↓▶◀▲▼

### Test Files

The `sample_files/` directory includes:
- `CHAT_PIPELINE_ARCHITECTURE.md` - Complex ASCII diagrams (CRITICAL test file)
- `sample.md` - Basic markdown features
- Various technical documents with different formatting

### Visual Regression Testing

To verify ASCII art rendering:
1. Open `CHAT_PIPELINE_ARCHITECTURE.md` in the viewer
2. Check the "High-Level Architecture" diagram:
   - User Interface box should be continuous
   - ChatController box with nested Processing Pipeline should be intact
   - All vertical and horizontal lines should align
   - No blank lines within boxes
   - No text wrapping within boxes

## Common Pitfalls

### 1. Re-enabling Text Wrapping
**Never** change `wrap=tk.NONE` to `wrap=tk.WORD` or `wrap=tk.CHAR`. This will immediately break ASCII art.

### 2. Adding Tag Spacing
Be very careful adding `spacing1`, `spacing2`, or `spacing3` parameters to the `code_block` tag. These can create unexpected vertical spacing.

### 3. Modifying Code Block Insertion
The code block content must be inserted as a single operation:
```python
# GOOD
code_text = ''.join(self.code_buffer)
self.text.insert(tk.END, code_text, 'code_block')

# BAD - Don't do this
for chunk in self.code_buffer:
    self.text.insert(tk.END, chunk, 'code_block')
```

### 4. Adding Syntax Highlighting
If you want to add syntax highlighting, DO NOT add the `codehilite` extension. Instead:
- Use a library like `pygments` to get color information
- Apply colors using Tkinter tags, not HTML spans
- Test thoroughly with ASCII art

## Future Enhancement Ideas

### Safe Enhancements
- Dark mode (invert colors, add theme switching)
- File browser dialog
- Recently opened files list
- Find/search functionality
- Font size adjustment
- Export to PDF

### Risky Enhancements (Test Carefully)
- Syntax highlighting for code blocks
- Image rendering
- Clickable links
- Table of contents generation
- Custom CSS/styling

### Not Recommended
- Changing wrap mode
- Adding markdown extensions that inject HTML
- Modifying the core rendering pipeline without thorough testing

## Debugging Tips

### Enable Debug Output

To debug rendering issues, temporarily add print statements:

```python
def handle_endtag(self, tag):
    if tag == 'pre':
        if self.code_buffer:
            code_text = ''.join(self.code_buffer)
            # DEBUG
            print(f"Code block: {len(self.code_buffer)} chunks, {len(code_text)} chars")
            print(f"First 200 chars: {repr(code_text[:200])}")
            print(f"Newlines: {code_text.count('\\n')}")
            # END DEBUG
            self.text.insert(tk.END, code_text, 'code_block')
```

### Check HTML Output

To see what HTML is being generated:

```python
import markdown

with open('test.md', 'r') as f:
    md_content = f.read()

html = markdown.markdown(md_content, extensions=['extra', 'tables', 'fenced_code'])
print(html[:500])  # Print first 500 chars
```

### Tag Inspection

To see what tags are applied to text:

```python
# In Tkinter, after rendering
for tag in self.text.tag_names():
    ranges = self.text.tag_ranges(tag)
    print(f"Tag '{tag}': {len(ranges)//2} ranges")
```

## Dependencies

### Required (GUI Version)
- `markdown>=3.4.0` - Markdown to HTML conversion
- `tkinter` - GUI (usually included with Python)

### Required (Terminal Version)
- `markdown>=3.4.0` - Markdown parsing (used by Rich)
- `rich>=13.0.0` - Terminal rendering and pager functionality

### Optional (for building)
- `pyinstaller` - Create standalone executables

### System Fonts Required
- DejaVu Sans
- DejaVu Sans Mono

If these fonts are missing, Tkinter will fall back to system defaults, which may affect rendering quality.

## Build Process

The project can be compiled to a standalone binary using PyInstaller:

```bash
pyinstaller markdown-viewer.spec
```

The spec file configures:
- Entry point: `markdown_viewer.py`
- Binary name: `markdown-viewer`
- Hidden imports: `markdown` and extensions
- One-file vs one-directory output

## Git and Version Control

### Important Files
- `markdown_viewer.py` - Core GUI application (track changes carefully)
- `markdown_viewer_term.py` - Terminal application
- `markdown-viewer` - GUI launcher script
- `markdown-viewer-term` - Terminal launcher script
- `requirements.txt` - Dependencies
- `README.md` - User documentation
- `DEVELOPMENT_NOTES.md` - This file
- `TERMINAL_VIEWER_IMPLEMENTATION_PLAN.md` - Terminal version design

### Generated Files (can be ignored)
- `build/` - PyInstaller artifacts
- `dist/` - Compiled binaries
- `__pycache__/` - Python bytecode

## Changelog

### 2025-11-20 - Terminal Version Implementation
- Added terminal-based markdown viewer using Rich library
- Created `markdown_viewer_term.py` with direct stdout output
- Created `markdown-viewer-term` launcher script with automatic pager detection
- Removed built-in pager in favor of user choice (pipe to any pager)
- Launcher script automatically uses `less -R` when output is to terminal
- Set `force_terminal=True` to preserve colors when piped
- Added `rich>=13.0.0` dependency to requirements.txt
- Updated README.md with terminal version documentation
- Updated DEVELOPMENT_NOTES.md with terminal implementation details
- Tested with sample files including ASCII art diagrams
- Both GUI and terminal versions now available

### 2025-11-08 - ASCII Art Rendering Fixes
- Removed `codehilite` extension to prevent span fragmentation
- Removed spacing parameters from `code_block` tag
- Changed text widget wrap mode from WORD to NONE
- Verified rendering with CHAT_PIPELINE_ARCHITECTURE.md
- Created comprehensive project documentation

### Initial Version
- Basic markdown rendering
- GitHub-like styling
- Support for headers, lists, code, tables, blockquotes
- PyInstaller build configuration
