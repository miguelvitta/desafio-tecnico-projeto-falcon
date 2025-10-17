import streamlit as st
import cv2
from vision import process_frame, model
from db import log_event
import pandas as pd
import time

st.title("Falcon Vision AI Dashboard")

# Initialize state
if 'pause' not in st.session_state:
    st.session_state['pause'] = False
    st.session_state['persons_count'] = 0
    st.session_state['running'] = False

frame_placeholder = st.empty()

# Control Buttons
if st.button("Start") and not st.session_state['running']:
    st.session_state['running'] = True
    st.session_state['pause'] = False
if st.button("Resume") and st.session_state['pause']:
    st.session_state['pause'] = False
    log_event("resume", {"reason": "UI button"})
    st.success("Process was resumed")
if st.button("Stop"):
    st.session_state['running'] = False
    st.session_state['pause'] = True

# Vision Loop
cap = None
try:
    if st.session_state['running'] and not st.session_state['pause']:
        if cap is None or not cap.isOpened():
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Error when opening the webcam.")
                st.session_state['running'] = False
                raise Exception("Webcam not available.")
        
        ret, frame = cap.read()
        if ret:
            annotated_frame, persons_count, details, updated_pause = process_frame(frame, st.session_state['pause'])
            st.session_state['persons_count'] = persons_count
            st.session_state['pause'] = updated_pause
            if details:
                log_event("detection", details)
            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            st.rerun()
        else:
            st.error("Failure when capturing frame.")
            st.session_state['running'] = False
except Exception as e:
    st.error(f"Error when processing: {e}")
finally:
    if cap is not None:
        cap.release()

st.header("Dashboard")
try:
    df = pd.read_sql_query("SELECT * FROM events LIMIT 100", "sqlite:///data/events.db")
    if df.empty:
        st.warning("No data in the database.")
    else:
        event_types = ['all'] + df['event_type'].unique().tolist()
        selected_event = st.selectbox("Filter by type of Event", event_types, index=0)
        if selected_event == "all":
            filtered_df = df
        else:
            filtered_df = df[df['event_type'] == selected_event]
        st.dataframe(filtered_df)
        st.metric("People Detected", st.session_state['persons_count'])
except pd.io.sql.DatabaseError:
    st.error("Error in connecting with the database. Verify data/events.db")
except Exception as e:
    st.error(f"Error when loading data: {e}")
