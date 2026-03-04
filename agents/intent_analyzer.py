from upsonic import Agent, Task
from config.constants import INTENT_MODEL


class IntentAnalyzerAgent:
    """Analyzes user shopping intent and extracts structured information."""

    def __init__(self, model: str = INTENT_MODEL):
        self.agent = Agent(
            name="Intent Analyzer",
            role="Shopping intent analysis",
            goal="Extract keywords, gender preference, and scenario from user requests",
            instructions="""Analyze user shopping requests and extract:
1. Product keywords (simple terms like 'keyboard', 'shirt', 'sneakers')
2. Gender preference (men/women/unisex)
3. Shopping scenario (date/athletic/casual/tech/standard)

Scenario Detection Rules:
- date: dinner, restaurant, impress, sharp, evening → smart casual wear
- athletic: workout, gym, running, training → activewear
- tech: workspace, setup, desk, coding → tech products
- casual: everyday, comfortable, relaxed → casual wear
- standard: direct product request

ALWAYS return valid JSON format:
{
  "keywords": ["keyword1", "keyword2"],
  "gender": "men|women|unisex",
  "scenario": "date|athletic|casual|tech|standard"
}

Max 3 keywords for efficiency.""",
            model=model
        )

    def analyze(self, prompt: str) -> dict:
        import json
        try:
            task = Task(description=f"Analyze this shopping request: {prompt}")
            result = self.agent.do(task)

            result_str = str(result)
            if "```json" in result_str:
                json_str = result_str.split("```json")[1].split("```")[0].strip()
            else:
                json_str = result_str

            return json.loads(json_str)
        except Exception as e:
            print(f"⚠️  Intent analysis error: {e}, using fallback")
            return {
                "keywords": [prompt],
                "gender": "unisex",
                "scenario": "standard"
            }
