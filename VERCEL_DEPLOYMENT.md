# Vercel Deployment Guide

## Quick Setup (5 minutes)

### Step 1: Sign up for Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign up"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub account

### Step 2: Deploy the App
1. Click "New Project" on your Vercel dashboard
2. Find your repository: `yaronskihoma/Arousal`
3. Click "Import" next to your repository
4. **Important**: Set these settings:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
5. Click "Deploy"

### Step 3: Wait for Deployment
- Deployment takes 1-2 minutes
- You'll get a URL like: `https://arousal-xxxxx.vercel.app`

## Testing Your Deployment

### Test URLs:
Replace `your-app-url` with your actual Vercel URL:

```
https://your-app-url.vercel.app/?video=video1&code=EM7K2X9Q
https://your-app-url.vercel.app/?video=video2&code=B4N6P8R1
https://your-app-url.vercel.app/?video=video5&code=L9B5H3F7
```

### Test Steps:
1. Open each URL in browser
2. Check console logs show correct video/code
3. Verify video loads and plays correctly
4. Complete a full test run to ensure data uploads

## Survey Links Generation

Once deployed, you'll have **10 different survey links**:

1. `https://your-app-url.vercel.app/?video=video1&code=EM7K2X9Q`
2. `https://your-app-url.vercel.app/?video=video2&code=B4N6P8R1`
3. `https://your-app-url.vercel.app/?video=video3&code=Y3M7C5W9`
4. `https://your-app-url.vercel.app/?video=video4&code=Q8T2V6K4`
5. `https://your-app-url.vercel.app/?video=video5&code=L9B5H3F7`
6. `https://your-app-url.vercel.app/?video=video6&code=R6X8N2M4`
7. `https://your-app-url.vercel.app/?video=video7&code=Z4K7Q3P9`
8. `https://your-app-url.vercel.app/?video=video8&code=W5J9R7T2`
9. `https://your-app-url.vercel.app/?video=video9&code=F8L3B6N1`
10. `https://your-app-url.vercel.app/?video=video10&code=C2Y7M4K8`

## Excel File Generation

Run the provided Python script to generate the Excel file with 500 rows (50 per video).

## Video Mapping

- **video1**: 24s - CAY_R91_V1 (Code: EM7K2X9Q)
- **video2**: 36s - CAY_C2_V2 (Code: B4N6P8R1)
- **video3**: 28s - CAY_C31_V4 (Code: Y3M7C5W9)
- **video4**: 28s - CAY_C38_V3 (Code: Q8T2V6K4)
- **video5**: 55s - CAY_C44_V4 (Code: L9B5H3F7)
- **video6**: 57s - CAY_C47_V2 (Code: R6X8N2M4)
- **video7**: 28s - CAY_C46_V3 (Code: Z4K7Q3P9)
- **video8**: S3 Asset 1 (Code: W5J9R7T2)
- **video9**: S3 Asset 2 (Code: F8L3B6N1)
- **video10**: S3 Asset 3 (Code: C2Y7M4K8)

## Troubleshooting

### Common Issues:
1. **Video won't play**: Check browser console for CORS errors
2. **Config not loading**: Ensure ES6 modules are supported
3. **Wrong video showing**: Check URL parameters are correct
4. **Supabase errors**: Verify credentials in config.js

### Support:
- Test locally first: `python3 -m http.server 8080`
- Check browser console for errors
- Verify all video URLs are accessible

## Automatic Updates

Any changes pushed to GitHub will automatically update your Vercel deployment. 