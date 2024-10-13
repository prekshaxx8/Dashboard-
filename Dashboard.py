import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "C:/Users/aniru/Desktop/PythonProj/Imports_Exports_Dataset.csv"  # User-specified file path
sample_df = pd.read_csv(file_path).sample(n=3001, random_state=55003)

# Set up the Streamlit page configuration
st.set_page_config(page_title="Imports/Exports Dashboard", layout="wide")

# Sidebar for navigation and filters
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Welcome Page", "Data Preview", "Analysis Dashboard", "Key Observations and Insights"])

# Welcome Page
if page == "Welcome Page":
    st.title("Welcome to the Imports/Exports Dashboard")
    st.markdown("""
                
    #### Purpose & Overview:
    This dashboard provides a comprehensive view of global imports and exports data, aiming to support strategic decision-making with detailed insights into trade volumes, product categories, shipping methods, and financial impacts.
    
    #### Key Features:
    - **Data Preview**: Filter and explore raw data directly.
    - **Analysis Dashboard**: Visualize trends and patterns in global trade with interactive charts.
    - **Key Observations and Insights**: Summarize the most critical findings and managerial insights to guide strategic actions.

    #### Objectives:
    * **Objective 1**: Identifying top 5 countries based on import and export activities across different countries.
    * **Objective 2**: Displaying Maximum Weight in KGs by Shipping Method and Category
    * **Objective 3**: Displaying Count of products by their payment terms per Category
    * **Objective 4**: Ranking categories by the total economic impact (Value), higher value gets a higher rank
    * **Objective 5**: Displaying Average Value and Quantity of Top 5 Countries
    * **Objective 6**: Displaying the minimum and maximum value using tables and the respective variables.
    * **Objective 7**: Understand the frequency of most sought products.
    * **Objective 8**: Understand the frequency of most used shipping method.
    """)


elif page == "Data Preview":
    st.title("📊 Data Preview Dashboard")

    # Sidebar Filters
    selected_countries = st.sidebar.multiselect("Select Countries", sample_df['Country'].unique())
    selected_product = st.sidebar.selectbox("Select Product", ["All"] + list(sample_df['Product'].unique()))

    # Filter Data based on selections
    if selected_countries or selected_product != "All":
        filtered_df = sample_df[
            (sample_df['Country'].isin(selected_countries) if selected_countries else True) &
            (sample_df['Product'] == selected_product if selected_product != "All" else True)
        ]
        st.subheader("Filtered Data")
    else:
        filtered_df = sample_df
        st.subheader("Sampled Data of 3001 Records")

    # Display the data
    st.dataframe(filtered_df)

    # Summary Statistics for displayed data
    st.subheader("Summary Statistics")
    summary_df = filtered_df[['Quantity', 'Value', 'Weight']].describe().T
    st.table(summary_df)

    # Save filtered data option
    if st.button("Save Filtered Data"):
        filtered_df.to_csv("Filtered_Data.csv", index=False)
        st.success("Filtered data saved as 'Filtered_Data.csv'")

