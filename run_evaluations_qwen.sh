#!/bin/bash
# Run evaluate_batch_qwen.py for L4.6 through L4.14
# Usage: ./run_evaluations_qwen.sh

set -e  # Exit on error

# Configuration
CONCURRENCY=3
DELAY=0.0
BATCH_SIZE=20
BATCH_PAUSE=10

# Define L4 folders to process (L4.6 to L4.14)
declare -a L4_FOLDERS=(
    "L2.2/L4.6"
    "L2.2/L4.7"
    "L2.2/L4.8"
    "L2.3/L4.9"
    "L2.3/L4.10"
    "L2.4/L4.11"
    "L2.4/L4.12"
    "L2.4/L4.13"
    "L2.4/L4.14"
)

echo "=========================================="
echo "Running Qwen evaluations for ${#L4_FOLDERS[@]} L4 folders"
echo "Concurrency: $CONCURRENCY"
echo "Delay: ${DELAY}s"
echo "Batch size: $BATCH_SIZE, Batch pause: ${BATCH_PAUSE}s"
echo "=========================================="
echo ""

# Track progress
COMPLETED=0
FAILED=0

for L4_FOLDER in "${L4_FOLDERS[@]}"; do
    echo ""
    echo "=========================================="
    echo "Processing: $L4_FOLDER"
    echo "=========================================="
    
    if uv run python Data/evaluate_batch_qwen.py \
        --l4 "$L4_FOLDER" \
        --concurrency "$CONCURRENCY" \
        --delay "$DELAY" \
        --batch-size "$BATCH_SIZE" \
        --batch-pause "$BATCH_PAUSE"; then
        echo "✓ Completed: $L4_FOLDER"
        ((COMPLETED++))
    else
        echo "✗ Failed: $L4_FOLDER"
        ((FAILED++))
    fi
    
    echo ""
done

echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo "Completed: $COMPLETED"
echo "Failed: $FAILED"
echo "Total: ${#L4_FOLDERS[@]}"
echo "=========================================="

