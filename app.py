import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# Function to load dataset
@st.cache_data
def load_data(file_url):
    return pd.read_csv(file_url)

# Load dataset from a public URL (replace with your hosted file URL)
file_url = "https://path_to_your_file.csv"  # Replace this with the actual file URL

# Display spinner while loading app
with st.spinner('Loading app...'):
    time.sleep(1)

# Load the data from the cloud
df = load_data("https://drive.google.com/uc?export=download&id=1wuElVDAP8erlGjsXkq_fPGCPLrtsljQY")

# Main dashboard title
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='font-size: 3.5em; font-family: "Arial", sans-serif; font-weight: 700; color: #71C6FF;'>Supply Chain Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Dataset display expander
with st.expander("📋 Show Dataset"):
    st.write(df)


# Sidebar filters
product_types = st.sidebar.multiselect("Select Product Type(s)", options=df['Product type'].unique(), default=df['Product type'].unique())
df = df[df['Product type'].isin(product_types)]

search_term = st.sidebar.text_input("Search Product/Order ID")
if search_term:
    df = df[df['Product Name'].str.contains(search_term, case=False)]

# Filter for Manufacturing Costs (Range Slider)
min_cost, max_cost = st.sidebar.slider(
    "Select Manufacturing Cost Range:",
    min_value=int(df['Manufacturing costs'].min()), 
    max_value=int(df['Manufacturing costs'].max()),
    value=(int(df['Manufacturing costs'].min()), int(df['Manufacturing costs'].max()))
)
df = df[(df['Manufacturing costs'] >= min_cost) & (df['Manufacturing costs'] <= max_cost)]

# Additional Filters
# Filter for Order Quantities
min_quantity, max_quantity = st.sidebar.slider(
    "Select Order Quantity Range:",
    min_value=int(df['Order quantities'].min()), 
    max_value=int(df['Order quantities'].max()),
    value=(int(df['Order quantities'].min()), int(df['Order quantities'].max()))
)
df = df[(df['Order quantities'] >= min_quantity) & (df['Order quantities'] <= max_quantity)]

# Filter for Inspection Results
inspection_results_filter = st.sidebar.multiselect(
    "Select Inspection Results:", options=df['Inspection results'].unique(),
    default=df['Inspection results'].unique()
)
df = df[df['Inspection results'].isin(inspection_results_filter)]

# Filter for Locations
location_filter = st.sidebar.multiselect(
    "Select Locations:", options=df['Location'].unique(),
    default=df['Location'].unique()
)
df = df[df['Location'].isin(location_filter)]

# Filter for Transportation Modes
transportation_modes_filter = st.sidebar.multiselect(
    "Select Transportation Modes:", options=df['Transportation modes'].unique(),
    default=df['Transportation modes'].unique()
)
df = df[df['Transportation modes'].isin(transportation_modes_filter)]

