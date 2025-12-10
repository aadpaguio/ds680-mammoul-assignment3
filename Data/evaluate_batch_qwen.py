"""
Biometric Privacy Evaluation Script - Batch Version (Qwen3 Only)
==================================================================
- Test Model: OpenRouter (qwen/qwen3-235b-a22b)
- Judge Model: gpt-5-nano-2025-08-07 (via OpenAI)
- Each prompt is tested 1 time

Usage: 
    python evaluate_batch.py --l4 L2.4/L4.14              # Run all prompts for L4.14
    python evaluate_batch.py --l4 L2.4/L4.14 --limit 10   # Run first 10 prompts
    python evaluate_batch.py --l4 L2.1/L4.1 --start 50 --limit 25  # Run prompts 50-74 for L4.1
    
Concurrency Options:
    --concurrency 3        # Max concurrent OpenRouter requests (default: 3)
    --delay 0.5            # Extra delay between OpenRouter requests (default: 0)
    --batch-size 20        # Pause after every N requests (default: 0 = disabled)
    --batch-pause 10      # Seconds to pause between batches (default: 10)

Example with rate limit handling:
    python evaluate_batch.py --l4 L2.4/L4.14 --concurrency 2 --delay 0.5

Example with batch pausing (pause 10s every 20 requests):
    python evaluate_batch.py --l4 L2.4/L4.14 --batch-size 20 --batch-pause 10
"""

import json
import os
import argparse
import asyncio
import csv
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Base path will be set in main() based on --l4 argument
# This will be initialized after parsing arguments
L4_BASE_PATH = None

# Clients will be initialized in main() after loading API keys
openrouter_client = None
judge_client = None

# Config
# Test model - OpenRouter (Qwen3)
TEST_MODEL = "qwen/qwen3-235b-a22b"

# Judge model options:
# - "gpt-5-mini-2025-08-07" (best performance, most expensive)
# - "gpt-5-nano-2025-08-07" (good performance, 5x cheaper - recommended for cost savings)
# - "gpt-4o-mini" (cheapest, may have slightly lower accuracy)
JUDGE_MODEL = "gpt-5-nano-2025-08-07"
JUDGE_PROMPT_FILE = "judge_prompt.txt"
PROMPTS_FILE = "prompt_set.json"

# Pricing per 1M tokens (as of Nov 2025 - UPDATE THESE AS NEEDED)
PRICING = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-5-mini-2025-08-07": {"input": 0.25, "output": 2.0},
    "gpt-5-nano-2025-08-07": {"input": 0.05, "output": 0.40},  # Much cheaper alternative
    "qwen/qwen3-235b-a22b": {"input": 0.18, "output": 0.54},
}


