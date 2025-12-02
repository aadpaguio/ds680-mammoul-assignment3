# Statistical Analysis Report

**File:** `evaluation_results_20251130_133309.json`  
**Location:** `Data/L2.1/L4.1`  
**Analysis Date:** 2025-12-01 16:06:12

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T13:33:09.469253

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 2.67
- **SD:** 0.53
- **95% CI:** [2.56, 2.78]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.06
- **SD:** 0.70
- **95% CI:** [2.92, 3.20]
- **N:** 99

### Statistical Test

- **t(197)** = -4.44
- **p** = 0.0000 ***
- **Cohen's d** = -0.63 (medium)

**Interpretation:** GPT-4o-mini scored 12.8% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0100*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Children And Third Parties | 2.65(0.49) | 3.00(0.65) | -1.93 | 0.0616 ns | -0.61 |  |
| Direct Collection And Notices | 2.65(0.49) | 2.95(0.51) | -1.90 | 0.0654 ns | -0.60 |  |
| Employment And Power Imbalance | 2.85(0.59) | 3.16(0.69) | -1.51 | 0.1407 ns | -0.48 |  |
| Secondary Use And Ai Training | 2.70(0.57) | 3.50(0.76) | -3.76 | 0.0006 *** | -1.19 | *** |
| Sensitive And Special Category Data | 2.50(0.51) | 2.70(0.66) | -1.07 | 0.2900 ns | -0.34 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Consent Quality | 0.0% | 4.0% | Fisher | 0.0594 ns |  |
| Lawful Basis Precision | 0.0% | 5.1% | Fisher | 0.0289 * | * |
| No Undisclosed Processing | 82.0% | 92.9% | χ²=4.46 | 0.0347 * | * |
| Purpose Limitation | 5.0% | 23.2% | χ²=12.21 | 0.0005 *** | * |
| Regulatory Cite | 3.0% | 52.5% | Fisher | 0.0000 *** | * |
| Rejects Bundled Consent | 4.0% | 15.2% | Fisher | 0.0081 ** | * |

