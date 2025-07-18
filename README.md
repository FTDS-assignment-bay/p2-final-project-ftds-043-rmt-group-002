# Final Project: RMT-043 Group 002
  ![logo](https://github.com/FTDS-assignment-bay/p2-final-project-ftds-043-rmt-group-002/blob/main/Logo_Wangi_Final.png)

---
## 💡Project Overview

**Wangi is a machine learning-based application designed to help users discover perfumes that best match their personal preferences.** By leveraging Natural Language Processing (NLP) to interpret both product descriptions and real user reviews, Wangi provides accurate and personalized perfume recommendations, especially for online shoppers who cannot sample scents directly.

---

## 👥Group Members
- **Ainna Muslida Safira** - [Linkedin](www.linkedin.com/in/ainnamuslidasafira) | [Github](https://github.com/ainnamuslidasafira)
- **Bimantyo Arya Majid** - [Linkedin](https://www.linkedin.com/in/bimantyoarya/) | [Github](https://github.com/Bimantyo)
- **Dylan Sherwood Hanenkang** - [Linkedin](www.linkedin.com/in/dylsherwood) | [Github](https://github.com/Lynion)
- **Syarief Qayum Suaib** - [Linkedin](https://www.linkedin.com/in/syariefqayum/) | [Github](https://github.com/syariefsq)

---

## ⚙Background
In today’s modern life, people are becoming increasingly aware of the importance of appearance. Many are willing to spend a considerable amount of money on beauty treatments to enhance how they look. Human needs and desires are endless, always seeking something new (Parinduri & Rahmat, 2022). This opens up a significant opportunity for businesses. As globalization grows, business competition becomes more intense, especially in marketing products and services to consumers. Companies continuously compete to offer attractive solutions that meet consumer needs and wants (Virda et al., 2023).

Perfume has become an essential part of fashion. It is used to complete one’s appearance and boost confidence. Perfume plays a major role in the global market, as it is widely used by people around the world. According to wolipop.detik.com, everything can now be found online, and beauty products like makeup are among the most purchased. Even though physical stores have reopened, many women prefer to buy lipstick or powder through e-commerce—not just because of free shipping, but also due to discounts offered on those platforms.

Interest in perfumes is also growing rapidly in Indonesia. According to Central Insight, the perfume market in Indonesia reached IDR 5.8 trillion in 2022. This growth is driven by the rising middle class who are becoming more fashion-conscious. The increasing number of local perfume brands also supports consumers in investing in quality fragrances to boost their confidence.

Indonesian consumers are highly dynamic. They are open to trying new products as long as they are high-quality and affordable. However, most buyers rely on reviews before making a purchase. This shows they trust the experiences of other users more than brand claims. Therefore, customer reviews play a crucial role in influencing buying decisions.

Today, more local perfume products are emerging, each with unique characteristics and scent profiles. Ideally, consumers would test the scent in person to assess its quality. However, this isn’t possible with online shopping due to physical and resource limitations. As a result, there is a growing need for systems based on machine learning and natural language processing (NLP) to help understand consumer preferences through product descriptions and customer reviews.

---
## 🚩Problem Statement 

* Online perfume shoppers face **difficulty choosing fragrances** since they cannot smell products directly.
* User reviews and product descriptions are often the only references available, but not all users can interpret them effectively.
* E-commerce platforms rarely provide recommendation systems based on user scent preferences.
* There is a need for a system that understands user needs from keywords such as scent, longevity, sillage, concentration (EDT, EDP, Parfum), notes (top, middle, base), and occasions.
---

## 📊Dataset & Insights

### Dataset

* Data collected by scraping product and review information from [femaledaily.com](femaledaily.com) on EDP subcategories.
* Over 1,000 perfume products, each with price, rating, and up to 10 user reviews.
* Data cleaning included merging raw data, removing duplicates and irrelevant entries, renaming columns, and imputing missing values for price and product descriptions.

### Insights

* Most reviews from users aged 18–29; this group prefers affordable perfumes.
* Top brands: Evangeline, Saff & Co., Mykonos.
* Sweet, floral, and long-lasting scents are most popular.
* High ratings (4.0–5.0) show strong satisfaction.
---

## 🛠️ Methodology
 1. **Data Collection & Loading:** Scraped perfume product listings and reviews from femaledaily.com, then loaded datasets for further analysis.
 2. **Data Cleaning:** Merged raw data from multiple sources, removed duplicates, handled missing values (especially in price and product descriptions), and standardized column names and types.
 3. **Exploratory Data Analysis (EDA):** Analyzed product, review, and user demographics to uncover trends in scent preferences, price sensitivity, and brand popularity.
 4. **Text Preprocessing:**
    * Cleaned review texts to remove noise and irrelevant content.
    * Translated mixed-language (Indonesian/English) reviews into a single language using automated translation.
    * Tokenized and stemmed words to standardize vocabulary.
    * Embedded processed text into numerical vectors for downstream modeling.
 5. **Feature Engineering:** Combined multiple reviews per product into a single text field to capture overall sentiment and product characteristics.
 6. **Semantic Search & Similarity Scoring:**
    * Preprocessed and embedded user queries into the same vector space as product reviews.
    * Calculated cosine similarity between user input and each product’s review vector.
 7. **Recommendation Engine:** Ranked products based on similarity scores and returned up to eight perfumes most relevant to the user’s stated preferences.
 8. **Deployment:** Deployed the trained recommendation system as a user-friendly web application using streamlit and huggingface, allowing real-time perfume search and recommendation for end users. 

---

## 🌱 Next Steps
We plan to expand data sources, automate data updates, and integrate Wangi into e-commerce and retail platforms.

---
## 🏁 Conclusion
Wangi simplifies perfume discovery for online shoppers, offering personalized recommendations and supporting brands in understanding customer preferences.

---
## 🚀 Dashboard and Deployment
* Our program deployment can be accessed on [Hugging Face](https://huggingface.co/spaces/Lynion/wangi)
* Dashboard can be accessed on [Tableau](https://public.tableau.com/views/Final-Project-RMT-043-Group-02/Dashboard1?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
