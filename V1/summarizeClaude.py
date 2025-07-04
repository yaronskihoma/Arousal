import os
import json
import numpy as np

def process_report(file_path):
    with open(file_path, 'r') as file:
        report_data = json.load(file)

    media_times = []
    arousal_values = []

    for entry in report_data['trackingData']:
        if 'mediaTime' in entry and entry['type'] == 'FACE_AROUSAL_VALENCE':
            media_times.append(entry['mediaTime'])
            arousal_values.append(entry['arousal'])

    return media_times, arousal_values

def align_data_to_60_seconds(media_times, arousal_values):
    aligned_times = np.array(media_times)
    aligned_arousal = np.array(arousal_values)
    
    # Ensure the data doesn't exceed 60 seconds
    mask = aligned_times <= 60
    aligned_times = aligned_times[mask]
    aligned_arousal = aligned_arousal[mask]
    
    return aligned_times, aligned_arousal

def calculate_average(aligned_data):
    max_length = max(len(data) for data in aligned_data)
    padded_data = [np.pad(arr, (0, max_length - len(arr)), 'constant', constant_values=np.nan) for arr in aligned_data]
    avg = np.nanmean(padded_data, axis=0)
    return avg

def create_summary_json(avg_times, avg_arousal, output_dir):
    summary_report = {
        "trackingData": [
            {
                "mediaTime": float(time),
                "type": "FACE_AROUSAL_VALENCE",
                "arousal": float(arousal)
            }
            for time, arousal in zip(avg_times, avg_arousal)
            if not np.isnan(arousal)
        ]
    }

    output_path = os.path.join(output_dir, 'summarized_arousal_report.json')
    with open(output_path, 'w') as json_file:
        json.dump(summary_report, json_file, indent=4)
    print(f"Summarized report saved to: {output_path}")

def process_all_json_files(directory):
    json_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]
    
    aligned_times_list = []
    aligned_arousal_list = []

    if not json_files:
        print(f"No JSON files found in: {directory}")
        return

    output_dir = os.path.join(directory, "summarized_reports")
    os.makedirs(output_dir, exist_ok=True)

    for file_path in json_files:
        print(f"Processing file: {file_path}")
        media_times, arousal_values = process_report(file_path)
        aligned_times, aligned_arousal = align_data_to_60_seconds(media_times, arousal_values)
        aligned_times_list.append(aligned_times)
        aligned_arousal_list.append(aligned_arousal)

    # Calculate the average times and arousal values
    avg_times = calculate_average(aligned_times_list)
    avg_arousal = calculate_average(aligned_arousal_list)

    # Create a summarized JSON report
    create_summary_json(avg_times, avg_arousal, output_dir)

# Run the script
if __name__ == "__main__":
    json_directory = 'reportsVideo2_60s'  # Replace with your directory
    process_all_json_files(json_directory)