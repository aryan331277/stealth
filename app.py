import streamlit as st

def real_calculator():
    st.markdown("""
        <style>
            /* ... (keep existing styles the same) ... */
        </style>
    
    <div class="calculator-container">
        <h2>Stealth Calculator</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if "expression" not in st.session_state:
        st.session_state["expression"] = ""
    
    st.text_input("", value=st.session_state["expression"], key="expression_display", disabled=True)
    
    col1, col2 = st.columns(2)
    if col1.button("Clear"):
        st.session_state["expression"] = ""
    if col2.button("="):
        try:
            result = eval(st.session_state["expression"])
            st.session_state["expression"] = str(result)
        except Exception as e:
            st.error("Invalid Expression")
    
    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', 'q', '+')
    ]
    
    for row in buttons:
        cols = st.columns(4)
        for i, char in enumerate(row):
            if cols[i].button(char):
                if char == 'q':
                    st.session_state["expression"] = ""
                    st.warning("Emergency Mode Activated!")
                    st.success("Silent alert sent to nearby police officers! 🚨")
                else:
                    current_expr = st.session_state["expression"]
                    st.session_state["expression"] = current_expr + char

def main():
    st.title("Stealth UI Demo")
    real_calculator()

if __name__ == "__main__":
    main()
