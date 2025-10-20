import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title("🥧 Pie Chart Visualization")

st.markdown(
    """
    This page demonstrates a pie chart visualization using data from a CSV file.
    The chart shows the distribution of values across different categories.
    """
)

# Load the CSV file using absolute path
@st.cache_data
def load_pie_data():
    """Load pie chart data from CSV file in the data folder."""
    # Get absolute path to the data folder
    data_path = Path(__file__).parent.parent / "data" / "pie_demo.csv"
    try:
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        st.error(f"Could not find file at: {data_path}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the data
df = load_pie_data()

if df is not None:
    # Display the raw data
    with st.expander("📋 View Raw Data"):
        st.dataframe(df, use_container_width=True)
        st.write(f"**Total rows:** {len(df)}")
        st.write(f"**Columns:** {list(df.columns)}")
    
    # Add interactive controls
    st.markdown("### Chart Customization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Color scheme selector
        color_scheme = st.selectbox(
            "Color Scheme",
            options=["Plotly", "Viridis", "Plasma", "Inferno", "Magma", "Cividis"],
            index=0
        )
    
    with col2:
        # Display percentages toggle
        show_percentages = st.checkbox("Show Percentages", value=True)
    
    # Hole size slider for donut chart effect
    hole_size = st.slider(
        "Donut Hole Size (0 = full pie, 0.5 = donut)",
        min_value=0.0,
        max_value=0.5,
        value=0.0,
        step=0.05
    )
    
    # Create the pie chart
    st.markdown("### Distribution Chart")
    
    # Map color scheme names to plotly color sequences
    color_map = {
        "Plotly": px.colors.qualitative.Plotly,
        "Viridis": px.colors.sequential.Viridis,
        "Plasma": px.colors.sequential.Plasma,
        "Inferno": px.colors.sequential.Inferno,
        "Magma": px.colors.sequential.Magma,
        "Cividis": px.colors.sequential.Cividis
    }
    
    fig = px.pie(
        df,
        names="Category",
        values="Value",
        title="Distribution by Category",
        hole=hole_size,
        color_discrete_sequence=color_map[color_scheme]
    )
    
    # Update layout for better appearance
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label' if show_percentages else 'label',
        hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics section
    st.markdown("### 📊 Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Value", f"{df['Value'].sum()}")
    
    with col2:
        st.metric("Average Value", f"{df['Value'].mean():.2f}")
    
    with col3:
        st.metric("Categories", len(df))
    
    # Top category
    top_category = df.loc[df['Value'].idxmax()]
    st.info(f"🏆 **Top Category:** {top_category['Category']} with a value of {top_category['Value']}")
    
    # Help section
    with st.expander("ℹ️ How to use this chart"):
        st.write(
            """
            - **Pie/Donut Chart:** Shows the proportion of each category relative to the total
            - **Hover:** Move your mouse over slices to see detailed information
            - **Color Scheme:** Change the color palette using the dropdown menu
            - **Donut Hole Size:** Adjust the slider to create a donut chart effect
            - **Percentages:** Toggle to show/hide percentage labels on the chart
            - **Legend:** Click on legend items to show/hide specific categories
            """
        )

st.divider()
st.caption("Data loaded from `data/pie_demo.csv` • Edit `pages/3_Pie.py` to customize this page.")
