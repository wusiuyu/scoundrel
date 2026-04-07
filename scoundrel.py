# Leisure Project to play scoundrel on webapp
# streamlit run "C:\Projects\Project 038 Scoundrel\src\scoundrel - test.py"

import streamlit as st

col1, col2 = st.columns([1,1])
with col1:
    st.button("🎴 Draw", key="draw_button")
with col2:
    st.button("✅ Confirm", key="confirm_button")