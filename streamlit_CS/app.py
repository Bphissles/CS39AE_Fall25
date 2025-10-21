import streamlit as st

st.set_page_config(
    page_title="My Streamlit Site",
    page_icon="📊",
    layout="wide"
)

st.title(" Welcome to My Streamlit Site")
st.markdown(
    """
    This is a three-page Streamlit app:
    - **Bio**: who I am
    - **Visualization**: a tiny interactive chart
    - **Pie Chart**: a pie chart visualization

    Use the left sidebar to switch pages.
    """
)

with st.expander("How this app is organized (for students)"):
    st.write(
        """
        - `app.py` is the entry point.
        - Pages live in the `/pages` folder and auto-appear in the sidebar.
        - Edit `pages/1_Bio.py` and `pages/2_Visualization.py` to complete the assignment.
        - `pages/3_Pie.py` is a pie chart visualization page.
        """
    )

st.caption("Built with Streamlit • Class template")
