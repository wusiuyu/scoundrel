# Leisure Project to play scoundrel on webapp

import streamlit as st

st.markdown("""
<style>
.button-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
}
.button-row button {
    width: 100%;
    height: 50px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# Wrap buttons in a grid container
st.markdown('<div class="button-row">', unsafe_allow_html=True)

draw_pressed = st.button("🎴 Draw", key="draw_button")
confirm_pressed = st.button("✅ Confirm", key="confirm_button")
skip_pressed = st.button("⏭️ Skip", key="skip_button")
restart_pressed = st.button("🔄 Restart", key="restart_button")

st.markdown('</div>', unsafe_allow_html=True)