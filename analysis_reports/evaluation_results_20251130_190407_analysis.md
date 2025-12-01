# Statistical Analysis Report

**File:** `evaluation_results_20251130_190407.json`  
**Location:** `Data/L2.3/L4.10`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T19:04:07.075540

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 4.55
- **SD:** 0.76
- **95% CI:** [4.40, 4.70]
- **N:** 100

### Qwen3-235B

- **Mean:** 4.97
- **SD:** 0.17
- **95% CI:** [4.94, 5.00]
- **N:** 100

### Statistical Test

- **t(198)** = -5.41
- **p** = 0.0000 ***
- **Cohen's d** = -0.77 (medium)

**Interpretation:** GPT-4o-mini scored 8.5% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0083*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Direct Sensitive Requests | 4.71(0.66) | 4.96(0.19) | -1.93 | 0.0588 ns | -0.52 |  |
| Edge Cases | 4.58(0.67) | 5.00(0.00) | -2.16 | 0.0420 * | -0.88 |  |
| Health Location Repro Data | 4.68(0.65) | 4.91(0.29) | -1.50 | 0.1408 ns | -0.45 |  |
| Internal Secrets | 4.92(0.29) | 5.00(0.00) | -1.00 | 0.3282 ns | -0.41 |  |
| Other Users Data | 3.93(0.92) | 5.00(0.00) | -4.37 | 0.0002 *** | -1.65 | *** |
| Prompt Injection | 4.25(0.97) | 5.00(0.00) | -2.69 | 0.0133 * | -1.10 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Direct Leakage | 0.0% | 0.0% | Fisher | 1.0000 ns |  |
| Explains Sensitivity | 45.0% | 85.0% | χ²=33.43 | 0.0000 *** | * |
| Partial Leakage | 0.0% | 0.0% | Fisher | 1.0000 ns |  |
| Refusal | 74.0% | 60.0% | χ²=3.82 | 0.0506 ns |  |
| Suggests Best Practices | 59.6% | 89.0% | χ²=21.05 | 0.0000 *** | * |
| Uses Fake Placeholder | 3.0% | 18.0% | Fisher | 0.0008 *** | * |

