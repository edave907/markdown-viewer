#!/usr/bin/env python3
"""
Markdown Viewer - A simple GUI application to view markdown files with GitHub-like styling
Usage: python markdown_viewer.py <filename.md>
"""

import sys
import tkinter as tk
from tkinter import scrolledtext, font
import markdown
from html.parser import HTMLParser
import re


class MarkdownRenderer(HTMLParser):
    """Parse HTML from markdown and render it in Tkinter with GitHub-like styling"""

    def __init__(self, text_widget):
        super().__init__()
        self.text = text_widget
        self.current_tags = []
        self.list_level = 0
        self.in_code_block = False
        self.code_buffer = []
        self.in_table = False
        self.suppress_next_newline = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.text.insert(tk.END, '\n')
            self.current_tags.append(tag)
        elif tag == 'strong' or tag == 'b':
            self.current_tags.append('bold')
        elif tag == 'em' or tag == 'i':
            self.current_tags.append('italic')
        elif tag == 'code':
            self.current_tags.append('code')
        elif tag == 'pre':
            self.in_code_block = True
            self.code_buffer = []
            self.text.insert(tk.END, '\n')
        elif tag == 'a':
            self.current_tags.append('link')
        elif tag == 'ul':
            self.list_level += 1
            if self.list_level == 1:
                self.text.insert(tk.END, '\n')
        elif tag == 'ol':
            self.list_level += 1
            if self.list_level == 1:
                self.text.insert(tk.END, '\n')
        elif tag == 'li':
            indent = '  ' * (self.list_level - 1)
            self.text.insert(tk.END, f'{indent}• ', 'bullet')
        elif tag == 'blockquote':
            self.current_tags.append('blockquote')
        elif tag == 'hr':
            self.text.insert(tk.END, '\n' + '─' * 80 + '\n', 'hr')
        elif tag == 'table':
            self.in_table = True
            self.text.insert(tk.END, '\n')
        elif tag == 'tr':
            pass
        elif tag in ['th', 'td']:
            self.current_tags.append('table_cell')

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if tag in self.current_tags:
                self.current_tags.remove(tag)
            self.text.insert(tk.END, '\n')
        elif tag in ['strong', 'b'] and 'bold' in self.current_tags:
            self.current_tags.remove('bold')
        elif tag in ['em', 'i'] and 'italic' in self.current_tags:
            self.current_tags.remove('italic')
        elif tag == 'code' and 'code' in self.current_tags:
            self.current_tags.remove('code')
        elif tag == 'pre':
            if self.code_buffer:
                code_text = ''.join(self.code_buffer)
                self.text.insert(tk.END, code_text, 'code_block')
                self.text.insert(tk.END, '\n')
            self.in_code_block = False
            self.code_buffer = []
        elif tag == 'a' and 'link' in self.current_tags:
            self.current_tags.remove('link')
        elif tag == 'ul':
            self.list_level -= 1
            if self.list_level == 0:
                self.text.insert(tk.END, '\n')
        elif tag == 'ol':
            self.list_level -= 1
            if self.list_level == 0:
                self.text.insert(tk.END, '\n')
        elif tag == 'li':
            self.text.insert(tk.END, '\n')
        elif tag == 'blockquote' and 'blockquote' in self.current_tags:
            self.current_tags.remove('blockquote')
            self.text.insert(tk.END, '\n')
        elif tag == 'p':
            self.text.insert(tk.END, '\n')
        elif tag == 'table':
            self.in_table = False
            self.text.insert(tk.END, '\n')
        elif tag == 'tr':
            self.text.insert(tk.END, '\n')
        elif tag in ['th', 'td']:
            if 'table_cell' in self.current_tags:
                self.current_tags.remove('table_cell')
            self.text.insert(tk.END, ' | ', 'table_cell')

    def handle_data(self, data):
        if self.in_code_block:
            self.code_buffer.append(data)
        else:
            # Skip purely whitespace data unless we're in specific contexts
            if data.strip() or self.current_tags:
                tags = tuple(self.current_tags)
                self.text.insert(tk.END, data, tags if tags else None)


