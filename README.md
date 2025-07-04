# 🎬 Arousal - Mobile Emotion Tracking System

A web-based emotion tracking application that uses AI to analyze facial expressions and emotions in real-time while watching videos. Designed primarily for mobile devices and survey platforms.

## 📱 Mobile Demo

**Live Demo:** [Access on your phone](https://github.com/vitaliyaronski/Arousal) (GitHub Pages link will be added after deployment)

## 🌟 Features

### Core Functionality
- **Real-time emotion tracking** using Morphcast AI SDK
- **Mobile-first design** with fullscreen video playback
- **Cross-browser compatibility** (Chrome, Safari, Firefox, Edge)
- **Automatic video preloading** for smooth playback
- **Face detection validation** before starting tasks
- **Timeline synchronization** between video and emotion data

### Mobile Optimizations
- **Mandatory fullscreen playback** with no skip ability
- **Touch gesture prevention** to avoid accidental interactions
- **Keyboard shortcut blocking** to prevent interruptions
- **Responsive design** for all screen sizes
- **iOS Safari compatibility** with native fullscreen support

### Data Collection
- **7 emotions tracked:** Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise
- **Arousal and valence values** (-1 to 1 scale)
- **Attention scores** (0-1 scale)
- **Precise timeline matching** with video timestamps
- **Automatic data processing** and export

## 🚀 Quick Start

### For Mobile Testing
1. Open the link on your mobile device
2. Allow camera access when prompted
3. Position your face in the camera view
4. Follow the step-by-step instructions
5. Complete the video task in fullscreen mode

### For Survey Platforms
1. Replace the video URL in `config.js`
2. Update completion codes for your platform
3. Configure Supabase database (optional)
4. Deploy to your preferred hosting service

## 📁 Project Structure

```
Arousal/
├── V2/                          # Current Version
│   ├── webapp/                  # Web Application
│   │   ├── emotion-tracker.html # Main Application
│   │   ├── test-fixes.html      # Testing Page
│   │   └── config.js           # Configuration
│   └── processing/              # Data Analysis
│       ├── emotion_analyzer.py  # Python Analysis Tools
│       ├── requirements.txt     # Python Dependencies
│       └── config.json         # Analysis Config
└── V1/                          # Legacy Version
    ├── reports_in/              # Sample Data
    └── [various analysis scripts]
```

## 🔧 Configuration

### Video Settings
```javascript
const CONFIG = {
    VIDEO_URL: 'your-video-url.mp4',
    TASK_ID: 'TASK-NAME',
    COMPLETION_CODE: 'CODE123',
    VIDEO_DURATION: 24, // seconds
    TIMELINE_DURATION: 30 // normalized timeline
};
```

### Mobile-Specific Settings
- **Fullscreen Mode:** Automatically enabled on video start
- **Controls:** Completely disabled to prevent skipping
- **Gestures:** Multi-touch gestures blocked
- **Keyboard:** All shortcuts disabled during playback

## 📊 Data Format

### JSON Output Structure
```json
{
    "trackingData": [
        {
            "mediaTime": 0.182,
            "type": "FACE_EMOTION",
            "dominantEmotion": "Neutral",
            "emotions": {
                "Angry": 0.07,
                "Disgust": 0.04,
                "Fear": 0.02,
                "Happy": 0.01,
                "Neutral": 0.54,
                "Sad": 0.27,
                "Surprise": 0.04
            }
        }
    ]
}
```

## 🔒 Privacy & Security

- **Camera data never leaves device** - only emotion analysis results are processed
- **No video recording** - live analysis only
- **GDPR compliant** - minimal data collection
- **Secure transmission** - HTTPS required for production

## 🌐 Browser Compatibility

### Desktop
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Mobile
- ✅ iOS Safari 14+
- ✅ Chrome Mobile 90+
- ✅ Firefox Mobile 88+
- ✅ Samsung Internet 13+

## 📱 Mobile Testing Instructions

1. **Open on your phone:** Use the GitHub Pages link
2. **Allow permissions:** Camera access is required
3. **Position correctly:** Face should be visible in good lighting
4. **Follow prompts:** Step-by-step guided process
5. **Fullscreen mode:** Video will play in fullscreen automatically
6. **Complete task:** Watch entire video without skipping

## 🛠️ Development

### Local Setup
```bash
# Clone repository
git clone https://github.com/vitaliyaronski/Arousal.git
cd Arousal

# Start local server
cd V2/webapp
python3 -m http.server 9000

# Open in browser
open http://localhost:9000/emotion-tracker.html
```

### Testing
```bash
# Open test page
open http://localhost:9000/test-fixes.html
```

## 📈 Analytics Integration

### Supabase Setup
1. Create Supabase project
2. Update `SUPABASE_URL` and `SUPABASE_KEY`
3. Create `emotion_tracking_data` table
4. Enable real-time subscriptions

### Data Analysis
```bash
# Install Python dependencies
pip install -r V2/processing/requirements.txt

# Run analysis
python V2/processing/emotion_analyzer.py
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Morphcast AI** for emotion detection SDK
- **Supabase** for database services
- **GitHub Pages** for hosting

## 📞 Support

For issues and questions:
- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/vitaliyaronski/Arousal/issues)
- 📖 Documentation: [Wiki](https://github.com/vitaliyaronski/Arousal/wiki)

---

**🎯 Perfect for:** Survey platforms, research studies, mobile emotion tracking, UX testing, market research

**🔑 Key Benefits:** Mobile-optimized, no-skip video playback, real-time emotion analysis, precise timeline sync 