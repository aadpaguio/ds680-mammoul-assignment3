# Statistical Analysis Report

**File:** `evaluation_results_20251130_202710.json`  
**Location:** `Data/L2.4/L4.12`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T20:27:10.190680

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 3.19
- **SD:** 0.90
- **95% CI:** [3.01, 3.37]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.73
- **SD:** 1.00
- **95% CI:** [3.53, 3.93]
- **N:** 100

### Statistical Test

- **t(198)** = -4.01
- **p** = 0.0001 ***
- **Cohen's d** = -0.57 (medium)

**Interpretation:** GPT-4o-mini scored 14.5% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0083*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Age Verification | 2.60(0.97) | 4.20(1.03) | -3.58 | 0.0022 ** | -1.60 | *** |
| Direct Age Disclosure | 3.00(0.65) | 3.30(0.92) | -1.19 | 0.2419 ns | -0.38 |  |
| Educational Guidance | 3.88(0.34) | 4.19(0.66) | -1.69 | 0.1010 ns | -0.60 |  |
| Implicit Age Indicators | 2.50(0.95) | 2.65(0.88) | -0.52 | 0.6057 ns | -0.16 |  |
| Parental Scenarios | 3.30(0.80) | 4.30(0.66) | -4.32 | 0.0001 *** | -1.36 | *** |
| Risk Scenarios | 3.93(0.47) | 4.21(0.43) | -1.68 | 0.1056 ns | -0.63 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Age Band Awareness | 14.0% | 44.0% | χ²=20.42 | 0.0000 *** | * |
| Age Verification | 13.0% | 31.0% | χ²=8.42 | 0.0037 ** | * |
| Differentiation | 19.0% | 50.0% | χ²=19.91 | 0.0000 *** | * |
| Parental Consent | 42.4% | 66.0% | χ²=10.21 | 0.0014 ** | * |
| Regulatory Cite | 36.0% | 53.0% | χ²=5.18 | 0.0228 * | * |
| Transparency | 55.0% | 69.0% | χ²=3.59 | 0.0582 ns |  |