class MarkdownViewer:
    def __init__(self, root, filename):
        self.root = root
        self.root.title(f"Markdown Viewer - {filename}")
        self.root.geometry("900x700")

        # Create main frame with padding
        main_frame = tk.Frame(root, bg='#ffffff', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create scrolled text widget
        self.text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.NONE,
            bg='#ffffff',
            fg='#24292e',
            padx=15,
            pady=15,
            borderwidth=0,
            highlightthickness=0
        )
        self.text.pack(fill=tk.BOTH, expand=True)

        # Configure fonts
        default_font = font.Font(family='DejaVu Sans', size=11)
        bold_font = font.Font(family='DejaVu Sans', size=11, weight='bold')
        italic_font = font.Font(family='DejaVu Sans', size=11, slant='italic')
        code_font = font.Font(family='DejaVu Sans Mono', size=10)

        h1_font = font.Font(family='DejaVu Sans', size=24, weight='bold')
        h2_font = font.Font(family='DejaVu Sans', size=20, weight='bold')
        h3_font = font.Font(family='DejaVu Sans', size=16, weight='bold')
        h4_font = font.Font(family='DejaVu Sans', size=14, weight='bold')
        h5_font = font.Font(family='DejaVu Sans', size=12, weight='bold')
        h6_font = font.Font(family='DejaVu Sans', size=11, weight='bold')

        # Configure tags for styling (GitHub-like colors)
        self.text.tag_configure('h1', font=h1_font, foreground='#24292e', spacing3=10)
        self.text.tag_configure('h2', font=h2_font, foreground='#24292e', spacing3=8)
        self.text.tag_configure('h3', font=h3_font, foreground='#24292e', spacing3=6)
        self.text.tag_configure('h4', font=h4_font, foreground='#24292e', spacing3=4)
        self.text.tag_configure('h5', font=h5_font, foreground='#24292e', spacing3=4)
        self.text.tag_configure('h6', font=h6_font, foreground='#6a737d', spacing3=4)

        self.text.tag_configure('bold', font=bold_font)
        self.text.tag_configure('italic', font=italic_font)
        self.text.tag_configure('code', font=code_font, background='#f6f8fa', foreground='#e83e8c')
        self.text.tag_configure('code_block', font=code_font, background='#f6f8fa', foreground='#24292e',
                                lmargin1=10, lmargin2=10, rmargin=10)
        self.text.tag_configure('link', foreground='#0366d6', underline=True)
        self.text.tag_configure('blockquote', foreground='#6a737d', lmargin1=20, lmargin2=20,
                                borderwidth=2, relief=tk.SOLID)
        self.text.tag_configure('bullet', foreground='#0366d6')
        self.text.tag_configure('hr', foreground='#e1e4e8')
        self.text.tag_configure('table_cell', font=code_font, foreground='#24292e')

        # Load and render markdown
        self.load_markdown(filename)

        # Make text widget read-only
        self.text.configure(state=tk.DISABLED)

    def load_markdown(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Convert markdown to HTML
            html = markdown.markdown(
                md_content,
                extensions=['extra', 'tables', 'fenced_code']
            )

            # Parse and render HTML
            self.text.configure(state=tk.NORMAL)
            renderer = MarkdownRenderer(self.text)
            renderer.feed(html)

        except FileNotFoundError:
            self.text.insert(tk.END, f"Error: File '{filename}' not found.", 'bold')
        except Exception as e:
            self.text.insert(tk.END, f"Error loading file: {str(e)}", 'bold')


def main():
    if len(sys.argv) != 2:
        print("Usage: python markdown_viewer.py <filename.md>")
        sys.exit(1)

    filename = sys.argv[1]

    root = tk.Tk()
    app = MarkdownViewer(root, filename)
    root.mainloop()


if __name__ == '__main__':
    main()
