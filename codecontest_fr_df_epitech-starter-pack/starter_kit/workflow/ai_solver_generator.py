#!/usr/bin/env python3
"""
AI-Guided Solver Evolution

This module uses Claude AI to:
1. Analyze performance of existing solvers
2. Generate new specialized solvers for each dataset
3. Iteratively improve solver quality through evolution

The AI writes actual Python code that gets executed and validated.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import anthropic


class SolverEvolutionEngine:
    """
    Manages the AI-guided evolution of optimization solvers.

    This is meta-optimization: using AI to generate and improve
    optimization algorithms themselves.
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.methods_dir = Path(__file__).parent.parent / "methods"
        self.generated_dir = self.methods_dir / "generated"
        self.generated_dir.mkdir(exist_ok=True)

        # Track all generated solvers
        self.generation_history = []

    def analyze_solver_performance(
        self,
        benchmark_results: Dict[str, Dict],
        dataset_characteristics: Dict[str, Dict]
    ) -> Dict:
        """
        Have AI analyze which solvers work well on which dataset types.

        Args:
            benchmark_results: Performance of each solver on each dataset
            dataset_characteristics: Properties of each dataset

        Returns:
            AI analysis with insights and patterns
        """

        prompt = self._build_analysis_prompt(benchmark_results, dataset_characteristics)

        print("🤖 Analyzing solver performance patterns...")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis_text = response.content[0].text

        # Try to parse JSON from response
        try:
            if "```json" in analysis_text:
                json_start = analysis_text.index("```json") + 7
                json_end = analysis_text.index("```", json_start)
                analysis_text = analysis_text[json_start:json_end].strip()

            analysis = json.loads(analysis_text)
        except:
            # If parsing fails, wrap in basic structure
            analysis = {"raw_analysis": analysis_text}

        return analysis

    def generate_specialized_solver(
        self,
        dataset_name: str,
        dataset_characteristics: Dict,
        benchmark_results: Dict[str, float],
        analysis: Dict,
        generation: int = 1
    ) -> Tuple[str, str]:
        """
        Generate a new solver specialized for a specific dataset.

        Args:
            dataset_name: Target dataset name
            dataset_characteristics: Dataset properties
            benchmark_results: Performance of existing solvers
            analysis: AI analysis from previous phase
            generation: Generation number (for versioning)

        Returns:
            (solver_filename, solver_code)
        """

        prompt = self._build_generation_prompt(
            dataset_name,
            dataset_characteristics,
            benchmark_results,
            analysis,
            generation
        )

        print(f"🧬 Generating specialized solver for {dataset_name} (gen {generation})...")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,  # Solvers can be long
            messages=[{"role": "user", "content": prompt}]
        )

        code = response.content[0].text

        # Extract Python code from markdown if present
        if "```python" in code:
            code_start = code.index("```python") + 9
            code_end = code.index("```", code_start)
            code = code[code_start:code_end].strip()
        elif "```" in code:
            code_start = code.index("```") + 3
            code_end = code.index("```", code_start)
            code = code[code_start:code_end].strip()

        # Generate filename
        safe_name = dataset_name.replace("_", "").replace("-", "")
        filename = f"ai_{safe_name}_gen{generation}.py"

        # Save metadata
        self.generation_history.append({
            "dataset": dataset_name,
            "generation": generation,
            "filename": filename,
            "timestamp": time.time(),
            "based_on_analysis": analysis.get("key_insights", [])
        })

        return filename, code

    def save_solver(self, filename: str, code: str) -> Path:
        """
        Save generated solver to disk.

        Args:
            filename: Name for the solver file
            code: Python code for the solver

        Returns:
            Path to saved file
        """

        filepath = self.generated_dir / filename

        # Add header comment
        header = f'''"""
AI-Generated Solver
Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
Model: {self.model}

This solver was automatically generated by Claude AI based on
analysis of existing solver performance patterns.
"""

'''

        full_code = header + code

        with open(filepath, 'w') as f:
            f.write(full_code)

        print(f"💾 Saved solver: {filepath}")

        return filepath

    def validate_solver_syntax(self, filepath: Path) -> Tuple[bool, Optional[str]]:
        """
        Check if generated solver has valid Python syntax.

        Args:
            filepath: Path to solver file

        Returns:
            (is_valid, error_message)
        """

        try:
            with open(filepath) as f:
                code = f.read()

            compile(code, filepath, 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Compilation error: {e}"

    def _build_analysis_prompt(
        self,
        benchmark_results: Dict,
        dataset_characteristics: Dict
    ) -> str:
        """Build prompt for performance analysis."""

        prompt = """You are an expert in optimization algorithms and meta-learning.

Analyze the performance of different solvers across various datasets to identify patterns.

# Benchmark Results

"""

        # Add results for each dataset
        for dataset_name, results in benchmark_results.items():
            prompt += f"\n## {dataset_name}\n"

            if dataset_name in dataset_characteristics:
                chars = dataset_characteristics[dataset_name]
                prompt += f"Dataset characteristics:\n"
                prompt += f"- Buildings: {chars.get('num_buildings', 'N/A')}\n"
                prompt += f"- Spatial distribution: {chars.get('distribution', 'N/A')}\n"
                prompt += f"- Avg demand: {chars.get('avg_demand', 'N/A')}\n"
                prompt += f"- Clustering: {chars.get('clustering', 'N/A')}\n"
                prompt += "\n"

            prompt += "Solver performance:\n"
            for solver_name, cost in sorted(results.items(), key=lambda x: x[1]):
                prompt += f"- {solver_name}: {cost:,}\n"
            prompt += "\n"

        prompt += """

# Your Task

Analyze these results and provide insights in JSON format:

{
  "key_patterns": [
    "Pattern 1: Which solver types work best for which dataset sizes/types",
    "Pattern 2: ...",
    "Pattern 3: ..."
  ],
  "solver_strengths": {
    "solver_name": "What this solver does well and why"
  },
  "solver_weaknesses": {
    "solver_name": "What this solver struggles with and why"
  },
  "dataset_insights": {
    "dataset_name": "What makes this dataset challenging"
  },
  "recommendations": [
    "Specific algorithmic improvements that could help",
    "..."
  ]
}

Focus on ACTIONABLE insights that can guide new solver design.
"""

        return prompt

    def _build_generation_prompt(
        self,
        dataset_name: str,
        dataset_characteristics: Dict,
        benchmark_results: Dict[str, float],
        analysis: Dict,
        generation: int
    ) -> str:
        """Build prompt for solver code generation."""

        # Read base.py to show the interface
        base_path = self.methods_dir / "base.py"
        with open(base_path) as f:
            base_code = f.read()

        # Read existing solvers as examples
        examples = []
        for solver_file in ["baseline_place_on_buildings.py", "randomized_greedy.py"]:
            solver_path = self.methods_dir / solver_file
            if solver_path.exists():
                with open(solver_path) as f:
                    examples.append(f"# {solver_file}\n{f.read()}\n")

        prompt = f"""You are an expert in optimization algorithms. Generate a NEW solver specifically optimized for the dataset: {dataset_name}

# Dataset Characteristics

{json.dumps(dataset_characteristics, indent=2)}

# Existing Solver Performance

{json.dumps(benchmark_results, indent=2)}

# Analysis Insights

{json.dumps(analysis.get('key_patterns', []), indent=2)}
{json.dumps(analysis.get('recommendations', []), indent=2)}

# Problem Context

This is a 5G antenna placement optimization problem:
- Goal: Minimize total installation cost
- Constraints: Coverage, capacity, range
- Antennas: Nano, Spot, Density, MaxRange (different cost/capacity/range)

# Required Interface

Your solver MUST follow this interface (from methods/base.py):

```python
def solve(dataset: dict, *, seed: int, params: dict = None) -> dict:
    '''
    Args:
        dataset: Dict with 'buildings' list
        seed: Random seed for reproducibility
        params: Optional parameters dict

    Returns:
        Dict with 'antennas' list, each antenna has:
        - type: str (Nano/Spot/Density/MaxRange)
        - x: int
        - y: int
        - buildings: list of building IDs
    '''
    pass
```

# Existing Solvers (for reference)

{chr(10).join(examples[:2000])}  # Truncated for brevity

# Your Task

Generate a COMPLETE, WORKING Python solver that:

1. **Imports from base.py**: Use ANTENNA_TYPES, get_building_demand, distance, etc.
2. **Follows the interface**: Function signature must match exactly
3. **Is specialized for {dataset_name}**: Use insights from the analysis
4. **Implements a novel approach**: Don't just copy existing solvers
5. **Handles edge cases**: All buildings covered, valid ranges, capacities
6. **Uses the seed**: For reproducible randomness (random.Random(seed))

Generate ONLY the Python code, no explanations. Make it production-ready.

Focus on algorithms that would excel given:
- Dataset size: {dataset_characteristics.get('num_buildings', 'unknown')} buildings
- The weaknesses you identified in existing solvers
- The specific characteristics of this dataset type

Be creative but practical. The code must work on first try.
"""

        return prompt

    def save_generation_report(self, output_path: Path):
        """Save a report of all generated solvers."""

        report = {
            "generation_count": len(self.generation_history),
            "solvers": self.generation_history,
            "timestamp": time.time()
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        exit(1)

    # Initialize engine
    engine = SolverEvolutionEngine(api_key)

    # Mock benchmark results for testing
    benchmark_results = {
        "1_peaceful_village": {
            "baseline": 150000,
            "randomized_greedy": 120000,
            "optimized": 125000
        },
        "3_suburbia": {
            "baseline": 32000000,
            "randomized_greedy": 28500000,
            "optimized": 30700000
        }
    }

    dataset_characteristics = {
        "1_peaceful_village": {
            "num_buildings": 10,
            "distribution": "sparse",
            "avg_demand": 300,
            "clustering": "low"
        },
        "3_suburbia": {
            "num_buildings": 1000,
            "distribution": "moderate",
            "avg_demand": 500,
            "clustering": "medium"
        }
    }

    # Phase 1: Analyze
    print("=" * 70)
    print("PHASE 1: PERFORMANCE ANALYSIS")
    print("=" * 70)
    analysis = engine.analyze_solver_performance(
        benchmark_results,
        dataset_characteristics
    )
    print("\n✅ Analysis complete")
    print(json.dumps(analysis, indent=2))

    # Phase 2: Generate specialized solver
    print("\n" + "=" * 70)
    print("PHASE 2: SOLVER GENERATION")
    print("=" * 70)
    filename, code = engine.generate_specialized_solver(
        dataset_name="3_suburbia",
        dataset_characteristics=dataset_characteristics["3_suburbia"],
        benchmark_results=benchmark_results["3_suburbia"],
        analysis=analysis,
        generation=1
    )

    # Save and validate
    filepath = engine.save_solver(filename, code)
    is_valid, error = engine.validate_solver_syntax(filepath)

    if is_valid:
        print(f"\n✅ Solver is syntactically valid!")
        print(f"\nYou can now test it with:")
        print(f"  python tools/run_experiment.py \\")
        print(f"    --dataset 3_suburbia \\")
        print(f"    --method methods.generated.{filename[:-3]}:solve \\")
        print(f"    --seeds 5")
    else:
        print(f"\n❌ Solver has syntax errors: {error}")
        print("AI will need to regenerate...")
