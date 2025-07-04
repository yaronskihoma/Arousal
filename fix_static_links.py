#!/usr/bin/env python3
"""
Fixed Static Links Generator - Properly replaces CONFIG values
"""

import os
import re
from datetime import datetime

def fix_static_html_files():
    """Fix the static HTML files by properly replacing CONFIG values"""
    
    # Video configurations
    videos_config = [
        {"id": 1, "url": "https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/f4bea092-1f69-4f99-8d7a-fc8fb52ac610/CAY_R91_V1_WW_VID_1080x1920_24s.mp4", "code": "EM7K2X9Q", "desc": "CAY_R91_V1 (24s)"},
        {"id": 2, "url": "https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/42588136-407d-4f3c-b9d3-3bbdff874c01/CAY_C2_V2_WW_VID_1080x1920_36s.mp4", "code": "B4N6P8R1", "desc": "CAY_C2_V2 (36s)"},
        {"id": 3, "url": "https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/0c017021-67de-4289-adb0-513be3bab6ad/CAY_C31_V4_WW_VID_1080x1920_28s.mp4", "code": "Y3M7C5W9", "desc": "CAY_C31_V4 (28s)"},
        {"id": 4, "url": "https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/41d2ec4f-e68e-4979-b23b-8e70fda4d3e0/CAY_C38_V3_WW_VID_1080x1920_28s.mp4", "code": "Q8T2V6K4", "desc": "CAY_C38_V3 (28s)"},
        {"id": 5, "url": "https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/a81667e4-941c-4f79-bb55-73f4b7fa5195/CAY_C44_V4_WW_VID_1080x1920_55s.mp4", "code": "L9B5H3F7", "desc": "CAY_C44_V4 (55s)"},
        {"id": 6, "url": "https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/188f3e44-468a-4bbf-bbd6-31cae958658f/CAY_C47_V2_WW_VID_1080x1920_57s.mp4", "code": "R6X8N2M4", "desc": "CAY_C47_V2 (57s)"},
        {"id": 7, "url": "https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/0e6f38ec-c31d-4e48-9cca-a42be08eabdc/CAY_C46_V3_WW_VID_1080x1920_28s.mp4", "code": "Z4K7Q3P9", "desc": "CAY_C46_V3 (28s)"},
        {"id": 8, "url": "https://x-ad-assets.s3.amazonaws.com/media_asset/fb933ca4ddaaed31/media", "code": "W5J9R7T2", "desc": "S3 Asset 1"},
        {"id": 9, "url": "https://x-ad-assets.s3.amazonaws.com/media_asset/0b70f4ccb1ab283b/media", "code": "F8L3B6N1", "desc": "S3 Asset 2"},
        {"id": 10, "url": "https://x-ad-assets.s3.amazonaws.com/media_asset/00b01c9653131b14/media", "code": "C2Y7M4K8", "desc": "S3 Asset 3"}
    ]
    
    # Read the template HTML file
    with open('index.html', 'r') as f:
        template_html = f.read()
    
    print("🔧 Fixing static HTML files with correct VIDEO_URL and COMPLETION_CODE...")
    
    fixed_files = []
    for config in videos_config:
        filename = f"arousal{config['id']}.html"
        
        # Start with the template
        fixed_html = template_html
        
        # Replace the VIDEO_URL in the CONFIG object
        # Look for: VIDEO_URL: 'https://assets.homa-cloud.com/cm0wqgm1d002gdslcdl3hq3yl/f4bea092-1f69-4f99-8d7a-fc8fb52ac610/CAY_R91_V1_WW_VID_1080x1920_24s.mp4',
        video_url_pattern = r"VIDEO_URL: '[^']*'"
        fixed_html = re.sub(video_url_pattern, f"VIDEO_URL: '{config['url']}'", fixed_html)
        
        # Replace the COMPLETION_CODE in the CONFIG object
        # Look for: COMPLETION_CODE: 'CLEAN123',
        completion_code_pattern = r"COMPLETION_CODE: '[^']*'"
        fixed_html = re.sub(completion_code_pattern, f"COMPLETION_CODE: '{config['code']}'", fixed_html)
        
        # Replace the TASK_ID
        task_id_pattern = r"TASK_ID: '[^']*'"
        fixed_html = re.sub(task_id_pattern, f"TASK_ID: 'AROUSAL-{config['id']}'", fixed_html)
        
        # Write the fixed HTML file
        with open(filename, 'w') as f:
            f.write(fixed_html)
        
        fixed_files.append({
            'filename': filename,
            'url': f"https://arousal.vercel.app/{filename}",
            'code': config['code'],
            'desc': config['desc']
        })
        
        print(f"✅ Fixed {filename} - {config['desc']} (Code: {config['code']})")
    
    return fixed_files

def generate_fixed_csv(files_info):
    """Generate CSV with fixed static links"""
    
    import pandas as pd
    
    print("\n📊 Generating corrected CSV file...")
    
    data = []
    id_counter = 1
    
    for file_info in files_info:
        # Create 50 rows for each static link
        for i in range(50):
            data.append({
                "ID": id_counter,
                "url_to_survey": file_info['url'],
                "confirmation_code": file_info['code'],
                "video_description": file_info['desc'],
                "batch": f"batch_{id_counter:03d}"
            })
            id_counter += 1
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"CORRECTED_static_survey_links_{timestamp}.csv"
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    print(f"✅ Generated corrected CSV with {len(data)} rows")
    print(f"📁 Saved to: {filename}")
    
    # Show sample
    print(f"\n📋 Sample corrected data:")
    print(df.head(10).to_string(index=False))
    
    return filename

if __name__ == "__main__":
    print("🚀 FIXING Static Links for Emotion Tracking Study")
    print("=" * 60)
    
    # Fix the static HTML files
    files_info = fix_static_html_files()
    
    # Generate corrected CSV
    csv_filename = generate_fixed_csv(files_info)
    
    print(f"\n🎉 Fixed! Updated:")
    print(f"   📄 10 static HTML files with correct video URLs and completion codes")
    print(f"   📊 New CSV file: {csv_filename}")
    print(f"\n🌐 Your corrected static links:")
    for file_info in files_info:
        print(f"   {file_info['url']} - {file_info['desc']} (Code: {file_info['code']})")
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Test one of the links to verify it works")
    print(f"   2. git add arousal*.html {csv_filename}")
    print(f"   3. git commit -m 'Fix static HTML files with correct video URLs and codes'")
    print(f"   4. git push origin master")
    print(f"   5. Use {csv_filename} for Clickworker upload") 