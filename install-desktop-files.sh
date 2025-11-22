#!/usr/bin/env bash
# Install .desktop files for markdown and mermaid viewers
# This allows double-clicking .md and .mmd files to open them

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing desktop files for viewers..."

# Create applications directory if it doesn't exist
mkdir -p ~/.local/share/applications

# Create Markdown Viewer desktop file
cat > ~/.local/share/applications/markdown-viewer.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Markdown Viewer
Comment=View Markdown files with GitHub-like styling
Exec=$SCRIPT_DIR/markdown-viewer %f
Terminal=false
Categories=Office;Viewer;TextEditor;
MimeType=text/markdown;text/x-markdown;
Icon=text-x-generic
EOF

echo "✓ Created markdown-viewer.desktop"

# Create Mermaid Viewer desktop file
cat > ~/.local/share/applications/mermaid-viewer.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Mermaid Diagram Viewer
Comment=View Mermaid diagrams
Exec=$SCRIPT_DIR/mermaid-viewer %f
Terminal=false
Categories=Graphics;Viewer;
MimeType=text/plain;
Icon=image-x-generic
EOF

echo "✓ Created mermaid-viewer.desktop"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications
    echo "✓ Updated desktop database"
else
    echo "⚠ update-desktop-database not found, you may need to log out and back in"
fi

echo ""
echo "Installation complete!"
echo ""
echo "You can now:"
echo "  - Right-click any .md file → Open With → Markdown Viewer"
echo "  - Right-click any .mmd file → Open With → Mermaid Diagram Viewer"
echo "  - Set either as default for their file types"
echo ""
echo "To uninstall:"
echo "  rm ~/.local/share/applications/markdown-viewer.desktop"
echo "  rm ~/.local/share/applications/mermaid-viewer.desktop"
echo "  update-desktop-database ~/.local/share/applications"
