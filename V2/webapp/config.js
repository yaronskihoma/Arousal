/**
 * Configuration file for Emotion Tracking V2
 * 
 * Replace the placeholder values with your actual configuration:
 * - VIDEO_URL: Replace with your video URL
 * - COMPLETION_CODE: Replace with your completion code
 * - TASK_ID: Replace with your task identifier
 * - PRIVACY_POLICY_URL: Replace with your privacy policy URL
 * - Supabase credentials: Replace with your actual Supabase credentials
 * - MORPHCAST_LICENSE: Replace with your Morphcast license key
 */

console.log('🔧 Loading Emotion Tracking V2 Configuration...');

const config = {
  // Video Configuration
  VIDEO_URL: 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/f4bea092-1f69-4f99-8d7a-fc8fb52ac610/CAY_R91_V1_WW_VID_1080x1920_24s.mp4',
  
  // Study Configuration
  TASK_ID: 'TASK-V2-DEMO',
  COMPLETION_CODE: 'DEMO123',
  
  // Privacy Policy URL (optional)
  PRIVACY_POLICY_URL: 'https://yaronskihoma.github.io/VideoTask2/privacypolicy.html',
  
  // Supabase Configuration
  SUPABASE_URL: 'https://szshayacurojnsbdcwkc.supabase.co',
  SUPABASE_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6c2hheWFjdXJvam5zYmRjd2tjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMTg2MTU0MywiZXhwIjoyMDQ3NDM3NTQzfQ.GQIgU6vFz0ZcIgxmuNxAXQnpoaqh3YKdCdHQMFTJvUg',
  
  // Morphcast Configuration
  MORPHCAST_LICENSE: 'ap95c1923492e8512306644ca7fea0e66e7c27a47b97bb',
  
  // Advanced Configuration (optional)
  VIDEO_MAX_DURATION: 30, // Maximum video duration in seconds (current video is 24s)
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

console.log('✅ Configuration loaded successfully:', config);
console.log('📹 Video URL:', config.VIDEO_URL);
console.log('🔑 Morphcast License:', config.MORPHCAST_LICENSE ? 'Present' : 'Missing');
console.log('💾 Supabase URL:', config.SUPABASE_URL ? 'Present' : 'Missing');

export default config; 