import os
from dotenv import load_dotenv
from config.stores import SHOPIFY_STORES
from agents.orchestrator import OrchestratorAgent


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment")
        return

    os.environ["OPENAI_API_KEY"] = api_key

    orchestrator = OrchestratorAgent(SHOPIFY_STORES)

    example_queries = [
        "I need a mechanical keyboard and wireless mouse for my workspace",
        "Men's workout outfit for the gym",
        "Dinner date tonight - need a sharp outfit",
        "Comfortable everyday casual wear"
    ]

    prompt = example_queries[0]
    print(f"🎯 Query: {prompt}")
    print(f"💡 Try these queries: {', '.join(example_queries[1:3])}\n")
    print("=" * 70)

    result = orchestrator.execute(prompt)

    print("\n📋 Execution Steps:")
    print("-" * 70)
    for step in result["steps"]:
        print(f"  {step}")

    print(f"\n🎁 Found {len(result['products'])} Products:")
    print("-" * 70)
    for product in result["products"]:
        print(f"  • {product['title']}")
        print(f"    💰 ${product['price']} | 🏪 {product['store_domain']}")
        print()


if __name__ == "__main__":
    main()
