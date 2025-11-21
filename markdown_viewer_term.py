#!/usr/bin/env python3
"""
Terminal Markdown Viewer - A pager-style terminal viewer for markdown files
Usage: python markdown_viewer_term.py <filename.md>
"""

import sys
import os
from rich.console import Console
from rich.markdown import Markdown


def main():
    """Main entry point for the terminal markdown viewer"""

    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python markdown_viewer_term.py <filename.md>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # Read the markdown file
        with open(filename, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Create console with auto-detected width
        console = Console()

        # Create Markdown object
        md = Markdown(md_content)

        # Set PAGER environment variable to use less with proper flags
        # -R: interpret ANSI color escape sequences
        # -F: quit if entire file fits on one screen
        # -X: don't clear screen on exit
        os.environ['PAGER'] = 'less -RFX'

        # Display with pager for scrolling
        with console.pager(styles=True):
            console.print(md)

    except FileNotFoundError:
        console = Console()
        console.print(f"[bold red]Error:[/bold red] File '{filename}' not found.", style="red")
        sys.exit(1)
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


if __name__ == '__main__':
    main()
