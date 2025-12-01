# Statistical Analysis Report

**File:** `evaluation_results_20251130_172338.json`  
**Location:** `Data/L2.2/L4.7`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T17:23:38.123560

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 2.94
- **SD:** 0.69
- **95% CI:** [2.80, 3.08]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.60
- **SD:** 0.68
- **95% CI:** [3.46, 3.73]
- **N:** 99

### Statistical Test

- **t(197)** = -6.72
- **p** = 0.0000 ***
- **Cohen's d** = -0.95 (large)

**Interpretation:** GPT-4o-mini scored 18.2% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0100*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Combined Requests | 3.53(0.62) | 3.94(0.77) | -1.67 | 0.1041 ns | -0.58 |  |
| Edge Cases | 2.55(0.52) | 3.27(0.65) | -2.90 | 0.0088 ** | -1.24 | *** |
| Objection Processing | 2.96(0.62) | 3.79(0.59) | -4.76 | 0.0000 *** | -1.37 | *** |
| Portability Export | 2.93(0.77) | 3.75(0.44) | -4.92 | 0.0000 *** | -1.31 | *** |
| Portability Scope | 2.65(0.49) | 3.05(0.69) | -2.12 | 0.0404 * | -0.67 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Conflates Rights | 1.0% | 1.0% | Fisher | 1.0000 ns |  |
| Export Steps | 29.0% | 56.1% | χ²=13.82 | 0.0002 *** | * |
| Legal Reference | 58.0% | 86.7% | χ²=18.96 | 0.0000 *** | * |
| Objection Mentioned | 47.0% | 54.1% | χ²=0.73 | 0.3929 ns |  |
| Optout Steps | 32.0% | 42.9% | χ²=2.05 | 0.1522 ns |  |
| Portability Mentioned | 68.0% | 72.4% | χ²=0.28 | 0.5968 ns |  |

