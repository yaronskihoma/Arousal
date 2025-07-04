console.log('🚀 Starting Emotion Tracker V2...');

class EmotionTracker {
  constructor() {
    console.log('🎯 Initializing EmotionTracker class...');
    this.supabaseClient = null;
    this.morphcastInstance = null;
    this.trackingData = [];
    this.currentStep = 1;
    this.videoPlayer = null;
    this.progressFill = null;
    this.isTracking = false;
    this.startTime = null;
    
    console.log('🔄 Starting initialization...');
    this.init();
  }

  init() {
    console.log('🔧 Initializing Emotion Tracker components...');
    
    try {
      // Initialize Supabase client
      console.log('💾 Initializing Supabase client...');
      if (typeof supabase !== 'undefined') {
        const { createClient } = supabase;
        this.supabaseClient = createClient(config.SUPABASE_URL, config.SUPABASE_KEY);
        console.log('✅ Supabase client initialized');
      } else {
        console.error('❌ Supabase library not loaded');
      }
      
      // Get DOM elements
      console.log('🎨 Getting DOM elements...');
      this.videoPlayer = document.getElementById('videoPlayer');
      this.progressFill = document.getElementById('progressFill');
      
      if (!this.videoPlayer) {
        console.error('❌ Video player element not found');
      } else {
        console.log('✅ Video player element found');
      }
      
      // Set up event listeners
      console.log('👂 Setting up event listeners...');
      this.setupEventListeners();
      
      // Initialize Morphcast
      console.log('🧠 Initializing Morphcast...');
      this.initializeMorphcast();
      
      // Set replaceable content
      console.log('🔄 Setting up replaceable content...');
      this.setupReplacableContent();
      
      console.log('✅ Emotion Tracker initialization complete');
      
    } catch (error) {
      console.error('❌ Error during initialization:', error);
    }
  }

  setupReplacableContent() {
    // Set video source
    const videoSource = document.getElementById('videoSource');
    if (videoSource && config.VIDEO_URL) {
      videoSource.src = config.VIDEO_URL;
      console.log('📹 Video source set to:', config.VIDEO_URL);
      
      // Force video to reload
      this.videoPlayer.load();
    }

    // Set completion code
    const completionCodeElement = document.getElementById('completionCode');
    if (completionCodeElement) {
      completionCodeElement.textContent = config.COMPLETION_CODE;
    }

    // Set privacy policy link
    const privacyLink = document.getElementById('privacyLink');
    if (privacyLink && config.PRIVACY_POLICY_URL) {
      privacyLink.href = config.PRIVACY_POLICY_URL;
    }
  }

