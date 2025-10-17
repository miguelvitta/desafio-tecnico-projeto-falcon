# FALCON Vision AI

FALCON Vision AI is a real-time computer vision application designed to detect and monitor people using a webcam feed. The system leverages the YOLOv8 object detection model and provides a dynamic web-based dashboard for visualizing analytics.

---

## How It Works

The application is built on a modular architecture, with three core Python scripts working together:

* **`app.py`**: This is the main entry point for the Streamlit web application. It handles the user interface, manages the application's state (e.g., whether the camera is running), and coordinates the other modules. It's responsible for displaying the live video feed and the analytics dashboard.

* **`vision.py`**: This script contains all the computer vision logic. It captures frames from the webcam, performs QR code detection for pausing/resuming the feed, and uses the pre-trained YOLO model to detect and track people. It then annotates the video frames with this information and returns the results to the main app.

* **`db.py`**: This module manages the SQLite database. It handles creating the database file and table, as well as logging all key events, such as application start/stop times and details from each person detection (like person count and dominant clothing color).

The workflow is straightforward: `app.py` runs a loop that continuously grabs frames from the webcam. Each frame is sent to `vision.py` for processing and AI analysis. The results and the annotated video frame are returned to `app.py` for display, while the analytical data is sent to `db.py` to be logged in the database.

---

## Challenge Requirements Fulfilled

This project successfully implements the core functional and technical requirements outlined in the "🧠 Desafio Técnico – FALCON Vision AI" document.

### Functional Requirements

* **Real-Time Person Detection & Tracking**: The application uses a YOLO model to detect and track people from a live webcam feed.
* **Event Timestamping**: It logs the timestamp for when individuals are detected.
* **Visual Characteristic Collection**: The system captures the dominant clothing color of detected individuals.
* **Interactive UI**: A Streamlit dashboard provides a real-time video feed and data visualizations.
* **QR Code Control**: Detection is stopped when a specific QR code is shown to the camera.
* **Data Visualization Dashboard**: The UI includes a dashboard with Plotly and Altair charts to filter and visualize statistics, avoiding basic chart types like pie charts as requested.

### Technical Requirements

* **Language**: The application is written entirely in **Python**.
* **AI Frameworks**: It utilizes **ultralytics** for the YOLO model and **opencv** for image processing.
* **UI Framework**: The user interface is built with **Streamlit**.
* **Local Storage**: Event data is stored locally in a **SQLite** database.

*Note: The integration with an LLM for a chat-based query interface is a planned feature for future development.*

---

## Requirements

* Python 3.10+
* The following Python libraries:
    * `streamlit`
    * `opencv-python`
    * `ultralytics`
    * `pandas`
    * `plotly`
    * `altair`
    * `qrcode` (for generating QR codes)

---

## Setup and Installation

### 1. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone [hhttps://github.com/miguelvitta/desafio-tecnico-projeto-falcon.git](https://github.com/miguelvitta/desafio-tecnico-projeto-falcon.git)
cd desafio-tecnico-projeto-falcon
```

### 2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

For Windows
```PowerShell

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```
For Linux / macOS
```Bash

# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 3. Install Dependencies
With your virtual environment active, install all the required packages using pip:

```Bash

pip install streamlit opencv-python ultralytics pandas plotly altair
```
Running the Application`
Once the setup is complete, you can run the application with a single command from your terminal:

```Bash

streamlit run app.py
```
The application will automatically open in a new tab in your default web browser.

---

## Utilities
The project includes utility scripts for maintenance and setup.

### Resetting the Database
If you need to wipe all logged data and start fresh, you can create and run a reset_db.py script with the following content:

```Python

from db import init_db
# This drops the events table and creates a new one.
init_db(recreate=True)
print("Database has been reset successfully.")
```
Run it from your terminal: 
```Python
python reset_db.py
```

### Generating QR Codes
To generate the necessary QR codes for controlling the application, you can create and run a generate_qr.py script:

```Python

import qrcode

def create_qr(data, filename):
    img = qrcode.make(data)
    img.save(filename)
    print(f"QR Code saved as {filename}")

# Create the QR code to stop the vision processing
create_qr("STOP_FALCON", "qr_stop_falcon.png")

# Create the QR code to resume the vision processing
create_qr("START_FALCON", "qr_start_falcon.png")
```

Run it from your terminal: 
```Python
python generate_qr.py.
```
This will save the .png files in your project directory.