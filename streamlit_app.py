import streamlit as st

# Create pages as well as set up navigation
home_page = st.Page("home.py", title="Home!", icon=":material/home:")
about_me_page = st.Page("about_me.py", title="About Me!", icon=":material/person:")
airbnb_dashboard_page = st.Page("airbnb_dashboard.py", title="Dashboard")

# Sets up navigation between pages
pg = st.navigation([home_page, about_me_page, airbnb_dashboard_page])
pg.run()