# Leisure Project to play scoundrel on webapp

import streamlit as st

# Inject CSS for a responsive grid
st.markdown("""
<style>
.button-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* force 2 per row */
    gap: 10px;
}
.button-grid > div {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Wrap each st.button in a div inside the grid
st.markdown('<div class="button-grid">', unsafe_allow_html=True)

with st.container():
    st.markdown('<div>', unsafe_allow_html=True)
    draw_pressed = st.button("🎴 Draw", key="draw_button", disabled=st.session_state.draw_used)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div>', unsafe_allow_html=True)
    confirm_pressed = st.button("✅ Confirm", key="confirm_button")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div>', unsafe_allow_html=True)
    skip_pressed = st.button("⏭️ Skip", key="skip_button")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div>', unsafe_allow_html=True)
    restart_pressed = st.button("🔄 Restart", key="restart_button")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)