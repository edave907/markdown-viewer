# Project Checkpoint - Markdown & Mermaid Viewer

**Date:** 2025-11-22
**Status:** Feature Complete - Production Ready
**Repository:** github.com:edave907/markdown-viewer.git
**Branch:** main

---

## Project Overview

A complete collection of lightweight viewers for markdown files and Mermaid diagrams, with GitHub-like styling. Available in both GUI (Tkinter) and terminal (Rich) versions. **Includes file association support for double-click viewing.**

### Current Features

#### 1. Markdown Viewer - GUI Version (Tkinter)
- GitHub-like styling with professional rendering
- Full markdown support (headers, lists, code blocks, tables, blockquotes)
- ASCII art rendering with horizontal scrolling (no wrapping)
- Custom HTML parser converting to Tkinter tags
- **File:** `markdown_viewer.py`
- **Launcher:** `markdown-viewer`
- **File Association:** Via `.desktop` file

#### 2. Markdown Viewer - Terminal Version (Rich)
- Direct stdout output (pipe-friendly)
- Syntax highlighting for code blocks
- Auto-width detection for terminal
- Launcher auto-pipes to `less -R` when available
- Works with any pager (less, more, most)
- **File:** `markdown_viewer_term.py`
- **Launcher:** `markdown-viewer-term`

#### 3. Mermaid Diagram Viewer - GUI Version (Tkinter) **NEW!**
- Click and view - double-click `.mmd` files to open
- Auto-downloads rendered diagram from mermaid.ink
- Scrollable canvas for large diagrams
- Loading message while fetching
- Supports all Mermaid diagram types
- **File:** `mermaid_viewer_gui.py`
- **Launcher:** `mermaid-viewer`
- **File Association:** Via `.desktop` file

#### 4. Mermaid Diagram Viewer - Terminal Version (Rich)
- Syntax-highlighted Mermaid source code display
- Generates mermaid.ink URLs (PNG and SVG)
- Ready-to-use curl download commands
- Supports all Mermaid diagram types
- Pure Python (no Node.js required)
- **File:** `mermaid_viewer_term.py`
- **Launcher:** `mermaid-viewer-term`

#### 5. Desktop Integration **NEW!**
- One-command installation script
- Automatic file association setup
- Double-click `.md` and `.mmd` files to view
- **File:** `install-desktop-files.sh`

---

## Project Structure

```
markdown_viewer/
├── markdown_viewer.py          # Markdown GUI application (Tkinter)
├── markdown_viewer_term.py     # Markdown terminal viewer (Rich)
├── mermaid_viewer_gui.py       # Mermaid GUI viewer (Tkinter)
├── mermaid_viewer_term.py      # Mermaid terminal viewer (Rich)
├── markdown-viewer             # Markdown GUI launcher script
├── markdown-viewer-term        # Markdown terminal launcher script
├── mermaid-viewer              # Mermaid GUI launcher script
├── mermaid-viewer-term         # Mermaid terminal launcher script
├── install-desktop-files.sh    # Desktop file installer
├── markdown-viewer.spec        # PyInstaller configuration
├── requirements.txt            # Python dependencies
├── README.md                   # User documentation
├── DEVELOPMENT_NOTES.md        # Technical implementation notes
├── TERMINAL_VIEWER_IMPLEMENTATION_PLAN.md
├── PROJECT_CHECKPOINT.md       # This file
├── sample_files/               # Test files
│   ├── *.md                    # Markdown test files
│   ├── sample_flowchart.mmd    # Mermaid flowchart example
│   └── sample_sequence.mmd     # Mermaid sequence diagram example
├── build/                      # PyInstaller build artifacts
└── dist/                       # Compiled binaries
```

---

## Dependencies

### Python Packages (requirements.txt)
```
markdown>=3.4.0
rich>=13.0.0
mermaid-py>=0.4.0
Pillow>=9.0.0
```

### System Requirements
- Python 3.6+
- Tkinter (usually included with Python) - for GUI versions
- Pillow (PIL) - for Mermaid GUI image display
- Terminal with Unicode support (for best terminal experience)
- Internet connection (for Mermaid diagram rendering via mermaid.ink)

---

