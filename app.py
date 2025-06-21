import os
import cv2
import numpy as np
import insightface
import warnings
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import base64
from PIL import Image
import io

# --- Suppress Warnings ---
warnings.filterwarnings("ignore", category=FutureWarning)

# --- Initial Flask and SocketIO App Setup ---
app = Flask(__name__)
# The secret key is needed for session management
app.config['SECRET_KEY'] = 'mysecretkey!'
socketio = SocketIO(app)

# --- Global Variables and Constants ---
MODEL_NAME = "buffalo_l"
THRESHOLD = 0.7
DB_DIR = "live_face_db"
os.makedirs(DB_DIR, exist_ok=True)
# A dictionary to hold session data (embeddings and frames) for each user
SESSIONS = {}

# --- Initialize InsightFace Model (do this once) ---
print("Loading InsightFace model...")
# REMINDER: Remove 'CUDAExecutionProvider' if you don't have an NVIDIA GPU
face_app = insightface.app.FaceAnalysis(name=MODEL_NAME, providers=['CUDAExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))
print("InsightFace model loaded.")


# --- Core Logic Functions (Adapted from your script) ---

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6)

def save_session_data(session_id, name):
    """Saves unique embeddings and corresponding face images for a session."""
    if session_id not in SESSIONS or not SESSIONS[session_id]['embeddings']:
        print(f"No data to save for session {session_id}")
        return 0

    session_embeddings = SESSIONS[session_id]['embeddings']
    session_frames = SESSIONS[session_id]['frames']

    person_dir = os.path.join(DB_DIR, name)
    os.makedirs(person_dir, exist_ok=True)

    # Find unique embeddings and their corresponding frames
    unique_indices = []
    unique_embeddings = []
    for i, emb in enumerate(session_embeddings):
        is_unique = True
        for u_emb in unique_embeddings:
            if cosine_sim(emb, u_emb) > THRESHOLD:
                is_unique = False
                break
        if is_unique:
            unique_embeddings.append(emb)
            unique_indices.append(i)
    
    # Save the unique embeddings and images
    existing_files = len(os.listdir(person_dir)) // 2 # Each face has a .npy and .jpg
    for i, unique_idx in enumerate(unique_indices):
        emb_path = os.path.join(person_dir, f"{name}_{existing_files + i}.npy")
        img_path = os.path.join(person_dir, f"{name}_{existing_files + i}.jpg")
        
        np.save(emb_path, session_embeddings[unique_idx])
        cv2.imwrite(img_path, session_frames[unique_idx])

    print(f"Saved {len(unique_indices)} unique faces for '{name}'")
    return len(unique_indices)


# --- Flask Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')


# --- SocketIO Event Handlers ---

@socketio.on('connect')
def handle_connect():
    """A new user connects. Create a session for them."""
    session_id = request.sid
    SESSIONS[session_id] = {'name': '', 'embeddings': [], 'frames': []}
    print(f"Client connected: {session_id}")

@socketio.on('disconnect')
def handle_disconnect():
    """A user disconnects. Clean up their session data."""
    session_id = request.sid
    if session_id in SESSIONS:
        del SESSIONS[session_id]
    print(f"Client disconnected: {session_id}")

@socketio.on('frame')
def handle_frame(data):
    """Receives a video frame from the client."""
    session_id = request.sid
    
    # Decode the base64 image
    image_data = base64.b64decode(data['image'].split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Process frame with insightface
    faces = face_app.get(frame)

    if faces:
        socketio.emit('status', {'message': f'Face Detected! ({len(SESSIONS[session_id]["embeddings"])} collected)'}, room=session_id)
        for face in faces:
            SESSIONS[session_id]['embeddings'].append(face.embedding)
            # Crop the face from the frame for saving
            bbox = face.bbox.astype(int)
            face_crop = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            SESSIONS[session_id]['frames'].append(face_crop)
    else:
        socketio.emit('status', {'message': 'Searching for face...'}, room=session_id)

@socketio.on('save')
def handle_save(data):
    """Handles the save request from the client."""
    session_id = request.sid
    name = data.get('name', 'unknown')
    if not name.strip():
        socketio.emit('status', {'message': 'Error: Name cannot be empty.'}, room=session_id)
        return

    num_saved = save_session_data(session_id, name)
    
    # Clear session data after saving
    SESSIONS[session_id]['embeddings'] = []
    SESSIONS[session_id]['frames'] = []
    
    socketio.emit('status', {'message': f'Success! Saved {num_saved} unique faces for {name}. Ready for new registration.'}, room=session_id)

@socketio.on('discard')
def handle_discard(data):
    """Handles the discard request from the client."""
    session_id = request.sid
    # Just clear the temporary data
    SESSIONS[session_id]['embeddings'] = []
    SESSIONS[session_id]['frames'] = []
    socketio.emit('status', {'message': 'Session discarded. Ready for new registration.'}, room=session_id)
    print(f"Session discarded for {session_id}")


# --- Main Execution ---
if __name__ == '__main__':
    print("Starting Flask server...")
    # Use eventlet as the server to support WebSockets efficiently
    socketio.run(app, host='0.0.0.0', port=5000)