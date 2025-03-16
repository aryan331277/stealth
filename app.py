import streamlit as st
import random

def fake_tax_screenshot():
    return "Fake Tax Calculation: ₹{}".format(random.randint(1000, 99999))

def real_calculator():
    st.write("### Real Calculator")
    expression = st.text_input("Enter expression:")
    if st.button("Calculate"):
        try:
            result = eval(expression)
            st.success(f"Result: {result}")
        except:
            st.error("Invalid Expression")

def emergency_ui():
    st.write("### Emergency Mode")
    st.write("Fake Tax Calculation Screenshot:")
    st.info(fake_tax_screenshot())
    st.button("Trigger SOS Alert")

def main():
    st.title("Stealth UI Demo")
    mode = st.radio("Select Mode", ["Real Calculator", "Emergency Mode"])
    
    if mode == "Real Calculator":
        real_calculator()
    else:
        emergency_ui()

if __name__ == "__main__":
    main()
