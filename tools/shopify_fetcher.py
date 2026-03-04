from typing import List, Dict, Any
import asyncio
import httpx
from upsonic.tools import Tool
from config.constants import SHOPIFY_FETCH_TIMEOUT, SHOPIFY_FETCH_LIMIT


class ShopifyFetcher(Tool):
    """Fetches products from Shopify stores."""

    def __init__(self, stores: List[str]):
        super().__init__(
            name="shopify_fetcher",
            description="Fetch products from Shopify stores by keyword"
        )
        self.stores = stores
        self.timeout = SHOPIFY_FETCH_TIMEOUT

    async def _fetch_from_store(self, domain: str, keyword: str) -> List[Dict[str, Any]]:
        url = f"https://{domain}/products.json"
        params = {"limit": SHOPIFY_FETCH_LIMIT}
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True, headers=headers) as client:
            try:
                response = await client.get(url, params=params)
                if response.status_code == 403:
                    # Try a different approach or just log it
                    return []
                response.raise_for_status()
                data = response.json()

                products = []
                keyword_lower = keyword.lower()

                for item in data.get("products", []):
                    title = item.get("title", "").lower()
                    body = item.get("body_html", "").lower()
                    tags = [t.lower() for t in item.get("tags", [])]
                    
                    # Broader matching
                    matches = (
                        keyword_lower in title or 
                        keyword_lower in body or 
                        any(keyword_lower in tag for tag in tags)
                    )
                    
                    if not matches:
                        continue

                    variants = item.get("variants", [])
                    if not variants:
                        continue

                    images = item.get("images", [])
                    image_url = images[0].get("src") if images else None

                    products.append({
                        "id": str(item["id"]),
                        "title": item["title"],
                        "price": float(variants[0].get("price", 0)),
                        "image": image_url,
                        "store_domain": domain,
                        "url": f"https://{domain}/products/{item.get('handle', '')}"
                    })

                return products
            except Exception:
                return []

    async def _aexecute(self, keyword: str) -> Dict[str, Any]:
        tasks = [self._fetch_from_store(store, keyword) for store in self.stores]
        results = await asyncio.gather(*tasks)

        all_products = []
        for result in results:
            all_products.extend(result)

        return {
            "keyword": keyword,
            "products": all_products,
            "total": len(all_products)
        }

    def _execute(self, keyword: str) -> Dict[str, Any]:
        try:
            # Try running with asyncio.run() first (standard for modern Python)
            return asyncio.run(self._aexecute(keyword))
        except RuntimeError as e:
            # If we get "Running in a thread" or "Event loop is already running"
            if "running" in str(e).lower():
                import threading
                import queue
                
                res_queue = queue.Queue()
                
                def run_async():
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        result = loop.run_until_complete(self._aexecute(keyword))
                        res_queue.put(result)
                        loop.close()
                    except Exception as ex:
                        res_queue.put(ex)
                
                thread = threading.Thread(target=run_async)
                thread.start()
                thread.join()
                
                ans = res_queue.get()
                if isinstance(ans, Exception):
                    raise ans
                return ans
            else:
                raise e
