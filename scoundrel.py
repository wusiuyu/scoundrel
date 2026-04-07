# Leisure Project to play scoundrel on webapp

import streamlit as st

# CSS grid for two-per-row layout
st.markdown("""
<style>
.button-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}
.button-grid button {
    width: 100%;
    height: 50px;
    font-size: 16px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Render HTML buttons
clicked = st.session_state.get("clicked", "")
st.markdown(f"""
<div class="button-grid">
    <button onclick="fetch('/?clicked=draw')">🎴 Draw</button>
    <button onclick="fetch('/?clicked=confirm')">✅ Confirm</button>
    <button onclick="fetch('/?clicked=skip')">⏭️ Skip</button>
    <button onclick="fetch('/?clicked=restart')">🔄 Restart</button>
</div>
""", unsafe_allow_html=True)

# Then check st.query_params or st.session_state["clicked"]