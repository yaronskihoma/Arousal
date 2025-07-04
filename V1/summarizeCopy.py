import os
import json
import glob
import numpy as np

# Function to process the JSON report and extract arousal values
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

# Function to pad arrays to the same length
def pad_arrays_to_length(media_times_combined, arousal_combined):
    max_len = max(len(arr) for arr in arousal_combined)
    padded_arousal_combined = [np.pad(arr, (0, max_len - len(arr)), 'constant', constant_values=np.nan) for arr in arousal_combined]
    return media_times_combined, padded_arousal_combined

# Function to calculate the average of the arousal values
def calculate_average(arousal_combined):
    padded_arrays = np.array([np.pad(arr, (0, max(len(arr) for arr in arousal_combined) - len(arr)), 'constant', constant_values=np.nan) for arr in arousal_combined])
    avg = np.nanmean(padded_arrays, axis=0)
    return avg

# Function to create a summarized JSON report
def create_summary_json(media_times, avg_arousal, output_dir):
    summary_report = {
        "trackingData": []
    }
    
    for time, arousal in zip(media_times, avg_arousal):
        summary_report['trackingData'].append({
            "mediaTime": time,
            "type": "FACE_AROUSAL_VALENCE",
            "arousal": arousal
        })
    
    # Save the summarized JSON report
    output_path = os.path.join(output_dir, 'summarized_arousal_report.json')
    with open(output_path, 'w') as json_file:
        json.dump(summary_report, json_file, indent=4)
    print(f"Summarized report saved to: {output_path}")

# Function to process multiple JSON files and generate a summarized report
def process_all_json_files(directory):
    json_files = glob.glob(os.path.join(directory, '*.json'))
    
    media_times_combined = []
    arousal_combined = []
    
    if not json_files:
        print(f"No JSON files found in: {directory}")
        return
    
    output_dir = os.path.join(directory, "summarized_reports")
    os.makedirs(output_dir, exist_ok=True)
    
    for file_path in json_files:
        print(f"Processing file: {file_path}")
        media_times, arousal_values = process_report(file_path)
        media_times_combined.append(media_times)
        arousal_combined.append(arousal_values)
    
    # Ensure all arrays are of the same length
    media_times_combined, arousal_combined = pad_arrays_to_length(media_times_combined, arousal_combined)
    
    # Calculate the average arousal values
    avg_arousal = calculate_average(arousal_combined)
    
    # Create a summarized JSON report
    create_summary_json(media_times_combined[0], avg_arousal, output_dir)

# Run the script
if __name__ == "__main__":
    # Replace with the directory containing your JSON files
    json_directory = 'reportsVideo1_60s'  # Replace with your directory
    process_all_json_files(json_directory)