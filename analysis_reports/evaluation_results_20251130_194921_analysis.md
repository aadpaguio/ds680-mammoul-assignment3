# Statistical Analysis Report

**File:** `evaluation_results_20251130_194921.json`  
**Location:** `Data/L2.4/L4.11`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T19:49:21.798167

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 3.00
- **SD:** 0.75
- **95% CI:** [2.85, 3.15]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.67
- **SD:** 0.82
- **95% CI:** [3.50, 3.83]
- **N:** 99

### Statistical Test

- **t(197)** = -5.98
- **p** = 0.0000 ***
- **Cohen's d** = -0.85 (large)

**Interpretation:** GPT-4o-mini scored 18.2% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0100*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Advisory Requests | 3.00(0.38) | 3.67(0.62) | -3.57 | 0.0013 ** | -1.30 | *** |
| Direct Sharing | 3.30(0.65) | 3.87(0.90) | -2.79 | 0.0070 ** | -0.72 | *** |
| Edge Cases | 2.56(0.71) | 3.60(0.65) | -5.41 | 0.0000 *** | -1.53 | *** |
| Implicit Processing | 2.40(0.63) | 2.87(0.83) | -1.73 | 0.0952 ns | -0.63 |  |
| Risk Assessment | 3.73(0.46) | 4.21(0.43) | -2.92 | 0.0069 ** | -1.09 | *** |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Alternatives | 43.0% | 70.7% | χ²=14.45 | 0.0001 *** | * |
| Differentiation | 23.0% | 54.5% | χ²=19.56 | 0.0000 *** | * |
| Irreversibility | 9.0% | 31.3% | χ²=14.06 | 0.0002 *** | * |
| Regulatory Cite | 20.0% | 47.5% | χ²=15.61 | 0.0001 *** | * |
| Transparency | 38.0% | 40.4% | χ²=0.04 | 0.8398 ns |  |
| Warning | 38.0% | 63.6% | χ²=12.08 | 0.0005 *** | * |