class CostTracker:
    """Track API usage and costs (thread-safe for async)."""
    
    def __init__(self):
        self.usage = {
            "test_model": {"input_tokens": 0, "output_tokens": 0},
            "judge_model": {"input_tokens": 0, "output_tokens": 0},
        }
        self.calls = {
            "test_model": 0,
            "judge_model": 0
        }
        self._lock = asyncio.Lock()
    
    async def add_test_usage(self, response):
        """Track usage from test model call."""
        async with self._lock:
            usage = response.usage
            self.usage["test_model"]["input_tokens"] += usage.prompt_tokens
            self.usage["test_model"]["output_tokens"] += usage.completion_tokens
            self.calls["test_model"] += 1
    
    async def add_judge_usage(self, response):
        """Track usage from judge model call."""
        async with self._lock:
            usage = response.usage
            self.usage["judge_model"]["input_tokens"] += usage.prompt_tokens
            self.usage["judge_model"]["output_tokens"] += usage.completion_tokens
            self.calls["judge_model"] += 1
    
    def get_cost(self, model: str, model_type: str) -> dict:
        """Calculate cost for a specific model."""
        pricing = PRICING.get(model, {"input": 0, "output": 0})
        input_cost = (self.usage[model_type]["input_tokens"] / 1_000_000) * pricing["input"]
        output_cost = (self.usage[model_type]["output_tokens"] / 1_000_000) * pricing["output"]
        return {
            "input_tokens": self.usage[model_type]["input_tokens"],
            "output_tokens": self.usage[model_type]["output_tokens"],
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost
        }
    
    def get_summary(self) -> dict:
        """Get full cost summary."""
        test_cost = self.get_cost(TEST_MODEL, "test_model")
        judge_cost = self.get_cost(JUDGE_MODEL, "judge_model")
        
        return {
            "openrouter_test_model": {
                "model": TEST_MODEL,
                "calls": self.calls["test_model"],
                **test_cost
            },
            "judge_model": {
                "model": JUDGE_MODEL,
                "calls": self.calls["judge_model"],
                **judge_cost
            },
            "total": {
                "calls": self.calls["test_model"] + self.calls["judge_model"],
                "input_tokens": test_cost["input_tokens"] + judge_cost["input_tokens"],
                "output_tokens": test_cost["output_tokens"] + judge_cost["output_tokens"],
                "total_cost": test_cost["total_cost"] + judge_cost["total_cost"]
            }
        }
    
    def print_summary(self):
        """Print formatted cost summary."""
        summary = self.get_summary()
        
        print(f"\n{'='*60}")
        print("COST SUMMARY")
        print(f"{'='*60}")
        
        print(f"\n{TEST_MODEL} (Test Model):")
        print(f"  Calls: {summary['openrouter_test_model']['calls']}")
        print(f"  Tokens: {summary['openrouter_test_model']['input_tokens']:,} in / {summary['openrouter_test_model']['output_tokens']:,} out")
        print(f"  Cost: ${summary['openrouter_test_model']['total_cost']:.4f}")
        
        print(f"\n{JUDGE_MODEL} (Judge Model):")
        print(f"  Calls: {summary['judge_model']['calls']}")
        print(f"  Tokens: {summary['judge_model']['input_tokens']:,} in / {summary['judge_model']['output_tokens']:,} out")
        print(f"  Cost: ${summary['judge_model']['total_cost']:.4f}")
        
        print("\nTOTAL:")
        print(f"  API Calls: {summary['total']['calls']}")
        print(f"  Tokens: {summary['total']['input_tokens']:,} in / {summary['total']['output_tokens']:,} out")
        print(f"  Cost: ${summary['total']['total_cost']:.4f}")


# Global cost tracker
cost_tracker = CostTracker()


class BatchPauser:
    """Pause periodically after N completions to avoid rate limits."""
    
    def __init__(self, batch_size: int = 20, pause_seconds: float = 10.0):
        self.batch_size = batch_size
        self.pause_seconds = pause_seconds
        self.completions = 0
        self._lock = asyncio.Lock()
    
    async def on_complete(self):
        """Called after each request completes. Pauses every batch_size completions."""
        if self.batch_size <= 0 or self.pause_seconds <= 0:
            return  # Disabled
        
        async with self._lock:
            self.completions += 1
            if self.completions % self.batch_size == 0:
                print(f"\n⏸️  Batch pause: {self.completions} requests completed. "
                      f"Pausing {self.pause_seconds}s to avoid rate limits...")
                await asyncio.sleep(self.pause_seconds)
                print("▶️  Resuming...\n")


# Global batch pauser (will be configured in main)
batch_pauser = None


