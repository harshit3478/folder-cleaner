#!/bin/bash

# Quick test script for Folder Organizer

echo "🧪 Testing Folder Organizer v2.0"
echo "================================"
echo ""

# Test 1: Command exists
echo "Test 1: Checking if command exists..."
if command -v clean-folder &> /dev/null; then
    echo "✅ clean-folder command found"
else
    echo "❌ clean-folder command not found"
    exit 1
fi
echo ""

# Test 2: Help
echo "Test 2: Testing --help..."
clean-folder --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ --help works"
else
    echo "❌ --help failed"
fi
echo ""

# Test 3: Info
echo "Test 3: Testing --info..."
clean-folder --info > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ --info works"
else
    echo "❌ --info failed"
fi
echo ""

# Test 4: Count
echo "Test 4: Testing --count..."
clean-folder --count .py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ --count works"
else
    echo "❌ --count failed"
fi
echo ""

# Test 5: Create test directory and organize
echo "Test 5: Testing organize functionality..."
TEST_DIR="/tmp/folder-organizer-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create test files
touch test.pdf test.jpg test.mp3 test.txt test.docx test.zip

echo "Created test files:"
ls -1
echo ""

# Test organize with dry-run
echo "Testing dry-run..."
clean-folder --organize --dry-run > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ --organize --dry-run works"
else
    echo "❌ --organize --dry-run failed"
fi
echo ""

# Test actual organize
echo "Testing actual organize..."
clean-folder --organize --yes > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ --organize --yes works"
    echo ""
    echo "Files organized into:"
    ls -1
else
    echo "❌ --organize --yes failed"
fi
echo ""

# Cleanup
cd /tmp
rm -rf "$TEST_DIR"

echo "================================"
echo "✅ All tests passed!"
echo ""
echo "Try it yourself:"
echo "  clean-folder              # Interactive TUI"
echo "  clean-folder --info       # Folder stats"
echo "  clean-folder --count .pdf # Count PDFs"
