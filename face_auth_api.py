<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face Shield | Live Verification</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lucide/0.263.1/umd/lucide.min.js"></script>
</head>
<body class="bg-slate-50 min-h-screen font-sans text-slate-800">

    <nav class="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-50">
        <div class="max-w-4xl mx-auto px-4 h-16 flex items-center gap-2">
            <i data-lucide="scan-face" class="h-8 w-8 text-indigo-600"></i>
            <span class="font-bold text-xl tracking-tight">FaceShield Live</span>
        </div>
    </nav>

    <main class="max-w-4xl mx-auto px-4 py-8">
        
        <!-- Tabs -->
        <div class="flex gap-4 mb-6 border-b border-slate-200">
            <button onclick="setMode('register')" id="tab-register" class="pb-2 px-4 border-b-2 border-indigo-600 font-medium text-indigo-600 transition-all">Register New</button>
            <button onclick="setMode('verify')" id="tab-verify" class="pb-2 px-4 border-b-2 border-transparent text-slate-500 hover:text-slate-700 transition-all">Scan Face</button>
        </div>

        <div class="grid md:grid-cols-2 gap-8">
            
            <!-- Left: Input & Camera -->
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                    <h2 id="form-title" class="text-lg font-bold mb-4 text-slate-800">Register New User</h2>
                    
                    <div class="space-y-4">
                        <!-- ID Input (Only shown in Register Mode) -->
                        <div id="username-field">
                            <label class="block text-sm font-medium mb-1 text-slate-600">Full Name / ID</label>
                            <input type="text" id="username" class="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all" placeholder="Enter ID to register">
                        </div>

                        <!-- Camera Viewport -->
                        <div class="relative bg-black rounded-xl overflow-hidden aspect-[4/3] shadow-inner">
                            <video id="video-feed" autoplay playsinline muted class="w-full h-full object-cover transform -scale-x-100"></video>
                            <canvas id="canvas-capture" class="hidden"></canvas>
                            
                            <!-- Overlay Text -->
                            <div id="cam-overlay" class="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/70 to-transparent text-center">
                                <span class="text-xs text-white/80 font-medium">Camera Active</span>
                            </div>
                        </div>

                        <!-- Camera Controls -->
                        <div class="grid grid-cols-2 gap-2">
                            <button onclick="startCamera()" id="btn-start-cam" class="col-span-2 py-2.5 bg-slate-800 text-white rounded-lg text-sm font-medium hover:bg-slate-900 transition-colors flex justify-center items-center gap-2">
                                <i data-lucide="camera" class="w-4 h-4"></i> Start Camera
                            </button>
                            
                            <button onclick="manualCapture()" id="btn-capture" class="hidden col-span-2 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-bold hover:bg-indigo-700 transition-colors flex justify-center items-center gap-2">
                                <i data-lucide="aperture" class="w-4 h-4"></i> Freeze Frame
                            </button>
                        </div>

                        <button onclick="handleSubmit()" id="btn-action" class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg shadow-lg shadow-indigo-200 transition-all flex justify-center items-center gap-2 mt-2">
                            <span>Register User</span>
                            <i data-lucide="arrow-right" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Right: Results -->
            <div class="space-y-6">
                <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 h-full flex flex-col items-center justify-center text-center min-h-[400px]">
                    
                    <!-- Loader -->
                    <div id="loader" class="hidden flex flex-col items-center">
                        <div class="w-16 h-16 border-4 border-indigo-100 border-t-indigo-600 rounded-full animate-spin mb-4"></div>
                        <p class="text-indigo-600 font-semibold animate-pulse">Analyzing Biometrics...</p>
                        <p class="text-slate-400 text-xs mt-2">Matching against database</p>
                    </div>

                    <!-- Default / Result State -->
                    <div id="result-area" class="w-full">
                        <div class="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6 border border-slate-100">
                            <i data-lucide="scan-face" class="w-10 h-10 text-slate-300"></i>
                        </div>
                        <h3 class="text-slate-400 font-medium">Ready to Scan</h3>
                        <p class="text-slate-400 text-sm mt-2 max-w-xs mx-auto">Select a mode and take a photo to begin verification.</p>
                    </div>

                </div>
            </div>
        </div>

    </main>

    <script>
        lucide.createIcons();
        
        let currentMode = 'register';
        let capturedBlob = null;
        const video = document.getElementById('video-feed');
        const canvas = document.getElementById('canvas-capture');
        
        // Determine API URL
        const API_BASE = window.location.protocol === 'file:' ? 'http://127.0.0.1:8000' : '';

        // Initialize Camera on Load
        window.addEventListener('load', () => {
            startCamera();
        });

        function setMode(mode) {
            currentMode = mode;
            capturedBlob = null; // Reset capture
            
            const title = document.getElementById('form-title');
            const btnAction = document.getElementById('btn-action');
            const usernameField = document.getElementById('username-field');
            const tabReg = document.getElementById('tab-register');
            const tabVer = document.getElementById('tab-verify');

            if (mode === 'register') {
                title.innerText = 'Register New User';
                btnAction.querySelector('span').innerText = 'Save Identity';
                usernameField.classList.remove('hidden'); // Show Name Input
                
                tabReg.className = "pb-2 px-4 border-b-2 border-indigo-600 font-medium text-indigo-600 transition-all";
                tabVer.className = "pb-2 px-4 border-b-2 border-transparent text-slate-500 hover:text-slate-700 transition-all";
            } else {
                title.innerText = 'Identify Person';
                btnAction.querySelector('span').innerText = 'Scan & Identify';
                usernameField.classList.add('hidden'); // Hide Name Input
                
                tabVer.className = "pb-2 px-4 border-b-2 border-indigo-600 font-medium text-indigo-600 transition-all";
                tabReg.className = "pb-2 px-4 border-b-2 border-transparent text-slate-500 hover:text-slate-700 transition-all";
            }
            
            // Clear results
            resetResultUI();
        }

        function resetResultUI() {
            document.getElementById('result-area').innerHTML = `
                <div class="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6 border border-slate-100">
                    <i data-lucide="scan-face" class="w-10 h-10 text-slate-300"></i>
                </div>
                <h3 class="text-slate-400 font-medium">Ready to Scan</h3>
                <p class="text-slate-400 text-sm mt-2 max-w-xs mx-auto">Select a mode and take a photo to begin verification.</p>
            `;
            lucide.createIcons();
        }

        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                video.srcObject = stream;
                document.getElementById('btn-start-cam').classList.add('hidden');
                document.getElementById('btn-capture').classList.remove('hidden');
            } catch(err) {
                console.error(err);
                alert("Please allow camera access to use this app.");
            }
        }

        // Wrapper to trigger manual capture UI
        function manualCapture() {
            getSnapshot().then(() => {
                // Visual feedback only
                video.classList.add('opacity-50', 'scale-95');
                setTimeout(() => video.classList.remove('opacity-50', 'scale-95'), 200);
            });
        }

        // Returns a Promise that resolves with the blob
        function getSnapshot() {
            return new Promise((resolve, reject) => {
                if (!video.srcObject) {
                    reject("Camera not active");
                    return;
                }
                
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                
                canvas.toBlob(blob => {
                    capturedBlob = blob;
                    resolve(blob);
                }, 'image/jpeg');
            });
        }

        async function handleSubmit() {
            // Auto-capture if user hasn't manually frozen the frame
            if(!capturedBlob) {
                try {
                    await getSnapshot();
                } catch(e) {
                    return alert("Please ensure camera is running.");
                }
            }

            if(!capturedBlob) return alert("Failed to capture image.");

            const formData = new FormData();
            formData.append('file', new File([capturedBlob], "capture.jpg", { type: "image/jpeg" }));

            // Handle Register vs Verify Logic
            if(currentMode === 'register') {
                const username = document.getElementById('username').value;
                if(!username) return alert("Please enter a name to register this face.");
                formData.append('username', username);
            } 
            // In Verify mode, we don't append username. Backend handles 1:N search.

            // UI Loading
            document.getElementById('loader').classList.remove('hidden');
            document.getElementById('result-area').classList.add('hidden');

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
                // Optional: Clear capture after success to force new scan next time?
                // capturedBlob = null; 
            }
        }

        function renderError(msg) {
            const container = document.getElementById('result-area');
            container.innerHTML = `
                <div class="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i data-lucide="wifi-off" class="w-8 h-8 text-red-500"></i>
                </div>
                <h3 class="text-xl font-bold text-red-600">Connection Failed</h3>
                <p class="text-slate-500 text-sm mt-2">Is the server running?</p>
                <code class="text-xs bg-slate-100 p-2 rounded mt-4 block text-slate-500">${msg}</code>
            `;
            lucide.createIcons();
        }

        function renderResult(data, mode) {
            const container = document.getElementById('result-area');
            
            if(!data.status || data.status !== 'success') {
                // Error State
                container.innerHTML = `
                    <div class="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i data-lucide="alert-circle" class="w-8 h-8 text-red-500"></i>
                    </div>
                    <h3 class="text-lg font-bold text-red-600">Operation Failed</h3>
                    <p class="text-slate-600 mt-2">${data.detail || 'Unknown error occurred'}</p>
                `;
            } else if (mode === 'register') {
                // Registration Success
                container.innerHTML = `
                    <div class="w-20 h-20 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i data-lucide="user-check" class="w-8 h-8 text-green-600"></i>
                    </div>
                    <h3 class="text-xl font-bold text-green-600">Registered!</h3>
                    <p class="text-slate-600 mt-2">${data.message}</p>
                    <button onclick="setMode('verify')" class="mt-6 text-sm text-indigo-600 font-medium hover:underline">Try identifying now &rarr;</button>
                `;
            } else {
                // Verification/Identification Result
                const isMatch = data.match;
                const color = isMatch ? 'text-green-600' : 'text-red-500';
                const bg = isMatch ? 'bg-green-50' : 'bg-red-50';
                const icon = isMatch ? 'check-circle' : 'help-circle';
                const title = isMatch ? `Hello, ${data.username}!` : "Unknown Person";
                
                container.innerHTML = `
                    <div class="w-24 h-24 ${bg} rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce-short">
                        <i data-lucide="${icon}" class="w-10 h-10 ${color}"></i>
                    </div>
                    <h3 class="text-2xl font-bold ${color}">${title}</h3>
                    <div class="mt-4 flex justify-center gap-4 text-sm">
                        <div class="bg-slate-50 px-3 py-1 rounded border border-slate-100">
                            <span class="text-slate-400">Confidence</span>
                            <div class="font-semibold text-slate-700">${(data.similarity_score * 100).toFixed(1)}%</div>
                        </div>
                    </div>
                    ${!isMatch ? `<p class="text-slate-400 text-sm mt-4">Face not found in database.</p>` : ''}
                `;
            }
            lucide.createIcons();
        }
    </script>
    <style>
        .animate-bounce-short { animation: bounce-short 0.5s ease-out; }
        @keyframes bounce-short {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
    </style>
</body>
</html>
