import streamlit as st
import pandas as pd
from category_matcher import CategoryMatcher
import json

st.set_page_config(
    page_title="Categorical Search with Typesense",
    page_icon="🔍",
    layout="wide"
)

st.title("Categorical Search with Typesense")
st.markdown("Search for categorical values across tables and columns")

# Initialize the category matcher
@st.cache_resource
def get_matcher():
    return CategoryMatcher()

# Main search functionality
def perform_search(query, limit=30):
    matcher = get_matcher()
    results = matcher.find_categories(query, top_k=limit)
    return results

# Create the search interface
search_col, results_col = st.columns([1, 2])

with search_col:
    st.subheader("Search")
    query = st.text_input("Enter your search query:", placeholder="e.g., IRON FERROUS")
    limit = st.slider("Maximum results to display:", min_value=5, max_value=100, value=30)
    search_button = st.button("Search")

    # Display a sample of categories available
    st.subheader("Sample Categories")
    try:
        # Load a sample of categories from the CSV
        sample_data = pd.read_csv('data/All_cat_values.csv', nrows=10)
        st.dataframe(sample_data, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading sample data: {e}")

# Perform search when button is clicked
if search_button and query:
    with results_col:
        st.subheader(f"Search Results for: '{query}'")
        
        with st.spinner("Searching..."):
            results = perform_search(query, limit)
        
        if results:
            # Convert to DataFrame for easier display
            df = pd.DataFrame(results)
            
            # Display as table
            st.dataframe(df, use_container_width=True)
            
            # Create expandable sections for each table found
            table_groups = df.groupby('Table_name')
            for table_name, group in table_groups:
                with st.expander(f"Table: {table_name} ({len(group)} matches)"):
                    st.dataframe(group[['Value', 'Column_name', 'Table_path']], use_container_width=True)
            
            # Download option
            st.download_button(
                "Download Results as CSV",
                df.to_csv(index=False).encode('utf-8'),
                f"cat_search_results_{query.replace(' ', '_')}.csv",
                "text/csv",
                key='download-csv'
            )
        else:
            st.info("No results found. Try a different search term.")

# Add information about Typesense in the sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This application uses Typesense for fast and typo-tolerant categorical search.
    
    The search looks for matches in:
    - Category values
    - Table names
    - Column names
    
    It handles typos and partial matches to help you find relevant categorical data quickly.
    """)
    
    # Display connection status
    try:
        matcher = get_matcher()
        health = matcher.client.health.retrieve()
        st.success("✅ Connected to Typesense")
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
        st.info("Make sure your Typesense server is running on http://localhost:8108")

# Footer
st.markdown("---")
st.markdown("Powered by Typesense | Categorical Search Demo")
