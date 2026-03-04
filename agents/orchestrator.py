from typing import List, Dict, Any
from agents.intent_analyzer import IntentAnalyzerAgent
from agents.product_fetcher import ProductFetcherAgent
from agents.relevance_filter import RelevanceFilterAgent
from config.constants import (
    MAX_PRODUCTS_PER_KEYWORD,
    MAX_TOTAL_PRODUCTS,
    MAX_KEYWORDS
)


class OrchestratorAgent:
    """Orchestrates multiple agents to fulfill shopping requests."""

    def __init__(self, stores: List[str]):
        self.intent_analyzer = IntentAnalyzerAgent()
        self.product_fetcher = ProductFetcherAgent(stores)
        self.relevance_filter = RelevanceFilterAgent()

    def execute(self, prompt: str) -> Dict[str, Any]:
        steps = []

        steps.append("🔍 Analyzing shopping intent...")
        intent = self.intent_analyzer.analyze(prompt)

        keywords = intent.get("keywords", [prompt])
        gender = intent.get("gender", "unisex")
        scenario = intent.get("scenario", "standard")

        steps.append(
            f"✓ Detected: {', '.join(keywords)} | "
            f"Gender: {gender} | Scenario: {scenario}"
        )

        all_products = []
        seen_ids = set()

        for keyword in keywords[:MAX_KEYWORDS]:
            steps.append(f"🛍️  Searching for '{keyword}' across 24 stores...")

            raw_products = self.product_fetcher.fetch(keyword)
            steps.append(f"📦 Found {len(raw_products)} raw products")

            steps.append(f"🤖 Filtering with AI for relevance and gender...")
            filtered = self.relevance_filter.filter(raw_products, keyword, gender)

            count = 0
            for product in filtered:
                if product["id"] in seen_ids:
                    continue

                if count >= MAX_PRODUCTS_PER_KEYWORD:
                    break

                all_products.append(product)
                seen_ids.add(product["id"])
                count += 1

                steps.append(
                    f"✓ Added: {product['title'][:50]}... | "
                    f"${product['price']} | {product['store_domain']}"
                )

            if len(all_products) >= MAX_TOTAL_PRODUCTS:
                break

        return {
            "status": "success",
            "products": all_products[:MAX_TOTAL_PRODUCTS],
            "steps": steps,
            "intent": intent
        }
