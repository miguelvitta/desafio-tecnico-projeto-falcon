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

## Features

* **Real-Time Person Detection**: Utilizes the YOLOv8 model to detect and track people in a live webcam stream.
* **Event Logging**: All key events, such as application start/stop and person detections, are logged to a local SQLite database for persistence.
* **QR Code Control**: The camera feed can be stopped by showing a specific QR code to the camera.
* **Interactive Dashboard**: A web interface built with Streamlit displays the live camera feed and an analytics dashboard with charts and filterable data.

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

---

## Setup and Installation

### 1. Clone the Repository

First, clone this repository to your local machine.

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
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