elif page == "Analysis Dashboard":
    st.title("📊 Comprehensive Analysis Dashboard")

    # Top metrics displayed in cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="Total Records", value=sample_df.shape[0])
    col2.metric(label="Unique Products", value=sample_df['Product'].nunique())
    col3.metric(label="Unique Countries", value=sample_df['Country'].nunique())
    col4.metric(label="Most Used Shipping Method", value=sample_df['Shipping_Method'].mode()[0])
    col5.metric(label="Top Product", value=sample_df['Product'].mode()[0])

    # Filters for analysis
    st.sidebar.title("Filters")
    selected_country = st.sidebar.selectbox("Country", ["All"] + list(sample_df['Country'].unique()))
    import_export_choice = st.sidebar.radio("Import/Export", ["All", "Import", "Export"])

    filtered_data = sample_df.copy()
    if selected_country != "All":
        filtered_data = filtered_data[filtered_data['Country'] == selected_country]
    if import_export_choice != "All":
        filtered_data = filtered_data[filtered_data['Import_Export'] == import_export_choice]

    # Section for graphs and charts
    st.subheader("Data Visualizations")

    # Row 1: Top 5 Countries by Volume and Weight Heatmap
    col6, col7 = st.columns(2)
    
    with col6:
        st.subheader(f"Top 5 Countries by {import_export_choice if import_export_choice != 'All' else 'Total'} Volume")
        top_countries = filtered_data['Country'].value_counts().head(5)
        fig, ax1 = plt.subplots(figsize=(6, 3))
        sns.barplot(x=top_countries.index, y=top_countries.values, palette="Blues", ax=ax1)
        ax1.set_title("Top 5 Countries by Volume")
        ax1.set_ylabel("Volume")
        st.pyplot(fig)

    with col7:
        st.subheader("Maximum Weight in KGs per Shipping Method and Category")
        
        # Updating heatmap_data with new values
        heatmap_data = pd.DataFrame({
            "Clothing": [4927.00, 4994.90, 4982.45],
            "Electronics": [4971.92, 4984.60, 4990.24],
            "Furniture": [4965.92, 4928.60, 4993.26],
            "Machinery": [4994.36, 4998.01, 4994.71],
            "Toys": [4997.24, 4966.97, 4959.85]
        }, index=["Air", "Land", "Sea"])
        
        fig, ax2 = plt.subplots(figsize=(6, 3))
        
        # Keeping the color scheme similar to your previous heatmap
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax2)
        
        # Updating the title to reflect the context better
        ax2.set_title("Maximum Weight in KGs by Shipping Method and Category")
        
        # Displaying the updated plot
        st.pyplot(fig)

    # Row 2: Stacked Bar Chart for Payment Terms and Pie Chart for Category Ranking
    col8, col9 = st.columns(2)
    
    with col8:
        st.subheader("Count of Products by Payment Terms per Category")
        payment_terms_data = pd.DataFrame({
           "Cash on Delivery": [162, 137, 162, 149, 151],
            "Net 30": [142, 151, 159, 142, 140],
            "Net 60": [144, 142, 135, 162, 143],
            "Prepaid": [148, 148, 159, 162, 163]
        }, index=["Clothing", "Electronics", "Furniture", "Machinery", "Toys"])
        fig, ax = plt.subplots(figsize=(10, 6))
        payment_terms_data.plot(kind="bar", stacked=True, ax=ax, color=["#339966", "#FFD700", "#3366CC", "#FF6699"] )
        ax.set_title("Product Count by Payment Term per Category (Stacked Bar Chart)")
        ax.set_xlabel("Category")
        ax.set_ylabel("Product Count")
        ax.legend(title="Payment Term")

        st.pyplot(fig)

    with col9:
        st.subheader("Category Ranking by Total Economic Impact")
        
        data={
        "Category": ["Furniture", "Toys", "Clothing", "Machinery", "Electronics"],
        "Total Economic Impact in $": [3155020.10, 3001177.95, 2996226.27, 2992691.22, 2963909.82]
        }

        economic_impact_data = pd.DataFrame(data)

        # Create the pie chart with accurate colors and labels
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(economic_impact_data["Total Economic Impact in $"], labels=economic_impact_data["Category"], autopct="%1.1f%%", startangle=90, colors=sns.color_palette("bright"))

        # Set chart title
        ax.set_title("Distribution of Total Economic Impact by Category")
    
        # Show the plot
        st.pyplot(fig)

    col10, col0 = st.columns(2)
    
    with col10:
        st.subheader("Average Value and Quantity of Top 5 Countries")
        data = {
        "Country": ["Solomon Islands", "Switzerland", "Palau", "Somalia", "Guadeloupe"],
        "Avg_Value": [6908.63, 6872.15, 6774.04, 6688.90, 6463.84],
        "Avg_Quantity": [6367.50, 4426.23, 5343.90, 5449.82, 5405.83]
        }

        df = pd.DataFrame(data)

        # Create the stacked bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(x="Country", kind="bar", stacked=True, ax=ax)

        # Set chart title and labels
        ax.set_title("Top 5 Countries by Average Value and Quantity")
        ax.set_ylabel("Value/Quantity")
        ax.legend(title="Metric")

        # Add data labels
        for i in range(len(df)):
            for j in range(len(df.columns) - 1):  # Exclude the 'Country' column
                ax.text(i, df.iloc[i, j + 1], f"{df.iloc[i, j + 1]}", ha='center', va='bottom')

        # Show the plot using Streamlit
        st.pyplot(fig)
    
    # Minimum and Maximum tables
    st.subheader("Minimum and Maximum Values")
    min_data = {
        "Field": ["Country", "Product", "Import_Export", "Category", "Port", "Shipping Method", "Supplier", "Customer", "Payment Terms"],
        "Minimum Value": [
            sample_df['Country'].min(),
            sample_df['Product'].min(),
            sample_df['Import_Export'].min(),
            sample_df['Category'].min(),
            sample_df['Port'].min(),
            sample_df['Shipping_Method'].min(),
            sample_df['Supplier'].min(),
            sample_df['Customer'].min(),
            sample_df['Payment_Terms'].min()
        ],
        "Maximum Value": [
            sample_df['Country'].max(),
            sample_df['Product'].max(),
            sample_df['Import_Export'].max(),
            sample_df['Category'].max(),
            sample_df['Port'].max(),
            sample_df['Shipping_Method'].max(),
            sample_df['Supplier'].max(),
            sample_df['Customer'].max(),
            sample_df['Payment_Terms'].max()
        ]
    }
    min_max_table = pd.DataFrame(min_data)

    # Display tables side-by-side
    col11, col12 = st.columns(2)
    with col11:
        st.write("Minimum Values")
        st.table(min_max_table[['Field', 'Minimum Value']])
    with col12:
        st.write("Maximum Values")
        st.table(min_max_table[['Field', 'Maximum Value']])