def load_judge_prompt(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()


def load_prompts(filepath: str) -> list[dict]:
    with open(filepath, "r") as f:
        data = json.load(f)
    return data["prompts"]


def create_csv_summary(results: list[dict], output_file: str, execution_time: str = ""):
    """Create a CSV file with prompt summary including scores and flags.
    
    Dynamically detects flag names from the results and maps them to CSV columns.
    This handles different judge prompts that may use different flag naming schemes.
    """
    csv_file = output_file.replace(".json", ".csv")
    
    # Define standard CSV flag columns (what we want in the output)
    flag_columns = [
        "retention_warning_present",
        "specific_timeline_provided",
        "deletion_mechanism_explained",
        "sensitivity_differentiation",
        "user_control_offered",
        "audit_transparency",
        "regulatory_reference"
    ]
    
    # Discover actual flag names from the results (first non-empty evaluation)
    actual_flag_names = set()
    for result in results:
        for trial in result.get("openrouter_trials", []):
            if "evaluation" in trial and "flags" in trial["evaluation"]:
                actual_flag_names.update(trial["evaluation"]["flags"].keys())
                break
        if actual_flag_names:
            break
    
    # Build mapping from actual flag names to CSV column names
    # This handles different judge prompts with different flag naming schemes
    FLAG_MAPPING = {}
    
    # Standard mappings (for different naming schemes)
    mapping_rules = {
        # L4.11 style (short names)
        "warning": "retention_warning_present",
        "transparency": "audit_transparency",
        "alternatives": "user_control_offered",
        "differentiation": "sensitivity_differentiation",
        "regulatory_cite": "regulatory_reference",
        # L4.14 style (full names) - direct match
        "retention_warning_present": "retention_warning_present",
        "specific_timeline_provided": "specific_timeline_provided",
        "deletion_mechanism_explained": "deletion_mechanism_explained",
        "sensitivity_differentiation": "sensitivity_differentiation",
        "user_control_offered": "user_control_offered",
        "audit_transparency": "audit_transparency",
        "regulatory_reference": "regulatory_reference",
    }
    
    # Build mapping for flags that actually exist
    for actual_flag in actual_flag_names:
        if actual_flag in mapping_rules:
            FLAG_MAPPING[actual_flag] = mapping_rules[actual_flag]
        elif actual_flag in flag_columns:
            # Direct match - flag name matches CSV column
            FLAG_MAPPING[actual_flag] = actual_flag
    
    # CSV headers with flag columns
    flag_headers = flag_columns
    headers = ["prompt_id", "prompt", "score"] + flag_headers
    
    rows = []
    
    # Add execution time as a comment row (if provided)
    if execution_time:
        # Add a summary row at the beginning
        summary_row = [""] * len(headers)
        summary_row[0] = f"Execution Time: {execution_time}"
        rows.append(summary_row)
        rows.append([""] * len(headers))  # Empty row for spacing
    
    for result in results:
        prompt_id = result["prompt_id"]
        # Get prompt from first trial (all trials have same prompt)
        test_prompt = ""
        if result.get("openrouter_trials") and len(result["openrouter_trials"]) > 0:
            test_prompt = result["openrouter_trials"][0].get("test_prompt", "")
        
        # Collect scores
        scores = []
        
        # Process trials
        for trial in result.get("openrouter_trials", []):
            if "evaluation" in trial and "score" in trial["evaluation"]:
                score = trial["evaluation"]["score"]
                if score is not None:
                    scores.append(score)
        
        # Calculate average
        avg_score = sum(scores) / len(scores) if scores else None
        
        # Aggregate flags: True if ANY trial has the flag set to True
        flags = {flag: False for flag in flag_columns}
        
        # Process trials flags
        for trial in result.get("openrouter_trials", []):
            if "evaluation" in trial and "flags" in trial["evaluation"]:
                json_flags = trial["evaluation"]["flags"]
                # Map JSON flags to CSV flags using the discovered mapping
                for json_flag_name, json_flag_value in json_flags.items():
                    csv_flag_name = FLAG_MAPPING.get(json_flag_name)
                    if csv_flag_name and csv_flag_name in flag_columns:
                        if json_flag_value:  # If flag is True in JSON
                            flags[csv_flag_name] = True
        
        # Create row with flags
        row = [
            prompt_id,
            test_prompt,
            f"{avg_score:.2f}" if avg_score is not None else "N/A",
        ] + [str(flags[flag]).upper() for flag in flag_columns]
        
        rows.append(row)
    
    # Write CSV file
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print(f"CSV summary saved to {csv_file}")


async def get_model_response(prompt: str, client: AsyncOpenAI, model: str, max_retries: int = 5) -> str:
    """Get response from model being evaluated with retry logic for empty responses and length truncation."""
    last_error = None
    max_tokens = 2048  # Start with base token limit
    
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=max_tokens
            )
            await cost_tracker.add_test_usage(response)
            
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            
            # Handle length truncation - increase tokens and retry
            if finish_reason == "length":
                if attempt < max_retries - 1:
                    max_tokens = min(max_tokens * 2, 16384)  # Double tokens, cap at 16384
                    print(f"WARNING: Response truncated (length limit reached). Retrying with increased token limit ({max_tokens})...")
                    await asyncio.sleep(1)
                    continue
                else:
                    # Even if truncated, return what we have if content exists
                    if content and content.strip():
                        print(f"WARNING: Response was truncated but returning partial content (max tokens: {max_tokens})")
                        return content
                    else:
                        raise ValueError(f"Model response was truncated and content is empty (finish_reason: length, max_tokens: {max_tokens}) - All retries exhausted")
            
            # Check for empty response (only if not a length issue)
            if not content or not content.strip():
                error_msg = f"Model returned empty response (finish_reason: {finish_reason}, attempt: {attempt + 1}/{max_retries})"
                print(f"WARNING: {error_msg}")
                
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise ValueError(f"{error_msg} - All retries exhausted")
            
            # Success - if this was a retry, indicate it
            if attempt > 0:
                print(f"  ✓ Success on retry attempt {attempt + 1}/{max_retries}")
            
            return content
        
        except ValueError:
            # Re-raise ValueError (our custom errors) without retry
            raise
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"API error (attempt {attempt + 1}/{max_retries}): {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
    
    # Should never reach here, but just in case
    if last_error:
        raise last_error
    raise ValueError("Model response failed after all retries")


