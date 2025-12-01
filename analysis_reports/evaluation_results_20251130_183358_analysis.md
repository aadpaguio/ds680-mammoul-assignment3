# Statistical Analysis Report

**File:** `evaluation_results_20251130_183358.json`  
**Location:** `Data/L2.3/L4.9`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T18:33:58.039450

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 3.00
- **SD:** 0.83
- **95% CI:** [2.84, 3.16]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.35
- **SD:** 1.26
- **95% CI:** [3.10, 3.60]
- **N:** 100

### Statistical Test

- **t(198)** = -2.32
- **p** = 0.0212 *
- **Cohen's d** = -0.33 (small)

**Interpretation:** GPT-4o-mini scored 10.4% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0083*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Dataset Membership | 3.00(0.49) | 3.06(0.87) | -0.24 | 0.8148 ns | -0.08 |  |
| Membership Inference Others | 2.70(1.06) | 3.10(1.37) | -0.73 | 0.4746 ns | -0.33 |  |
| Membership Inference Self | 2.75(1.25) | 3.85(1.23) | -2.81 | 0.0078 ** | -0.89 | *** |
| Mixed Attacks | 3.00(0.69) | 2.92(1.62) | 0.22 | 0.8250 ns | 0.06 |  |
| Reidentification Quasi Identifiers | 3.19(0.54) | 3.81(0.91) | -2.36 | 0.0251 * | -0.83 |  |
| Research Edge Cases | 3.50(0.53) | 3.50(0.71) | 0.00 | 1.0000 ns | 0.00 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Attempts Identification | 2.0% | 7.0% | Fisher | 0.1697 ns |  |
| Educative Tone | 38.0% | 91.0% | χ²=59.05 | 0.0000 *** | * |
| Explains Reid Risk | 11.0% | 55.0% | χ²=41.81 | 0.0000 *** | * |
| Explicit Refusal | 53.0% | 35.0% | χ²=5.86 | 0.0154 * | * |
| Gives Probabilities | 3.0% | 32.0% | Fisher | 0.0000 *** | * |
| Mentions Training Data Limits | 46.0% | 45.0% | Fisher | 1.0000 ns |  |

