#!/usr/bin/env python3
"""
Run statistical analysis comparing Gemini vs Qwen (OpenRouter) results.
Finds Gemini results in gemini_results/ subfolders and Qwen results in qwen_results/ subfolders.
Generates markdown reports organized by L4 folder.
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def load_results(file_path):
    """Load the single evaluation result file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        results = data.get('results', [])
        return results, data.get('metadata', {})
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return [], {}
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {file_path}: {e}")
        return [], {}
    except Exception as e:
        print(f"ERROR: {e}")
        return [], {}


def extract_gemini_scores_and_flags(results):
    """Extract scores and flags from Gemini results (uses 'trials' structure)."""
    data = {
        'scores': [],
        'categories': [],
        'subcategories': [],
        'prompt_ids': [],
        'flags': defaultdict(list)
    }
    
    if not results:
        return data
    
    for result in results:
        prompt_id = result.get('prompt_id', 'unknown')
        category = result.get('category', 'uncategorized')
        subcategory = result.get('subcategory', 'uncategorized')
        
        # Extract from trials (Gemini structure)
        trials = result.get('trials', [])
        for trial in trials:
            eval_data = trial.get('evaluation', {})
            
            score = eval_data.get('score')
            if score is not None:
                data['scores'].append(score)
                data['categories'].append(category)
                data['subcategories'].append(subcategory)
                data['prompt_ids'].append(prompt_id)
                
                # Extract flags
                flags = eval_data.get('flags', {})
                for flag_name, flag_value in flags.items():
                    data['flags'][flag_name].append(flag_value)
    
    return data


def extract_openrouter_scores_and_flags(results):
    """Extract scores and flags from Qwen/OpenRouter results (uses 'openrouter_trials' structure)."""
    data = {
        'scores': [],
        'categories': [],
        'subcategories': [],
        'prompt_ids': [],
        'flags': defaultdict(list)
    }
    
    if not results:
        return data
    
    for result in results:
        prompt_id = result.get('prompt_id', 'unknown')
        category = result.get('category', 'uncategorized')
        subcategory = result.get('subcategory', 'uncategorized')
        
        # Extract from openrouter_trials (OpenRouter structure)
        openrouter_trials = result.get('openrouter_trials', [])
        for trial in openrouter_trials:
            eval_data = trial.get('evaluation', {})
            
            score = eval_data.get('score')
            if score is not None:
                data['scores'].append(score)
                data['categories'].append(category)
                data['subcategories'].append(subcategory)
                data['prompt_ids'].append(prompt_id)
                
                # Extract flags
                flags = eval_data.get('flags', {})
                for flag_name, flag_value in flags.items():
                    data['flags'][flag_name].append(flag_value)
    
    return data


def combine_data_by_prompt_id(gemini_data, qwen_data):
    """Combine Gemini and Qwen (OpenRouter) data, matching by prompt_id."""
    combined = {
        'gemini': {
            'scores': [],
            'categories': [],
            'subcategories': [],
            'prompt_ids': [],
            'flags': defaultdict(list)
        },
        'qwen3': {
            'scores': [],
            'categories': [],
            'subcategories': [],
            'prompt_ids': [],
            'flags': defaultdict(list)
        }
    }
    
    # Create prompt_id to index mapping for both datasets
    gemini_prompt_map = {pid: i for i, pid in enumerate(gemini_data['prompt_ids'])}
    qwen_prompt_map = {pid: i for i, pid in enumerate(qwen_data['prompt_ids'])}
    
    # Find common prompt_ids
    common_prompts = set(gemini_prompt_map.keys()) & set(qwen_prompt_map.keys())
    
    if not common_prompts:
        print("WARNING: No common prompt_ids found between Gemini and Qwen results")
        return combined
    
    print(f"Found {len(common_prompts)} common prompts out of {len(gemini_prompt_map)} Gemini and {len(qwen_prompt_map)} Qwen prompts")
    
    # Add data for common prompts only
    for prompt_id in sorted(common_prompts):
        gemini_idx = gemini_prompt_map[prompt_id]
        qwen_idx = qwen_prompt_map[prompt_id]
        
        # Add Gemini data
        combined['gemini']['scores'].append(gemini_data['scores'][gemini_idx])
        combined['gemini']['categories'].append(gemini_data['categories'][gemini_idx])
        combined['gemini']['subcategories'].append(gemini_data['subcategories'][gemini_idx])
        combined['gemini']['prompt_ids'].append(prompt_id)
        
        # Add Gemini flags
        for flag_name in gemini_data['flags']:
            if gemini_idx < len(gemini_data['flags'][flag_name]):
                combined['gemini']['flags'][flag_name].append(gemini_data['flags'][flag_name][gemini_idx])
        
        # Add Qwen data
        combined['qwen3']['scores'].append(qwen_data['scores'][qwen_idx])
        combined['qwen3']['categories'].append(qwen_data['categories'][qwen_idx])
        combined['qwen3']['subcategories'].append(qwen_data['subcategories'][qwen_idx])
        combined['qwen3']['prompt_ids'].append(prompt_id)
        
        # Add Qwen flags
        for flag_name in qwen_data['flags']:
            if qwen_idx < len(qwen_data['flags'][flag_name]):
                combined['qwen3']['flags'][flag_name].append(qwen_data['flags'][flag_name][qwen_idx])
    
    return combined


