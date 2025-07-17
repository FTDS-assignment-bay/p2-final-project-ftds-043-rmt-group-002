import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from sklearn.metrics.pairwise import cosine_similarity

def run():

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #F1E0E1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
      )

    # Sidebar with branding, instructions, and filters
    st.sidebar.markdown("## Wangi: Perfume Recommender")
    st.sidebar.markdown("### Welcome, fragrance explorer! 👃✨")
    st.sidebar.markdown(
        "Discover your next signature scent with **Wangi**. "
        "Describe your dream perfume, set your budget, and let the magic happen! "
        "Whether you love florals, musks, or something totally unique, we've got you covered."
    )

    st.sidebar.markdown("""
    **💁🏻‍♀️ How to use:**  
    - Enter your desired perfume characteristics (e.g. "flowery scent, suitable for women, great as a gift")  
    - Click **Find Recommendations** to get matching perfumes!

    > 🗣️ **You can use Bahasa Indonesia, English, or mix both in your search!**
    """)

    with st.sidebar.expander("📝 Beginner's Guide (click to expand)"):
        st.markdown("""
    **How to get the best recommendations:**

    - **Describe the scent:**  
      Use simple words like `fresh`, `sweet`, `woody`, `fruity`, `floral`, or `spicy`.

    - **Mention the user:**  
      Say if it’s for `men`, `women`, or `unisex`.

    - **Add the occasion (optional):**  
      For example: `daily use`, `gift`, `special event`, `work`, or `date night`.

    **Example queries:**
    - `fresh citrus scent for men`
    - `parfum floral manis untuk wanita, cocok untuk sehari-hari`
    - `unisex woody fragrance, cocok untuk hadiah`
    - `spicy and musky, untuk acara spesial`

    *Tip: The more details you give, the better the recommendations!*
    """)

    # Sidebar filters
    st.sidebar.subheader("💰  Filter by Price (IDR)")
    min_price = st.sidebar.number_input(
        "Min Price", min_value=0, max_value=3000000, value=150000, step=100000, format="%d"
    )
    max_price = st.sidebar.number_input(
        "Max Price", min_value=0, max_value=3000000, value=3000000, step=100000, format="%d"
    )
    st.sidebar.markdown(
        f"**Selected Price Range:** IDR {min_price:,} - IDR {max_price:,}"
    )

    # Load model and data with error handling
    @st.cache_resource(show_spinner=False)
    def load_resources():
        try:
            model = SentenceTransformer('./src/model_saved', device='cpu')
        except Exception as e:
            st.error(f"Failed to load model: {e}")
            return None, None, None
        try:
            df = pd.read_csv('./src/concated.csv')
        except Exception as e:
            st.error(f"Failed to load perfume data: {e}")
            return None, None, None
        try:
            embedding = torch.tensor(np.load('./src/embedding.npy'))
        except Exception as e:
            st.error(f"Failed to load embedding: {e}")
            return None, None, None
        return model, df, embedding

    model, df, embedding = load_resources()

    def recommend_items(query, min_price, max_price, top_n=8):
        if model is None or df is None or embedding is None:
            return pd.DataFrame()
        query_embedding = model.encode([query], convert_to_tensor=True)
        similarities = cosine_similarity(query_embedding.cpu().numpy(), embedding.cpu().numpy())[0]
        df['similarity_score'] = similarities
        filtered = df[
            (df['price'].astype(float) >= min_price) &
            (df['price'].astype(float) <= max_price)
        ]
        if filtered.empty:
            return pd.DataFrame()
        top_indices = filtered['similarity_score'].nlargest(top_n).index
        return filtered.loc[top_indices].copy()

    st.image("src/logo_wangi_fix.png", width=800)
    st.title('Perfume Recommendations Based on Your Preferences')
    st.write("Describe the perfume characteristics you are looking for, and we'll recommend the best products for you.")

    with st.form(key='perfume_recommend'):
        text = st.text_input('Perfume characteristics', placeholder='e.g. flowery scent, suitable for women, great as a gift')
        submitted = st.form_submit_button('Find Recommendations')

    if submitted:
        if not text.strip():
            st.warning('Please enter perfume characteristics first.')
            return
        st.subheader("Our Recommendations:")
        recommendations = recommend_items(text, min_price, max_price)
        if not recommendations.empty:
            cols = st.columns(2)
            image_size = 200
            for i, (_, row) in enumerate(recommendations.iterrows()):
                with cols[i % 2]:
                    # Always show a fixed-size image (real or placeholder)
                    if pd.notna(row['product_image']) and str(row['product_image']).startswith('http'):
                        st.image(row['product_image'], width=image_size)
                    else:
                        # Gray placeholder
                        st.image(np.full((image_size, image_size, 3), 220, dtype=np.uint8), width=image_size)
                    st.markdown(f"**🏷️ Brand:** {row['brand_name'] if pd.notna(row['brand_name']) else '-'}")
                    st.markdown(f"**💠 Product:** {row['full_name_product'] if pd.notna(row['full_name_product']) else '-'}")
                    st.markdown(f"**💰 Price:** IDR {int(row['price']):,}" if pd.notna(row['price']) else "-")
                    st.markdown(f"**⭐ {row['ratings']:.2f}**" if pd.notna(row['ratings']) else "**⭐ -**")
                    if pd.notna(row['link_product']) and str(row['link_product']).startswith('http'):
                        st.markdown(f"[🔗 View Product]({row['link_product']})")
                    desc = row['product_description'] if 'product_description' in row and pd.notna(row['product_description']) else row['review_processed'] if pd.notna(row['review_processed']) else "-"
                    with st.expander("📝 Product Description"):
                        st.write(desc)
                    st.write("---")
        else:
            st.info("No products found. Try different or more specific characteristics.")

    st.write("")

if __name__ == '__main__':
    run()