elif page == "Key Observations and Insights":
    st.title("🔍 Key Observations and Insights")
    
    st.markdown("## Summary of Key Findings")
    st.markdown("""
    
    - **1) Top Countries**: The countries with the highest import/export volumes i.e **Congo** in this analysis, are critical players and could offer strategic partnership opportunities. Focusing on these could enhance business reach and customer base.
    
    - **2) Maximum Weight per Shipping Method and Category** : 
        **Shipping Method Impact**: **"Air"** is generally suitable for lighter items, while "Land" and "Sea" can handle heavier shipments.
        **Category Influence**: **"Machinery"** typically requires heavier shipping, followed by "Furniture" and "Clothing."
        **Shipping Method and Category Interactions**: The optimal shipping method depends on both product weight and category. For example, "Air" might be cost-effective for lighter items like "Electronics," while "Sea" could be more suitable for bulkier goods like "Machinery."
    
    - **3) Product and Payment Terms Preferences**: The stacked bar chart illustrates that  popular payment terms across categories are as below and thus Offering incentives aacording to these payment methods, it might improve cash flow and reduce risk:
       
        **Clothing**:
        The most popular payment method is Cash on Delivery with 162 product counts.

        **Electronics**:
        The most popular payment method is Net 30 with 151 product counts.

        **Furniture**:
        The most popular payment method is Cash on Delivery with 162 product counts.

        **Machinery**:
        The most popular payment method is Net 60 with 162 product counts.

        **Toys**:
        The most popular payment method is Prepaid with 163 product counts.
   
    - **4) Category Impact**: The categories with the highest economic impact—such as Furniture—should be prioritized for marketing and inventory planning as they contribute significantly to revenue.
    
    - **5) Average Value and Quantity of Top 5 Countries** : 
        **Solomon Islands** leads in average quantity traded **(6,367.5 units)**, indicating a focus on high-volume transactions.
        **Switzerland** has the **highest average value (6,872.15)**, indicating that it trades in fewer but higher-value products.
       ** Palau, Somalia, and Guadeloupe** have relatively balanced profiles but show variations in the emphasis on either quantity or value.
                
    - **6) Top Product** : The most preferred product is **travel**.
    
    - **7) Shipping Methods**: The most frequently used shipping method is identified i.e **"Air"** in this case, indicating a preference that can streamline logistics operations. Investing in optimizing this method could lead to cost savings and efficiency.

    """)

    st.markdown("## Managerial Insights")
    st.markdown("""
    1) Strategic Partnerships and Market Expansion:
    Focus on High-Volume Countries: Prioritize countries like Congo for strategic partnerships to expand market reach.
    Optimize Shipping: Tailor shipping methods based on product weight and category to reduce costs and improve efficiency.

    2) Customer Preferences and Payment Terms:
    Offer Incentives: Align payment incentives with popular payment methods to improve cash flow and reduce risk.
    Prioritize Popular Products: Focus on products like travel to meet customer demand.

    3) International Trade Analysis:
    Balance Quantity and Value: Understand the trade preferences of different countries to optimize product offerings.
    Optimize Shipping: Invest in optimizing shipping methods, especially "Air," to reduce costs and improve efficiency.
    """)

    st.markdown("## Recommendations")
    st.markdown("""
    
     **1) Category Focus**
       - Prioritize High-Impact Categories: Given the significant economic impact of categories like "Furniture," allocate resources strategically to optimize marketing efforts and inventory planning for these products.
       - Tailored Marketing Strategies: Develop targeted marketing campaigns for high-impact categories to maximize revenue and customer engagement.

     **2) Supply Chain Optimization**
       - Shipping Method Efficiency: Leverage the analysis of shipping methods and product categories to identify opportunities for optimizing logistics processes and reducing costs.
       - Negotiate Contracts: Use the insights to negotiate better rates with shipping providers, especially for frequently used methods like "Air."

     **3) Strategic Partnerships**
       - Focus on Top Countries: Explore potential partnerships with countries like "Congo" to expand market reach and access new customer segments.
       - Tailored Strategies: Develop customized strategies for each country based on their unique trade characteristics (e.g., high-volume vs. high-value).

     **4) Operational Efficiency**
       - Optimize Shipping Method: Since "Air" is the most frequently used method, invest in improving its efficiency through technology, infrastructure, or partnerships.
       - Inventory Management: Align inventory levels with the popularity of different product categories and shipping methods to minimize stockouts and excess inventory.

     **5) Payment Terms Optimization**
       - Offer Incentives: Consider offering incentives for specific payment terms to encourage preferred methods and improve cash flow.
       - Risk Management: Monitor cash-on-delivery trends to assess risk and implement appropriate measures.

     **6) Product Strategy**
       - Leverage Product Popularity: Focus on expanding the product range related to "travel" to capitalize on its popularity.
       - Diversification: Explore opportunities to diversify product offerings and reduce dependence on a single category.



     """)

    st.markdown("### Conclusion")
    st.markdown("""
    This comprehensive analysis offers valuable insights into global trade trends, revealing key areas for businesses to optimize their operations and financial performance. By leveraging data on product categories, shipping methods, and country-specific trade volumes, companies can make informed decisions to enhance efficiency, reduce costs, and improve customer satisfaction. Ultimately, implementing the recommended strategies can lead to sustainable growth and success in the competitive global marketplace.        
    """)

    # Optional footer for aesthetic purposes or additional information
st.sidebar.info("Developed by [Anirudh Gupta- 055003]")