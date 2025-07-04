#!/usr/bin/env python3
"""
Static Links Generator for Emotion Tracking Study

Creates 10 static HTML files with hardcoded video URLs and completion codes.
Much simpler than URL parameters approach.
"""

import os
import shutil
from datetime import datetime

def create_static_html_files():
    """Create 10 static HTML files with hardcoded configs"""
    
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
    
    print("🏗️  Creating 10 static HTML files...")
    
    created_files = []
    for config in videos_config:
        filename = f"arousal{config['id']}.html"
        
        # Create a simple static config for each file
        static_config = f"""
const CONFIG = {{
  VIDEO_URL: '{config['url']}',
  COMPLETION_CODE: '{config['code']}',
  TASK_ID: 'AROUSAL-{config['id']}',
  SUPABASE_URL: 'https://nxlyelvtfphybhyfhxwc.supabase.co',
  SUPABASE_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im54bHllbHZ0ZnBoeWJoeWZoeHdjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTYyNzgxOSwiZXhwIjoyMDY3MjAzODE5fQ.8F-la271rAdg-kPuxEySLUDaKyqNItrsoOzwoWWjnbw',
  MORPHCAST_LICENSE: 'ap95c1923492e8512306644ca7fea0e66e7c27a47b97bb',
  PRIVACY_POLICY_URL: 'https://yaronskihoma.github.io/VideoTask2/privacypolicy.html',
  VIDEO_MAX_DURATION: 60,
  RETRY_ATTEMPTS: 3,
  PROGRESS_UPDATE_INTERVAL: 250,
  TRACKING_MODULES: {{
    FACE_AROUSAL_VALENCE: {{ smoothness: 0.70 }},
    FACE_EMOTION: {{ smoothness: 0.40 }},
    FACE_ATTENTION: {{ smoothness: 0.83 }},
    FACE_DETECTOR: {{ maxInputFrameSize: 320, smoothness: 0.83 }},
    ALARM_NO_FACE: {{ timeWindowMs: 10000, initialToleranceMs: 7000, threshold: 0.75 }},
    DATA_AGGREGATOR: {{ initialWaitMs: 2000, periodMs: 1000 }}
  }},
  DEBUG_MODE: true,
  CONSOLE_LOGGING: true
}};

console.log('✅ Static Configuration loaded for Video {config['id']}');
console.log('📹 Video URL:', CONFIG.VIDEO_URL);
console.log('🔑 Completion Code:', CONFIG.COMPLETION_CODE);
"""
        
        # Replace the config.js import with inline config
        modified_html = template_html.replace(
            '<script type="module" src="config.js"></script>',
            f'<script>{static_config}</script>'
        )
        
        # Update the script that imports config to use the global CONFIG
        modified_html = modified_html.replace(
            "import config from './config.js';",
            "const config = CONFIG;"
        )
        
        # Write the static HTML file
        with open(filename, 'w') as f:
            f.write(modified_html)
        
        created_files.append({
            'filename': filename,
            'url': f"https://arousal.vercel.app/{filename}",
            'code': config['code'],
            'desc': config['desc']
        })
        
        print(f"✅ Created {filename} - {config['desc']} (Code: {config['code']})")
    
    return created_files

def generate_static_csv(files_info):
    """Generate CSV with static links"""
    
    import pandas as pd
    
    print("\n📊 Generating CSV file...")
    
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
    filename = f"static_survey_links_{timestamp}.csv"
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    print(f"✅ Generated CSV with {len(data)} rows")
    print(f"📁 Saved to: {filename}")
    
    # Show sample
    print(f"\n📋 Sample data:")
    print(df.head(10).to_string(index=False))
    
    return filename

if __name__ == "__main__":
    print("🚀 Static Links Generator for Emotion Tracking Study")
    print("=" * 60)
    
    # Create the static HTML files
    files_info = create_static_html_files()
    
    # Generate CSV
    csv_filename = generate_static_csv(files_info)
    
    print(f"\n🎉 Done! Created:")
    print(f"   📄 10 static HTML files (arousal1.html to arousal10.html)")
    print(f"   📊 CSV file: {csv_filename}")
    print(f"\n🌐 Your static links:")
    for file_info in files_info:
        print(f"   {file_info['url']} - {file_info['desc']}")
    
    print(f"\n🚀 Next steps:")
    print(f"   1. git add arousal*.html {csv_filename}")
    print(f"   2. git commit -m 'Add static HTML files'")
    print(f"   3. git push origin master")
    print(f"   4. Upload {csv_filename} to Clickworker") 