import streamlit as st
import cv2
from vision import process_frame
from db import log_event, init_db
import pandas as pd
import plotly.express as px
import json
import altair as alt

# --- Database Initialization ---
# Ensures the database and table exist before the app runs.
init_db()

# --- Page Configuration ---
# Sets the browser tab title, icon, and layout for the application.
st.set_page_config(
    page_title="Falcon Vision AI",
    page_icon="🦅",
    layout="wide"
)

st.title("🦅 Falcon Vision AI Dashboard")

# --- Session State Initialization ---
# Initializes session state variables to track the camera's running status.
if 'running' not in st.session_state:
    st.session_state.running = False
    st.session_state.persons_count = 0

# --- Sidebar Controls ---
# Defines the control buttons in the sidebar to start and stop the camera feed.
st.sidebar.header("🎥 Controls")
if st.sidebar.button("Start Camera", type="primary", width='stretch', disabled=st.session_state.running):
    st.session_state.running = True
    log_event("start", {"reason": "UI button"})
    st.rerun()

if st.sidebar.button("Stop Camera", width='stretch', disabled=not st.session_state.running):
    st.session_state.running = False
    log_event("stop", {"reason": "UI button"})
    st.rerun()

# --- Video Feed Placeholder ---
# Creates an empty container in the UI that will be updated with live video frames.
frame_placeholder = st.empty()

# --- Main Vision Loop ---
# Captures frames from the webcam and processes them if the 'running' state is True.
if st.session_state.running:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
        st.session_state.running = False
    else:
        while st.session_state.running:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture frame from webcam.")
                st.session_state.running = False
                break
            
            current_pause_status = st.session_state.get('pause_status', False)
            annotated_frame, persons_count, details, updated_pause = process_frame(frame, current_pause_status)
            
            st.session_state.persons_count = persons_count
            st.session_state.pause_status = updated_pause

            if details:
                log_event("detection", details)
            
            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", width='stretch')

            if updated_pause and not current_pause_status:
                st.info("💡 Camera stopped by QR Code.")
                st.session_state.running = False

    if 'cap' in locals() and cap.isOpened():
        cap.release()

# --- Analytics Dashboard Section ---
# Renders the data visualization components below the video feed.
st.divider()
st.header("📊 Analytics Dashboard")

try:
    # Loads event data from the SQLite database into a pandas DataFrame.
    conn_str = "sqlite:///data/events.db"
    df = pd.read_sql_query("SELECT * FROM events ORDER BY timestamp DESC LIMIT 200", conn_str)
    
    if df.empty:
        st.warning("No event data in the database yet.")
    else:
        # Defines the layout for metrics and the data table.
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Current People Detected", st.session_state.persons_count)
            event_types = ['all'] + df['event_type'].unique().tolist()
            selected_event = st.selectbox("Filter by Event Type", event_types)

        with col2:
            st.info("The dashboard shows the latest 200 events recorded.")
            filtered_df = df if selected_event == "all" else df[df['event_type'] == selected_event]
            st.dataframe(filtered_df, width='stretch')

        # Prepares the data and generates charts for detection trends.
        detection_df = df[df['event_type'] == 'detection'].copy()
        if not detection_df.empty:
            st.subheader("Detection Trends")
            
            detection_df['timestamp'] = pd.to_datetime(detection_df['timestamp'])
            details_df = detection_df['details'].apply(lambda d: pd.Series(json.loads(d) if d else {}))
            detection_df = pd.concat([detection_df.drop('details', axis=1), details_df], axis=1)

            fig = px.line(detection_df, x='timestamp', y='persons_count', title='People Detected Over Time')
            st.plotly_chart(fig, use_container_width=True)

            color_df = detection_df.dropna(subset=['dominant_color'])
            chart = alt.Chart(color_df).mark_bar().encode(
                x=alt.X('dominant_color:N', title='Dominant Color'),
                y=alt.Y('count():Q', title='Detection Count'),
                tooltip=['dominant_color', 'count()']
            ).properties(title='Frequency of Dominant Colors Detected').interactive()
            st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"Error loading dashboard data: {e}")