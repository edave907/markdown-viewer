#!/usr/bin/env python3
"""
Mermaid Diagram Viewer GUI - A simple GUI application to view Mermaid diagrams
Usage: python mermaid_viewer_gui.py <filename.mmd>
"""

import sys
import tkinter as tk
from tkinter import messagebox
from mermaid import Mermaid
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO


class MermaidViewerGUI:
    def __init__(self, root, filename):
        self.root = root
        self.root.title(f"Mermaid Viewer - {filename}")
        self.root.geometry("900x700")

        # Create main frame with padding
        main_frame = tk.Frame(root, bg='#ffffff', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas with scrollbars
        self.canvas = tk.Canvas(
            main_frame,
            bg='#ffffff',
            highlightthickness=0
        )

        # Add scrollbars
        v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load and render mermaid diagram
        self.load_mermaid(filename)

    def load_mermaid(self, filename):
        try:
            # Read the mermaid file
            with open(filename, 'r', encoding='utf-8') as f:
                mermaid_content = f.read()

            # Show loading message
            self.canvas.create_text(
                450, 350,
                text="Loading diagram...",
                font=('DejaVu Sans', 14),
                fill='#666666',
                tags='loading'
            )
            self.root.update()

            # Create Mermaid object and get PNG URL
            mermaid = Mermaid(mermaid_content)
            png_url = mermaid.img_response.url

            # Download the image
            with urlopen(png_url) as response:
                image_data = response.read()

            # Load image
            image = Image.open(BytesIO(image_data))

            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(image)

            # Remove loading message
            self.canvas.delete('loading')

            # Display image on canvas
            self.canvas.create_image(10, 10, anchor=tk.NW, image=self.photo)

            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{filename}' not found.")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading diagram: {str(e)}")
            self.root.quit()


def main():
    if len(sys.argv) != 2:
        print("Usage: python mermaid_viewer_gui.py <filename.mmd>")
        sys.exit(1)

    filename = sys.argv[1]

    root = tk.Tk()
    app = MermaidViewerGUI(root, filename)
    root.mainloop()


if __name__ == '__main__':
    main()
