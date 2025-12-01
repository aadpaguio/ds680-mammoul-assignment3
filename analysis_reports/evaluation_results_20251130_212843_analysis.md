# Statistical Analysis Report

**File:** `evaluation_results_20251130_212843.json`  
**Location:** `Data/L2.4/L4.13`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T21:28:43.048195

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 3.29
- **SD:** 0.52
- **95% CI:** [3.19, 3.39]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.77
- **SD:** 0.51
- **95% CI:** [3.67, 3.87]
- **N:** 99

### Statistical Test

- **t(197)** = -6.54
- **p** = 0.0000 ***
- **Cohen's d** = -0.93 (large)

**Interpretation:** GPT-4o-mini scored 12.7% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0050*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Ai Specific | 3.60(0.52) | 3.90(0.57) | -1.24 | 0.2323 ns | -0.55 |  |
| Compliance Questions | 3.00(0.00) | 3.56(0.53) | -3.16 | 0.0060 ** | -1.49 |  |
| Cross Border | 3.44(0.53) | 3.67(0.50) | -0.92 | 0.3724 ns | -0.43 |  |
| Direct Health Collection | 3.30(0.48) | 3.90(0.32) | -3.29 | 0.0041 ** | -1.47 | *** |
| Dpia Scoping | 3.30(0.48) | 4.00(0.00) | -4.58 | 0.0002 *** | -2.05 | *** |
| Edge Cases | 3.36(0.67) | 3.91(0.54) | -2.10 | 0.0491 * | -0.89 |  |
| Inference Risk | 3.09(0.30) | 3.36(0.50) | -1.54 | 0.1395 ns | -0.66 |  |
| Mitigation Guidance | 3.50(0.53) | 4.11(0.33) | -2.98 | 0.0084 ** | -1.39 |  |
| Research Scenarios | 2.80(0.42) | 3.60(0.52) | -3.79 | 0.0013 ** | -1.70 | *** |
| Third Party Integration | 3.50(0.53) | 3.70(0.67) | -0.74 | 0.4697 ns | -0.33 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Dpia Identified | 56.0% | 75.8% | χ²=7.78 | 0.0053 ** | * |
| Inference Recognized | 11.0% | 27.3% | χ²=7.51 | 0.0061 ** | * |
| Integration Flagged | 35.0% | 59.6% | χ²=11.11 | 0.0009 *** | * |
| Lifecycle Comprehensive | 26.0% | 60.6% | χ²=22.89 | 0.0000 *** | * |
| Necessity Discussed | 32.0% | 55.6% | χ²=10.28 | 0.0013 ** | * |
| Regulatory Cited | 80.0% | 98.0% | Fisher | 0.0001 *** | * |
| Specific Mitigations | 42.0% | 83.8% | χ²=35.51 | 0.0000 *** | * |

