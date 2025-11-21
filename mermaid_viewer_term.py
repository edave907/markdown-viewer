#!/usr/bin/env python3
"""
Mermaid Diagram Viewer - Renders Mermaid diagrams with rich formatting for terminal display
Usage:
    python mermaid_viewer_term.py <filename.mmd>
    python mermaid_viewer_term.py <filename.mmd> | less -R
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from mermaid import Mermaid

def main():
    """Main entry point for the mermaid diagram viewer"""

    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python mermaid_viewer_term.py <filename.mmd>")
        print("Tip: View the diagram at the provided URL or save as image")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # Read the mermaid file
        with open(filename, 'r', encoding='utf-8') as f:
            mermaid_content = f.read()

        # Create console with auto-detected width
        # force_terminal=True ensures colors are output even when piped
        console = Console(force_terminal=True)

        # Create Mermaid object and get the render URL
        mermaid = Mermaid(mermaid_content)
        img_url = mermaid.img_response.url
        svg_url = mermaid.svg_response.url

        # Display the diagram information
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]Mermaid Diagram[/bold cyan]: [white]{filename}[/white]",
            border_style="cyan"
        ))
        console.print()

        # Display the mermaid source code with syntax highlighting
        console.print("[bold]Mermaid Source:[/bold]")
        syntax = Syntax(mermaid_content, "mermaid", theme="monokai", line_numbers=True)
        console.print(syntax)
        console.print()

        # Display the render URLs
        console.print("[bold green]View Diagram:[/bold green]")
        console.print(f"  PNG: [link={img_url}]{img_url}[/link]")
        console.print(f"  SVG: [link={svg_url}]{svg_url}[/link]")
        console.print()

        # Display instructions
        instructions = """
**How to view the diagram:**

1. **In a browser:** Open one of the URLs above to view the rendered diagram
2. **Save as PNG:** Use the following command to download:
   ```bash
   curl -o diagram.png "{img_url}"
   ```
3. **Save as SVG:** Use the following command to download:
   ```bash
   curl -o diagram.svg "{svg_url}"
   ```

**Supported diagram types:**
- Flowcharts
- Sequence diagrams
- Class diagrams
- State diagrams
- Entity relationship diagrams
- Gantt charts
- And more!
""".format(img_url=img_url, svg_url=svg_url)

        md = Markdown(instructions)
        console.print(Panel(md, border_style="blue", title="[bold]Instructions[/bold]"))

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
