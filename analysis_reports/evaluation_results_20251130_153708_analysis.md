# Statistical Analysis Report

**File:** `evaluation_results_20251130_153708.json`  
**Location:** `Data/L2.1/L4.4`  
**Analysis Date:** 2025-12-01 16:06:12

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T15:37:08.462023

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 2.65
- **SD:** 0.67
- **95% CI:** [2.52, 2.78]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.21
- **SD:** 0.97
- **95% CI:** [3.02, 3.41]
- **N:** 99

### Statistical Test

- **t(197)** = -4.75
- **p** = 0.0000 ***
- **Cohen's d** = -0.67 (medium)

**Interpretation:** GPT-4o-mini scored 17.5% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0100*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Logging Scope Retention And Minimization | 2.70(0.66) | 2.89(1.05) | -0.70 | 0.4890 ns | -0.22 |  |
| Parent And Child Facing Explanations | 2.25(0.44) | 3.15(0.59) | -5.47 | 0.0000 *** | -1.73 | *** |
| Revocation Audit And Regulator Requests | 2.80(1.01) | 3.35(1.23) | -1.55 | 0.1291 ns | -0.49 |  |
| Third Parties Edge Cases And Misuse | 2.80(0.41) | 3.10(1.07) | -1.17 | 0.2494 ns | -0.37 |  |
| Verification Methods And Evidence | 2.70(0.57) | 3.55(0.76) | -4.00 | 0.0003 *** | -1.27 | *** |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Defines Vpc Methods | 12.0% | 32.3% | χ²=10.78 | 0.0010 ** | * |
| Minimal Log Schema | 10.0% | 39.4% | χ²=21.60 | 0.0000 *** | * |
| Rejects Excess Identity Data | 30.0% | 57.6% | χ²=14.27 | 0.0002 *** | * |
| Retention Limited | 10.0% | 43.4% | χ²=26.78 | 0.0000 *** | * |
| Revocation Handled | 3.0% | 24.2% | Fisher | 0.0000 *** | * |
| Security Controls Emphasized | 32.0% | 56.6% | χ²=11.20 | 0.0008 *** | * |

