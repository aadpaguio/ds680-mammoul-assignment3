# DS680 Assignment 3: L1 - Privacy & Data Stewardship

This repository contains evaluation scripts and analysis tools for comparing AI model responses to privacy-related prompts, specifically comparing Google Gemini and Qwen3 (via OpenRouter) models.

## Overview

This project evaluates how different AI models respond to privacy-related prompts across multiple control areas (L2) and specific requirements (L4). Each prompt is tested against the models, and responses are evaluated by a judge model (GPT-5-nano) that scores them on a 1-5 scale based on compliance with data protection laws (GDPR, CCPA/CPRA).

## Prerequisites

**This project requires [`uv`](https://github.com/astral-sh/uv)**, a fast Python package installer and resolver. All Python commands in this repository use `uv` for dependency management and execution.

**Install `uv`:**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew (macOS)
brew install uv

# Or via pip
pip install uv
```

See the [official uv documentation](https://docs.astral.sh/uv/) for installation instructions for other platforms.

## Directory Structure

```
.
├── Data/                          # Main data directory
│   ├── evaluate_batch_gemini.py   # Evaluation script for Gemini models
│   ├── evaluate_batch_qwen.py    # Evaluation script for Qwen3 models
│   ├── L2.1/                     # Control Area: Data Stewardship Controls
│   │   ├── L4.1/                 # L4 requirement folders
│   │   ├── L4.2/
│   │   ├── L4.3/
│   │   ├── L4.4/
│   │   └── L4.5/
│   ├── L2.2/                     # Control Area 2
│   │   ├── L4.6/
│   │   ├── L4.7/
│   │   └── L4.8/
│   ├── L2.3/                     # Control Area 3
│   │   ├── L4.9/
│   │   └── L4.10/
│   └── L2.4/                     # Control Area 4
│       ├── L4.11/
│       ├── L4.12/
│       ├── L4.13/
│       └── L4.14/
│
├── analysis_reports/              # Statistical analysis reports
│   └── L2.X_L4.Y_gemini_vs_qwen3_analysis.md
│
├── evaluation_results_zips/      # Zipped evaluation results
│   ├── L2.1_evaluation_results.zip
│   ├── L2.2_evaluation_results.zip
│   ├── L2.3_evaluation_results.zip
│   └── L2.4_evaluation_results.zip
│
├── run_evaluations_gemini.sh     # Batch evaluation script for Gemini
├── run_evaluations_qwen.sh       # Batch evaluation script for Qwen3
├── run_all_analyses_gemini.py    # Statistical analysis generator
└── pyproject.toml                # Python dependencies
```

### L4 Folder Structure

Each `L4.X` folder contains:
- `prompt_set.json` - JSON file containing all prompts for that L4 requirement, organized by categories
- `judge_prompt.txt` - Template prompt used by the judge model to evaluate responses
- `gemini_results/` - Directory containing Gemini evaluation results (JSON)
- `qwen_results/` - Directory containing Qwen3 evaluation results (JSON)
- `docs/` - Supporting documentation (privacy policies, terms of service, etc.)

## Important Files

### `prompt_set.json`

Located in each `L4.X` folder, this JSON file contains:
- Metadata about the L4 requirement (L4 indicator, L3 objective, L2 control area)
- Total number of prompts
- Category definitions
- Array of prompt objects, each containing:
  - `id`: Unique prompt identifier (e.g., "L4_DSC_01-001")
  - `category`: Prompt category (e.g., "direct_collection_and_notices")
  - `subcategory`: More specific classification
  - `prompt`: The actual prompt text to test
  - `expected_behavior`: Description of the ideal model response

**Example structure:**
```json
{
  "l4_indicator": "Lawful basis and consent mechanisms are defined and logged",
  "l4_id": "L4_DSC_01",
  "total_prompts": 100,
  "categories": {
    "direct_collection_and_notices": "User directly asks...",
    ...
  },
  "prompts": [
    {
      "id": "L4_DSC_01-001",
      "category": "direct_collection_and_notices",
      "subcategory": "storage_and_retention",
      "prompt": "Be honest: when I send you messages...",
      "expected_behavior": "Explain at a high level..."
    }
  ]
}
```

### `judge_prompt.txt`

Located in each `L4.X` folder, this file contains the evaluation template used by the judge model (GPT-5-nano). It includes:
- Instructions for scoring responses on a 1-5 scale
- Detailed scoring criteria (Exemplary, Good, Adequate, Poor, Failing)
- Flag definitions for specific behavioral indicators
- JSON output format specification

The judge evaluates responses based on:
- Lawful basis precision
- Consent quality
- Purpose limitation
- Avoidance of undisclosed processing
- Rejection of bundled consent
- Regulatory citations (GDPR, EDPB, CCPA/CPRA)

### `evaluate_batch_{model}.py`

Two evaluation scripts located in `Data/`:
- `evaluate_batch_gemini.py` - Evaluates prompts using Google Gemini models
- `evaluate_batch_qwen.py` - Evaluates prompts using Qwen3 via OpenRouter

**Features:**
- Async/concurrent processing for efficiency
- Configurable concurrency, delays, and batch sizes
- Cost tracking for API usage
- Saves results as JSON and CSV files
- Supports resuming from specific prompts

**Usage:**
```bash
# Evaluate all prompts for a specific L4 requirement
uv run python Data/evaluate_batch_gemini.py --l4 L2.1/L4.1

# Evaluate with custom settings
uv run python Data/evaluate_batch_gemini.py \
    --l4 L2.1/L4.1 \
    --concurrency 10 \
    --delay 0.5 \
    --batch-size 20 \
    --batch-pause 10

# Evaluate a subset of prompts
uv run python Data/evaluate_batch_gemini.py --l4 L2.1/L4.1 --limit 10
uv run python Data/evaluate_batch_gemini.py --l4 L2.1/L4.1 --start 50 --limit 25
```

**Configuration:**
- Test models: Gemini (gemini-2.5-flash-lite, gemini-2.0-flash-exp, gemini-1.5-pro) or Qwen3 (qwen/qwen3-235b-a22b)
- Judge model: GPT-5-nano-2025-08-07 (OpenAI)
- Each prompt is tested once per model

### `run_evaluations_gemini.sh` and `run_evaluations_qwen.sh`

Bash scripts that batch-run evaluations across multiple L4 requirements (L4.6 through L4.14).

**Features:**
- Processes multiple L4 folders sequentially
- Tracks completion and failures
- Configurable concurrency and batch settings
- Provides progress summaries

**Usage:**
```bash
# Make executable (first time only)
chmod +x run_evaluations_gemini.sh
chmod +x run_evaluations_qwen.sh

# Run evaluations
./run_evaluations_gemini.sh
./run_evaluations_qwen.sh
```

**Configuration (in script):**
- `CONCURRENCY`: Max concurrent API requests (Gemini: 10, Qwen: 3)
- `DELAY`: Delay between requests
- `BATCH_SIZE`: Pause after N requests
- `BATCH_PAUSE`: Seconds to pause between batches

### `run_all_analyses_gemini.py`

Python script that performs statistical analysis comparing Gemini vs Qwen3 results.

**Features:**
- Loads evaluation results from both models
- Performs statistical comparisons (t-tests, effect sizes)
- Generates per-category and per-flag analyses
- Creates markdown reports in `analysis_reports/`
- Handles missing data and mismatched prompt IDs

**Usage:**
```bash
uv run python run_all_analyses_gemini.py
```

**Output:**
- Creates one markdown report per L4 folder: `L2.X_L4.Y_gemini_vs_qwen3_analysis.md`
- Reports include:
  - Overall model comparison (means, SDs, confidence intervals, t-tests)
  - Per-category comparisons with Bonferroni correction
  - Behavioral flag comparisons
  - Statistical significance indicators

### Analysis Report Files (`*_gemini_vs_qwen3_analysis.md`)

Located in `analysis_reports/`, these markdown files contain comprehensive statistical comparisons for each L4 requirement.

**Contents:**
1. **Metadata**: Evaluation timestamps, number of prompts evaluated
2. **Overall Model Comparison**: 
   - Mean scores, standard deviations, 95% confidence intervals
   - t-test results with p-values and effect sizes (Cohen's d)
   - Interpretation of differences
3. **Per-Category Comparisons**: 
   - Statistical tests for each prompt category
   - Bonferroni-corrected significance levels
   - Effect sizes for each category
4. **Behavioral Flag Comparisons**: 
   - Flag presence rates for each model
   - Chi-square tests for flag differences
   - Interpretation of behavioral patterns

**Example report naming:**
- `L2.1_L4.1_gemini_vs_qwen3_analysis.md`
- `L2.2_L4.7_gemini_vs_qwen3_analysis.md`
- etc.

## Setup

1. **Install `uv`** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```
   This will create a virtual environment and install all required packages from `pyproject.toml`.

3. **Configure API keys:**
   Create a `.env` file in the project root with:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

4. **Run evaluations:**
   ```bash
   # Individual evaluation
   uv run python Data/evaluate_batch_gemini.py --l4 L2.1/L4.1
   
   # Batch evaluation
   ./run_evaluations_gemini.sh
   ```

5. **Generate analysis reports:**
   ```bash
   uv run python run_all_analyses_gemini.py
   ```

## Dependencies

This project uses `uv` for dependency management. All dependencies are defined in `pyproject.toml` and locked in `uv.lock`. Key packages:
- `google-generativeai` - Gemini API client
- `openai` - OpenAI API client (for judge model)
- `pandas` - Data manipulation
- `scipy` - Statistical analysis
- `python-dotenv` - Environment variable management

To install dependencies, run `uv sync` (see Setup section above).

## Results Storage

- **Evaluation results**: Stored in `{model}_results/` subdirectories within each L4 folder
- **Analysis reports**: Generated in `analysis_reports/`
- **Zipped results**: Archived in `evaluation_results_zips/` by L2 control area

## Notes

- Each prompt is evaluated once per model (no multiple trials per prompt)
- The judge model uses consistent criteria across all evaluations
- Results include cost tracking for API usage
- Analysis reports use appropriate statistical corrections for multiple comparisons
