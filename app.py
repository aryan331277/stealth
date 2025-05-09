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
                gap: 10px;
            }
            .calculator-pane {
                width: 60%;
                padding: 20px;
                background: #f0f2f6;
                border-radius: 15px;
            }
            .emergency-pane {
                width: 40%;
                padding: 20px;
                background: #ffd4d4;
                border-left: 3px solid #ff4444;
                display: none;
                border-radius: 15px;
                box-shadow: -5px 0 15px rgba(255,0,0,0.1);
            }
            .emergency-visible {
                display: block !important;
                animation: slideIn 0.5s forwards;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .stButton > button {
                width: 100%;
                height: 60px;
                font-size: 24px;
                border-radius: 12px;
                border: 2px solid #2d5f2d;
                background-color: #4CAF50;
                color: white !important;
                transition: all 0.2s;
                margin: 2px;
            }
            .stButton > button:hover {
                background-color: #45a049;
                transform: scale(1.05);
                box-shadow: 0 3px 8px rgba(0,0,0,0.2);
            }
            .stButton > button:focus {
                background-color: #3d8b40;
            }
            .calculator-display {
                font-size: 32px;
                padding: 15px;
                text-align: right;
                background-color: #ffffff;
                border-radius: 12px;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
                margin-bottom: 15px;
                border: 2px solid #cccccc;
            }
            .police-message {
                background: #ffe6e6;
                border-left: 4px solid #ff4444;
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
                font-size: 0.95em;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .message-header {
                color: #ff4444;
                font-weight: 700;
                margin-bottom: 8px;
                font-size: 1.1em;
            }
            .message-time {
                font-size: 0.85em;
                color: #666;
                margin-bottom: 5px;
            }
            .emotion-meter {
                background: #ffffff;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .emotion-meter progress {
                width: 100%;
                height: 20px;
                border-radius: 10px;
                overflow: hidden;
            }
            .emotion-meter progress::-webkit-progress-bar {
                background-color: #eee;
                border-radius: 10px;
            }
            .emotion-meter progress::-webkit-progress-value {
                background-color: #ff4444;
                border-radius: 10px;
            }
            .emergency-alert {
                color: #ff4444;
                font-size: 1.5em;
                font-weight: 700;
                text-align: center;
                margin: 15px 0;
                animation: pulse 1s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            .section-title {
                color: #333;
                font-size: 1.3em;
                font-weight: 600;
                margin: 15px 0 10px;
                border-bottom: 2px solid #ff4444;
                padding-bottom: 5px;
            }
                    .emotion-meter {
            background: #ffffff;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            color: #000000; /* Force black text */
        }
        .emotion-meter strong {
            color: #000000 !important; /* Ensure emotion labels are black */
        }
        .emotion-meter progress {
            width: 100%;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
        }
        .emotion-meter progress::-webkit-progress-bar {
            background-color: #eee;
            border-radius: 10px;
        }
        .emotion-meter progress::-webkit-progress-value {
            background-color: #ff4444;
            border-radius: 10px;
        }
        .emotion-meter div {
            color: #000000 !important; /* Ensure percentage text is black */
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
