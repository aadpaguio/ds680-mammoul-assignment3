# Statistical Analysis Report

**File:** `evaluation_results_20251130_175614.json`  
**Location:** `Data/L2.2/L4.8`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T17:56:14.042057

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 3.43
- **SD:** 0.56
- **95% CI:** [3.32, 3.54]
- **N:** 100

### Qwen3-235B

- **Mean:** 4.18
- **SD:** 0.66
- **95% CI:** [4.05, 4.31]
- **N:** 99

### Statistical Test

- **t(197)** = -8.70
- **p** = 0.0000 ***
- **Cohen's d** = -1.23 (large)

**Interpretation:** GPT-4o-mini scored 18.0% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0083*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Data Retention Deletion | 3.00(0.00) | 4.00(0.74) | -4.69 | 0.0001 *** | -1.91 | *** |
| Edge Cases | 3.21(0.58) | 3.86(0.66) | -2.73 | 0.0111 * | -1.03 |  |
| Minor Location Sharing | 3.50(0.58) | 4.40(0.58) | -5.54 | 0.0000 *** | -1.55 | *** |
| Minor Safety Emergency | 3.75(0.44) | 4.30(0.86) | -2.53 | 0.0156 * | -0.80 |  |
| Parental Setup | 3.44(0.62) | 4.17(0.51) | -3.82 | 0.0005 *** | -1.27 | *** |
| Third Party Apps | 3.40(0.52) | 4.10(0.32) | -3.66 | 0.0018 ** | -1.63 | *** |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Discourages Precise Location | 48.0% | 78.6% | χ²=18.58 | 0.0000 *** | * |
| Emergency Guidance | 20.0% | 38.8% | χ²=7.54 | 0.0060 ** | * |
| Encourages Parental Involvement | 45.0% | 83.7% | χ²=30.53 | 0.0000 *** | * |
| Mentions Opt In Or Consent | 16.0% | 31.6% | χ²=5.85 | 0.0156 * | * |
| Minor Acknowledged | 34.0% | 71.4% | χ²=26.33 | 0.0000 *** | * |
| Suggests Live Tracking | 7.0% | 7.1% | Fisher | 1.0000 ns |  |

