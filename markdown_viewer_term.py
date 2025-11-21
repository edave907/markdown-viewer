#!/usr/bin/env python3
"""
Terminal Markdown Viewer - Renders markdown files with rich formatting for terminal display
Usage:
    python markdown_viewer_term.py <filename.md>
    python markdown_viewer_term.py <filename.md> | less -R
    python markdown_viewer_term.py <filename.md> | more
"""

import sys
from rich.console import Console
from rich.markdown import Markdown


def main():
    """Main entry point for the terminal markdown viewer"""

    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python markdown_viewer_term.py <filename.md>")
        print("Tip: Pipe to a pager for scrolling: python markdown_viewer_term.py <file.md> | less -R")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # Read the markdown file
        with open(filename, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Create console with auto-detected width
        # force_terminal=True ensures colors are output even when piped
        console = Console(force_terminal=True)

        # Create Markdown object
        md = Markdown(md_content)

        # Print directly to stdout - users can pipe to their preferred pager
        console.print(md)

    except FileNotFoundError:
        console = Console(force_terminal=True, stderr=True)
        console.print(f"[bold red]Error:[/bold red] File '{filename}' not found.", style="red")
        sys.exit(1)
    except Exception as e:
        console = Console(force_terminal=True, stderr=True)
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


if __name__ == '__main__':
    main()
