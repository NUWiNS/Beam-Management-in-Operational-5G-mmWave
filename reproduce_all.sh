#!/bin/bash

# Set relative scripts directory
SCRIPT_DIR="./scripts"

echo "=== Reproducing all Python scripts under $SCRIPT_DIR ==="

cd "$SCRIPT_DIR" || {
    echo "Error: Cannot cd to $SCRIPT_DIR"
    exit 1
}

# Loop over each Python file
for script in *.py; do
    echo "----------------------------------------"

    # Extract the figure label if present (e.g., "# Fig. 2(b)")
    fig_label=$(grep -m 1 '^# Fig\.' "$script" | sed 's/^# //')
    if [ -n "$fig_label" ]; then
        echo "📊 Generating: $fig_label"
    else
        echo "📄 Running: $script"
    fi

    echo "----------------------------------------"

    # Run the script and capture output to a temp log
    python3 "$script" 2>&1 | tee /tmp/reproduce_log.txt
    STATUS=${PIPESTATUS[0]}

    # Look for lines that mention saving files
    grep -iE 'saving to|saved at|\.pdf' /tmp/reproduce_log.txt | sed 's/^/💾 /'

    if [ $STATUS -eq 0 ]; then
        echo "✅ $script ran successfully"
    else
        echo "❌ $script failed with exit code $STATUS"
    fi
done

echo "=== Done running all scripts ==="
