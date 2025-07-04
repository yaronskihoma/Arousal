/**
 * Configuration file for Emotion Tracking V2
 * 
 * This configuration now supports URL parameters for dynamic video and completion code assignment:
 * - Use: yourapp.com/?video=video1&code=ABC123
 * - Fallback values are used for testing without parameters
 */

console.log('🔧 Loading Emotion Tracking V2 Configuration...');

// Function to get URL parameters
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Video URLs mapping
const VIDEO_URLS = {
    'video1': 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/f4bea092-1f69-4f99-8d7a-fc8fb52ac610/CAY_R91_V1_WW_VID_1080x1920_24s.mp4',
    'video2': 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/42588136-407d-4f3c-b9d3-3bbdff874c01/CAY_C2_V2_WW_VID_1080x1920_36s.mp4',
    'video3': 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/0c017021-67de-4289-adb0-513be3bab6ad/CAY_C31_V4_WW_VID_1080x1920_28s.mp4',
    'video4': 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/41d2ec4f-e68e-4979-b23b-8e70fda4d3e0/CAY_C38_V3_WW_VID_1080x1920_28s.mp4',
    'video5': 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/a81667e4-941c-4f79-bb55-73f4b7fa5195/CAY_C44_V4_WW_VID_1080x1920_55s.mp4',
    'video6': 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/188f3e44-468a-4bbf-bbd6-31cae958658f/CAY_C47_V2_WW_VID_1080x1920_57s.mp4',
    'video7': 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/0e6f38ec-c31d-4e48-9cca-a42be08eabdc/CAY_C46_V3_WW_VID_1080x1920_28s.mp4',
    'video8': 'https://x-ad-assets.s3.amazonaws.com/media_asset/fb933ca4ddaaed31/media',
    'video9': 'https://x-ad-assets.s3.amazonaws.com/media_asset/0b70f4ccb1ab283b/media',
    'video10': 'https://x-ad-assets.s3.amazonaws.com/media_asset/00b01c9653131b14/media'
};

// Completion codes mapping
const COMPLETION_CODES = {
    'video1': 'EM7K2X9Q',
    'video2': 'B4N6P8R1',
    'video3': 'Y3M7C5W9',
    'video4': 'Q8T2V6K4',
    'video5': 'L9B5H3F7',
    'video6': 'R6X8N2M4',
    'video7': 'Z4K7Q3P9',
    'video8': 'W5J9R7T2',
    'video9': 'F8L3B6N1',
    'video10': 'C2Y7M4K8'
};

// Get parameters from URL
const videoParam = getUrlParameter('video');
const codeParam = getUrlParameter('code');

// Determine video URL and completion code
const selectedVideoUrl = videoParam && VIDEO_URLS[videoParam] 
    ? VIDEO_URLS[videoParam] 
    : VIDEO_URLS['video1']; // Default to video1 for testing

const selectedCode = codeParam || (videoParam && COMPLETION_CODES[videoParam]) 
    ? (codeParam || COMPLETION_CODES[videoParam])
    : COMPLETION_CODES['video1']; // Default to video1 code for testing

const config = {
  // Dynamic Video Configuration
  VIDEO_URL: selectedVideoUrl,
  
  // Study Configuration
  TASK_ID: videoParam || 'TASK-TEST',
  COMPLETION_CODE: selectedCode,
  
  // Privacy Policy URL (optional)
  PRIVACY_POLICY_URL: 'https://yaronskihoma.github.io/VideoTask2/privacypolicy.html',
  
  // Supabase Configuration
  SUPABASE_URL: 'https://nxlyelvtfphybhyfhxwc.supabase.co',
  SUPABASE_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im54bHllbHZ0ZnBoeWJoeWZoeHdjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTYyNzgxOSwiZXhwIjoyMDY3MjAzODE5fQ.8F-la271rAdg-kPuxEySLUDaKyqNItrsoOzwoWWjnbw',
  
  // Morphcast Configuration
  MORPHCAST_LICENSE: 'ap95c1923492e8512306644ca7fea0e66e7c27a47b97bb',
  
  // Advanced Configuration (optional)
  VIDEO_MAX_DURATION: 60, // Maximum video duration in seconds (some videos are 57s)
  RETRY_ATTEMPTS: 3,      // Number of retry attempts for uploads
  PROGRESS_UPDATE_INTERVAL: 250, // Progress update interval in milliseconds
  
  // Tracking Configuration
  TRACKING_MODULES: {
    FACE_AROUSAL_VALENCE: { smoothness: 0.70 },
    FACE_EMOTION: { smoothness: 0.40 },
    FACE_ATTENTION: { smoothness: 0.83 },
    FACE_DETECTOR: { maxInputFrameSize: 320, smoothness: 0.83 },
    ALARM_NO_FACE: { timeWindowMs: 10000, initialToleranceMs: 7000, threshold: 0.75 },
    DATA_AGGREGATOR: { initialWaitMs: 2000, periodMs: 1000 }
  },
  
  // Debug Configuration
  DEBUG_MODE: true,
  CONSOLE_LOGGING: true
};

console.log('✅ Configuration loaded successfully');
console.log('📹 Selected Video:', videoParam || 'video1 (default)');
console.log('🔑 Completion Code:', selectedCode);
console.log('💾 Video URL:', selectedVideoUrl);
console.log('📝 URL Parameters:', { video: videoParam, code: codeParam });

export default config; 