## Recent Changes (Latest Session - 2025-11-22)

### Mermaid GUI Viewer (NEW)
- Implemented GUI Mermaid diagram viewer
- Downloads and displays diagrams from mermaid.ink
- Scrollable canvas for large diagrams
- Loading message during fetch
- Uses PIL/ImageTk for image display
- Created `mermaid_viewer_gui.py` (105 lines)
- Created `mermaid-viewer` launcher script

### Desktop Integration (NEW)
- Created `install-desktop-files.sh` installer
- One-command file association setup
- Auto-detects script directory (no hardcoded paths)
- Creates `.desktop` files for both viewers
- Updates desktop database automatically
- Enables double-click to open `.md` and `.mmd` files

### Previous Session Changes (2025-11-20)

#### Terminal Markdown Viewer
- Removed built-in pager in favor of user choice
- Added `force_terminal=True` to preserve colors when piped
- Launcher script auto-detects terminal output and pipes to `less -R`
- Fixed ANSI escape sequence rendering in xterm-256color

#### Mermaid Terminal Viewer
- Implemented terminal-based Mermaid viewer
- Uses mermaid-py library for URL generation
- Displays syntax-highlighted source code
- Provides PNG and SVG URLs via mermaid.ink
- Includes curl download commands
- Same pipe-friendly design as markdown viewer

---

## Git Status

**Last Commit:** `6f6f2c0` - Add .desktop file installer for easy file association
**Remote:** origin/main (up to date)
**Untracked Files:** `junk` (not part of project)

### Recent Commit History
```
6f6f2c0 - Add .desktop file installer for easy file association
e42b59f - Add Mermaid GUI viewer - click to view diagrams
f2b0abd - Add project checkpoint for future resumption
65076ca - Add Mermaid diagram viewer for terminal
7ea174f - Remove built-in pager, allow users to choose external pager
36bd89d - Fix ANSI escape sequences in terminal viewer
3831197 - Implement terminal-based markdown viewer with Rich library
47ada0f - Add implementation plan for terminal-based markdown viewer
8c24239 - Initial commit: Markdown viewer with GitHub-like styling
```

---

## Usage Examples

### Markdown GUI Viewer
```bash
./markdown-viewer sample_files/README.md
python3 markdown_viewer.py sample_files/CHAT_PIPELINE_ARCHITECTURE.md

# Or double-click any .md file (after running install-desktop-files.sh)
```

### Markdown Terminal Viewer
```bash
# Auto-pager (uses less -R automatically)
./markdown-viewer-term sample_files/README.md

# Manual pager selection
python3 markdown_viewer_term.py file.md | less -R
python3 markdown_viewer_term.py file.md | more
```

### Mermaid GUI Viewer
```bash
./mermaid-viewer sample_files/sample_flowchart.mmd
./mermaid-viewer sample_files/sample_sequence.mmd

# Or double-click any .mmd file (after running install-desktop-files.sh)
```

### Mermaid Terminal Viewer
```bash
# View Mermaid source and get URLs
./mermaid-viewer-term sample_files/sample_flowchart.mmd

# Download rendered diagram
curl -o diagram.png "https://mermaid.ink/img/..."
```

### Desktop Integration
```bash
# One-time setup for file associations
./install-desktop-files.sh

# Now you can double-click:
# - Any .md file → Opens in Markdown Viewer GUI
# - Any .mmd file → Opens in Mermaid Diagram Viewer GUI
```

---

## Key Technical Details

### GUI Version Architecture
```
Markdown File → markdown.markdown() → HTML → MarkdownRenderer → Tkinter Text Widget
```

**Critical Implementation:**
- `wrap=tk.NONE` - Essential for ASCII art (no word wrapping)
- No `codehilite` extension - Prevents HTML span fragmentation
- Code block buffering - Ensures proper rendering

### Terminal Version Architecture
```
Markdown File → Rich Markdown → Console → stdout (pipe to pager)
```

**Key Design:**
- `force_terminal=True` - Preserves colors when piped
- Direct stdout output - User chooses pager
- Launcher script intelligence - Auto-pipes to less if available

### Mermaid Viewer Architecture
```
Mermaid File → mermaid-py → mermaid.ink URLs → Display with Rich
```

