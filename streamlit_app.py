import streamlit as st
import os
from dotenv import load_dotenv
from config.stores import SHOPIFY_STORES
from agents.orchestrator import OrchestratorAgent

# Load environment variables just like main.py
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="UCP Shopify Agent",
    page_icon="🛍️",
    layout="wide"
)

def main():
    st.title("🛍️ UCP Shopify Agent")
    st.markdown("---")

    # API Key check from env or sidebar
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
        if not api_key:
            st.warning("Please enter your OpenAI API Key to start.")
            return
        os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.sidebar.success("✅ OpenAI API Key found")


    # Mirror the example queries from main.py
    example_queries = [
        "I need a mechanical keyboard for my workspace",
        "Men's workout outfit for the gym",
        "I need  pan for cooking",
        "I need a mouse wireless for my workspace",
        "I need a comfortable women's Breezer Point",
        "Men's sports shoes waterproofly",
        "I need a Overshirt",
        "I need man's coastal hoodie"
    ]
    
    # Initialize session state for the query widget key
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

    def h_click(q):
        # Update the exact key used by the text_input widget
        st.session_state.search_query = q

    st.markdown("**Suggestions:**")
    
    # Display the suggestions vertically for better readability
    for i, q in enumerate(example_queries):
        st.button(f"✨ {q}", key=f"ex_{i}", on_click=h_click, args=(q,))

    st.markdown("---")

    # Text input linked directly to the session_state key
    query = st.text_input("🔍 What are you looking for?", key="search_query")
    
    # Trigger search ONLY if button is clicked
    run_clicked = st.button("Run Agent", type="primary")
    
    st.caption("Note: you can search according to the current stock of connected stores")
    with st.expander("🔗 Connected Stores", expanded=False):
        for store in SHOPIFY_STORES:
            st.markdown(f"- [{store}](https://{store})")

    if run_clicked and st.session_state.search_query:
        current_query = st.session_state.search_query
        
        with st.spinner(f"🔍 Agent is orchestrating search for: '{current_query}'..."):
            try:
                # Initialize orchestrator just like main.py
                orchestrator = OrchestratorAgent(SHOPIFY_STORES)
                
                # Execute exactly like main.py
                result = orchestrator.execute(current_query)
                
                # Display Execution Steps
                with st.expander("📋 Execution Steps", expanded=False):
                    for step in result.get("steps", []):
                        st.write(f"- {step}")
                
                # Display Results
                products = result.get("products", [])
                st.subheader(f"🎁 Found {len(products)} Products")
                st.markdown("---")
                
                if products:
                    cols = st.columns(3)
                    for idx, product in enumerate(products):
                        with cols[idx % 3]:
                            with st.container(border=True):
                                if product.get('image'):
                                    st.image(product['image'], width='stretch')
                                st.markdown(f"**{product['title']}**")
                                st.markdown(f"💰 **${product['price']}** | 🏪 `{product['store_domain']}`")
                                st.link_button("View Product", product['url'])
                else:
                    st.info("No products were added to the final list. Try a different query.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.exception(e)

if __name__ == "__main__":
    main()
