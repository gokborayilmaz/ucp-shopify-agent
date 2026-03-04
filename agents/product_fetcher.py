from typing import List, Dict, Any
from upsonic import Agent, Task
from tools.shopify_fetcher import ShopifyFetcher


class ProductFetcherAgent:
    """Fetches products from multiple Shopify stores in parallel."""

    def __init__(self, stores: List[str], model: str = "openai/gpt-4o-mini"):
        self.stores = stores
        self.fetcher_tool = ShopifyFetcher(stores)
        self.agent = Agent(
            name="Product Fetcher",
            role="Product discovery from multiple stores",
            goal="Fetch relevant products efficiently from 24 Shopify stores",
            instructions="""Fetch products from Shopify stores using the shopify_fetcher tool.
Handle parallel requests and aggregate results.""",
            model=model
        )

    def fetch(self, keyword: str) -> List[Dict[str, Any]]:
        result = self.fetcher_tool._execute(keyword)
        return result.get("products", [])
