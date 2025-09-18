#!/bin/bash
set -e

echo "Installing Python deps..."
pip install -r requirements.txt

echo "Installing system libs via Homebrew..."
brew install pango cairo gdk-pixbuf libffi libxml2 libxslt || true

echo "Adding compatibility symlinks..."
ln -sf /opt/homebrew/lib/libpango-1.0.dylib /opt/homebrew/lib/libpango-1.0-0.dylib
ln -sf /opt/homebrew/lib/libpangocairo-1.0.dylib /opt/homebrew/lib/libpangocairo-1.0-0.dylib
ln -sf /opt/homebrew/lib/libpangoft2-1.0.dylib /opt/homebrew/lib/libpangoft2-1.0-0.dylib
ln -sf /opt/homebrew/lib/libharfbuzz.dylib /opt/homebrew/lib/libharfbuzz-0.dylib
ln -sf /opt/homebrew/lib/libfontconfig.dylib /opt/homebrew/lib/libfontconfig-1.dylib
ln -sf /opt/homebrew/lib/libgobject-2.0.dylib /opt/homebrew/lib/libgobject-2.0-0.dylib
ln -sf /opt/homebrew/lib/libglib-2.0.dylib /opt/homebrew/lib/libglib-2.0-0.dylib
ln -sf /opt/homebrew/lib/libcairo.dylib /opt/homebrew/lib/libcairo-2.dylib

echo "Setup complete!"
