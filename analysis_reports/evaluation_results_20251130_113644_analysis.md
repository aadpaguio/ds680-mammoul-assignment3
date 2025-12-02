# Statistical Analysis Report

**File:** `evaluation_results_20251130_113644.json`  
**Location:** `Data/L2.4/L4.14`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T11:36:44.769026

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 2.22
- **SD:** 0.80
- **95% CI:** [2.06, 2.38]
- **N:** 100

### Qwen3-235B

- **Mean:** 2.59
- **SD:** 0.93
- **95% CI:** [2.40, 2.77]
- **N:** 99

### Statistical Test

- **t(197)** = -2.99
- **p** = 0.0032 **
- **Cohen's d** = -0.42 (small)

**Interpretation:** GPT-4o-mini scored 14.1% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0050*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Audit Transparency | 1.56(0.73) | 3.00(0.87) | -3.83 | 0.0015 ** | -1.81 | *** |
| Biometric Retention | 2.62(0.52) | 3.00(0.53) | -1.43 | 0.1759 ns | -0.71 |  |
| Child Data Scenarios | 2.40(0.84) | 2.20(1.03) | 0.47 | 0.6410 ns | 0.21 |  |
| Compliance Questions | 2.82(0.40) | 3.09(0.30) | -1.79 | 0.0881 ns | -0.76 |  |
| Deletion Requests | 1.82(0.40) | 2.73(0.79) | -3.41 | 0.0028 ** | -1.45 | *** |
| Direct Retention Requests | 2.08(0.90) | 2.17(1.19) | -0.19 | 0.8487 ns | -0.08 |  |
| Financial Retention | 2.62(0.92) | 2.71(0.95) | -0.19 | 0.8561 ns | -0.10 |  |
| Health Data Retention | 2.20(0.92) | 2.10(1.10) | 0.22 | 0.8279 ns | 0.10 |  |
| Retention Policy Inquiries | 2.09(0.54) | 3.09(0.30) | -5.37 | 0.0000 *** | -2.29 | *** |
| Sensitivity Differentiation | 2.10(0.99) | 1.90(0.88) | 0.48 | 0.6389 ns | 0.21 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Audit Transparency | 1.0% | 10.1% | Fisher | 0.0050 ** | * |
| Deletion Mechanism Explained | 1.0% | 12.1% | Fisher | 0.0013 ** | * |
| Regulatory Reference | 16.0% | 42.4% | χ²=15.57 | 0.0001 *** | * |
| Retention Warning Present | 23.0% | 35.4% | χ²=3.10 | 0.0782 ns |  |
| Sensitivity Differentiation | 10.0% | 21.2% | χ²=3.94 | 0.0471 * | * |
| Specific Timeline Provided | 4.0% | 26.3% | Fisher | 0.0000 *** | * |
| User Control Offered | 6.0% | 38.4% | χ²=28.44 | 0.0000 *** | * |

