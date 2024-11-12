import streamlit as st
import pandas as pd


st.set_page_config(
   page_title="About me!"
)

st.markdown("# A little about me!")

# Container for General info
with st.container(border=True):
   # Two columns
   # First column is 30% the space of the container and contains the image
   # Second column is 70% the space of the container and contains the text
   col1, col2 = st.columns([0.3, 0.7])

   with col1:
      st.image("Data\\Images\\axel.jpg", use_container_width=True)

   with col2:
      image_info = '''Hey there! This is me, Axel. I am a software engineer with a passion for system architecture and large scale problems. I am currently a student
       at the University of San Diego, getting a **Masters in Applied Artificial Intelligence**! I enjoy the challenges that come with creating *Reliable*, *Scalable* and *Maintainable* systems.
       I love the process of improving and getting better at something!'''

      st.markdown(image_info)


# Define tabs for second block
tab1, skill_tab, achievment_tab = st.tabs(["Education", "Skills", "Achievments"])

with tab1:
   # Container for education
   with st.container(border=True):
      st.header("Education")
      df = pd.read_csv("Data\School\education.csv")

      st.dataframe(data=df, hide_index=True)

with skill_tab:
   with st.container(border=True):
      st.header("Skills")
      languages, libraries, soft_skills = st.columns([1,1,1])

      with languages:
         st.subheader("Programming Languages")
         languages_data = '''- Python
- MySQL
- C
- C++
- Java
- Powershell'''
         st.markdown(languages_data)
      
      with libraries:
         st.subheader("Libraries")
         libraries_data = '''- Pandas
- PyTorch
- Swagger
- Matplotlib
- Transformers
- Scikit-learn'''
         st.markdown(libraries_data)

      with soft_skills:
         st.subheader("Other Skills")
         other_skills_data = '''- Amazon Web Services
- Jenkins
- Docker
- REST API
- git
- Agile'''
         st.markdown(other_skills_data)


with achievment_tab:
   with st.container(border=True):
      st.header("Random things about me")
      st.subheader("Competitive game Achievments")
      games_info = '''- **Apex Legends**, Masters, Top 2%
- **Chess puzzles**, ~2000 elo, Top 7%
- **Valorant**, Ascendant, Top 6%
- **Fortnite**, Champion 3, Highest rank
- **Overwatch**, Masters, Top 10%
- **League of Legends**, Platinum, Top 13%
         '''
      st.markdown(games_info)

      st.subheader("Fun Facts")
      facts_info = '''- Bilingual native proficiency in both English and French
- Black Belt in Tang Soo Do karate'''
      st.markdown(facts_info)


# Links container
with st.container(border=True):
   st.subheader("Links!")
   st.page_link("https://www.linkedin.com/in/axel-magret-488a42171/", label="LinkedIn", icon="💻", help="Lets connect!")
   st.page_link("https://open.spotify.com/user/axelmagret", label="Spotify", icon="🎧", help="Some of the music I like!")