import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime
from streamlit_mic_recorder import mic_recorder

def real_calculator():
    st.markdown("""
        <style>
            .main > div {
                padding: 0 !important;
            }
            .split-screen {
                display: flex;
                height: 100vh;
            }
            .calculator-pane {
                width: 60%;
                padding: 20px;
                background: #f0f2f6;
            }
            .emergency-pane {
                width: 40%;
                padding: 20px;
                background: #ffebee;
                border-left: 3px solid #ff4444;
                display: none;
            }
            .emergency-visible {
                display: block !important;
                animation: slideIn 0.5s forwards;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); }
                to { transform: translateX(0); }
            }
            .stButton > button {
                width: 100%;
                height: 50px;
                font-size: 20px;
                border-radius: 10px;
                border: 2px solid #2d5f2d;
                background-color: #4CAF50;
                color: white !important;
                transition: 0.3s;
            }
            .stButton > button:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }
            .emotion-meter {
                background: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .police-message {
                background: #ffe6e6;
                border-left: 4px solid #ff4444;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                font-size: 0.9em;
            }
            .message-header {
                color: #ff4444;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .message-time {
                font-size: 0.8em;
                color: #666;
            }
            .audio-container {
                background: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "emergency" not in st.session_state:
        st.session_state.update({
            "emergency": False,
            "police_comms": [],
            "expression": "",
            "audio_data": None,
            "audio_analysis": None
        })

    # Split screen container
    st.markdown('<div class="split-screen">', unsafe_allow_html=True)
    
    # Left pane - Calculator
    with st.container():
        st.markdown('<div class="calculator-pane">', unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; margin-bottom: 20px;'>
                <h2>📟 Stealth Calculator</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.text_input("", value=st.session_state.expression, key="calc_display", disabled=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear"):
                st.session_state.expression = ""
        with col2:
            if st.button("="):
                try:
                    result = eval(st.session_state.expression)
                    st.session_state.expression = str(result)
                except:
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
                        st.session_state.expression = ""
                        st.session_state.emergency = True
                    else:
                        st.session_state.expression += char
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Right pane - Emergency UI
    with st.container():
        emergency_class = "emergency-pane emergency-visible" if st.session_state.emergency else "emergency-pane"
        st.markdown(f'<div class="{emergency_class}">', unsafe_allow_html=True)
        if st.session_state.emergency:
            st.error("🚨 EMERGENCY MODE ACTIVATED 🚨")
            
            # Voice recording section
            with st.expander("Voice Message to Police", expanded=True):
                st.write("**Record Emergency Message**")
                
                # Audio recorder component
                audio_data = mic_recorder(
                    start_prompt="🎤 Start Recording",
                    stop_prompt="⏹️ Stop Recording",
                    key="emergency_recorder"
                )
                
                # Store and analyze audio
                if audio_data and audio_data['bytes']:
                    st.session_state.audio_data = audio_data['bytes']
                    
                    with st.spinner("Analyzing voice message..."):
                        time.sleep(2)
                        st.session_state.audio_analysis = {
                            "Fear": np.random.randint(75, 95),
                            "Stress": np.random.randint(80, 95),
                            "Urgency": np.random.randint(85, 98),
                            "Calm": np.random.randint(5, 20)
                        }
                
                # Show analysis results
                if st.session_state.audio_analysis:
                    st.write("### Voice Analysis Results")
                    for emotion, value in st.session_state.audio_analysis.items():
                        st.markdown(f"""
                            <div class="emotion-meter">
                                <strong>{emotion}:</strong>
                                <progress value="{value}" max="100"></progress> {value}%
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Send button
                    if st.button("🚨 Send Voice Analysis to Police"):
                        lat, lon = np.random.uniform(-90, 90), np.random.uniform(-180, 180)
                        analysis_time = datetime.now().strftime("%H:%M:%S")
                        
                        new_msg = {
                            "time": analysis_time,
                            "content": f"""
                                <div>
                                    <strong>VOICE ANALYSIS ALERT:</strong>
                                    <ul>
                                        <li>📍 Location: {lat:.4f}°N, {lon:.4f}°E</li>
                                        <li>😨 Fear: {st.session_state.audio_analysis['Fear']}%</li>
                                        <li>😰 Stress: {st.session_state.audio_analysis['Stress']}%</li>
                                        <li>🚨 Urgency: {st.session_state.audio_analysis['Urgency']}%</li>
                                    </ul>
                                    <audio controls style="width: 100%; margin-top: 10px;">
                                        <source src="data:audio/wav;base64,{st.session_state.audio_data.decode('latin-1')}" type="audio/wav">
                                    </audio>
                                </div>
                            """
                        }
                        st.session_state.police_comms.append(new_msg)
                        st.success("Voice analysis sent to police!")
                        st.session_state.audio_data = None
                        st.session_state.audio_analysis = None
                        st.rerun()

            # Police communications
            with st.expander("Police Communications", expanded=True):
                st.subheader("Officer Dispatch Updates")
                
                for msg in st.session_state.police_comms:
                    st.markdown(f"""
                        <div class="police-message">
                            <div class="message-header">🚔 Emergency Alert</div>
                            <div class="message-time">{msg['time']}</div>
                            {msg['content']}
                        </div>
                    """, unsafe_allow_html=True)

            # Location tracking
            st.write("### Live Location Tracking")
            df = pd.DataFrame({
                'lat': [np.random.uniform(-90, 90)],
                'lon': [np.random.uniform(-180, 180)]
            })
            st.map(df)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.title("🔒 Stealth Emergency Interface")
    st.caption("Appears as normal calculator - Activates emergency features when 'q' is pressed")
    real_calculator()

if __name__ == "__main__":
    main()
