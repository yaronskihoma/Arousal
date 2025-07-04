#!/usr/bin/env python3
"""
Survey Links Generator for Emotion Tracking Study

This script generates an Excel file with 500 rows:
- 10 different video/code combinations
- 50 users per combination
- Ready for upload to survey platforms like Clickworker
"""

import pandas as pd
import os
from datetime import datetime

def generate_survey_links():
    """Generate survey links Excel file"""
    
    # IMPORTANT: Replace this with your actual Vercel URL after deployment
    BASE_URL = "https://your-app-url.vercel.app"
    
    # Video and code configurations
    videos_config = [
        {"video": "video1", "code": "EM7K2X9Q", "description": "CAY_R91_V1 (24s)"},
        {"video": "video2", "code": "B4N6P8R1", "description": "CAY_C2_V2 (36s)"},
        {"video": "video3", "code": "Y3M7C5W9", "description": "CAY_C31_V4 (28s)"},
        {"video": "video4", "code": "Q8T2V6K4", "description": "CAY_C38_V3 (28s)"},
        {"video": "video5", "code": "L9B5H3F7", "description": "CAY_C44_V4 (55s)"},
        {"video": "video6", "code": "R6X8N2M4", "description": "CAY_C47_V2 (57s)"},
        {"video": "video7", "code": "Z4K7Q3P9", "description": "CAY_C46_V3 (28s)"},
        {"video": "video8", "code": "W5J9R7T2", "description": "S3 Asset 1"},
        {"video": "video9", "code": "F8L3B6N1", "description": "S3 Asset 2"},
        {"video": "video10", "code": "C2Y7M4K8", "description": "S3 Asset 3"}
    ]
    
    # Generate data
    data = []
    id_counter = 1
    
    for config in videos_config:
        video_id = config["video"]
        code = config["code"]
        description = config["description"]
        
        # Generate 50 rows for each video/code combination
        for i in range(50):
            url = f"{BASE_URL}/?video={video_id}&code={code}"
            
            data.append({
                "ID": id_counter,
                "url_to_survey": url,
                "confirmation_code": code,
                "video_description": description,
                "batch": f"{video_id}_batch_{i+1:02d}"
            })
            id_counter += 1
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"emotion_tracking_survey_links_{timestamp}.xlsx"
    
    # Save to Excel
    df.to_excel(filename, index=False)
    
    print(f"✅ Generated {len(data)} survey links")
    print(f"📁 Saved to: {filename}")
    print(f"📊 Summary:")
    print(f"   - Total rows: {len(data)}")
    print(f"   - Videos: {len(videos_config)}")
    print(f"   - Users per video: 50")
    print(f"   - Base URL: {BASE_URL}")
    
    # Display sample data
    print(f"\n📋 Sample data:")
    print(df.head(10).to_string(index=False))
    
    # Display distribution
    print(f"\n📈 Distribution per video:")
    for config in videos_config:
        count = len(df[df['confirmation_code'] == config['code']])
        print(f"   {config['video']}: {count} users ({config['description']})")
    
    return filename

def update_base_url(new_base_url):
    """Update the base URL after Vercel deployment"""
    print(f"🔄 Updating BASE_URL to: {new_base_url}")
    
    # Read current script
    with open(__file__, 'r') as f:
        content = f.read()
    
    # Replace the BASE_URL
    old_line = 'BASE_URL = "https://your-app-url.vercel.app"'
    new_line = f'BASE_URL = "{new_base_url}"'
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        # Write back
        with open(__file__, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated BASE_URL successfully")
        print(f"🔄 Run the script again to generate with new URL")
    else:
        print(f"❌ Could not find BASE_URL line to update")

if __name__ == "__main__":
    print("🚀 Survey Links Generator for Emotion Tracking Study")
    print("=" * 60)
    
    # Check if user wants to update BASE_URL
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--update-url" and len(sys.argv) > 2:
            update_base_url(sys.argv[2])
            sys.exit(0)
    
    # Check if BASE_URL is still placeholder
    if "your-app-url.vercel.app" in open(__file__).read():
        print("⚠️  Warning: BASE_URL is still placeholder!")
        print("   Please update it with your actual Vercel URL:")
        print("   python3 generate_survey_links.py --update-url https://your-actual-url.vercel.app")
        print("   Or manually edit the BASE_URL variable in this script")
        print()
        
        proceed = input("Generate with placeholder URL anyway? (y/N): ").lower().strip()
        if proceed != 'y':
            print("❌ Cancelled. Update BASE_URL first.")
            sys.exit(1)
    
    # Generate the file
    filename = generate_survey_links()
    
    print(f"\n🎉 Done! Next steps:")
    print(f"   1. Deploy to Vercel following VERCEL_DEPLOYMENT.md")
    print(f"   2. Update BASE_URL in this script with your Vercel URL")
    print(f"   3. Re-run script to generate final Excel file")
    print(f"   4. Upload {filename} to your survey platform") 