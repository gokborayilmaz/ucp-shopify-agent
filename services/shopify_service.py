from typing import List, Optional
import httpx
from models.product import Product


class ShopifyService:
    TIMEOUT = 8.0

    @staticmethod
    async def fetch_products(domain: str, keyword: str) -> List[Product]:
        url = f"https://{domain}/products.json"
        params = {"limit": 250}

        async with httpx.AsyncClient(timeout=ShopifyService.TIMEOUT, follow_redirects=True) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                products = []
                for item in data.get("products", []):
                    if not ShopifyService._is_relevant(item, keyword):
                        continue

                    product = ShopifyService._parse_product(item, domain)
                    if product:
                        products.append(product)

                return products
            except Exception:
                return []

    @staticmethod
    def _is_relevant(item: dict, keyword: str) -> bool:
        title = item.get("title", "").lower()
        keyword_lower = keyword.lower()
        return keyword_lower in title

    @staticmethod
    def _parse_product(item: dict, domain: str) -> Optional[Product]:
        try:
            variants = item.get("variants", [])
            if not variants:
                return None

            price = float(variants[0].get("price", 0))
            image_url = None

            images = item.get("images", [])
            if images and len(images) > 0:
                image_url = images[0].get("src")

            return Product(
                id=str(item["id"]),
                title=item["title"],
                price=price,
                image=image_url,
                store_domain=domain,
                url=f"https://{domain}/products/{item.get('handle', '')}"
            )
        except Exception:
            return None
