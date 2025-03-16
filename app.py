import streamlit as st
import random
import numpy as np

def fake_tax_screenshot():
    return "Fake Tax Calculation: ₹{}".format(random.randint(1000, 99999))

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
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
            .calculator-container {
                padding: 20px;
                border-radius: 15px;
                background-color: #f8f9fa;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            }
        </style>
    
    <div class="calculator-container">
        <h3 style="text-align: center;">Real Calculator</h3>
    </div>
    
    """, unsafe_allow_html=True)
    
    expression = st.text_input("Enter expression:", key="expression")
    
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
                else:
                    st.session_state.expression += char
                st.experimental_rerun()

def emergency_ui():
    st.markdown("""
        <style>
            .emergency-container {
                padding: 20px;
                border-radius: 15px;
                background-color: #ffdddd;
                box-shadow: 2px 2px 10px rgba(255,0,0,0.2);
            }
        </style>
    
    <div class="emergency-container">
        <h3 style="text-align: center; color: red;">Emergency Mode</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Fake Tax Calculation Screenshot:")
    st.info(fake_tax_screenshot())
    st.button("Trigger SOS Alert", help="Send an emergency alert!")

def main():
    st.title("Stealth UI Demo")
    mode = st.radio("Select Mode", ["Real Calculator", "Emergency Mode"], horizontal=True)
    
    if mode == "Real Calculator":
        real_calculator()
    else:
        emergency_ui()

if __name__ == "__main__":
    main()

