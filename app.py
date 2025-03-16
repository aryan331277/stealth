import streamlit as st
import numpy as np

def real_calculator():
    st.markdown("""
        <style>
            .stButton > button {
                width: 100%;
                height: 50px;
                font-size: 20px;
                border-radius: 10px;
                border: none;
                background-color: #4CAF50;
                color: white;
                transition: 0.3s;
            }
            .stButton > button:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }
            .calculator-container {
                padding: 20px;
                border-radius: 15px;
                background-color: #f8f9fa;
                box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
                text-align: center;
            }
            .expression-box {
                font-size: 24px;
                padding: 10px;
                text-align: right;
                background-color: white;
                border-radius: 10px;
                box-shadow: inset 2px 2px 5px rgba(0,0,0,0.1);
                margin-bottom: 10px;
            }
        </style>
    
    <div class="calculator-container">
        <h2>Stealth Calculator</h2>
    </div>
    
    """, unsafe_allow_html=True)
    
    if "expression" not in st.session_state:
        st.session_state.expression = ""
    
    expression = st.text_input("", value=st.session_state.expression, key="expression")
    
    buttons = [
        ('7', '8', '9', '/'),
        ('4', '5', '6', '*'),
        ('1', '2', '3', '-'),
        ('0', '.', '=', '+')
    ]
    
    for row in buttons:
        cols = st.columns(4)
        for i, char in enumerate(row):
            if cols[i].button(char):
                if char == '=':
                    try:
                        result = eval(st.session_state.expression)
                        st.session_state.expression = str(result)
                    except:
                        st.error("Invalid Expression")
                elif char == 'q':
                    st.session_state.expression = ""
                    st.warning("Emergency Mode Activated!")
                else:
                    st.session_state.expression += char
                st.experimental_rerun()

def main():
    st.title("Stealth UI Demo")
    real_calculator()

if __name__ == "__main__":
    main()
