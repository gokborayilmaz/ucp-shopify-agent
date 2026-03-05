# 🛍🛒 ucp-shopify-agent

This agent intelligently analyzes your shopping intent and searches across 24 connected Shopify stores in parallel. Using a coordinated multi-agent system, it discovers and show the most relevant products,product infos and prices.

## Architecture

This Example Showcases:

- **4 Specialized Agents** working in coordination
- **Clean separation of concerns** (agents, tools, config)
- **Type-safe models** with Pydantic
- **Async parallel operations** across 24 Shopify stores

## Agents

### 1. IntentAnalyzerAgent
**Role**: Shopping intent analysis
**Default Model**: GPT-4o
**Purpose**: Extracts keywords, gender, and scenario from natural language

### 2. ProductFetcherAgent
**Role**: Product discovery from multiple stores
**Default Model**: GPT-4o-mini
**Purpose**: Fetches products from 24 Shopify stores in parallel

### 3. RelevanceFilterAgent
**Role**: Product relevance and gender filtering
**Default Model**: GPT-4o-mini
**Purpose**: AI-powered filtering with gender awareness

### 4. OrchestratorAgent
**Role**: Multi-agent coordination
**Purpose**: Manages workflow, deduplication, and result aggregation

## Installation

```bash
# Clone the repository
git clone https://github.com/gokborayilmaz/ucp-shopify-agent.git

# Create a virtual environment
uv venv

# Activate the virtual environment
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY 
```

## Usage
### Streamlit App (UI)

For a better visual experience, you can use the Streamlit interface:

```bash
streamlit run streamlit_app.py
```

This will launch a web interface where you can input your queries and see product images and details in a clean, modern layout.

[photo_2026-03-04_23-29-09](https://github.com/user-attachments/assets/394af8e4-f5ce-459a-90b0-5368854cb66e)


## Design Principles

- **SOLID**: Single responsibility per agent
- **DRY**: Reusable agent configurations
- **Clean Code**: Self-documenting, no comments needed
- **Type Safety**: Pydantic models throughout
- **Async First**: Parallel operations for performance

## Performance

- **24 stores** queried in parallel (~8 seconds)
- **Smart filtering** reduces LLM token usage
- **Max 12 products** for optimal response time
- **Fallback logic** ensures reliability

## Configuration

All constants are centralized in `config/constants.py`:

```python
MAX_PRODUCTS_PER_KEYWORD = 4  # Products per category
MAX_TOTAL_PRODUCTS = 12        # Total result limit
MAX_KEYWORDS = 3               # Maximum keywords to process
SHOPIFY_FETCH_TIMEOUT = 8.0    # Request timeout (seconds)
INTENT_MODEL = "openai/gpt-4o" # Intent analysis model
FILTER_MODEL = "openai/gpt-4o-mini" # Filtering model
```

## Powered By

- **Upsonic Agent Framework** v0.69.3
- **OpenAI** GPT-4o / GPT-4o-mini
- **Shopify** Products API (24 stores)
- **UCP** Universal Commerce Protocol principles
- **Python** 3.10+ with async/await
