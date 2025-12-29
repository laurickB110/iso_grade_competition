#!/usr/bin/env python3
"""
AI Reflection Template

This template shows how to implement the AI reflection phase using
the Anthropic API (Claude). The reflection phase analyzes solver
performance and suggests improvements.

To use this:
1. Set ANTHROPIC_API_KEY environment variable
2. Install anthropic SDK: pip install anthropic
3. Integrate into go.py's _reflect_and_improve method

DO NOT commit API keys to the repository!
"""

import os
import json
from typing import Dict, Optional


def reflect_with_claude(
    dataset_name: str,
    state: Dict,
    analysis: Dict,
    config: Dict
) -> Optional[Dict]:
    """
    Call Claude API to analyze performance and suggest improvements.

    Args:
        dataset_name: Name of the dataset
        state: Current dataset state from tracker
        analysis: Progress analysis
        config: Workflow configuration

    Returns:
        Dictionary with suggestions or None if API unavailable
    """

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not set. Skipping AI reflection.")
        return None

    try:
        import anthropic
    except ImportError:
        print("Warning: anthropic package not installed.")
        print("Install with: pip install anthropic")
        return None

    # Prepare context for Claude
    context = {
        "dataset": dataset_name,
        "best_cost": state["best_cost"],
        "iterations_completed": len(state["history"]),
        "trend": analysis["trend"],
        "improvement_rate": analysis["improvement_rate"],
        "current_params": config["solver_params"],
        "recent_history": [
            {
                "iteration": h["iteration"],
                "best_cost": h["best_cost"],
                "avg_cost": h["avg_cost"]
            }
            for h in state["history"][-10:]
        ]
    }

    # Build prompt for Claude
    prompt = f"""You are analyzing the performance of an optimization solver for a 5G antenna placement problem.

Dataset: {dataset_name}
Current best cost: {state['best_cost']:,}
Target cost: {config['target_scores'].get(dataset_name, 'Not set')}

Performance analysis:
- Trend: {analysis['trend']}
- Recent improvement: {analysis['improvement_rate']:.2f}%
- Iterations completed: {len(state['history'])}

Current solver parameters:
{json.dumps(config['solver_params'], indent=2)}

Recent iteration history (last 10):
{json.dumps(context['recent_history'], indent=2)}

The solver uses:
1. Greedy set cover for initial placement
2. Local optimization with three operators: OPTIMIZE_TYPE (downgrade antenna), MERGE (combine nearby), REMOVE (delete and redistribute)

Based on this analysis, please provide:

1. **Assessment**: What is working well? What are the bottlenecks?

2. **Parameter suggestions**: Recommend specific parameter changes that could improve results.
   Focus on: iteration count, spatial grid size, optimization operator weights.

3. **Strategy suggestions**: Are there algorithmic improvements to consider?

4. **Next steps**: Concrete actions to try in the next iteration cycles.

Format your response as JSON with this structure:
{{
  "assessment": "...",
  "parameter_changes": {{
    "param_name": {{
      "current": current_value,
      "suggested": new_value,
      "reason": "why this change helps"
    }}
  }},
  "strategy_suggestions": ["suggestion 1", "suggestion 2"],
  "confidence": "high/medium/low",
  "next_steps": ["step 1", "step 2"]
}}
"""

    # Call Claude API
    try:
        client = anthropic.Anthropic(api_key=api_key)
        model = config.get("ai_model", "claude-sonnet-4-5-20250929")

        message = client.messages.create(
            model=model,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse response
        response_text = message.content[0].text

        # Try to extract JSON from response
        # Claude might wrap it in markdown code blocks
        if "```json" in response_text:
            json_start = response_text.index("```json") + 7
            json_end = response_text.index("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.index("```") + 3
            json_end = response_text.index("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        suggestions = json.loads(response_text)
        return suggestions

    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return None


def apply_suggestions(
    suggestions: Dict,
    config: Dict,
    auto_apply: bool = False
) -> bool:
    """
    Apply suggestions from AI reflection.

    Args:
        suggestions: Suggestions from Claude
        config: Current configuration (will be modified)
        auto_apply: Whether to apply automatically or ask user

    Returns:
        True if suggestions were applied
    """

    if not suggestions:
        return False

    print("\n--- AI SUGGESTIONS ---")
    print(f"\nAssessment: {suggestions.get('assessment', 'N/A')}")
    print(f"Confidence: {suggestions.get('confidence', 'unknown')}")

    if "parameter_changes" in suggestions and suggestions["parameter_changes"]:
        print("\nParameter changes:")
        for param, change in suggestions["parameter_changes"].items():
            print(f"  {param}:")
            print(f"    Current: {change.get('current')}")
            print(f"    Suggested: {change.get('suggested')}")
            print(f"    Reason: {change.get('reason')}")

    if "strategy_suggestions" in suggestions:
        print("\nStrategy suggestions:")
        for i, suggestion in enumerate(suggestions["strategy_suggestions"], 1):
            print(f"  {i}. {suggestion}")

    if "next_steps" in suggestions:
        print("\nNext steps:")
        for i, step in enumerate(suggestions["next_steps"], 1):
            print(f"  {i}. {step}")

    # Apply or ask
    if not auto_apply:
        response = input("\nApply these parameter changes? (y/n): ")
        if response.lower() != 'y':
            return False

    # Apply parameter changes
    if "parameter_changes" in suggestions:
        for param, change in suggestions["parameter_changes"].items():
            if param in config["solver_params"]:
                old_value = config["solver_params"][param]
                new_value = change.get("suggested")
                config["solver_params"][param] = new_value
                print(f"Applied: {param} = {new_value} (was {old_value})")

    return True


# Example usage (for testing)
if __name__ == "__main__":
    # Example state and analysis
    example_state = {
        "best_cost": 150000,
        "history": [
            {"iteration": 1, "best_cost": 200000, "avg_cost": 220000},
            {"iteration": 2, "best_cost": 180000, "avg_cost": 190000},
            {"iteration": 3, "best_cost": 160000, "avg_cost": 170000},
            {"iteration": 4, "best_cost": 155000, "avg_cost": 160000},
            {"iteration": 5, "best_cost": 150000, "avg_cost": 155000},
            {"iteration": 6, "best_cost": 150000, "avg_cost": 152000},
            {"iteration": 7, "best_cost": 150000, "avg_cost": 151000},
        ]
    }

    example_analysis = {
        "trend": "stagnant",
        "improvement_rate": 0.3
    }

    example_config = {
        "target_scores": {"2_small_town": 100000},
        "solver_params": {"iterations": 1000},
        "ai_model": "claude-sonnet-4-5-20250929"
    }

    suggestions = reflect_with_claude(
        "2_small_town",
        example_state,
        example_analysis,
        example_config
    )

    if suggestions:
        apply_suggestions(suggestions, example_config, auto_apply=False)
