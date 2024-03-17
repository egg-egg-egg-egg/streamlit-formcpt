import streamlit as st



with open("./README.md",encoding="utf-8") as f:
    readme_file = f.read()
st.write(readme_file)


from example1 import *

exmp1()