console.log('🚀 Starting Emotion Tracker V2...');

import config from './config.js';

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
    // Replace video URL
    const videoSource = document.getElementById('videoSource');
    if (config.VIDEO_URL) {
      videoSource.src = config.VIDEO_URL;
      console.log('Video URL set to:', config.VIDEO_URL);
      
      // Force video to reload with new source
      this.videoPlayer.load();
    } else {
      console.error('No VIDEO_URL configured in config.js');
    }
    
    // Replace completion code
    const completionCodeElement = document.getElementById('completionCode');
    if (config.COMPLETION_CODE) {
      completionCodeElement.textContent = config.COMPLETION_CODE;
    }
    
    // Set privacy policy link
    const privacyLink = document.getElementById('privacyLink');
    if (config.PRIVACY_POLICY_URL) {
      privacyLink.href = config.PRIVACY_POLICY_URL;
      privacyLink.target = '_blank';
    } else {
      privacyLink.style.display = 'none';
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
    this.videoPlayer.addEventListener('loadedmetadata', () => {
      console.log('Video metadata loaded, duration:', this.videoPlayer.duration);
      this.setupVideoProgress();
    });

    this.videoPlayer.addEventListener('timeupdate', () => {
      this.updateProgress();
    });

    this.videoPlayer.addEventListener('ended', () => {
      this.onVideoEnded();
    });

    // Video error handling
    this.videoPlayer.addEventListener('error', (e) => {
      console.error('Video error:', e);
      this.showError('Video failed to load. Please check your internet connection and try again.');
    });

    this.videoPlayer.addEventListener('loadstart', () => {
      console.log('Video loading started');
    });

    this.videoPlayer.addEventListener('canplay', () => {
      console.log('Video can start playing');
    });

    this.videoPlayer.addEventListener('loadeddata', () => {
      console.log('Video data loaded');
    });

    // Prevent video manipulation
    this.videoPlayer.addEventListener('seeking', (e) => {
      if (this.isTracking) {
        e.preventDefault();
        this.videoPlayer.currentTime = this.videoPlayer.savedTime || 0;
      }
    });

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

    // Handle fullscreen changes
    const fullscreenEvents = [
      'fullscreenchange',
      'webkitfullscreenchange', 
      'mozfullscreenchange',
      'msfullscreenchange'
    ];

    fullscreenEvents.forEach(event => {
      document.addEventListener(event, () => {
        this.handleFullscreenChange();
      });
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
      console.error('Morphcast initialization failed:', error);
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
      this.showStep(3);
      
      // Show video and start tracking
      this.videoPlayer.style.display = 'block';
      this.isTracking = true;
      this.startTime = Date.now();
      
      // Start Morphcast tracking
      if (this.morphcastInstance) {
        await this.morphcastInstance.start();
      }
      
      // Enter fullscreen
      await this.enterFullscreen();
      
      // Start video playback
      await this.videoPlayer.play();
      
    } catch (error) {
      console.error('Error starting video:', error);
      this.showError('Failed to start video. Please try again.');
    }
  }

  async enterFullscreen() {
    try {
      if (this.videoPlayer.requestFullscreen) {
        await this.videoPlayer.requestFullscreen();
      } else if (this.videoPlayer.webkitRequestFullscreen) {
        await this.videoPlayer.webkitRequestFullscreen();
      } else if (this.videoPlayer.mozRequestFullscreen) {
        await this.videoPlayer.mozRequestFullscreen();
      } else if (this.videoPlayer.msRequestFullscreen) {
        await this.videoPlayer.msRequestFullscreen();
      }
    } catch (error) {
      console.warn('Fullscreen not supported or denied:', error);
    }
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
    } catch (error) {
      console.warn('Exit fullscreen failed:', error);
    }
  }

  handleFullscreenChange() {
    const isFullscreen = document.fullscreenElement || 
                        document.webkitFullscreenElement || 
                        document.mozFullScreenElement || 
                        document.msFullscreenElement;
    
    // If video is playing and user exits fullscreen, force back to fullscreen
    if (!isFullscreen && this.isTracking && !this.videoPlayer.paused && !this.videoPlayer.ended) {
      this.enterFullscreen();
    }
  }

  setupVideoProgress() {
    // Save current time periodically to prevent seeking
    this.progressInterval = setInterval(() => {
      if (!this.videoPlayer.seeking) {
        this.videoPlayer.savedTime = this.videoPlayer.currentTime;
      }
    }, 250);
  }

  updateProgress() {
    if (this.videoPlayer.duration && this.progressFill) {
      const progress = (this.videoPlayer.currentTime / this.videoPlayer.duration) * 100;
      this.progressFill.style.width = progress + '%';
    }
  }

  async onVideoEnded() {
    try {
      this.isTracking = false;
      
      // Stop tracking
      if (this.morphcastInstance) {
        await this.morphcastInstance.stop();
      }
      
      // Clear progress interval
      if (this.progressInterval) {
        clearInterval(this.progressInterval);
      }
      
      // Exit fullscreen
      await this.exitFullscreen();
      
      // Show processing step
      this.showStep(4);
      
      // Process and upload data
      await this.processAndUploadData();
      
    } catch (error) {
      console.error('Error processing video end:', error);
      this.showError('Failed to process your response. Please try again.');
    }
  }

  async processAndUploadData() {
    try {
      const sessionId = Date.now();
      const workerId = this.getWorkerId();
      
      // Create metadata
      const metadata = {
        sessionId: sessionId,
        workerId: workerId,
        taskId: config.TASK_ID,
        videoUrl: config.VIDEO_URL,
        totalFrames: this.trackingData.length,
        duration: this.videoPlayer.duration,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        screenResolution: `${screen.width}x${screen.height}`,
        viewport: `${window.innerWidth}x${window.innerHeight}`
      };

      // Prepare data for upload
      const trackingBlob = new Blob([JSON.stringify({
        trackingData: this.trackingData,
        metadata: metadata
      })], { type: 'application/json' });

      // Upload to Supabase
      const filename = `${config.TASK_ID}_${workerId}_${sessionId}.json`;
      
      await this.uploadWithRetry(trackingBlob, filename);
      
      // Show completion step
      this.showStep(5);
      
    } catch (error) {
      console.error('Upload failed:', error);
      this.showError('Failed to upload your response. Please check your internet connection and try again.');
    }
  }

  async uploadWithRetry(data, filename, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        const { data: uploadData, error } = await this.supabaseClient.storage
          .from('AROSUALDATA')
          .upload(filename, data, {
            cacheControl: '3600',
            contentType: 'application/json',
            upsert: true
          });

        if (error) throw error;
        return uploadData;
        
      } catch (error) {
        console.error(`Upload attempt ${i + 1} failed:`, error);
        if (i === maxRetries - 1) throw error;
        
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
      }
    }
  }

  getWorkerId() {
    // Try to get worker ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('workerId') || 
           urlParams.get('worker_id') || 
           urlParams.get('participantId') || 
           'anonymous_' + Date.now();
  }

  copyCompletionCode() {
    const codeElement = document.getElementById('completionCode');
    const text = codeElement.textContent;
    
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        this.showCopySuccess();
      }).catch(() => {
        this.fallbackCopyText(text);
      });
    } else {
      this.fallbackCopyText(text);
    }
  }

  fallbackCopyText(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
      document.execCommand('copy');
      this.showCopySuccess();
    } catch (err) {
      console.error('Copy failed:', err);
    }
    
    document.body.removeChild(textArea);
  }

  showCopySuccess() {
    const button = document.getElementById('copyCodeBtn');
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    button.style.background = '#4CAF50';
    
    setTimeout(() => {
      button.textContent = originalText;
      button.style.background = '';
    }, 2000);
  }

  showStep(stepNumber) {
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
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    this.showStep('error');
  }

  retry() {
    // Reset state
    this.trackingData = [];
    this.isTracking = false;
    this.startTime = null;
    
    // Reset video
    this.videoPlayer.currentTime = 0;
    this.videoPlayer.style.display = 'none';
    
    // Reset progress
    if (this.progressFill) {
      this.progressFill.style.width = '0%';
    }
    
    // Go back to step 1
    this.showStep(1);
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new EmotionTracker();
});

// Export for potential external use
window.EmotionTracker = EmotionTracker; 