**Key Features:**
- Online rendering via mermaid.ink
- No local JavaScript runtime needed
- Base64-encoded diagrams in URLs

---

## Testing

### Test Files Available
- `sample_files/sample.md` - Basic markdown features
- `sample_files/CHAT_PIPELINE_ARCHITECTURE.md` - Complex ASCII art (critical test)
- `sample_files/README.md` - Standard documentation
- `sample_files/sample_flowchart.mmd` - Mermaid flowchart
- `sample_files/sample_sequence.mmd` - Mermaid sequence diagram
- Plus 10+ other markdown samples (scientific papers, technical docs, etc.)

### Critical Tests to Run
1. **ASCII Art Rendering (GUI):**
   ```bash
   python3 markdown_viewer.py sample_files/CHAT_PIPELINE_ARCHITECTURE.md
   ```
   Verify: No blank lines in boxes, no wrapping, proper alignment

2. **Color Codes (Terminal):**
   ```bash
   ./markdown-viewer-term sample_files/sample.md | head -20
   ```
   Verify: ANSI codes rendered as colors, not literal ESC sequences

3. **Mermaid URLs (Terminal):**
   ```bash
   ./mermaid-viewer-term sample_files/sample_flowchart.mmd
   ```
   Verify: URLs are valid and open in browser

---

## Known Issues & Limitations

### GUI Version
- Read-only display (no editing)
- No dark mode
- Links styled but not clickable
- Images not rendered

### Terminal Version
- Links styled but not clickable
- Images not rendered
- Requires Unicode terminal for best experience

### Mermaid Viewer
- Requires internet connection (uses mermaid.ink)
- Diagrams rendered by external service
- No offline viewing (could add mermaid-cli option later)

---

## Future Enhancement Ideas

### High Priority
- [ ] Dark mode for GUI version
- [ ] Clickable links (both GUI and terminal)
- [ ] Image rendering support
- [ ] File browser dialog for GUI

### Medium Priority
- [ ] Mermaid GUI viewer (Tkinter-based)
- [ ] Local Mermaid rendering option (using mermaid-cli)
- [ ] Search functionality in viewers
- [ ] Export capabilities (PDF, HTML)

### Low Priority
- [ ] PyInstaller builds for terminal versions
- [ ] Config file for customization
- [ ] Bookmark/favorites system
- [ ] Recently opened files list

