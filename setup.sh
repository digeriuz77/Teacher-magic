#!/bin/bash
# Script to set up the proper directory structure for Teacher Magic

# Create necessary directories
mkdir -p tools utils

# Create empty __init__.py files in root directory and subdirectories
touch __init__.py
touch tools/__init__.py
touch utils/__init__.py

# List the files that should be present to ensure they exist
echo "Checking for required files..."

FILES=(
    "app.py"
    "styles.css"
    "requirements.txt"
    "README.md"
    "tools/__init__.py"
    "tools/content_tools.py"
    "tools/assessment_tools.py"
    "tools/support_tools.py"
    "tools/communication_tools.py"
    "utils/__init__.py"
    "utils/api.py"
    "utils/data.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file does not exist"
    fi
done

echo ""
echo "Directory structure setup complete. You can now run the app with:"
echo "streamlit run app.py"
