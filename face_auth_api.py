<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face Shield | Live Verification</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lucide/0.263.1/umd/lucide.min.js"></script>
</head>
<body class="bg-gray-50 min-h-screen font-sans text-gray-800">

    <nav class="bg-white border-b shadow-sm sticky top-0 z-50">
        <div class="max-w-4xl mx-auto px-4 h-16 flex items-center gap-2">
            <i data-lucide="scan-face" class="h-8 w-8 text-blue-600"></i>
            <span class="font-bold text-xl">FaceShield Live</span>
        </div>
    </nav>

    <main class="max-w-4xl mx-auto px-4 py-8">
        
        <!-- Tabs -->
        <div class="flex gap-4 mb-6 border-b border-gray-200">
            <button onclick="setMode('register')" id="tab-register" class="pb-2 px-1 border-b-2 border-blue-600 font-medium text-blue-600">Register</button>
            <button onclick="setMode('verify')" id="tab-verify" class="pb-2 px-1 border-b-2 border-transparent text-gray-500 hover:text-gray-700">Verify</button>
        </div>

        <div class="grid md:grid-cols-2 gap-8">
            
            <!-- Left: Input & Camera -->
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-xl shadow-sm border">
                    <h2 id="form-title" class="text-lg font-bold mb-4">Register New User</h2>
                    
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium mb-1">Username</label>
                            <input type="text" id="username" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Enter ID">
                        </div>

                        <!-- Camera / Upload Toggle -->
                        <div class="flex gap-2 text-sm bg-gray-100 p-1 rounded-lg">
                            <button id="btn-src-file" onclick="toggleSource('file')" class="flex-1 py-1 rounded bg-white shadow text-blue-700 transition-all">Upload File</button>
                            <button id="btn-src-camera" onclick="toggleSource('camera')" class="flex-1 py-1 rounded text-gray-600 hover:bg-gray-200 transition-all">Use Camera</button>
                        </div>

                        <!-- File Input -->
                        <div id="source-file" class="block">
                            <input type="file" id="file-input" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100">
                        </div>

                        <!-- Camera Input -->
                        <div id="source-camera" class="hidden">
                            <div class="relative bg-black rounded-lg overflow-hidden aspect-video mb-2">
                                <video id="video-feed" autoplay playsinline muted class="w-full h-full object-cover transform -scale-x-100"></video>
                                <canvas id="canvas-capture" class="hidden"></canvas>
                            </div>
                            <button onclick="startCamera()" id="btn-start-cam" class="w-full py-2 bg-gray-800 text-white rounded-lg text-sm mb-2 hover:bg-gray-900 transition-colors">Start Camera</button>
                            <button onclick="capturePhoto()" id="btn-capture" class="hidden w-full py-2 bg-red-600 text-white rounded-lg text-sm font-bold hover:bg-red-700 transition-colors">Capture Photo</button>
                        </div>

                        <button onclick="handleSubmit()" id="btn-action" class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg shadow transition-all flex justify-center items-center gap-2">
                            <span>Submit</span>
                            <i data-lucide="arrow-right" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Right: Results -->
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-xl shadow-sm border h-full flex flex-col items-center justify-center text-center min-h-[300px]">
                    
                    <div id="loader" class="hidden flex flex-col items-center">
                        <div class="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
                        <p class="text-blue-600 font-medium">Processing Biometrics...</p>
                    </div>

                    <div id="result-area" class="w-full">
                        <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i data-lucide="image" class="w-8 h-8 text-gray-400"></i>
                        </div>
                        <h3 class="text-gray-400 font-medium">Results will appear here</h3>
                    </div>

                </div>
            </div>
        </div>

    </main>

    <script>
        lucide.createIcons();
        
        let currentMode = 'register';
        let currentSource = 'file';
        let capturedBlob = null;
        const video = document.getElementById('video-feed');
        const canvas = document.getElementById('canvas-capture');
        
        // Determine API URL (Handles local file opening vs server hosting)
        const API_BASE = window.location.protocol === 'file:' ? 'http://127.0.0.1:8000' : '';

        function setMode(mode) {
            currentMode = mode;
            document.getElementById('form-title').innerText = mode === 'register' ? 'Register New User' : 'Verify Identity';
            document.getElementById('btn-action').querySelector('span').innerText = mode === 'register' ? 'Save Identity' : 'Verify Access';
            
            // Tab styling
            document.getElementById('tab-register').className = mode === 'register' ? "pb-2 px-1 border-b-2 border-blue-600 font-medium text-blue-600" : "pb-2 px-1 border-b-2 border-transparent text-gray-500 hover:text-gray-700";
            document.getElementById('tab-verify').className = mode === 'verify' ? "pb-2 px-1 border-b-2 border-blue-600 font-medium text-blue-600" : "pb-2 px-1 border-b-2 border-transparent text-gray-500 hover:text-gray-700";
            
            // Clear results
            document.getElementById('result-area').innerHTML = `
                <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i data-lucide="image" class="w-8 h-8 text-gray-400"></i>
                </div>
                <h3 class="text-gray-400 font-medium">Results will appear here</h3>
            `;
            lucide.createIcons();
        }

        function toggleSource(source) {
            currentSource = source;
            const btnFile = document.getElementById('btn-src-file');
            const btnCam = document.getElementById('btn-src-camera');
            
            const activeClass = "bg-white shadow text-blue-700";
            const inactiveClass = "text-gray-600 hover:bg-gray-200";

            if(source === 'file') {
                document.getElementById('source-file').classList.remove('hidden');
                document.getElementById('source-camera').classList.add('hidden');
                
                // Update Button Styles
                btnFile.className = "flex-1 py-1 rounded " + activeClass;
                btnCam.className = "flex-1 py-1 rounded " + inactiveClass;

                stopCamera();
            } else {
                document.getElementById('source-file').classList.add('hidden');
                document.getElementById('source-camera').classList.remove('hidden');
                
                // Update Button Styles
                btnCam.className = "flex-1 py-1 rounded " + activeClass;
                btnFile.className = "flex-1 py-1 rounded " + inactiveClass;
            }
        }

        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
                document.getElementById('btn-start-cam').classList.add('hidden');
                document.getElementById('btn-capture').classList.remove('hidden');
            } catch(err) {
                alert("Could not access camera. Please allow camera permissions.");
                console.error(err);
            }
        }

        function stopCamera() {
            if(video.srcObject) {
                video.srcObject.getTracks().forEach(track => track.stop());
                video.srcObject = null;
                document.getElementById('btn-start-cam').classList.remove('hidden');
                document.getElementById('btn-capture').classList.add('hidden');
            }
        }

        function capturePhoto() {
            if (!video.srcObject) return;
            
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            
            canvas.toBlob(blob => {
                capturedBlob = blob;
                // Flash effect
                video.classList.add('opacity-50');
                setTimeout(() => video.classList.remove('opacity-50'), 200);
            }, 'image/jpeg');
        }

        async function handleSubmit() {
            const username = document.getElementById('username').value;
            if(!username) return alert("Enter a username");

            let fileToSend = null;
            if(currentSource === 'file') {
                fileToSend = document.getElementById('file-input').files[0];
            } else {
                if(!capturedBlob) return alert("Please capture a photo first");
                fileToSend = new File([capturedBlob], "capture.jpg", { type: "image/jpeg" });
            }

            if(!fileToSend) return alert("Select an image or capture photo");

            // UI Loading
            document.getElementById('loader').classList.remove('hidden');
            document.getElementById('result-area').classList.add('hidden');

            const formData = new FormData();
            formData.append('username', username);
            formData.append('file', fileToSend);

            const endpoint = currentMode === 'register' ? `${API_BASE}/register` : `${API_BASE}/verify`;

            try {
                const res = await fetch(endpoint, { method: 'POST', body: formData });
                const data = await res.json();
                renderResult(data, currentMode);
            } catch(err) {
                renderError(err.message);
            } finally {
                document.getElementById('loader').classList.add('hidden');
                document.getElementById('result-area').classList.remove('hidden');
            }
        }

        function renderError(msg) {
            const container = document.getElementById('result-area');
            container.innerHTML = `
                <div class="text-red-500 mb-2"><i data-lucide="alert-triangle" class="w-12 h-12 mx-auto"></i></div>
                <h3 class="text-xl font-bold text-red-600">Connection Failed</h3>
                <p class="text-gray-600 text-sm mt-2">Is the backend server running?</p>
                <p class="text-gray-400 text-xs mt-1">${msg}</p>
            `;
            lucide.createIcons();
        }

        function renderResult(data, mode) {
            const container = document.getElementById('result-area');
            
            if(!data.status || data.status !== 'success') {
                container.innerHTML = `
                    <div class="text-red-500 mb-2"><i data-lucide="alert-circle" class="w-12 h-12 mx-auto"></i></div>
                    <h3 class="text-xl font-bold text-red-600">Error</h3>
                    <p class="text-gray-600">${data.detail || 'Operation failed'}</p>
                `;
            } else if (mode === 'register') {
                container.innerHTML = `
                    <div class="text-green-500 mb-2"><i data-lucide="check-circle" class="w-12 h-12 mx-auto"></i></div>
                    <h3 class="text-xl font-bold text-green-600">Success</h3>
                    <p class="text-gray-600">${data.message}</p>
                `;
            } else {
                // Verify Result
                const color = data.match ? 'text-green-600' : 'text-red-600';
                const icon = data.match ? 'check-circle' : 'x-circle';
                container.innerHTML = `
                    <div class="${color} mb-2"><i data-lucide="${icon}" class="w-12 h-12 mx-auto"></i></div>
                    <h3 class="text-2xl font-bold ${color}">${data.match ? "MATCHED" : "NO MATCH"}</h3>
                    <p class="text-gray-500 font-medium mt-2">Similarity: ${(data.similarity_score * 100).toFixed(1)}%</p>
                    <p class="text-sm text-gray-400 mt-4">${data.message}</p>
                `;
            }
            lucide.createIcons();
        }
    </script>
</body>
</html>
