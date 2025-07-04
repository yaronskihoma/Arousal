# Emotion Tracking System V2

A comprehensive emotion tracking system that combines modern web technologies with advanced data analysis for studying emotional responses to video content.

## Features

### Web Application
- **Cross-browser compatibility** - Works on Chrome, Firefox, Safari, Edge
- **Mobile-friendly design** - Responsive layout with touch support
- **Real-time emotion tracking** - Uses Morphcast SDK for facial expression analysis
- **Secure data collection** - Encrypted data transmission to Supabase
- **Professional UI/UX** - Step-by-step guided experience
- **Privacy compliant** - Clear privacy policy and consent management

### Data Processing
- **60-second fixed timeline** - Normalizes videos of different lengths
- **Advanced visualization** - Heatmaps, timelines, and statistical analysis
- **Multi-format export** - CSV, Excel, and JSON outputs
- **Cross-participant analysis** - Aggregate statistics and trends
- **High-quality reports** - Publication-ready visualizations

## Project Structure

```
V2/
├── webapp/                 # Web application
│   ├── index.html         # Main HTML template
│   ├── app.js             # Application logic
│   └── config.js          # Configuration template
├── processing/            # Python data analysis
│   ├── emotion_analyzer.py # Main analysis script
│   ├── requirements.txt   # Python dependencies
│   └── config.json        # Analysis configuration
└── README.md             # This documentation
```

## Quick Start

### 1. Web Application Setup

1. **Configure the application:**
   ```javascript
   // Edit webapp/config.js
   const config = {
     VIDEO_URL: 'https://your-video-url.mp4',
     COMPLETION_CODE: 'YOUR_CODE',
     TASK_ID: 'YOUR_TASK_ID',
     SUPABASE_URL: 'your-supabase-url',
     SUPABASE_KEY: 'your-supabase-key',
     MORPHCAST_LICENSE: 'your-morphcast-license'
   };
   ```

2. **Deploy the web application:**
   - Upload the `webapp/` folder to your web server
   - Ensure HTTPS is enabled (required for camera access)
   - Test the application in different browsers

### 2. Data Processing Setup

1. **Install Python dependencies:**
   ```bash
   cd V2/processing
   pip install -r requirements.txt
   ```

2. **Run the analysis:**
   ```bash
   python emotion_analyzer.py /path/to/data/directory
   ```

3. **Custom configuration:**
   ```bash
   python emotion_analyzer.py /path/to/data --config config.json
   ```

## Configuration

### Web Application Configuration

Edit `webapp/config.js` to customize:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `VIDEO_URL` | URL of the video to analyze | `https://example.com/video.mp4` |
| `COMPLETION_CODE` | Code shown to participants | `ABC123` |
| `TASK_ID` | Unique identifier for the task | `TASK-V2-001` |
| `PRIVACY_POLICY_URL` | Link to privacy policy | `https://example.com/privacy` |
| `SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | Supabase service key | `eyJhbGciOiJIUzI1NiI...` |
| `MORPHCAST_LICENSE` | Morphcast license key | `sk9bebf546...` |

### Python Analysis Configuration

Edit `processing/config.json` to customize:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FIXED_TIMELINE_SECONDS` | Timeline duration in seconds | `60` |
| `HIGH_AROUSAL_THRESHOLD` | Threshold for high arousal detection | `75` |
| `SMOOTHING_WINDOW` | Smoothing window size | `11` |
| `EXPORT_FORMATS` | Export formats | `["csv", "xlsx", "json"]` |
| `FIGURE_SIZE` | Plot dimensions | `[19.2, 10.8]` |

## Data Format

The system collects emotion data in the following format:

```json
{
  "trackingData": [
    {
      "mediaTime": 0.5,
      "type": "FACE_AROUSAL_VALENCE",
      "valence": -0.2,
      "arousal": 0.3
    },
    {
      "mediaTime": 0.5,
      "type": "FACE_EMOTION",
      "dominantEmotion": "Happy",
      "emotions": {
        "Happy": 0.8,
        "Sad": 0.1,
        "Angry": 0.1
      }
    },
    {
      "mediaTime": 0.5,
      "type": "FACE_ATTENTION",
      "attention": 0.9
    }
  ],
  "metadata": {
    "sessionId": 1625097600000,
    "workerId": "participant_001",
    "taskId": "TASK-V2-001"
  }
}
```

## Analysis Output

The Python analyzer generates:

### Individual Reports
- **Timeline plots** - Arousal, valence, and attention over time
- **Personal statistics** - Average scores and engagement metrics
- **High arousal moments** - Identified peaks in emotional response

### Aggregate Analysis
- **Heatmap visualization** - Arousal patterns across all participants
- **Statistical summary** - Mean, standard deviation, and trends
- **Cross-participant comparison** - Engagement rankings and patterns

### Export Files
- **CSV files** - Raw data for further analysis
- **Excel files** - Formatted spreadsheets with charts
- **JSON files** - Structured data for programmatic access

## Browser Compatibility

| Browser | Version | Status |
|---------|---------|---------|
| Chrome | 80+ | ✅ Full support |
| Firefox | 75+ | ✅ Full support |
| Safari | 13+ | ✅ Full support |
| Edge | 80+ | ✅ Full support |
| Mobile Chrome | 80+ | ✅ Full support |
| Mobile Safari | 13+ | ✅ Full support |

## Privacy and Security

### Data Protection
- **Local processing** - Video data processed locally, not transmitted
- **Encrypted transmission** - All data sent over HTTPS
- **Anonymization** - No personally identifiable information stored
- **Secure storage** - Data encrypted at rest in Supabase

### Privacy Compliance
- **Clear consent** - Explicit permission for camera access
- **Privacy policy** - Transparent data usage explanation
- **Right to withdraw** - Participants can stop at any time
- **Data retention** - Configurable retention policies

## Advanced Features

### Custom Video Integration
```javascript
// Support for multiple video formats
VIDEO_URL: 'https://example.com/video.mp4'  // MP4
VIDEO_URL: 'https://example.com/video.webm' // WebM
VIDEO_URL: 'https://example.com/video.mov'  // MOV
```

### Survey Platform Integration
```javascript
// Automatic worker ID detection
const workerId = urlParams.get('workerId') ||     // MTurk
                 urlParams.get('worker_id') ||     // Clickworker
                 urlParams.get('participantId');   // Custom
```

### Real-time Quality Monitoring
```javascript
// Face detection monitoring
window.addEventListener(CY.modules().FACE_DETECTOR.eventName, (evt) => {
  if (evt.detail.totalFaces === 0) {
    console.warn('No face detected');
  }
});
```

## Troubleshooting

### Common Issues

**Camera Access Denied**
- Ensure HTTPS is enabled
- Check browser permissions
- Try incognito/private mode

**Video Won't Play**
- Verify video URL accessibility
- Check video format compatibility
- Ensure proper CORS headers

**Data Upload Fails**
- Verify Supabase credentials
- Check internet connection
- Review browser console errors

**Analysis Fails**
- Install required Python packages
- Verify JSON file format
- Check file permissions

### Performance Optimization

**Web Application**
- Use CDN for video delivery
- Implement video preloading
- Optimize for mobile devices

**Data Processing**
- Use parallel processing for large datasets
- Implement data caching
- Optimize memory usage

## Migration from V1

### File Structure Changes
```bash
# V1 structure
project/
├── getReport.py
├── getReport_V2.py
├── online/
└── reports_in/

# V2 structure
project/
├── V1/                    # Legacy files
└── V2/                    # New system
    ├── webapp/
    └── processing/
```

### Configuration Updates
```javascript
// V1 config
const config = {
  TASK_ID: 'TASK-3'
};

// V2 config
const config = {
  TASK_ID: 'TASK-V2-001',
  VIDEO_URL: 'https://example.com/video.mp4',
  COMPLETION_CODE: 'ABC123'
};
```

### Data Processing Improvements
- **60-second normalization** - Consistent timeline across all videos
- **Advanced visualization** - Heatmaps and statistical overlays
- **Multiple export formats** - CSV, Excel, and JSON
- **Cross-participant analysis** - Aggregate statistics and trends

## Support and Contribution

### Getting Help
- Review this documentation
- Check the troubleshooting section
- Examine the example configurations
- Test with sample data

### Best Practices
- Always test on multiple browsers
- Use HTTPS in production
- Implement proper error handling
- Monitor data quality
- Regular backup of configurations

### Future Enhancements
- Real-time dashboard
- Machine learning predictions
- Advanced statistical analysis
- Multi-language support
- API integration

## License

This project incorporates the best practices from the original emotion tracking system and provides a modern, scalable solution for emotion research.

---

**Note**: This system is designed for research purposes. Ensure compliance with your institution's ethics guidelines and data protection regulations. 