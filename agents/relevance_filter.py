from typing import List, Dict, Any
from upsonic import Agent, Task
import json
from config.constants import FILTER_MODEL


class RelevanceFilterAgent:
    """Filters products for relevance using AI with gender awareness."""

    def __init__(self, model: str = FILTER_MODEL):
        self.agent = Agent(
            name="Relevance Filter",
            role="Product relevance and gender filtering",
            goal="Filter products by relevance and gender appropriateness",
            instructions="""Filter products based on keyword relevance and gender preference.

Gender Filtering Rules:
- men: EXCLUDE products with women/womens/women's/female/lady/ladies/girl
        INCLUDE products with men/mens/men's/male/boy/unisex
        Be STRICT with ambiguous products from women-focused stores
- women: EXCLUDE products with men/mens/men's/male/boy
         INCLUDE products with women/womens/women's/female/lady/ladies/girl/unisex
- unisex: Include all genders

ALWAYS return only relevant product IDs as valid JSON: {"relevant_ids": [id1, id2, ...]}""",
            model=model
        )

    def filter(
        self,
        products: List[Dict[str, Any]],
        keyword: str,
        gender: str = "unisex"
    ) -> List[Dict[str, Any]]:
        if not products:
            return []

        product_data = [
            {"id": p["id"], "title": p["title"], "store": p["store_domain"]}
            for p in products
        ]

        task = Task(
            description=f"""Filter these products for keyword '{keyword}' with gender '{gender}'.
Products: {json.dumps(product_data)}
Return relevant product IDs."""
        )

        try:
            result = self.agent.do(task)
            result_str = str(result)

            if "```json" in result_str:
                json_str = result_str.split("```json")[1].split("```")[0].strip()
            else:
                json_str = result_str

            parsed = json.loads(json_str)
            relevant_ids = set(parsed.get("relevant_ids", []))
            return [p for p in products if p["id"] in relevant_ids]
        except Exception as e:
            print(f"Filter error: {e}")
            return self._fallback_filter(products, keyword, gender)

    def _fallback_filter(
        self,
        products: List[Dict[str, Any]],
        keyword: str,
        gender: str
    ) -> List[Dict[str, Any]]:
        keyword_lower = keyword.lower()
        filtered = [p for p in products if keyword_lower in p["title"].lower()]

        if gender == "men":
            return [
                p for p in filtered
                if not any(w in p["title"].lower() for w in ["women", "womens", "women's"])
            ]
        elif gender == "women":
            return [
                p for p in filtered
                if not any(w in p["title"].lower() for w in ["men's", "mens", "male"])
            ]

        return filtered