def overall_comparison(data):
    """Perform overall statistical comparison."""
    gemini_scores = np.array(data['gemini']['scores'])
    qwen3_scores = np.array(data['qwen3']['scores'])
    
    if len(gemini_scores) == 0 or len(qwen3_scores) == 0:
        return None
    
    # Descriptive statistics
    gemini_mean = np.mean(gemini_scores)
    gemini_std = np.std(gemini_scores, ddof=1)
    qwen3_mean = np.mean(qwen3_scores)
    qwen3_std = np.std(qwen3_scores, ddof=1)
    
    # Confidence intervals
    ci_gemini = stats.t.interval(
        0.95, 
        len(gemini_scores)-1, 
        loc=gemini_mean, 
        scale=stats.sem(gemini_scores)
    )
    ci_qwen3 = stats.t.interval(
        0.95, 
        len(qwen3_scores)-1,
        loc=qwen3_mean,
        scale=stats.sem(qwen3_scores)
    )
    
    # t-test
    t_stat, p_value = stats.ttest_ind(gemini_scores, qwen3_scores)
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt((np.var(gemini_scores, ddof=1) + np.var(qwen3_scores, ddof=1)) / 2)
    cohens_d = (gemini_mean - qwen3_mean) / pooled_std if pooled_std > 0 else 0
    
    # Degrees of freedom
    df = len(gemini_scores) + len(qwen3_scores) - 2
    
    results = {
        'gemini': {
            'mean': gemini_mean,
            'std': gemini_std,
            'ci': ci_gemini,
            'n': len(gemini_scores)
        },
        'qwen3': {
            'mean': qwen3_mean,
            'std': qwen3_std,
            'ci': ci_qwen3,
            'n': len(qwen3_scores)
        },
        't_stat': t_stat,
        'p_value': p_value,
        'df': df,
        'cohens_d': cohens_d
    }
    
    return results


def category_comparison(data):
    """Perform per-category statistical comparisons with Bonferroni correction."""
    # Get all unique categories
    all_categories = set(data['gemini']['categories']) | set(data['qwen3']['categories'])
    
    if not all_categories or ('uncategorized' in all_categories and len(all_categories) == 1):
        return {}
    
    # Remove empty string if present
    all_categories = {cat for cat in all_categories if cat}
    
    if not all_categories:
        return {}
    
    # Bonferroni correction
    bonferroni_alpha = 0.05 / len(all_categories)
    
    results = {}
    
    for category in sorted(all_categories):
        # Get scores for this category
        gemini_cat_scores = [
            score for score, cat in zip(data['gemini']['scores'], data['gemini']['categories'])
            if cat == category
        ]
        qwen3_cat_scores = [
            score for score, cat in zip(data['qwen3']['scores'], data['qwen3']['categories'])
            if cat == category
        ]
        
        if not gemini_cat_scores or not qwen3_cat_scores:
            continue
        
        # Descriptive stats
        gemini_mean = np.mean(gemini_cat_scores)
        gemini_std = np.std(gemini_cat_scores, ddof=1)
        qwen3_mean = np.mean(qwen3_cat_scores)
        qwen3_std = np.std(qwen3_cat_scores, ddof=1)
        
        # t-test
        t_stat, p_value = stats.ttest_ind(gemini_cat_scores, qwen3_cat_scores)
        
        # Effect size
        pooled_std = np.sqrt(
            (np.var(gemini_cat_scores, ddof=1) + np.var(qwen3_cat_scores, ddof=1)) / 2
        )
        cohens_d = (gemini_mean - qwen3_mean) / pooled_std if pooled_std > 0 else 0
        
        # Significance after Bonferroni correction
        significant = p_value < bonferroni_alpha
        
        results[category] = {
            'gemini_mean': gemini_mean,
            'gemini_std': gemini_std,
            'gemini_n': len(gemini_cat_scores),
            'qwen3_mean': qwen3_mean,
            'qwen3_std': qwen3_std,
            'qwen3_n': len(qwen3_cat_scores),
            't_stat': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'significant': significant,
            'bonferroni_alpha': bonferroni_alpha
        }
    
    return results


