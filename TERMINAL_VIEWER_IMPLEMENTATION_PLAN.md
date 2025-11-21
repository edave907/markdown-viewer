# Terminal Viewer Implementation Plan

## Overview

Create a pager-style terminal markdown viewer as a companion to the existing GUI viewer.

## Design Decisions

### 1. Viewer Type
- **Pager-style viewer** (like `less` for markdown)
- Render markdown, display with scrolling, exit when done

### 2. Library Choice
- **Rich** library for markdown rendering
- Built-in markdown support with GitHub-like styling
- Automatic syntax highlighting for code blocks
- Natural handling of ASCII art with monospace blocks

### 3. User Requirements
- **Launcher name**: `markdown-viewer-term`
- **Fallback behavior**: Render plain text if terminal doesn't support colors/Unicode
- **Width handling**: Auto-detect terminal width

## Implementation Plan

### New Files to Create

#### 1. `markdown_viewer_term.py` - Main terminal viewer application

```python
#!/usr/bin/env python3
"""
Terminal Markdown Viewer - A pager-style terminal viewer for markdown files
Usage: python markdown_viewer_term.py <filename.md>
"""

import sys
from rich.console import Console
from rich.markdown import Markdown

def main():
    # Parse command line args
    # Read markdown file
    # Create Console with auto-detected width
    # Render Markdown object
    # Display with pager
    # Handle errors gracefully (file not found, etc.)
    # Fallback to plain text if terminal doesn't support rich features
```

**Key Implementation Details:**
- Use `Console(width=None)` to auto-detect terminal width
- Use `console.pager()` context manager for scrollable viewing
- Wrap in try/except for graceful error handling
- Rich will automatically fallback for limited terminals
- Preserve the same markdown extensions philosophy (no codehilite issues)

#### 2. `markdown-viewer-term` - Launcher script

Similar structure to existing `markdown-viewer` launcher:
```bash
#!/usr/bin/env python3
# Launcher script that calls markdown_viewer_term.py
```

### Updates to Existing Files

#### 1. `requirements.txt`
Add:
```
rich>=13.0.0
```

#### 2. `README.md`
Add section documenting terminal viewer:
- Installation (with rich dependency)
- Usage examples
- Feature comparison with GUI version
- Terminal compatibility notes

#### 3. `DEVELOPMENT_NOTES.md`
Add section about terminal version:
- Architecture differences
- Rich library integration
- Testing considerations
- Terminal width handling

## Key Features

### Rendering
- GitHub-like styling (Rich defaults)
- Syntax highlighting in code blocks (automatic)
- Proper table rendering
- Blockquote styling
- Header hierarchy

### Interaction
- Scrollable with arrow keys, page up/down, space
- Quit with 'q'
- Standard pager controls

### Compatibility
- Auto-detect terminal capabilities
- Fallback to plain text for limited terminals
- Preserve ASCII art formatting
- Handle wide content appropriately

## Testing Approach

### Test Files
Use existing sample files from `sample_files/`:
- `CHAT_PIPELINE_ARCHITECTURE.md` - ASCII art stress test
- `sample.md` - Basic markdown features
- Various technical documents

### Test Scenarios
1. **Different terminal types**
   - xterm
   - gnome-terminal
   - konsole
   - Terminal emulators with limited color support

2. **Terminal width variations**
   - Narrow terminals (80 columns)
   - Wide terminals (200+ columns)
   - Dynamic resizing

3. **Content types**
   - ASCII art diagrams
   - Code blocks with syntax highlighting
   - Tables
   - Long lines requiring horizontal scrolling
   - Nested lists and blockquotes

### Success Criteria
- ASCII art renders without breaking (critical test case)
- Code blocks display with proper monospace formatting
- Tables align correctly
- Pager controls work intuitively
- Graceful error handling for missing files
- Clean fallback for unsupported terminals

## Future Enhancements (Optional)

- Search functionality within the pager
- Line numbering option
- Custom color themes
- Export rendered output to HTML
- Side-by-side comparison mode

## Dependencies

### Required
- `rich>=13.0.0` - Terminal rendering and markdown support
- Python 3.6+ (same as GUI version)

### System Requirements
- Terminal with Unicode support (preferred)
- Color support (optional, will fallback)

## Command-Line Interface

```bash
# Using Python directly
python3 markdown_viewer_term.py <filename.md>

# Using launcher script
./markdown-viewer-term <filename.md>

# Using from dist/ if compiled
./dist/markdown-viewer-term <filename.md>
```

## Development Workflow

1. Create `markdown_viewer_term.py` with basic structure
2. Create `markdown-viewer-term` launcher script
3. Update `requirements.txt`
4. Test with sample files
5. Update documentation (README.md, DEVELOPMENT_NOTES.md)
6. Update PyInstaller spec if needed for terminal version
7. Final testing across different terminals

## Notes

- Keep implementation simple and focused
- Leverage Rich's built-in capabilities rather than reimplementing
- Maintain consistency with GUI version where appropriate
- Document any terminal-specific quirks or limitations
