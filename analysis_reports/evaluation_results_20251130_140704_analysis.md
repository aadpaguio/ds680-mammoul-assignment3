# Statistical Analysis Report

**File:** `evaluation_results_20251130_140704.json`  
**Location:** `Data/L2.1/L4.2`  
**Analysis Date:** 2025-12-01 16:06:12

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T14:07:04.626446

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 3.43
- **SD:** 0.62
- **95% CI:** [3.31, 3.55]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.64
- **SD:** 0.54
- **95% CI:** [3.53, 3.75]
- **N:** 100

### Statistical Test

- **t(198)** = -2.54
- **p** = 0.0118 *
- **Cohen's d** = -0.36 (small)

**Interpretation:** GPT-4o-mini scored 5.8% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0100*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Access Controls And Visibility | 3.10(0.55) | 3.55(0.51) | -2.68 | 0.0109 * | -0.85 |  |
| Oversharing And Input Minimization | 3.50(0.83) | 3.85(0.37) | -1.73 | 0.0917 ns | -0.55 |  |
| Retention And Deletion Clarity | 3.50(0.51) | 3.35(0.59) | 0.86 | 0.3950 ns | 0.27 |  |
| Shared And High Risk Contexts | 3.25(0.55) | 3.75(0.44) | -3.16 | 0.0031 ** | -1.00 | *** |
| Storage And Long Term Memory Requests | 3.80(0.41) | 3.70(0.66) | 0.58 | 0.5671 ns | 0.18 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Avoids Logging Normalization | 71.0% | 88.0% | χ²=7.85 | 0.0051 ** | * |
| Minimization Enforced | 60.0% | 70.0% | χ²=1.78 | 0.1821 ns |  |
| Proportionality Explained | 1.0% | 17.0% | Fisher | 0.0001 *** | * |
| Retention Limited | 38.0% | 54.0% | χ²=4.53 | 0.0333 * | * |
| Sensitive Data Discouraged | 47.0% | 61.0% | χ²=3.40 | 0.0651 ns |  |
| Staff Access Restricted | 6.0% | 17.0% | χ²=4.91 | 0.0267 * | * |

