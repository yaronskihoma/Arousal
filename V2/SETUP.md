# Quick Setup Guide - Emotion Tracking V2

## 🚀 Getting Started in 5 Minutes

### Step 1: Configure Web Application

1. **Edit `webapp/config.js`:**
   ```javascript
   const config = {
     // Replace with your video URL
     VIDEO_URL: 'https://your-video-url.mp4',
     
     // Replace with your completion code
     COMPLETION_CODE: 'YOUR_CODE_123',
     
     // Replace with your task identifier
     TASK_ID: 'TASK-V2-001',
     
     // Your Supabase credentials
     SUPABASE_URL: 'https://your-project.supabase.co',
     SUPABASE_KEY: 'your-supabase-key',
     
     // Your Morphcast license
     MORPHCAST_LICENSE: 'your-morphcast-license',
     
     // Optional: Privacy policy URL
     PRIVACY_POLICY_URL: 'https://your-site.com/privacy'
   };
   ```

### Step 2: Deploy Web Application

1. **Upload to web server:**
   - Copy the entire `webapp/` folder to your web server
   - Ensure the server supports HTTPS (required for camera access)

2. **Test the deployment:**
   - Open the URL in a browser
   - Grant camera permissions
   - Verify video plays correctly

### Step 3: Set Up Data Processing

1. **Install Python dependencies:**
   ```bash
   cd V2/processing
   pip install -r requirements.txt
   ```

2. **Test with sample data:**
   ```bash
   # Analyze data from V1 (if available)
   python emotion_analyzer.py ../V1/reports_in/
   
   # Or create a test directory
   mkdir test_data
   python emotion_analyzer.py test_data/
   ```

## 📁 Project Structure After Setup

```
V2/
├── webapp/
│   ├── index.html          ✅ Ready to deploy
│   ├── app.js              ✅ Cross-browser compatible
│   └── config.js           ⚠️ CONFIGURE THIS
├── processing/
│   ├── emotion_analyzer.py ✅ Ready to use
│   ├── requirements.txt    ✅ Install dependencies
│   └── config.json         ⚠️ Optional customization
└── README.md               📖 Full documentation
```

## ⚙️ Configuration Checklist

### Web Application (Required)
- [ ] `VIDEO_URL` - URL of video to analyze
- [ ] `COMPLETION_CODE` - Code for participants
- [ ] `TASK_ID` - Unique task identifier
- [ ] `SUPABASE_URL` - Supabase project URL
- [ ] `SUPABASE_KEY` - Supabase service key
- [ ] `MORPHCAST_LICENSE` - Morphcast license key

### Web Application (Optional)
- [ ] `PRIVACY_POLICY_URL` - Privacy policy link
- [ ] `VIDEO_MAX_DURATION` - Maximum video length
- [ ] `DEBUG_MODE` - Enable debug logging

### Python Processing (Optional)
- [ ] `FIXED_TIMELINE_SECONDS` - Timeline duration (default: 60)
- [ ] `HIGH_AROUSAL_THRESHOLD` - Arousal threshold (default: 75)
- [ ] `EXPORT_FORMATS` - Output formats (default: csv, xlsx, json)

## 🔧 Common Setup Issues

### Issue: Camera Access Denied
**Solution:** Ensure your web server uses HTTPS. Camera access requires secure connection.

### Issue: Video Won't Load
**Solutions:**
- Check video URL is accessible
- Verify CORS headers allow your domain
- Test video URL directly in browser

### Issue: Data Upload Fails
**Solutions:**
- Verify Supabase credentials are correct
- Check Supabase storage bucket exists
- Ensure proper permissions in Supabase

### Issue: Python Dependencies Fail
**Solutions:**
```bash
# Update pip first
pip install --upgrade pip

# Install dependencies one by one
pip install numpy pandas matplotlib seaborn scipy openpyxl

# Or use conda
conda install numpy pandas matplotlib seaborn scipy openpyxl
```

## 📊 Testing Your Setup

### 1. Test Web Application
```
✅ Open in browser
✅ Grant camera permission
✅ Start video successfully
✅ Video plays in fullscreen
✅ Completion code appears
✅ No console errors
```

### 2. Test Data Processing
```bash
# Create test data directory
mkdir test_analysis
cd test_analysis

# Copy sample JSON from V1 if available
cp ../V1/reports_in/participant1/data.json ./

# Run analysis
python ../processing/emotion_analyzer.py ./

# Check outputs
ls analysis_results/
```

### 3. Expected Outputs
```
analysis_results/
├── participant1_individual_report.png    # Individual timeline
├── arousal_heatmap_analysis.png         # Aggregate heatmap
├── timeline_data.csv                    # Raw timeline data
└── summary_statistics.csv              # Summary stats
```

## 🚀 Production Deployment

### Web Application
1. **Use CDN for video delivery** (recommended)
2. **Enable GZIP compression** for faster loading
3. **Set up SSL certificate** (required for camera access)
4. **Configure CSP headers** for security

### Data Processing
1. **Set up automated processing** with cron jobs
2. **Configure backup storage** for results
3. **Monitor disk space** for large datasets
4. **Set up error logging** for troubleshooting

## 📞 Need Help?

1. **Check the main README.md** for detailed documentation
2. **Review browser console** for error messages
3. **Test with sample data** to isolate issues
4. **Verify all credentials** are correctly configured

## 🎯 Next Steps

After successful setup:
1. **Test with real participants** to validate the workflow
2. **Monitor data quality** to ensure proper collection
3. **Customize analysis** based on your research needs
4. **Scale deployment** for larger studies

---

**Remember:** Always test thoroughly before deploying to participants! 