### Risky Changes (Test Carefully)
- Syntax highlighting in GUI (don't break ASCII art!)
- Custom CSS/theming
- Plugin system

---

## Development Environment

### Setup Commands
```bash
# Clone repository
git clone git@github.com:edave907/markdown-viewer.git
cd markdown-viewer

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x markdown-viewer markdown-viewer-term mermaid-viewer-term

# Test all viewers
./markdown-viewer sample_files/sample.md
./markdown-viewer-term sample_files/sample.md
./mermaid-viewer-term sample_files/sample_flowchart.mmd
```

### Terminal Used
- **Type:** xterm-256color
- **OS:** Linux 6.12.12+bpo-amd64
- **Pager:** less with `-R` flag (for ANSI colors)

---

## Important Notes for Resuming Development

### Before Making Changes

1. **Read DEVELOPMENT_NOTES.md** - Contains critical implementation details
2. **Test ASCII art rendering** - Use CHAT_PIPELINE_ARCHITECTURE.md
3. **Never change `wrap=tk.NONE`** - Will break ASCII art in GUI
4. **Never add `codehilite` extension** - Fragments ASCII art with spans
5. **Keep `force_terminal=True`** - Required for pipe color preservation

### Critical Files to Preserve
- `markdown_viewer.py:137` - `wrap=tk.NONE` setting
- `markdown_viewer.py:194` - Extension list (no codehilite)
- `markdown_viewer_term.py:33` - `force_terminal=True` setting
- `markdown-viewer-term:22-32` - Pager detection logic

### Git Workflow
```bash
# Check current status
git status
git log --oneline -5

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, test thoroughly

# Commit with descriptive message
git add -A
git commit -m "Description

Details...

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to remote
git push origin feature/your-feature-name
```

---

## Quick Reference Commands

### View Git History
```bash
git log --oneline --graph --all
git show <commit-hash>
git diff main..HEAD
```

### Test All Viewers
```bash
# GUI
python3 markdown_viewer.py sample_files/sample.md

# Terminal Markdown
./markdown-viewer-term sample_files/CHAT_PIPELINE_ARCHITECTURE.md

# Terminal Mermaid
./mermaid-viewer-term sample_files/sample_sequence.mmd
```

### Check Dependencies
```bash
pip list | grep -E 'markdown|rich|mermaid'
```

### Build Standalone Binary (GUI only)
```bash
pip install pyinstaller
pyinstaller markdown-viewer.spec
./dist/markdown-viewer sample_files/sample.md
```

---

## Resources & References

### Documentation
- [Mermaid Documentation](https://mermaid.js.org/)
- [Rich Library Documentation](https://rich.readthedocs.io/)
- [Python Markdown](https://python-markdown.github.io/)

### Services Used
- [mermaid.ink](https://mermaid.ink/) - Diagram rendering service
- [GitHub](https://github.com/edave907/markdown-viewer) - Repository hosting

### Related Projects Referenced
- mermaid-py - Python interface to mermaid.ink
- mermaid-ascii - Go-based ASCII rendering (not used)
- mermaid-cli - Node.js rendering tool (not used)

---

## Session Summary

### What Was Accomplished
1. ✅ Removed built-in pager from terminal markdown viewer
2. ✅ Fixed ANSI escape sequence rendering in xterm-256color
3. ✅ Implemented complete Mermaid diagram viewer
4. ✅ Added mermaid-py dependency
5. ✅ Created sample Mermaid files
6. ✅ Updated all documentation
7. ✅ Committed and pushed all changes

### Code Statistics
- **Total Python Files:** 4 (markdown_viewer.py, markdown_viewer_term.py, mermaid_viewer_gui.py, mermaid_viewer_term.py)
- **Total Lines of Python:** ~480 lines
- **Launcher Scripts:** 4 bash scripts + 1 installer script
- **Dependencies:** 4 Python packages (markdown, rich, mermaid-py, Pillow)
- **Sample Files:** 15+ markdown files, 2 Mermaid files
- **Desktop Integration:** 2 `.desktop` files (auto-generated)

### All Tests Passing
- ✅ GUI markdown rendering (including ASCII art)
- ✅ Terminal markdown rendering with colors
- ✅ Pager integration (less -R)
- ✅ Mermaid GUI viewer (downloads and displays diagrams)
- ✅ Mermaid terminal source highlighting
- ✅ Mermaid URL generation
- ✅ Desktop file installation

---

## Contact & Contribution

**Repository:** https://github.com/edave907/markdown-viewer
**License:** Provided as-is for educational and personal use
**AI Assistant:** Claude Code (Anthropic)

For issues or enhancements, see the repository's issue tracker.

---

## Next Steps (Suggested)

When resuming this project, consider:

1. ✅ ~~**Add Mermaid GUI viewer**~~ - COMPLETED!
2. ✅ ~~**Desktop file associations**~~ - COMPLETED!
3. **Implement dark mode** - Toggle for GUI versions
4. **Add clickable links** - Open URLs in default browser
5. **Local Mermaid rendering** - Optional mermaid-cli integration for offline use
6. **Image support** - Display embedded images in markdown
7. **Export functionality** - Save as PDF or HTML
8. **Find/search** - Text search within viewers

**Start with:** Testing all viewers to ensure everything still works after environment changes.

---

**Checkpoint Created:** 2025-11-22
**Checkpoint Updated:** 2025-11-22
**Ready to Resume:** Yes ✓
**Repository Status:** Clean, all changes committed and pushed

## Summary

This project is now **feature complete** with:
- ✅ 2 Markdown viewers (GUI + Terminal)
- ✅ 2 Mermaid diagram viewers (GUI + Terminal)
- ✅ Desktop integration for double-click file opening
- ✅ All viewers tested and working
- ✅ Complete documentation
- ✅ Sample files included

**Total viewers:** 4
**Installation method:** One command (`./install-desktop-files.sh`)
**Status:** Production ready
