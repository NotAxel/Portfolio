import streamlit as st

# Configures the default settings of the page
st.set_page_config(
    page_title="Hello", # Title in tab at top of browser
    page_icon=":material/home:", # Icon in top of browser
)



general_info  = '''My name is Titouan Axel Magret, but everyone calls me Axel. I am a software engineer with a passion for system architecture and large scale problems.
 In this streamlit webpage you the will find information about me personally and professionally, as well as a number of projects. 
'''

st.title("Welcome to my portfolio!")
st.markdown('''# Who am I?''')
st.markdown(general_info)