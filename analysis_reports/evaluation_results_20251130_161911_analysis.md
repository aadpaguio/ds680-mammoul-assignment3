# Statistical Analysis Report

**File:** `evaluation_results_20251130_161911.json`  
**Location:** `Data/L2.1/L4.5`  
**Analysis Date:** 2025-12-01 16:06:13

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T16:19:11.865630

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 3.25
- **SD:** 0.61
- **95% CI:** [3.13, 3.37]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.67
- **SD:** 0.73
- **95% CI:** [3.53, 3.81]
- **N:** 100

### Statistical Test

- **t(198)** = -4.43
- **p** = 0.0000 ***
- **Cohen's d** = -0.63 (medium)

**Interpretation:** GPT-4o-mini scored 11.4% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0100*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Classroom And Student Monitoring | 3.10(0.45) | 3.35(0.59) | -1.51 | 0.1381 ns | -0.48 |  |
| End User Monitoring Questions | 2.90(0.45) | 3.30(0.47) | -2.76 | 0.0089 ** | -0.87 | *** |
| Monitoring Design Metrics And Risk | 3.80(0.52) | 4.35(0.49) | -3.43 | 0.0015 ** | -1.09 | *** |
| Surveillance Edge Cases And Audits | 3.40(0.60) | 4.05(0.76) | -3.01 | 0.0047 ** | -0.95 | *** |
| Workplace And Remote Monitoring | 3.05(0.60) | 3.30(0.57) | -1.34 | 0.1869 ns | -0.42 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Anonymized Or Aggregated | 20.0% | 44.0% | χ²=12.16 | 0.0005 *** | * |
| Documentation Updates | 12.0% | 30.0% | χ²=8.71 | 0.0032 ** | * |
| Governance Linked | 16.0% | 52.0% | χ²=27.30 | 0.0000 *** | * |
| Incident Escalation | 11.0% | 29.0% | χ²=9.03 | 0.0027 ** | * |
| No User Surveillance | 67.0% | 79.0% | χ²=3.07 | 0.0798 ns |  |
| System Level Monitoring | 43.0% | 72.0% | χ²=16.04 | 0.0001 *** | * |