  setupEventListeners() {
    console.log('🎯 Setting up event listeners...');
    
    // Camera permission button
    const allowCameraBtn = document.getElementById('allowCameraBtn');
    if (allowCameraBtn) {
      console.log('✅ Allow camera button found, adding click listener');
      allowCameraBtn.addEventListener('click', () => {
        console.log('🎬 Camera permission button clicked');
        this.requestCameraAccess();
      });
    } else {
      console.error('❌ Allow camera button not found');
    }

    // Start video button
    const startVideoBtn = document.getElementById('startVideoBtn');
    if (startVideoBtn) {
      console.log('✅ Start video button found');
      startVideoBtn.addEventListener('click', () => {
        console.log('▶️ Start video button clicked');
        this.startVideo();
      });
    } else {
      console.error('❌ Start video button not found');
    }

    // Copy code button
    const copyCodeBtn = document.getElementById('copyCodeBtn');
    if (copyCodeBtn) {
      copyCodeBtn.addEventListener('click', () => {
        console.log('📋 Copy code button clicked');
        this.copyCompletionCode();
      });
    }

    // Retry button
    const retryBtn = document.getElementById('retryBtn');
    if (retryBtn) {
      retryBtn.addEventListener('click', () => {
        console.log('🔄 Retry button clicked');
        this.retry();
      });
    }

    // Video events
    if (this.videoPlayer) {
      this.videoPlayer.addEventListener('ended', () => {
        console.log('🎬 Video ended');
        this.onVideoEnded();
      });

      // Video error handling
      this.videoPlayer.addEventListener('error', (e) => {
        console.error('❌ Video error:', e);
        this.showError('Video failed to load. Please check your internet connection and try again.');
      });

      this.videoPlayer.addEventListener('loadstart', () => {
        console.log('📹 Video loading started');
      });

      this.videoPlayer.addEventListener('canplay', () => {
        console.log('✅ Video can start playing');
      });

      this.videoPlayer.addEventListener('loadeddata', () => {
        console.log('📊 Video data loaded');
      });

      // Prevent video manipulation
      this.videoPlayer.addEventListener('seeking', (e) => {
        if (this.isTracking) {
          e.preventDefault();
          this.videoPlayer.currentTime = this.videoPlayer.savedTime || 0;
        }
      });
    }

    // Prevent keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (this.isTracking && (
        e.code === 'Space' || 
        e.code === 'ArrowLeft' || 
        e.code === 'ArrowRight' || 
        e.code === 'Escape'
      )) {
        e.preventDefault();
      }
    });

    // Prevent page unload during tracking
    window.addEventListener('beforeunload', (e) => {
      if (this.isTracking) {
        e.preventDefault();
        e.returnValue = '';
        return '';
      }
    });
  }

  async initializeMorphcast() {
    try {
      console.log('🧠 Initializing Morphcast...');
      console.log('🔑 License key present:', config.MORPHCAST_LICENSE ? 'YES' : 'NO');
      console.log('🏗️ SDK available:', typeof CY !== 'undefined' ? 'YES' : 'NO');
      
      if (!config.MORPHCAST_LICENSE) {
        console.error('❌ Morphcast license key not configured');
        throw new Error('Morphcast license key not configured');
      }

      // Check if CY (Morphcast) is available
      if (typeof CY === 'undefined') {
        console.error('❌ Morphcast SDK not loaded - CY is undefined');
        console.log('🔍 Available globals:', Object.keys(window).filter(key => key.includes('CY') || key.includes('morphcast')));
        throw new Error('Morphcast SDK not loaded');
      }

      const morphcastLoader = CY.loader()
        .licenseKey(config.MORPHCAST_LICENSE)
        .addModule(CY.modules().FACE_AROUSAL_VALENCE.name, { smoothness: 0.70 })
        .addModule(CY.modules().FACE_EMOTION.name, { smoothness: 0.40 })
        .addModule(CY.modules().FACE_ATTENTION.name, { smoothness: 0.83 })
        .addModule(CY.modules().FACE_DETECTOR.name, { maxInputFrameSize: 320, smoothness: 0.83 })
        .addModule(CY.modules().ALARM_NO_FACE.name, { timeWindowMs: 10000, initialToleranceMs: 7000, threshold: 0.75 })
        .addModule(CY.modules().DATA_AGGREGATOR.name, { initialWaitMs: 2000, periodMs: 1000 });

      console.log('📦 Loading Morphcast modules...');
      const { start, stop } = await morphcastLoader.load();
      this.morphcastInstance = { start, stop };
      
      console.log('✅ Morphcast initialized successfully');
      console.log('🎯 Start function available:', typeof start === 'function');
      console.log('🛑 Stop function available:', typeof stop === 'function');
      
      // Set up Morphcast event listeners
      console.log('👂 Setting up Morphcast event listeners...');
      this.setupMorphcastEvents();
      
    } catch (error) {
      console.error('❌ Morphcast initialization failed:', error);
      this.showError('Failed to initialize emotion tracking. Please check your license key and try again.');
    }
  }

  setupMorphcastEvents() {
    // Arousal and Valence tracking
    window.addEventListener(CY.modules().FACE_AROUSAL_VALENCE.eventName, (evt) => {
      if (this.isTracking) {
        this.trackingData.push({
          mediaTime: this.videoPlayer.currentTime,
          timestamp: Date.now() - this.startTime,
          type: 'FACE_AROUSAL_VALENCE',
          valence: evt.detail.output.valence,
          arousal: evt.detail.output.arousal
        });
      }
    });

    // Emotion tracking
    window.addEventListener(CY.modules().FACE_EMOTION.eventName, (evt) => {
      if (this.isTracking) {
        this.trackingData.push({
          mediaTime: this.videoPlayer.currentTime,
          timestamp: Date.now() - this.startTime,
          type: 'FACE_EMOTION',
          dominantEmotion: evt.detail.output.dominantEmotion,
          emotions: evt.detail.output.emotion
        });
      }
    });

    // Attention tracking
    window.addEventListener(CY.modules().FACE_ATTENTION.eventName, (evt) => {
      if (this.isTracking) {
        this.trackingData.push({
          mediaTime: this.videoPlayer.currentTime,
          timestamp: Date.now() - this.startTime,
          type: 'FACE_ATTENTION',
          attention: evt.detail.output.attention
        });
      }
    });

    // Face detector
    window.addEventListener(CY.modules().FACE_DETECTOR.eventName, (evt) => {
      if (this.isTracking) {
        this.trackingData.push({
          mediaTime: this.videoPlayer.currentTime,
          timestamp: Date.now() - this.startTime,
          type: 'FACE_DETECTOR',
          totalFaces: evt.detail.totalFaces,
          status: evt.detail.status
        });
      }
    });
  }

  async requestCameraAccess() {
    console.log('🎬 Starting camera access request...');
    
    try {
      // Check if getUserMedia is supported
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error('❌ getUserMedia is not supported in this browser');
        this.showError('Your browser does not support camera access. Please use a modern browser.');
        return;
      }
      
      console.log('🔍 Requesting camera permission...');
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      console.log('✅ Camera permission granted');
      
      // Stop the stream immediately as we only needed permission
      stream.getTracks().forEach(track => {
        console.log('🛑 Stopping camera track:', track.kind);
        track.stop();
      });
      
      console.log('➡️ Moving to step 2...');
      this.showStep(2);
      
    } catch (error) {
      console.error('❌ Camera access denied:', error);
      console.error('Error name:', error.name);
      console.error('Error message:', error.message);
      
      let errorMessage = 'Camera access is required for this study. Please allow camera access and try again.';
      
      if (error.name === 'NotAllowedError') {
        errorMessage = 'Camera access was denied. Please click the camera icon in your browser address bar and allow camera access.';
      } else if (error.name === 'NotFoundError') {
        errorMessage = 'No camera found. Please make sure you have a camera connected.';
      } else if (error.name === 'NotReadableError') {
        errorMessage = 'Camera is already in use by another application.';
      }
      
      this.showError(errorMessage);
    }
  }

  async startVideo() {
    try {
      console.log('▶️ Starting video...');
      this.showStep(3);
      
      // Show video and start tracking
      this.videoPlayer.style.display = 'block';
      this.isTracking = true;
      this.startTime = Date.now();
      
      // Start Morphcast tracking
      if (this.morphcastInstance) {
        console.log('🧠 Starting Morphcast tracking...');
        await this.morphcastInstance.start();
      }
      
      // Enter fullscreen
      console.log('🔳 Attempting fullscreen...');
      await this.enterFullscreen();
      
      // Start video playback
      console.log('🎬 Starting video playback...');
      await this.videoPlayer.play();
      
    } catch (error) {
      console.error('❌ Error starting video:', error);
      this.showError('Failed to start video. Please try again.');
    }
  }

  async enterFullscreen() {
    try {
      if (this.videoPlayer.requestFullscreen) {
        await this.videoPlayer.requestFullscreen();
      } else if (this.videoPlayer.webkitRequestFullscreen) {
        await this.videoPlayer.webkitRequestFullscreen();
      } else if (this.videoPlayer.mozRequestFullScreen) {
        await this.videoPlayer.mozRequestFullScreen();
      } else if (this.videoPlayer.msRequestFullscreen) {
        await this.videoPlayer.msRequestFullscreen();
      }
      console.log('✅ Fullscreen enabled');
    } catch (error) {
      console.warn('⚠️ Fullscreen not available:', error);
      // Continue without fullscreen
    }
  }

  async onVideoEnded() {
    console.log('🎬 Video ended, processing data...');
    this.isTracking = false;
    
    // Stop Morphcast tracking
    if (this.morphcastInstance && this.morphcastInstance.stop) {
      await this.morphcastInstance.stop();
      console.log('🛑 Morphcast tracking stopped');
    }
    
    // Exit fullscreen
    await this.exitFullscreen();
    
    // Show processing step
    this.showStep(4);
    
    // Process and upload data
    await this.processAndUploadData();
  }

  async exitFullscreen() {
    try {
      if (document.exitFullscreen) {
        await document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        await document.webkitExitFullscreen();
      } else if (document.mozCancelFullScreen) {
        await document.mozCancelFullScreen();
      } else if (document.msExitFullscreen) {
        await document.msExitFullscreen();
      }
      console.log('✅ Exited fullscreen');
    } catch (error) {
      console.warn('⚠️ Could not exit fullscreen:', error);
    }
  }

  async processAndUploadData() {
    try {
      console.log('📊 Processing tracking data...');
      console.log('📈 Data points collected:', this.trackingData.length);
      
      // Generate worker ID
      const workerId = this.getWorkerId();
      console.log('👤 Worker ID:', workerId);
      
      // Prepare data for upload
      const uploadData = {
        taskId: config.TASK_ID,
        workerId: workerId,
        timestamp: new Date().toISOString(),
        videoUrl: config.VIDEO_URL,
        trackingData: this.trackingData,
        metadata: {
          userAgent: navigator.userAgent,
          duration: this.trackingData.length > 0 ? Math.max(...this.trackingData.map(d => d.timestamp)) : 0,
          videoLength: this.videoPlayer.duration || 0
        }
      };
      
      // Upload to Supabase
      if (this.supabaseClient) {
        console.log('☁️ Uploading to Supabase...');
        const { data, error } = await this.supabaseClient
          .from('emotion_tracking_data')
          .insert([uploadData]);
        
        if (error) {
          throw error;
        }
        
        console.log('✅ Data uploaded successfully');
      } else {
        console.warn('⚠️ Supabase not available, data not uploaded');
      }
      
      // Show completion
      this.showStep(5);
      
    } catch (error) {
      console.error('❌ Error processing data:', error);
      this.showError('Failed to upload your data. Please try again.');
    }
  }

  getWorkerId() {
    // Try to get worker ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const workerId = urlParams.get('worker_id') || urlParams.get('workerId') || urlParams.get('PROLIFIC_PID') || 'unknown_worker';
    return workerId;
  }

  copyCompletionCode() {
    const code = config.COMPLETION_CODE;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(code).then(() => {
        console.log('📋 Code copied to clipboard');
        this.showCopySuccess();
      }).catch(err => {
        console.error('❌ Failed to copy code:', err);
        this.fallbackCopyText(code);
      });
    } else {
      this.fallbackCopyText(code);
    }
  }

  fallbackCopyText(text) {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.width = '2em';
    textArea.style.height = '2em';
    textArea.style.padding = '0';
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';
    textArea.style.background = 'transparent';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
      document.execCommand('copy');
      console.log('📋 Code copied using fallback method');
      this.showCopySuccess();
    } catch (err) {
      console.error('❌ Fallback copy failed:', err);
      alert('Please manually copy this code: ' + text);
    }
    
    document.body.removeChild(textArea);
  }

  showCopySuccess() {
    const copyBtn = document.getElementById('copyCodeBtn');
    if (copyBtn) {
      const originalText = copyBtn.textContent;
      copyBtn.textContent = 'Copied!';
      copyBtn.style.background = '#28a745';
      
      setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.background = '#4CAF50';
      }, 2000);
    }
  }

  showStep(stepNumber) {
    console.log('📄 Showing step:', stepNumber);
    
    // Hide all steps
    const steps = document.querySelectorAll('.step');
    steps.forEach(step => step.classList.remove('active'));
    
    // Show target step
    const targetStep = document.getElementById(`step${stepNumber}`);
    if (targetStep) {
      targetStep.classList.add('active');
      this.currentStep = stepNumber;
    }
  }

  showError(message) {
    console.error('💥 Error:', message);
    
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
      errorMessage.textContent = message;
    }
    
    this.showStep('error');
  }

  retry() {
    console.log('🔄 Retrying...');
    
    // Reset tracking
    this.isTracking = false;
    this.trackingData = [];
    
    // Stop Morphcast if running
    if (this.morphcastInstance && this.morphcastInstance.stop) {
      this.morphcastInstance.stop();
    }
    
    // Reset video
    if (this.videoPlayer) {
      this.videoPlayer.pause();
      this.videoPlayer.currentTime = 0;
      this.videoPlayer.style.display = 'none';
    }
    
    // Go back to step 1
    this.showStep(1);
  }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
  console.log('📄 DOM loaded, initializing app...');
  window.emotionTracker = new EmotionTracker();
}); 