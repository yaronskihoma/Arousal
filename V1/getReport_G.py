import os
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import glob
import pandas as pd
import numpy as np

# Function to normalize arousal values, with handling for None values
def normalize_value(value, min_val=-1, max_val=1):
    if value is None:
        return np.nan  # Handle None values
    return 100 * (value - min_val) / (max_val - min_val)

# Function to process the JSON report and extract arousal values
def process_report(file_path):
    with open(file_path, 'r') as file:
        report_data = json.load(file)

    media_times = []
    arousal_values = []
    
    for entry in report_data['trackingData']:
        if 'mediaTime' in entry and entry['type'] == 'FACE_AROUSAL_VALENCE':
            media_times.append(entry['mediaTime'])
            # Append the normalized arousal values (handling None values)
            arousal_values.append(normalize_value(entry['arousal']))

    return media_times, arousal_values

# Function to plot arousal as a timeline for individual reports
def plot_timeline(media_times, arousal_values, file_name, output_dir):
    plt.figure(figsize=(19.2, 10.8))
    plt.ylim(0, 100)  # Ensure 0-100% is always visible
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='gray')
    
    # Plot arousal with distinct color
    plt.plot(media_times, arousal_values, label="Arousal", color='red')

    # Add labels and title
    plt.xlabel("Media Time (seconds)")
    plt.ylabel("Percentage (%)")
    plt.title(f"Emotion Tracking Timeline - {file_name}")  # Keep the original title
    
    # Add % sign to vertical scale and set ticks every 10%
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_axisbelow(True)
    
    # Add legend
    plt.legend()

    # Save the plot
    output_path = os.path.join(output_dir, f"{file_name}_timeline.png")  # Keep the original file name
    plt.savefig(output_path, dpi=100)
    plt.close()

    print(f"Saved arousal timeline to: {output_path}")

# Function to pad arrays to match the longest length
def pad_arrays_to_length(*arrays):
    max_length = max(len(arr) for arr in arrays)

    # Pad all arrays to the same length as the maximum length
    def pad(arr, max_len):
        return arr + [np.nan] * (max_len - len(arr))
    
    return [pad(arr, max_length) for arr in arrays]

# Function to export the data to CSV or Excel format
def export_to_csv_xlsx(media_times, arousal_values, file_name, output_dir):
    # Ensure that arrays are of the same length
    media_times, arousal_values = pad_arrays_to_length(media_times, arousal_values)

    # Combine data into a pandas DataFrame
    data = {
        'Media Time (seconds)': media_times,
        'Arousal (%)': arousal_values
    }
    df = pd.DataFrame(data)
    
    # Export to CSV
    csv_output_path = os.path.join(output_dir, f"{file_name}_data.csv")  # Keep the original file name
    df.to_csv(csv_output_path, index=False)
    
    # Export to Excel
    xlsx_output_path = os.path.join(output_dir, f"{file_name}_data.xlsx")  # Keep the original file name
    df.to_excel(xlsx_output_path, index=False)
    
    print(f"Exported arousal data to CSV and Excel for {file_name}")

# Function to create a summarized report combining all reports with grid cells for each 10% and 1-second step
def plot_summary(media_times_combined, arousal_combined, output_dir):
    plt.figure(figsize=(19.2, 10.8))  # Set horizontal size to 1920px
    
    # Set limits to ensure 0-100% is always visible
    plt.ylim(0, 100)
    
    # Plot arousal
    plt.plot(media_times_combined, arousal_combined, label="Arousal", color='red')

    # Add grid cells for every 10% and 1-second mark
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='gray')

    # Add labels and title
    plt.xlabel("Media Time (seconds)")
    plt.ylabel("Percentage (%)")
    plt.title("Summarized Emotion Tracking Timeline")  # Keep the original title
    plt.legend()

    # Save the plot
    output_path = os.path.join(output_dir, "summarized_timeline.png")  # Keep the original file name
    plt.savefig(output_path, dpi=100)  # Save with 100 dpi for 1920px size
    plt.close()

    print(f"Saved summarized arousal timeline to: {output_path}")

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
    output_dir = os.path.join(directory, "reports")  # Keep the original directory name
    os.makedirs(output_dir, exist_ok=True)
    
    for file_path in json_files:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"Processing file: {file_name}")
        
        # Process each JSON file and generate individual timeline charts
        media_times, arousal_values = process_report(file_path)
        plot_timeline(media_times, arousal_values, file_name, output_dir)
        
        # Append data to the combined lists for the summary
        media_times_combined.extend(media_times)
        arousal_combined.extend(arousal_values)
    
    # Ensure all arrays are of the same length for the summary report
    media_times_combined, arousal_combined = pad_arrays_to_length(media_times_combined, arousal_combined)
    
    # Create the summarized report with grid cells
    plot_summary(media_times_combined, arousal_combined, output_dir)
    
    # Export combined data to CSV and Excel for summary
    export_to_csv_xlsx(media_times_combined, arousal_combined, "summarized", output_dir)

    print("Processing complete!")

# Run the script
if __name__ == "__main__":
    # Replace with the directory containing your JSON files
    json_directory = 'reportsVideo1_60s'  # Set your folder path here
    process_all_json_files(json_directory)