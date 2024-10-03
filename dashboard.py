import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data=pd.read_csv('day.csv')

# Group by 'workingday' and 'holiday' to get aggregated counts
day_type_agg = data.groupby(by=["workingday", "holiday"]).agg({"cnt": "sum"}).reset_index()

# Create 'day_type' column to merge workingday and holiday information
day_type_agg['day_type'] = day_type_agg.apply(
    lambda row: 'Holiday' if row['holiday'] == 1 else 'Working Day' if row['workingday'] == 1 else 'Weekend',
    axis=1
)

# Group again by 'day_type' to get total counts per day type
day_type_total = day_type_agg.groupby('day_type')['cnt'].sum().reset_index()

# Weather condition aggregation
weather_agg = data.groupby(by="weathersit").agg({"cnt": "sum"}).reset_index()
weather_agg['weather_label'] = weather_agg['weathersit'].map(
    {1: 'Clear/Few Clouds', 2: 'Mist/Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
)

# Streamlit dashboard starts here
st.title("Bike Rentals Insights: Data Analysis by Day Type and Weather Conditions, by Vridha Amalia Rozaq")

# Create tabs for better navigation
tab1, tab2, tab3 = st.tabs(["Day Type Analysis", "Weather Analysis", "Summary"])

# Day Type Analysis
with tab1:
    st.header("- **How do bike rental patterns vary across working days, weekends, and holidays?**")
    
    # Barplot
    st.subheader("Barplot: Rentals by Day Type")
    st.write("""
    The bar plot below shows the total bike rentals based on the day type. We distinguish between **Working Days**, 
    **Weekends**, and **Holidays**. This helps to understand the usage trends on different types of days, where rentals 
    are generally higher on working days as people use bikes for commuting.
    """)
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.barplot(x='day_type', y='cnt', data=day_type_agg, palette='Set2', ax=ax1)
    ax1.set_title('Total Bike Rentals by Day Type (Working Day, Weekend, Holiday)')
    ax1.set_xlabel('Day Type')
    ax1.set_ylabel('Total Rentals')
    st.pyplot(fig1)
    
    # Pie Chart
    st.subheader("Pie Chart: Proportion of Rentals by Day Type")
    st.write("""
    The pie chart shows the proportion of bike rentals across different day types. It allows us to compare the share 
    of rentals on working days, weekends, and holidays, illustrating the dominance of bike rentals on working days compared 
    to holidays and weekends.
    """)
    fig2, ax2 = plt.subplots(figsize=(7, 7))
    ax2.pie(day_type_total['cnt'], labels=day_type_total['day_type'], autopct='%1.1f%%', startangle=90,
            colors=['#66b3ff', '#99ff99', '#ffcc99'])
    ax2.set_title('Proportion of Bike Rentals by Day Type (Working Day, Weekend, Holiday)')
    ax2.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
    st.pyplot(fig2)

# Weather Analysis
with tab2:
    st.header("- **How do weather conditions impact the number of bike rentals?**")
    
    # Barplot for weather condition
    st.subheader("Barplot: Rentals by Weather Condition")
    st.write("""
    Weather conditions greatly affect bike rental activity. The bar chart below shows the total rentals for each weather condition, 
    ranging from **clear skies** to **heavy rain/snow**. Generally, bike rentals are higher on clear days, while bad weather conditions 
    like heavy rain or snow significantly reduce rentals.
    """)
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.barplot(x='weather_label', y='cnt', data=weather_agg, palette='Blues_d', ax=ax3)
    ax3.set_title('Total Bike Rentals by Weather Condition')
    ax3.set_xlabel('Weather Condition')
    ax3.set_ylabel('Total Rentals')
    plt.xticks(rotation=45)
    st.pyplot(fig3)
    
    # Lineplot for weather situation trends
    st.subheader("Lineplot: Rentals Trend by Weather Situation")
    st.write("""
    The line plot shows the trend of bike rentals based on weather conditions, with each weather condition represented 
    by a number (1: Clear, 2: Mist, 3: Light Rain/Snow, 4: Heavy Rain/Snow). This gives an overview of how bike rentals decrease 
    significantly during adverse weather conditions.
    """)
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='weathersit', y='cnt', data=data, marker='o', ci=None, ax=ax4)
    ax4.set_title('Trend of Bike Rentals by Weather Situation')
    ax4.set_xlabel('Weather Situation (1: Clear, 2: Mist, 3: Light Rain/Snow, 4: Heavy Rain/Snow)')
    ax4.set_ylabel('Total Rentals')
    plt.xticks([1, 2, 3, 4], ['Clear', 'Mist', 'Light Rain/Snow', 'Heavy Rain/Snow'])
    st.pyplot(fig4)

# Summary
with tab3:
    st.header("Summary of Bike Rentals")
    st.write("""
    From the above analysis, we can draw several key insights:
    
    - **Working Days** have the highest number of rentals compared to weekends and holidays. This shows that bikes are commonly 
    used for daily commuting, especially for work-related travel.
    
    - In terms of weather, **Clear Weather** leads to the most bike rentals, while poor weather conditions like **Heavy Rain or Snow** 
    drastically reduce the number of rentals.
    
    - The **Proportion of Bike Rentals** shown in the pie chart provides an overview of how rentals are distributed across working days, weekends, 
    and holidays, with working days dominating the rentals.
    
    This analysis can help in operational planning for bike rentals, especially in adjusting services based on weather conditions and day types.
    """)