def flag_comparison(data):
    """Compare binary flag frequencies using chi-square tests."""
    # Get flags from either model (they should have the same flag names)
    flag_names = list(data['gemini']['flags'].keys()) or list(data['qwen3']['flags'].keys())
    
    if not flag_names:
        return {}
    
    results = {}
    
    for flag in flag_names:
        gemini_flags = data['gemini']['flags'].get(flag, [])
        qwen3_flags = data['qwen3']['flags'].get(flag, [])
        
        if not gemini_flags or not qwen3_flags:
            continue
        
        # Ensure same length (should be if matched by prompt_id)
        min_len = min(len(gemini_flags), len(qwen3_flags))
        gemini_flags = gemini_flags[:min_len]
        qwen3_flags = qwen3_flags[:min_len]
        
        # Count occurrences
        gemini_count = sum(gemini_flags)
        gemini_total = len(gemini_flags)
        qwen3_count = sum(qwen3_flags)
        qwen3_total = len(qwen3_flags)
        
        # Percentages
        gemini_pct = (gemini_count / gemini_total * 100) if gemini_total > 0 else 0
        qwen3_pct = (qwen3_count / qwen3_total * 100) if qwen3_total > 0 else 0
        
        # Contingency table
        contingency_table = np.array([
            [gemini_count, qwen3_count],
            [gemini_total - gemini_count, qwen3_total - qwen3_count]
        ])
        
        # Chi-square test (or Fisher's exact for small counts)
        if gemini_count < 5 or qwen3_count < 5 or (gemini_total - gemini_count) < 5 or (qwen3_total - qwen3_count) < 5:
            # Use Fisher's exact test for small counts
            odds_ratio, p_value = stats.fisher_exact(contingency_table)
            chi2_stat = None
            test_used = 'fisher'
        else:
            chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
            odds_ratio = None
            test_used = 'chi2'
        
        results[flag] = {
            'gemini_count': gemini_count,
            'gemini_total': gemini_total,
            'gemini_pct': gemini_pct,
            'qwen3_count': qwen3_count,
            'qwen3_total': qwen3_total,
            'qwen3_pct': qwen3_pct,
            'chi2_stat': chi2_stat,
            'p_value': p_value,
            'odds_ratio': odds_ratio,
            'test_used': test_used,
            'significant': p_value < 0.05
        }
    
    return results


def format_p_value(p_value):
    """Format p-value with significance markers."""
    if p_value < 0.001:
        return f"{p_value:.4f} ***"
    elif p_value < 0.01:
        return f"{p_value:.4f} **"
    elif p_value < 0.05:
        return f"{p_value:.4f} *"
    else:
        return f"{p_value:.4f} ns"


def interpret_effect_size(d):
    """Interpret Cohen's d effect size."""
    d_abs = abs(d)
    if d_abs < 0.2:
        return "negligible"
    elif d_abs < 0.5:
        return "small"
    elif d_abs < 0.8:
        return "medium"
    else:
        return "large"


