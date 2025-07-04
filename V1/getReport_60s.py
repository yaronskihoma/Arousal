import numpy as np
import os
import json
import matplotlib.pyplot as plt
import glob
import pandas as pd

# Function to normalize values to 0-100% scale (for arousal)
def normalize_value(value, min_val=-1, max_val=1):
    return 100 * (value - min_val) / (max_val - min_val)

# Fixed timeline of 60 seconds
FIXED_TIMELINE_SECONDS = 60

# Function to process the JSON report and extract arousal values
def process_report(file_path):
    with open(file_path, 'r') as file:
        report_data = json.load(file)
    
    media_times = []
    arousal_values = []
    
    # Extracting arousal values from the JSON
    for entry in report_data['trackingData']:
        if 'mediaTime' in entry:
            media_time = entry['mediaTime']
            
            if entry['type'] == 'FACE_AROUSAL_VALENCE':
                media_times.append(media_time)
                arousal_values.append(normalize_value(entry['arousal']))

    return media_times, arousal_values

# Function to plot the metrics as a timeline for individual reports
def plot_timeline(media_times, arousal_values, file_name, output_dir):
    plt.figure(figsize=(12, 6))
    
    # Plot arousal with the original media times on a fixed 60s timeline
    plt.plot(media_times, arousal_values, label="Arousal", color='red')

    # Add labels and title
    plt.xlabel("Media Time (seconds)")
    plt.ylabel("Percentage (%)")
    plt.title(f"Emotion Tracking Timeline - {file_name}")
    plt.legend()

    # Add grid lines and 10% marks, 1 second steps
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    plt.xlim(0, FIXED_TIMELINE_SECONDS)  # Fixed 60-second timeline

    # Set x-axis ticks to every 5 seconds for readability
    plt.xticks(np.arange(0, FIXED_TIMELINE_SECONDS + 1, 5))  # 5-second steps

    # 10% y-axis steps for readability
    plt.yticks(np.arange(0, 101, 10))  # 10% steps

    # Rotate x-axis labels slightly for better readability
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    plt.xticks(rotation=45)

    # Save the plot
    output_path = os.path.join(output_dir, f"{file_name}_timeline.png")
    plt.savefig(output_path)
    plt.close()

    print(f"Saved timeline to: {output_path}")

# Function to create a summarized report with a fixed timeline
def plot_summary(media_times_combined, arousal_combined, output_dir):
    plt.figure(figsize=(12, 6))
    
    # Plot the average arousal across the combined reports
    if media_times_combined and arousal_combined:
        plt.plot(media_times_combined, np.nanmean(arousal_combined, axis=0), label="Arousal (summary)", color='red', linewidth=2)
    
    # Add labels and title
    plt.xlabel("Media Time (seconds)")
    plt.ylabel("Percentage (%)")
    plt.title("Summarized Emotion Tracking Timeline")
    plt.legend()

    # Add grid lines and 10% marks, 1 second steps
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    plt.xlim(0, FIXED_TIMELINE_SECONDS)  # Fixed 60-second timeline

    # Set x-axis ticks to every 5 seconds for readability
    plt.xticks(np.arange(0, FIXED_TIMELINE_SECONDS + 1, 5))  # 5-second steps

    # Rotate x-axis labels slightly for better readability
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
    plt.xticks(rotation=45)

    # 10% y-axis steps for readability
    plt.yticks(np.arange(0, 101, 10))  # 10% steps

    # Save the summary plot
    output_path = os.path.join(output_dir, "summarized_timeline.png")
    plt.savefig(output_path)
    plt.close()

    print(f"Saved summarized timeline to: {output_path}")

# Function to pad arrays to the length of the fixed timeline (up to 60s)
def pad_arrays_to_fixed_timeline(arrays):
    max_len = FIXED_TIMELINE_SECONDS  # Fixed to 60 seconds
    padded_arrays = np.array([np.pad(arr, (0, max_len - len(arr)), 'constant', constant_values=np.nan) for arr in arrays])
    return padded_arrays

# Function to process multiple JSON files and generate both individual and summary reports
def process_all_json_files(directory):
    json_files = glob.glob(os.path.join(directory, '*.json'))
    
    # Lists to store combined data for the summary report
    media_times_combined = []
    arousal_combined = []
    
    if not json_files:
        print(f"No JSON files found in: {directory}")
        return
    
    # Create an output directory for the generated reports
    output_dir = os.path.join(directory, "reports")
    os.makedirs(output_dir, exist_ok=True)
    
    for file_path in json_files:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"Processing file: {file_name}")
        
        # Process each JSON file and generate individual timeline charts
        media_times, arousal_values = process_report(file_path)
        plot_timeline(media_times, arousal_values, file_name, output_dir)
        
        # Append data to the combined lists for the summary
        media_times_combined.extend(media_times)
        arousal_combined.append(arousal_values)
    
    # Ensure all arrays are of the same length for the summary report
    media_times_combined, arousal_combined = pad_arrays_to_fixed_timeline([media_times_combined]), pad_arrays_to_fixed_timeline(arousal_combined)
    
    # Create the summarized report
    plot_summary(media_times_combined, arousal_combined, output_dir)

    print("Processing complete!")

# Run the script
if __name__ == "__main__":
    # Replace with the directory containing your JSON files
    json_directory = 'reportsVideo2_60s'  # Set your folder path here
    process_all_json_files(json_directory)