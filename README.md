# 🎭 FaceFolio

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FaceFolio** is a web application for interactively creating high-quality facial datasets. It leverages a live camera feed and the powerful InsightFace model to capture and curate unique facial profiles, ready for use in any downstream computer vision application.

<br>

## 📸 Demo

*(**Pro Tip:** Record a short GIF of you using the application and replace this image. Use a tool like [ScreenToGif](https://www.screentogif.com/) or [Kap](https://getkap.co/). A GIF is the best way to showcase your project!)*

  <!-- This is a placeholder GIF, replace it with your own! -->

<br>

## 🌟 Core Features

*   **✨ Interactive Web UI:** A modern, responsive interface built with HTML, CSS, and JavaScript allows for easy name input and live video capture directly from the browser.
*   **🧠 Real-Time Face Analysis:** Utilizes the state-of-the-art **InsightFace** library on the server to perform robust face detection and embedding extraction on the fly.
*   **💎 Unique Embedding Curation:** Intelligently calculates cosine similarity between facial vectors to ensure only new, unique poses are saved. This prevents data redundancy and dramatically improves dataset quality.
*   **🗂️ Structured Dataset Output:** Saves data in a clean, organized format. Each subject gets their own folder containing their unique facial embeddings (`.npy` files) and the corresponding cropped face images (`.jpg` files).
*   **🔌 Real-Time Communication:** Built with a reliable **Flask-SocketIO** backend for seamless, low-latency communication between the client and server.

<br>

## 🛠️ Tech Stack

| Component | Technology                                                              |
| :-------- | :---------------------------------------------------------------------- |
| **Backend** | Python, Flask, Flask-SocketIO, InsightFace, OpenCV, NumPy, Eventlet     |
| **Frontend**| HTML5, CSS3, Vanilla JavaScript                                         |
| **Real-time**| WebSockets                                                              |

<br>

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

*   Python 3.9 or higher
*   `pip` package manager
*   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Ronin-117/FaceFolio.git
    cd FaceFolio
    ```

2.  **Create and activate a virtual environment (recommended):**
    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

<br>

## ▶️ How to Run the Application

1.  **Start the Flask server:**
    ```bash
    python app.py
    ```
    The server will start, and you will see output indicating that the InsightFace model is loading. Once ready, it will be running on `http://127.0.0.1:5000`.

2.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

3.  **(Optional) Expose to the public with ngrok:**
    To test on other devices (like your phone) or share with a friend, use `ngrok` to create a secure public URL.
    ```bash
    ngrok http 5000
    ```
    Use the `https://...` URL provided by `ngrok`.

<br>

## 🔧 How to Use

1.  **Enter a Name:** Type the name of the person whose face you are registering into the input box.
2.  **Start Recording:** Click the "Start Recording" button and grant the browser permission to use your camera.
3.  **Capture Poses:** Move your head around (up, down, left, right, tilted) to capture a variety of unique angles. The status message will update you on the progress.
4.  **Save or Discard:**
    *   Click **Save Session** to process the captured frames, save the unique embeddings and images to the server, and prepare for a new registration.
    *   Click **Discard Session** to clear the captured data for the current session without saving.

<br>

## 📂 Project Structure

```
FaceFolio/
│
├── app.py                  # Main Flask application, SocketIO events, and InsightFace logic
├── requirements.txt        # Python dependencies
│
├── static/                 # All static files (CSS, JS, images)
│   ├── style.css           # Custom styles for the frontend
│   └── script.js           # Frontend JavaScript for camera access and SocketIO communication
│
├── templates/              # HTML templates
│   └── index.html          # The main (and only) HTML page for the application
│
└── live_face_db/           # Auto-generated directory to store the final datasets
    └── subject_name/       # Each subject gets their own folder
        ├── subject_name_0.jpg
        ├── subject_name_0.npy
        └── ...
```

<br>

## ✨ Future Improvements

*   **Recognition Mode:** Add a new page/mode to use the created datasets for real-time face recognition.
*   **Dataset Gallery:** Create a simple gallery page to view the subjects and the captured images in the database.
*   **Configuration UI:** Allow users to adjust parameters like the similarity `THRESHOLD` from the web interface.

<br>

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.