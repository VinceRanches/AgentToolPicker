#!/bin/bash

# Setup script for the Agent Exercise
echo "Setting up Agent Exercise with OpenAI GPT-4o-mini"
echo "================================================"

# Check if OPENAI_API_KEY is already set
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "OpenAI API Key is not set in your environment."
    echo "Please follow these steps:"
    echo ""
    echo "1. Get your OpenAI API key from: https://platform.openai.com/api-keys"
    echo "2. Set the environment variable by running:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "3. Or add it to your ~/.bashrc for permanent setup:"
    echo "   echo 'export OPENAI_API_KEY=\"your-api-key-here\"' >> ~/.bashrc"
    echo "   source ~/.bashrc"
    echo ""
    echo "4. Then run the tests with:"
    echo "   python run_tests.py"
    echo ""
else
    echo "✓ OPENAI_API_KEY is set"
    echo "Running tests..."
    python run_tests.py
fi