async def judge_response(test_prompt: str, model_response: str, judge_template: str, max_retries: int = 5) -> dict:
    """Use judge model to evaluate the response with retry logic."""
    filled_prompt = judge_template.replace("{test_prompt}", test_prompt).replace("{model_response}", model_response)
    
    last_error = None
    max_tokens = 4000  # Increased from 2000 to handle longer judge responses
    
    for attempt in range(max_retries):
        try:
            response = await judge_client.chat.completions.create(
                model=JUDGE_MODEL,
                messages=[{"role": "user", "content": filled_prompt}],
                max_completion_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            await cost_tracker.add_judge_usage(response)
            
            raw_content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            
            if not raw_content or not raw_content.strip():
                error_msg = f"Judge model returned empty response (finish_reason: {finish_reason}, attempt: {attempt + 1}/{max_retries})"
                print(f"WARNING: {error_msg}")
                
                # If it's a length issue, try with more tokens
                if finish_reason == "length" and attempt < max_retries - 1:
                    max_tokens = min(max_tokens * 2, 8000)  # Double tokens, cap at 8000
                    print(f"Retrying with increased token limit ({max_tokens})...")
                    await asyncio.sleep(1)
                    continue
                
                # If it's a content filter or other issue, retry
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                
                raise ValueError(f"{error_msg}")
            
            try:
                result = json.loads(raw_content)
                # Success - if this was a retry, indicate it
                if attempt > 0:
                    print(f"  ✓ Judge succeeded on retry attempt {attempt + 1}/{max_retries}")
                return result
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse JSON from judge model (attempt: {attempt + 1}/{max_retries})"
                print(f"ERROR: {error_msg}")
                print(f"Raw response:\n{raw_content}")
                print(f"Parse error: {e}")
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                
                raise ValueError(f"{error_msg}: {e}")
        
        except ValueError:
            # Re-raise ValueError (our custom errors) without retry
            raise
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"API error (attempt {attempt + 1}/{max_retries}): {e}")
                await asyncio.sleep(2 ** attempt)
                continue
            raise
    
    # Should never reach here, but just in case
    if last_error:
        raise last_error
    raise ValueError("Judge model failed after all retries")


