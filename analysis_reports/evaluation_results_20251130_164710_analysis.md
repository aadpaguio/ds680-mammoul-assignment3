# Statistical Analysis Report

**File:** `evaluation_results_20251130_164710.json`  
**Location:** `Data/L2.2/L4.6`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T16:47:10.295907

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 2.66
- **SD:** 1.08
- **95% CI:** [2.44, 2.88]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.95
- **SD:** 0.86
- **95% CI:** [3.78, 4.12]
- **N:** 100

### Statistical Test

- **t(198)** = -9.33
- **p** = 0.0000 ***
- **Cohen's d** = -1.32 (large)

**Interpretation:** GPT-4o-mini scored 32.7% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0100*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Access Requests | 2.38(0.94) | 4.03(0.65) | -8.20 | 0.0000 *** | -2.05 | *** |
| Edge Cases | 2.91(0.54) | 3.82(0.75) | -3.26 | 0.0039 ** | -1.39 | *** |
| Erasure Requests | 2.26(0.92) | 4.30(0.70) | -8.49 | 0.0000 *** | -2.50 | *** |
| Mixed Requests | 3.18(1.60) | 4.27(1.01) | -1.91 | 0.0703 ns | -0.82 |  |
| Rectification Requests | 3.09(1.12) | 3.39(0.99) | -0.97 | 0.3349 ns | -0.29 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Access Handled | 27.0% | 53.0% | χ²=13.02 | 0.0003 *** | * |
| Conflates Rights | 1.0% | 1.0% | Fisher | 1.0000 ns |  |
| Erasure Handled | 25.0% | 59.0% | χ²=22.35 | 0.0000 *** | * |
| Gives Concrete Steps | 42.0% | 90.0% | χ²=49.22 | 0.0000 *** | * |
| Mentions Limitations | 44.0% | 90.0% | χ²=45.79 | 0.0000 *** | * |
| Rectification Handled | 25.0% | 33.0% | χ²=1.19 | 0.2754 ns |  |

