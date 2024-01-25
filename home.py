import streamlit as st 
from PIL import Image

st.set_page_config(page_title='home')

imagePath = r'images/analysis.png'

st.sidebar.image(Image.open(imagePath))