def generate_markdown_report(l4_folder, gemini_metadata, qwen_metadata, overall, category, flags):
    """Generate a markdown report from analysis results."""
    
    # Get model names from metadata
    gemini_model = gemini_metadata.get('test_model', 'Gemini') if gemini_metadata else 'Gemini'
    qwen3_model = qwen_metadata.get('openrouter_test_model', 'Qwen3-235B') if qwen_metadata else 'Qwen3-235B'
    
    report = f"""# Statistical Analysis Report: Gemini vs OpenRouter (Qwen3)

**L4 Folder:** `{l4_folder}`  
**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    # Metadata
    report += "## Metadata\n\n"
    if gemini_metadata:
        prompts_evaluated = gemini_metadata.get('prompts_evaluated', 'N/A')
        report += f"- **Gemini Prompts Evaluated:** {prompts_evaluated}\n"
        if 'timestamp' in gemini_metadata:
            report += f"- **Gemini Evaluation Timestamp:** {gemini_metadata.get('timestamp', 'N/A')}\n"
    if qwen_metadata:
        prompts_evaluated = qwen_metadata.get('prompts_evaluated', 'N/A')
        report += f"- **Qwen Prompts Evaluated:** {prompts_evaluated}\n"
        if 'timestamp' in qwen_metadata:
            report += f"- **Qwen Evaluation Timestamp:** {qwen_metadata.get('timestamp', 'N/A')}\n"
    report += "\n"
    
    # Overall comparison
    if overall:
        report += "## Overall Model Comparison\n\n"
        gemini = overall['gemini']
        qwen3 = overall['qwen3']
        
        report += f"### {gemini_model}\n\n"
        report += f"- **Mean:** {gemini['mean']:.2f}\n"
        report += f"- **SD:** {gemini['std']:.2f}\n"
        report += f"- **95% CI:** [{gemini['ci'][0]:.2f}, {gemini['ci'][1]:.2f}]\n"
        report += f"- **N:** {gemini['n']}\n\n"
        
        report += f"### {qwen3_model}\n\n"
        report += f"- **Mean:** {qwen3['mean']:.2f}\n"
        report += f"- **SD:** {qwen3['std']:.2f}\n"
        report += f"- **95% CI:** [{qwen3['ci'][0]:.2f}, {qwen3['ci'][1]:.2f}]\n"
        report += f"- **N:** {qwen3['n']}\n\n"
        
        report += f"### Statistical Test\n\n"
        report += f"- **t({overall['df']})** = {overall['t_stat']:.2f}\n"
        report += f"- **p** = {format_p_value(overall['p_value'])}\n"
        report += f"- **Cohen's d** = {overall['cohens_d']:.2f} ({interpret_effect_size(overall['cohens_d'])})\n\n"
        
        # Interpretation
        if qwen3['mean'] != 0:
            diff_pct = ((gemini['mean'] - qwen3['mean']) / qwen3['mean'] * 100)
            if gemini['mean'] < qwen3['mean']:
                report += f"**Interpretation:** {gemini_model} scored {abs(diff_pct):.1f}% lower than {qwen3_model}.\n\n"
            else:
                report += f"**Interpretation:** {gemini_model} scored {abs(diff_pct):.1f}% higher than {qwen3_model}.\n\n"
    
    # Category comparison
    if category:
        report += "## Per-Category Comparisons\n\n"
        bonferroni_val = list(category.values())[0]['bonferroni_alpha']
        report += f"*Bonferroni-corrected α = {bonferroni_val:.4f}*\n\n"
        
        report += f"| Category | {gemini_model} M(SD) | {qwen3_model} M(SD) | t | p | d | Sig. |\n"
        report += "|----------|----------------------|---------------------|---|----|----|------|\n"
        
        for cat, data in sorted(category.items()):
            cat_clean = cat.replace('_', ' ').title()
            sig_marker = "***" if data['significant'] else ""
            report += f"| {cat_clean} | {data['gemini_mean']:.2f}({data['gemini_std']:.2f}) | "
            report += f"{data['qwen3_mean']:.2f}({data['qwen3_std']:.2f}) | "
            report += f"{data['t_stat']:.2f} | {format_p_value(data['p_value'])} | "
            report += f"{data['cohens_d']:.2f} | {sig_marker} |\n"
        
        report += "\n"
    
    # Flag comparison
    if flags:
        report += "## Behavioral Flag Comparisons\n\n"
        report += "*Note: * p < .05. Fisher's exact test used when expected cell counts < 5.*\n\n"
        
        report += f"| Flag | {gemini_model} % | {qwen3_model} % | Test | p | Sig. |\n"
        report += "|------|------------------|-----------------|------|----|------|\n"
        
        for flag, data in sorted(flags.items()):
            flag_clean = flag.replace('_', ' ').title()
            stat_str = f"χ²={data['chi2_stat']:.2f}" if data['chi2_stat'] else "Fisher"
            sig_marker = "*" if data['significant'] else ""
            report += f"| {flag_clean} | {data['gemini_pct']:.1f}% | "
            report += f"{data['qwen3_pct']:.1f}% | {stat_str} | "
            report += f"{format_p_value(data['p_value'])} | {sig_marker} |\n"
        
        report += "\n"
    
    return report


def find_l4_folders(data_dir):
    """Find all L4 folders that have both Gemini and Qwen (OpenRouter) results."""
    l4_folders = {}
    
    # Find all L4 folders
    for l2_dir in data_dir.glob("L2.*"):
        for l4_dir in l2_dir.glob("L4.*"):
            l4_path = f"{l2_dir.name}/{l4_dir.name}"
            
            # Check for Gemini results
            gemini_results_dir = l4_dir / "gemini_results"
            gemini_files = list(gemini_results_dir.glob("evaluation_results_*.json")) if gemini_results_dir.exists() else []
            
            # Check for Qwen results (in qwen_results subfolder)
            qwen_results_dir = l4_dir / "qwen_results"
            qwen_files = list(qwen_results_dir.glob("evaluation_results_*.json")) if qwen_results_dir.exists() else []
            
            if gemini_files and qwen_files:
                # Use most recent files
                gemini_file = max(gemini_files, key=lambda p: p.stat().st_mtime)
                qwen_file = max(qwen_files, key=lambda p: p.stat().st_mtime)
                l4_folders[l4_path] = {
                    'gemini_file': gemini_file,
                    'openrouter_file': qwen_file,  # Keep name for compatibility
                    'l4_dir': l4_dir
                }
    
    return l4_folders


def analyze_l4_folder(l4_folder, file_info, output_dir):
    """Run analysis on a single L4 folder, combining Gemini and Qwen (OpenRouter) results."""
    print(f"\n{'='*80}")
    print(f"Analyzing L4 folder: {l4_folder}")
    print(f"  Gemini file: {file_info['gemini_file'].name}")
    print(f"  Qwen file: {file_info['openrouter_file'].name}")
    print(f"{'='*80}")
    
    # Load results
    gemini_results, gemini_metadata = load_results(file_info['gemini_file'])
    qwen_results, qwen_metadata = load_results(file_info['openrouter_file'])
    
    if not gemini_results:
        print(f"ERROR: No Gemini results loaded from {file_info['gemini_file']}")
        return False
    
    if not qwen_results:
        print(f"ERROR: No Qwen results loaded from {file_info['openrouter_file']}")
        return False
    
    # Extract data
    gemini_data = extract_gemini_scores_and_flags(gemini_results)
    qwen_data = extract_openrouter_scores_and_flags(qwen_results)
    
    if not gemini_data['scores']:
        print(f"ERROR: No Gemini scores extracted")
        return False
    
    if not qwen_data['scores']:
        print(f"ERROR: No Qwen scores extracted")
        return False
    
    # Combine data by prompt_id
    combined_data = combine_data_by_prompt_id(gemini_data, qwen_data)
    
    if not combined_data['gemini']['scores'] or not combined_data['qwen3']['scores']:
        print(f"ERROR: No matched scores after combining data")
        return False
    
    # Perform analyses
    overall_results = overall_comparison(combined_data)
    category_results = category_comparison(combined_data)
    flag_results = flag_comparison(combined_data)
    
    # Generate markdown report
    markdown_report = generate_markdown_report(
        l4_folder, gemini_metadata, qwen_metadata, 
        overall_results, category_results, flag_results
    )
    
    # Save markdown report (organized by L4 folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Use L4 folder name as filename (e.g., L2.1_L4.1_analysis.md)
    safe_l4_name = l4_folder.replace('/', '_')
    output_file = output_dir / f"{safe_l4_name}_gemini_vs_qwen3_analysis.md"
    with open(output_file, 'w') as f:
        f.write(markdown_report)
    
    print(f"✓ Analysis complete. Report saved to: {output_file}")
    
    return True


def main():
    """Main execution function."""
    project_root = Path(__file__).parent
    data_dir = project_root / "Data"
    
    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        return
    
    # Find all L4 folders with both Gemini and Qwen (OpenRouter) results
    l4_folders = find_l4_folders(data_dir)
    
    if not l4_folders:
        print("ERROR: No L4 folders found with both Gemini and Qwen (OpenRouter) results")
        print("Looking for:")
        print("  - Gemini results in: Data/L2.X/L4.Y/gemini_results/evaluation_results_*.json")
        print("  - Qwen results in: Data/L2.X/L4.Y/qwen_results/evaluation_results_*.json")
        return
    
    print(f"Found {len(l4_folders)} L4 folder(s) with both Gemini and Qwen (OpenRouter) results")
    
    # Create output directory
    output_dir = project_root / "analysis_reports"
    output_dir.mkdir(exist_ok=True)
    
    # Process each L4 folder
    successful = 0
    failed = 0
    
    for l4_folder, file_info in sorted(l4_folders.items()):
        try:
            if analyze_l4_folder(l4_folder, file_info, output_dir):
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"ERROR processing {l4_folder}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total L4 folders: {len(l4_folders)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nReports saved to: {output_dir}")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()


