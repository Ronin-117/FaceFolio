document.addEventListener('DOMContentLoaded', () => {
    // Connect to the WebSocket server
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Get HTML elements
    const video = document.getElementById('video');
    const nameInput = document.getElementById('nameInput');
    const startBtn = document.getElementById('startBtn');
    const saveBtn = document.getElementById('saveBtn');
    const discardBtn = document.getElementById('discardBtn');
    const statusDiv = document.getElementById('status');
    const controlsDiv = document.getElementById('controls');
    const sessionControlsDiv = document.getElementById('sessionControls');

    let stream;
    let frameInterval;

    // --- Socket.IO Event Listeners ---
    socket.on('connect', () => {
        console.log('Connected to server!');
        statusDiv.textContent = 'Connected. Ready to start.';
    });

    socket.on('status', (data) => {
        console.log('Status update:', data.message);
        statusDiv.textContent = data.message;
        // If save/discard was successful, reset the UI
        if (data.message.includes('Success!') || data.message.includes('discarded')) {
            stopRecording();
        }
    });

    // --- Button Event Handlers ---
    startBtn.addEventListener('click', startRecording);
    saveBtn.addEventListener('click', saveSession);
    discardBtn.addEventListener('click', discardSession);

    // --- Core Functions ---
    async function startRecording() {
        if (!nameInput.value.trim()) {
            alert('Please enter a name first.');
            return;
        }

        // Get camera access
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        } catch (err) {
            console.error("Error accessing camera: ", err);
            statusDiv.textContent = 'Error: Could not access camera.';
            return;
        }

        // Hide start controls, show session controls
        controlsDiv.style.display = 'none';
        sessionControlsDiv.style.display = 'block';
        statusDiv.textContent = 'Recording started. Move your head around.';

        // Send frames to the server every 500ms
        frameInterval = setInterval(() => {
            sendFrame();
        }, 500); // Send a frame twice a second
    }

    function stopRecording() {
        clearInterval(frameInterval);
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        video.srcObject = null;
        controlsDiv.style.display = 'block';
        sessionControlsDiv.style.display = 'none';
    }

    function sendFrame() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convert the canvas image to a Base64 string
        const data = canvas.toDataURL('image/jpeg', 0.8);
        
        // Send the frame over the WebSocket
        socket.emit('frame', { image: data });
    }

    function saveSession() {
        statusDiv.textContent = 'Saving... Please wait.';
        socket.emit('save', { name: nameInput.value.trim() });
    }

    function discardSession() {
        socket.emit('discard', {});
        statusDiv.textContent = 'Discarding session...';
        // The server will send a status update to confirm and reset the UI
    }
});