# Display cards for KPIs
card_container = st.container()
with card_container:
    col1, col2, col3 = st.columns(3, gap="large")

    # Card: Total Revenue Generated
    with col1:
        if 'Revenue generated' in df.columns:
            total_revenue = df['Revenue generated'].sum()
            st.markdown(
                f"""
                <div style="background-color: #f0f2f6; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                    <h2 style="font-size: 24px; color: #333;">💰 Total Revenue Generated</h2>
                    <h1 style="font-size: 36px; color: #2b8c42;">₹{total_revenue:,.2f}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("The 'Revenue generated' column is missing.")

    # Card: Total Order Quantity
    with col2:
        if 'Order quantities' in df.columns:
            total_order_quantity = df['Order quantities'].sum()
            st.markdown(
                f"""
                <div style="background-color: #f0f2f6; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                    <h2 style="font-size: 24px; color: #333;">📦 Total Order Quantity</h2>
                    <h1 style="font-size: 36px; color: #2b8c42;">{total_order_quantity:,}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("The 'Order quantities' column is missing.")

    # Card: Total Availability
    with col3:
        if 'Stock levels' in df.columns:
            total_availability = df['Stock levels'].sum()
            st.markdown(
                f"""
                <div style="background-color: #f0f2f6; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                    <h2 style="font-size: 24px; color: #333;">📊 Total Availability</h2>
                    <h1 style="font-size: 36px; color: #2b8c42;">{total_availability:,}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("The 'Stock levels' column is missing.")

# Add space above the collapsible section
st.markdown("<br><br>", unsafe_allow_html=True)  # Adds space above the summary
# Display the dataset and summary text
with st.expander("📋 Show Summary"):
    st.write("""
    ### Supply Chain Summary

    #### 1. Overall Business Performance (KPIs)
    - The business has achieved **total revenue** of **₹577,604.82**, showcasing a robust financial performance.
    - **Order volumes** remain strong with a cumulative **4,922 orders**, reflecting sustained demand.
    - Product **availability levels** are healthy at **4,840 units**, ensuring readiness to meet market needs.

    #### 2. Operational Efficiency (Gauges)
    - **Stock levels** are maintained at a commendable **4,777 units**, ensuring smooth operations without overstocking.
    - **Lead times** average at **15.96 days**, indicating room for improvement to enhance customer satisfaction.

    #### 3. Product Performance
    - **Revenue by Product Type:**
        - **Skincare** is the top performer, generating **₹241,628.16** in revenue.
        - **Haircare** follows with **₹174,455.39**, while **Cosmetics** contribute **₹161,521.27**.
    - **Price vs. Cost with Profit Margins:**
        - **Cosmetics** lead profitability with an average margin of **₹14.31 per unit.**
        - **Haircare** and **Skincare** show slight losses, with margins of **- ₹2.44** and **- ₹1.73**, respectively, suggesting cost optimization opportunities.

    #### 4. Regional and Logistic Trends
    - **Revenue by Location:**
        - Mumbai and Kolkata emerge as the top contributors, earning **₹137,755.03** and **₹137,077.55**, respectively.
        - Bangalore, Chennai, and Delhi perform moderately, generating revenues between **₹81,027** and **₹119,143**.
    - **Order Quantities by Location:**
        - Highest orders come from **Kolkata (1,228)** and **Chennai (1,109)**, highlighting strong regional demand.
        - **Bangalore (769)** and **Delhi (733)** present opportunities for growth.
    - **Transportation Modes:**
        - **Road (1,386 orders)** and **Rail (1,342 orders)** dominate as the preferred transportation methods.
        - **Air (1,341 orders)** offers efficiency but might involve higher costs, while **Sea (853 orders)** has the lowest usage.

    #### 5. Cost Management and Quality Control
    - **Manufacturing Costs by Inspection Results:**
        - **Pending inspections** account for the largest costs (**₹1,785.07**), highlighting a need for process acceleration.
        - **Failed inspections** contribute **₹1,880.30**, pointing to quality assurance gaps.
    - **Cost by Supplier:**
        - **Supplier 1 (₹1,221.86)** and **Supplier 4 (₹1,128.78)** handle the bulk of costs, suggesting potential high-value partnerships.
        - **Supplier 3 (₹654.51)** incurs the least costs, indicating efficient operations.

    #### 6. Insights on Revenue vs. Costs
    - **Manufacturing Costs and Revenue Relationship:**
        - Higher revenues correlate with moderate manufacturing costs, with outliers at both extremes.
        - Balancing cost control and revenue generation remains critical for profitability.
    """)

# Create two columns for the two gauges side by side
gauge_col1, gauge_col2 = st.columns(2)

# Plot 1: Total Stock Levels
if 'Stock levels' in df.columns:
    total_stock_levels = df['Stock levels'].sum()

    fig_stock_levels = go.Figure(go.Indicator(
        mode="number+gauge",
        value=total_stock_levels,
        gauge={
            'axis': {'range': [0, total_stock_levels * 1.2]},
            'bar': {'color': "rgba(31, 119, 180, 0.8)"},
            'steps': [
                {'range': [0, total_stock_levels / 2], 'color': "lightgray"},
                {'range': [total_stock_levels / 2, total_stock_levels], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': total_stock_levels
            }
        }
    ))

    fig_stock_levels.update_layout(
        title={'text': "Current Stock Levels", 'font': {'size': 20}},
        font=dict(size=18, color='white'),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    gauge_col1.plotly_chart(fig_stock_levels, key="stock_levels_chart")
else:
    gauge_col1.warning("The 'Stock levels' column is missing.")

# Plot 2: Total Lead Times
if 'Lead times' in df.columns:
    total_lead_times = df['Lead times'].sum()

    fig_lead_times = go.Figure(go.Indicator(
        mode="number+gauge",
        value=total_lead_times,
        gauge={
            'axis': {'range': [0, total_lead_times * 1.2]},
            'bar': {'color': "rgba(180, 119, 31, 0.8)"},
            'steps': [
                {'range': [0, total_lead_times / 2], 'color': "lightgray"},
                {'range': [total_lead_times / 2, total_lead_times], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': total_lead_times
            }
        }
    ))

    fig_lead_times.update_layout(
        title={'text': "Current Lead Times", 'font': {'size': 20}},
        font=dict(size=18, color='white'),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    gauge_col2.plotly_chart(fig_lead_times, key="lead_times_chart")
else:
    gauge_col2.warning("The 'Lead times' column is missing.")

# New Row for Revenue and Manufacturing Costs
col1, col2 = st.columns(2)

# Plot: Relationship between Manufacturing Costs and Revenue Generated
with col1:
    if 'Manufacturing costs' in df.columns and 'Revenue generated' in df.columns:
        fig_relationship = px.scatter(
            df,
            x='Manufacturing costs',
            y='Revenue generated',
            title='Relationship between Manufacturing Costs and Revenue Generated',
            labels={
                'Manufacturing costs': 'Manufacturing Costs ($)',
                'Revenue generated': 'Revenue Generated ($)'
            },
            color='Product type' if 'Product type' in df.columns else None,
            size='Revenue generated',
            hover_data=['Product type'] if 'Product type' in df.columns else None
        )

        fig_relationship.update_layout(
            xaxis_title="Manufacturing Costs ($)",
            yaxis_title="Revenue Generated ($)",
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )

        fig_relationship.update_traces(marker=dict(opacity=0.8))

        col1.plotly_chart(fig_relationship)
    else:
        col1.warning("The 'Manufacturing costs' or 'Revenue generated' columns are missing.")

# Plot: Revenue Generated by Product Type
with col2:
    if 'Product type' in df.columns and 'Revenue generated' in df.columns:
        revenue_by_product = df.groupby('Product type').agg({'Revenue generated': 'sum'}).reset_index()
        fig_revenue_product = px.bar(
            revenue_by_product,
            x='Product type',
            y='Revenue generated',
            title='Revenue Generated by Product Type',
            labels={'Revenue generated': 'Total Revenue ($)', 'Product type': 'Product Type'}
        )

        fig_revenue_product.update_layout(
            xaxis_title="Product Type",
            yaxis_title="Total Revenue ($)",
            yaxis_tickprefix="$",
            yaxis_tickformat=".2f",
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            bargap=0,
            bargroupgap=0.1
        )

        fig_revenue_product.update_traces(marker=dict(color=['#813cf6', '#15abbd', '#df9def']))

        col2.plotly_chart(fig_revenue_product)
    else:
        col2.warning("The 'Product type' or 'Revenue generated' columns are missing.")


# Add Profit Margin Percentage column
df['Profit Margin (%)'] = ((df['Price'] - df['Manufacturing costs']) / df['Price']) * 100

# Create a layout with three columns
col1, col2, col3 = st.columns(3)

# Visualization 1: Revenue Distribution by Location (Pie Chart)
with col1:
    if 'Revenue generated' in df.columns and 'Location' in df.columns:
        fig1, ax1 = plt.subplots()

        custom_colors = ['#d62728', '#e33bc2', '#ff7f0e', '#1f77b4', '#2ca02c']  # Example custom colors
        ax1.pie(
            df.groupby('Location')['Revenue generated'].sum(),
            labels=df['Location'].unique(),
            autopct='%1.1f%%',
            colors=custom_colors[:len(df['Location'].unique())],
            textprops={'fontsize': 12, 'color': 'white'}
        )
        ax1.set_title("Revenue by Location", fontsize=16, color='white')
        fig1.patch.set_facecolor((0, 0, 0, 0))
        ax1.set_facecolor((0, 0, 0, 0))
        st.pyplot(fig1)
    else:
        st.warning("Required columns ('Revenue generated', 'Location') are missing.")

# Visualization 2: Distribution of Manufacturing Cost by Supplier (Pie Chart)
with col2:
    if 'Manufacturing costs' in df.columns and 'Supplier name' in df.columns:
        fig2, ax2 = plt.subplots()
        colors = sns.color_palette('Set2', len(df['Supplier name'].unique()))
        ax2.pie(
            df.groupby('Supplier name')['Manufacturing costs'].sum(),
            labels=df['Supplier name'].unique(),
            autopct='%1.1f%%',
            colors=colors,
            textprops={'fontsize': 12, 'color': 'white'}
        )
        ax2.set_title("Manufacturing Costs by Supplier", fontsize=16, color='white')
        fig2.patch.set_facecolor((0, 0, 0, 0))
        ax2.set_facecolor((0, 0, 0, 0))
        st.pyplot(fig2)
    else:
        st.warning("Required columns ('Manufacturing costs', 'Supplier name') are missing.")
# Visualization 3: Comparison of Price and Manufacturing Cost by Product Type (Bar Graph with Profit Margin)
# Visualization 3: Comparison of Price and Manufacturing Cost by Product Type (Bar Graph with Profit Margin)
with col3:
    if 'Price' in df.columns and 'Manufacturing costs' in df.columns and 'Product type' in df.columns:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        bar_width = 0.35
        product_types = df['Product type'].unique()
        x = range(len(product_types))

        # Calculate mean price, manufacturing cost, and profit margin
        price_aggregated = df.groupby('Product type')['Price'].mean()
        manufacturing_cost_aggregated = df.groupby('Product type')['Manufacturing costs'].mean()
        profit_margins = ((price_aggregated - manufacturing_cost_aggregated) / price_aggregated * 100).round(2)

        # Create bar chart for price and manufacturing cost
        ax3.bar(x, price_aggregated, width=bar_width, label='Price', color='blue')
        ax3.bar([i + bar_width for i in x], manufacturing_cost_aggregated, width=bar_width, label='Manufacturing Cost', color='orange')

        # Add profit margin text above the bars
        for i, profit in enumerate(profit_margins):
            ax3.text(i + bar_width / 2, price_aggregated[i] + 10, f'{profit:.1f}%', ha='center', fontsize=10, color='white')

        # Set x-axis labels and make them visible in white
        ax3.set_xticks([i + bar_width / 2 for i in x])
        ax3.set_xticklabels(product_types, rotation=45, fontsize=12, color='white')
        ax3.set_xlabel("Product Type", fontsize=14, color='white')
        ax3.set_ylabel("Cost / Price", fontsize=14, color='white')

        # Adjust the legend location and make it white
        ax3.legend(loc='upper left', fontsize=10, frameon=False, facecolor='black', edgecolor='white', labelcolor='white')
    
        # Remove gridlines and adjust background color for visibility
        ax3.grid(False)
        fig3.patch.set_facecolor((0, 0, 0, 0))
        ax3.set_facecolor((0, 0, 0, 0))
        
        # Make all text (axis values, labels) white
        for tick in ax3.get_xticklabels() + ax3.get_yticklabels():
            tick.set_color('white')

        st.pyplot(fig3)
    else:
        st.warning("Required columns ('Price', 'Manufacturing costs', 'Product type') are missing.")

# Adjusted layout with 3 visuals in 1 row for other visualizations
col1, col2, col3 = st.columns(3)  # Create 3 columns for side-by-side layout

# Plot 5: Manufacturing Costs by Inspection Results in col1
with col1:
    if 'Inspection results' in df.columns and 'Manufacturing costs' in df.columns:
        cost_summary = df.groupby('Inspection results').agg({'Manufacturing costs': 'sum'}).reset_index()

        total_costs = cost_summary['Manufacturing costs'].sum()

        cost_summary['Percentage Contribution'] = (cost_summary['Manufacturing costs'] / total_costs * 100).round(2)

        cost_summary['Manufacturing costs'] = cost_summary['Manufacturing costs'].astype(float).round(2)
        cost_summary['Percentage Contribution'] = cost_summary['Percentage Contribution'].astype(float).round(2)

        cost_summary = cost_summary.sort_values(by='Manufacturing costs', ascending=False)

        fig = px.pie(
            cost_summary,
            names='Inspection results',
            values='Manufacturing costs',
            title='Manufacturing Costs by Inspection Results',
            color_discrete_sequence=px.colors.sequential.Plasma  # Updated color scheme
        )

        fig.update_traces(
            hoverinfo='label+value+percent',
            textinfo='value+percent'
        )

        fig.update_layout(
            font=dict(size=14, color='white'),
            showlegend=True,
            legend_title_text='Inspection Results',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
        )

        st.plotly_chart(fig, key="cost_inspection_results")  # Add a unique key
    else:
        st.warning("The 'Inspection results' or 'Manufacturing costs' columns are missing.")

# Plot 6: Order Quantities by Location in col2
with col2:
    if 'Location' in df.columns and 'Order quantities' in df.columns:
        result = df.groupby('Location')['Order quantities'].sum().reset_index()

        result = result.sort_values(by='Order quantities', ascending=False)

        fig = px.bar(result, x='Location', y='Order quantities',
                     title='Order Quantities by Location',
                     labels={'Location': 'Location', 'Order quantities': 'Total Order Quantities'},
                     color='Location',
                     color_discrete_sequence=px.colors.qualitative.Set1,  # Updated color scheme
                    )

        fig.update_layout(
            xaxis_title="Location",
            yaxis_title="Total Order Quantities",
            font=dict(size=14, color='white'),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            bargap=0.1,
        )

        st.plotly_chart(fig, key="order_quantities_location")  # Add a unique key

# Total Order Quantities by Transportation Mode in col3
with col3:
    if 'Transportation modes' in df.columns and 'Order quantities' in df.columns:
        transport_data = df.groupby('Transportation modes')['Order quantities'].sum().reset_index()
        
        # Update the color_discrete_sequence to navy blue to light blue
        fig_transport = px.pie(
            transport_data,
            names='Transportation modes',
            values='Order quantities',
            title='Order Quantities by Transportation Mode',
            color_discrete_sequence=['#003366', '#3366CC', '#66CCFF']  # Navy blue to light blue color gradient
        )
        
        fig_transport.update_traces(textinfo='percent+label')
        fig_transport.update_layout(
            font=dict(size=14, color='white'),
            showlegend=True,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
        )
        
        st.plotly_chart(fig_transport, key="order_quantities_transportation_mode")  # Add a unique key

    else:
        st.warning("The 'Transportation modes' or 'Order quantities' columns are missing.")

