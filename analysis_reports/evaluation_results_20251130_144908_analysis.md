# Statistical Analysis Report

**File:** `evaluation_results_20251130_144908.json`  
**Location:** `Data/L2.1/L4.3`  
**Analysis Date:** 2025-12-01 16:06:12

## Metadata

- **Prompts Evaluated:** 100
- **Evaluation Timestamp:** 2025-11-30T14:49:08.640936

## Overall Model Comparison

### GPT-4o-mini

- **Mean:** 3.43
- **SD:** 0.71
- **95% CI:** [3.29, 3.57]
- **N:** 100

### Qwen3-235B

- **Mean:** 3.85
- **SD:** 0.70
- **95% CI:** [3.71, 3.99]
- **N:** 100

### Statistical Test

- **t(198)** = -4.19
- **p** = 0.0000 ***
- **Cohen's d** = -0.59 (medium)

**Interpretation:** GPT-4o-mini scored 10.9% lower than Qwen3-235B.

## Per-Category Comparisons

*Bonferroni-corrected α = 0.0100*

| Category | GPT-4o M(SD) | Qwen3 M(SD) | t | p | d | Sig. |
|----------|--------------|-------------|---|----|----|------|
| Bypass And Misrepresentation | 3.05(1.00) | 3.95(1.00) | -2.85 | 0.0070 ** | -0.90 | *** |
| Id And Biometric Age Proof | 3.45(0.69) | 3.65(0.67) | -0.93 | 0.3572 ns | -0.29 |  |
| Parental And Youth Contexts | 3.75(0.44) | 4.10(0.45) | -2.48 | 0.0176 * | -0.79 |  |
| Self Declared Age And Content Gating | 3.80(0.62) | 4.10(0.55) | -1.62 | 0.1131 ns | -0.51 |  |
| Service Age Checks And Data Use | 3.10(0.31) | 3.45(0.51) | -2.63 | 0.0124 * | -0.83 |  |

## Behavioral Flag Comparisons

*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*

| Flag | GPT-4o % | Qwen3 % | Test | p | Sig. |
|------|----------|---------|------|----|------|
| Blocks Harmful Content | 20.0% | 40.0% | χ²=8.60 | 0.0034 ** | * |
| Minimization Preserved | 68.0% | 86.0% | χ²=8.16 | 0.0043 ** | * |
| No Age Profiling | 90.0% | 97.0% | Fisher | 0.0818 ns |  |
| Parental Involvement | 23.0% | 52.0% | χ²=16.73 | 0.0000 *** | * |
| Protective Default | 34.0% | 58.0% | χ²=10.65 | 0.0011 ** | * |
| Rejects Intrusive Verification | 16.0% | 21.0% | χ²=0.53 | 0.4664 ns |  |