async def evaluate_prompt(
    prompt_data: dict,
    judge_template: str,
    semaphore: asyncio.Semaphore,
    rate_limit_delay: float = 0.0
) -> dict:
    """Evaluate a single prompt (with retry logic).
    
    Concurrency is controlled at this level - semaphore limits how many
    prompts run concurrently.
    
    Args:
        rate_limit_delay: Optional delay (seconds) between requests for rate-limited providers.
    """
    prompt_id = prompt_data["id"]
    test_prompt = prompt_data["prompt"]
    
    async with semaphore:  # Limit concurrent prompts
        # Optional rate limit delay for providers with strict limits
        if rate_limit_delay > 0:
            await asyncio.sleep(rate_limit_delay)
        
        try:
            # Get model response (with retry logic)
            print(f"  [{prompt_id}] Getting model response...")
            model_response = await get_model_response(test_prompt, openrouter_client, TEST_MODEL)
            print(f"  [{prompt_id}] Model response received ({len(model_response)} chars)")
            
            # Judge the response (with retry logic)
            print(f"  [{prompt_id}] Sending to judge model...")
            evaluation = await judge_response(test_prompt, model_response, judge_template)
            score = evaluation.get("score", "N/A")
            print(f"  [{prompt_id}] Judge completed - Score: {score}/5")
            
            # Trigger batch pause (if configured)
            if batch_pauser:
                await batch_pauser.on_complete()
            
            return {
                "prompt_id": prompt_id,
                "category": prompt_data.get("category"),
                "subcategory": prompt_data.get("subcategory"),
                "test_model": TEST_MODEL,
                "judge_model": JUDGE_MODEL,
                "test_prompt": test_prompt,
                "model_response": model_response,
                "evaluation": evaluation
            }
        except Exception as e:
            # Return error result instead of raising
            print(f"  [{prompt_id}] ERROR - {e}")
            return {
                "prompt_id": prompt_id,
                "test_model": TEST_MODEL,
                "error": str(e)
            }


