import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob

# Function to normalize arousal to 0-100% scale
def normalize_value(value, min_val=-1, max_val=1):
    return 100 * (value - min_val) / (max_val - min_val)

# Function to process the JSON report and extract arousal metrics
def process_report(file_path):
    with open(file_path, 'r') as file:
        report_data = json.load(file)

    media_times = []
    arousal_values = []

    for entry in report_data['trackingData']:
        if 'mediaTime' in entry:
            media_time = entry['mediaTime']

            # Extract arousal metrics
            if entry['type'] == 'FACE_AROUSAL_VALENCE':
                arousal_values.append(normalize_value(entry['arousal']))  # Rescale arousal
                media_times.append(media_time)

    return media_times, arousal_values

# Function to plot the arousal timeline for individual reports
def plot_timeline(media_times, arousal_values, file_name, output_dir):
    plt.figure(figsize=(12, 6))

    # Plot arousal metric with distinct color and label
    plt.plot(media_times, arousal_values, label="Arousal", color='red')

    # Add labels and title
    plt.xlabel("Media Time (seconds)")
    plt.ylabel("Percentage (%)")
    plt.xticks(np.arange(0, max(media_times) + 1, 1))
    plt.yticks(np.arange(0, 101, 10))
    plt.title(f"Arousal Tracking Timeline - {file_name}")
    plt.grid(True)
    plt.legend()

    # Save the plot
    output_path = os.path.join(output_dir, f"{file_name}_timeline.png")
    plt.savefig(output_path)
    plt.close()

    print(f"Saved timeline to: {output_path}")

# Function to pad arrays to the same length
def pad_arrays_to_length(media_times_combined, arousal_combined):
    max_len = max(len(media_times_combined), len(arousal_combined))

    # Pad media times and arousal to the same length
    media_times_combined = np.pad(media_times_combined, (0, max_len - len(media_times_combined)), 'constant', constant_values=np.nan)
    arousal_combined = np.pad(arousal_combined, (0, max_len - len(arousal_combined)), 'constant', constant_values=np.nan)

    return media_times_combined, arousal_combined

# Function to calculate the average arousal values
def calculate_average(arousal_combined):
    max_len = max(len(arr) for arr in arousal_combined)  # Define max_len here
    padded_arrays = np.array([np.pad(arr, (0, max_len - len(arr)), 'constant', constant_values=np.nan) for arr in arousal_combined])
    return np.nanmean(padded_arrays, axis=0)

# Function to export the data to CSV and Excel
def export_to_csv_xlsx(media_times, arousal_values, file_name, output_dir):
    data = {
        'Media Time (seconds)': media_times,
        'Arousal (%)': arousal_values
    }

    df = pd.DataFrame(data)
    output_csv_path = os.path.join(output_dir, f"{file_name}.csv")
    output_xlsx_path = os.path.join(output_dir, f"{file_name}.xlsx")
    
    df.to_csv(output_csv_path, index=False)
    df.to_excel(output_xlsx_path, index=False)

    print(f"Exported data to CSV and Excel for {file_name}")

# Function to plot the summary of arousal over time
def plot_summary(media_times_combined, arousal_combined, output_dir):
    plt.figure(figsize=(12, 6))

    # Calculate average arousal values
    arousal_avg = calculate_average(arousal_combined)

    # Plot the summary line
    plt.plot(media_times_combined, arousal_avg, label="Arousal (summary)", color='red', linewidth=2)

    # Formatting grid and labels
    plt.grid(True)
    plt.xticks(np.arange(0, max(media_times_combined) + 1, 1))
    plt.yticks(np.arange(0, 101, 10))
    plt.xlabel("Media Time (seconds)")
    plt.ylabel("Percentage (%)")
    plt.title("Arousal Summary Over Time")
    plt.legend()

    # Save the summary plot
    output_path = os.path.join(output_dir, "arousal_summary_timeline.png")
    plt.savefig(output_path)
    plt.close()

    print(f"Saved summary timeline to: {output_path}")

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
        export_to_csv_xlsx(media_times, arousal_values, file_name, output_dir)

        # Append data to the combined lists for the summary
        media_times_combined.extend(media_times)
        arousal_combined.append(arousal_values)

    # Pad arrays to ensure all are the same length
    media_times_combined, arousal_combined = pad_arrays_to_length(media_times_combined, arousal_combined)

    # Create the summarized report
    plot_summary(media_times_combined, arousal_combined, output_dir)

    # Export combined data to CSV and Excel for summary
    export_to_csv_xlsx(media_times_combined, arousal_combined, "summarized", output_dir)

    print("Processing complete!")

# Run the script
if __name__ == "__main__":
    # Replace with the directory containing your JSON files
    json_directory = 'reportsVideo1'  # Set your folder path here
    process_all_json_files(json_directory)