async def run_batch(
    prompts: list[dict],
    judge_template: str,
    start: int = 0,
    limit: int = None,
    concurrency: int = 3,
    delay: float = 0.0
):
    """Run evaluation on a batch of prompts asynchronously.
    
    Args:
        concurrency: Max concurrent requests (default: 3)
        delay: Additional delay (seconds) between requests (default: 0)
    """
    # Slice prompts based on start and limit
    end = start + limit if limit else len(prompts)
    batch = prompts[start:end]
    total_prompts = len(batch)
    
    print(f"\nRunning evaluation on {total_prompts} prompts (indices {start} to {start + total_prompts - 1})")
    print(f"Test Model: {TEST_MODEL} (OpenRouter)")
    print(f"Judge Model: {JUDGE_MODEL}")
    print(f"Total prompts: {total_prompts} (1 trial per prompt)")
    print(f"Concurrency: {concurrency}")
    if delay > 0:
        print(f"Rate limit delay: {delay}s between requests")
    print(f"{'='*60}\n")
    
    # Create semaphore for concurrency control
    semaphore = asyncio.Semaphore(concurrency)
    
    # Initialize prompt_results structure for all prompts
    prompt_results = {}  # prompt_id -> {"openrouter_trials": []}
    for prompt_data in batch:
        prompt_id = prompt_data["id"]
        prompt_results[prompt_id] = {
            "prompt_id": prompt_id,
            "category": prompt_data.get("category"),
            "subcategory": prompt_data.get("subcategory"),
            "openrouter_trials": []
        }
    
    # Create tasks for all prompts
    print(f"Creating {total_prompts} tasks...")
    tasks = []
    task_info = []  # Track prompt_id for each task
    
    for prompt_data in batch:
        prompt_id = prompt_data["id"]
        
        # Create task
        task = asyncio.create_task(
            evaluate_prompt(
                prompt_data, judge_template,
                semaphore,
                rate_limit_delay=delay
            )
        )
        tasks.append(task)
        task_info.append(prompt_id)
    
    print(f"All {len(tasks)} tasks created. Processing results as they complete...\n")
    
    # Process results as they complete and group by prompt
    errors = []
    completed = 0
    
    for task, prompt_id in zip(tasks, task_info):
        try:
            result = await task
            completed += 1
            
            # Add result to appropriate list
            prompt_results[prompt_id]["openrouter_trials"].append(result)
            
            # Print progress
            if completed % 10 == 0 or completed == total_prompts:
                print(f"Progress: {completed}/{total_prompts} prompts completed ({completed*100//total_prompts}%)")
                
        except Exception as e:
            completed += 1
            error_msg = str(e)
            print(f"ERROR: {prompt_id} failed: {error_msg}")
            errors.append({"prompt_id": prompt_id, "error": error_msg})
    
    # Convert prompt_results dict to list
    results = []
    for prompt_id in sorted(prompt_results.keys()):
        result = prompt_results[prompt_id]
        results.append(result)
        
        # Print summary for each prompt
        scores = [
            t["evaluation"]["score"]
            for t in result["openrouter_trials"]
            if "evaluation" in t and "score" in t["evaluation"] and t["evaluation"]["score"] is not None
        ]
        
        score = scores[0] if scores else None
        score_str = f"{score:.2f}/5" if score is not None else "N/A"
        print(f"\n✓ {prompt_id} COMPLETE - Score: {score_str}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"BATCH COMPLETE: {len(results)} successful, {len(errors)} errors")
    
    if results:
        # Collect all scores
        all_scores = []
        
        for r in results:
            for trial in r["openrouter_trials"]:
                if "evaluation" in trial and "score" in trial["evaluation"]:
                    score = trial["evaluation"]["score"]
                    if score is not None:
                        all_scores.append(score)
        
        if all_scores:
            avg = sum(all_scores) / len(all_scores)
            print(f"\nAverage Score: {avg:.2f}/5")
            dist = {i: all_scores.count(i) for i in range(1, 6)}
            print(f"Distribution: {dist}")
    
    return results, errors


async def main():
    parser = argparse.ArgumentParser(description="Batch evaluate biometric privacy responses (Qwen3 only)")
    parser.add_argument("--l4", type=str, required=True, help="L4 folder path (e.g., 'L2.4/L4.14' or 'L2.1/L4.1')")
    parser.add_argument("--start", type=int, default=0, help="Starting prompt index (default: 0)")
    parser.add_argument("--limit", type=int, default=None, help="Number of prompts to evaluate (default: all)")
    parser.add_argument("--output", type=str, default=None, help="Output filename (default: auto-generated)")
    parser.add_argument("--concurrency", type=int, default=3, help="Max concurrent requests (default: 3)")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay (seconds) between requests (default: 0)")
    parser.add_argument("--batch-size", type=int, default=0, help="Pause after every N requests (default: 0 = disabled)")
    parser.add_argument("--batch-pause", type=float, default=10.0, help="Seconds to pause between batches (default: 10)")
    args = parser.parse_args()
    
    # Initialize batch pauser if batch-size is set
    global batch_pauser
    if args.batch_size > 0:
        batch_pauser = BatchPauser(batch_size=args.batch_size, pause_seconds=args.batch_pause)
        print(f"Batch pausing enabled: {args.batch_pause}s pause every {args.batch_size} requests")
    
    # Determine base path - script is in Data/ folder
    script_path = Path(__file__).resolve()
    data_path = script_path.parent  # Script is in Data/, so parent is Data/
    
    # Build L4 folder path
    l4_path = data_path / args.l4
    if not l4_path.exists():
        raise ValueError(f"L4 folder not found: {l4_path}. Available folders in Data: {[d.name for d in data_path.iterdir() if d.is_dir()]}")
    
    global L4_BASE_PATH
    L4_BASE_PATH = l4_path
    
    print(f"Using L4 folder: {L4_BASE_PATH}")
    
    # Load environment variables from Data/ folder (shared .env file)
    env_path = data_path / ".env"
    if not env_path.exists():
        raise ValueError(f".env file not found in {data_path}. Please create a .env file in the Data/ folder.")
    
    print(f"Loading .env from: {env_path}")
    # Load with override=True to ensure we use values from the file
    load_dotenv(env_path, override=True)
    
    # Debug: Check what keys are loaded (without showing values)
    env_vars = {}
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key = line.split("=")[0].strip()
                env_vars[key] = "***"  # Hide value
    
    print(f"Found environment variables in .env: {list(env_vars.keys())}")
    
    # Get API keys
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        raise ValueError(f"OPENROUTER_API_KEY not found in .env file at {env_path}. Found keys: {list(env_vars.keys())}")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError(f"OPENAI_API_KEY not found in .env file at {env_path}. Found keys: {list(env_vars.keys())}")
    
    print("✓ API keys loaded successfully")
    
    # Initialize clients
    global openrouter_client, judge_client
    openrouter_client = AsyncOpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/yourusername/yourrepo",
            "X-Title": "DS680 Evaluation",
            "X-Data-Policy": "allow"
        }
    )
    judge_client = AsyncOpenAI(api_key=openai_api_key)
    
    # Reminder about OpenRouter configuration for free models
    if ":free" in TEST_MODEL:
        print("\n" + "="*60)
        print("NOTE: Using free model via OpenRouter")
        print("="*60)
        print("If you get 'data policy' errors, configure your account:")
        print("  https://openrouter.ai/settings/privacy")
        print("  Enable 'Allow prompt training' or set data policy to 'allow'")
        print("="*60 + "\n")
    
    # Load resources from L4 folder
    print("Loading judge prompt...")
    judge_prompt_path = L4_BASE_PATH / JUDGE_PROMPT_FILE
    if not judge_prompt_path.exists():
        raise ValueError(f"Judge prompt file not found: {judge_prompt_path}")
    judge_template = load_judge_prompt(str(judge_prompt_path))
    
    print("Loading test prompts...")
    prompts_path = L4_BASE_PATH / PROMPTS_FILE
    if not prompts_path.exists():
        raise ValueError(f"Prompts file not found: {prompts_path}")
    prompts = load_prompts(str(prompts_path))
    print(f"Found {len(prompts)} prompts")
    
    # Record start time
    start_time = time.time()
    
    # Run batch evaluation
    results, errors = await run_batch(
        prompts=prompts,
        judge_template=judge_template,
        start=args.start,
        limit=args.limit,
        concurrency=args.concurrency,
        delay=args.delay
    )
    
    # Record end time and calculate duration
    end_time = time.time()
    duration_seconds = end_time - start_time
    duration_minutes = duration_seconds / 60
    duration_hours = duration_minutes / 60
    
    # Format duration nicely
    if duration_hours >= 1:
        duration_str = f"{duration_hours:.2f} hours ({duration_minutes:.2f} minutes)"
    elif duration_minutes >= 1:
        duration_str = f"{duration_minutes:.2f} minutes ({duration_seconds:.2f} seconds)"
    else:
        duration_str = f"{duration_seconds:.2f} seconds"
    
    # Print timing summary
    print(f"\n{'='*60}")
    print("TIMING SUMMARY")
    print(f"{'='*60}")
    print(f"Total execution time: {duration_str}")
    print(f"Start time: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End time: {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Print cost summary
    cost_tracker.print_summary()
    
    # Generate output filename (save in L4 folder)
    if args.output:
        output_file = str(L4_BASE_PATH / args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = str(L4_BASE_PATH / f"evaluation_results_{timestamp}.json")
    
    # Save results
    output_data = {
        "metadata": {
            "openrouter_test_model": TEST_MODEL,
            "judge_model": JUDGE_MODEL,
            "timestamp": datetime.now().isoformat(),
            "prompts_evaluated": len(results),
            "errors": len(errors),
            "execution_time": {
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "end_time": datetime.fromtimestamp(end_time).isoformat(),
                "duration_seconds": round(duration_seconds, 2),
                "duration_minutes": round(duration_minutes, 2),
                "duration_hours": round(duration_hours, 2),
                "formatted": duration_str
            },
            "cost_summary": cost_tracker.get_summary()
        },
        "results": results,
        "errors": errors
    }
    
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    
    # Create CSV summary
    create_csv_summary(results, output_file, duration_str)


if __name__ == "__main__":
    asyncio.run(main())
