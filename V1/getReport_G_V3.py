import glob
import json
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

# Function to normalize valence and arousal to 0-100% scale
def normalize_value(value, min_val=-1, max_val=1):
    return 100 * (value - min_val) / (max_val - min_val)

# Function to process the JSON report and extract metrics
def process_report(file_path):
    with open(file_path, "r") as file:
        report_data = json.load(file)

    media_times = []
    attention_values = []
    valence_values = []
    arousal_values = []

    for entry in report_data["trackingData"]:
        if "mediaTime" in entry:
            media_time = entry["mediaTime"]

            # Extract relevant metrics
            if entry["type"] == "FACE_ATTENTION":
                attention_values.append(entry["attention"] * 100)  # Already in percentage
                media_times.append(media_time)
            elif entry["type"] == "FACE_AROUSAL_VALENCE":
                valence_values.append(
                    normalize_value(entry["valence"])
                )  # Rescale valence
                arousal_values.append(
                    normalize_value(entry["arousal"])
                )  # Rescale arousal

    return media_times, attention_values, valence_values, arousal_values

# Function to plot the metrics as a timeline for individual reports
def plot_timeline(
    media_times, attention_values, valence_values, arousal_values, file_name, output_dir
):
    plt.figure(
        figsize=(19.2, 10.8)
    )  # Set the horizontal size to 1920px (19.2 inches with 100 dpi)

    # Ensure 0-100% is always visible
    plt.ylim(0, 100)

    # Add grid background for better readability
    plt.grid(
        True, which="both", axis="both", linestyle="--", linewidth=0.5, color="gray"
    )

    # Plot each metric with distinct colors and labels
    plt.plot(media_times, attention_values, label="Attention", color="cyan")
    plt.plot(
        media_times[: len(valence_values)], valence_values, label="Valence", color="orange"
    )
    plt.plot(
        media_times[: len(arousal_values)], arousal_values, label="Arousal", color="red"
    )

    # Add labels and title
    plt.xlabel("Media Time (seconds)")
    plt.ylabel("Percentage (%)")
    plt.title(f"Emotion Tracking Timeline - {file_name}")

    # Add % sign to vertical scale and set ticks every 10%
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))

    # Add 1-second markers on the x-axis
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    # Add grid background for easy navigation of the data
    ax.set_axisbelow(True)

    # Add legend
    plt.legend()

    # Save the plot
    output_path = os.path.join(output_dir, f"{file_name}_timeline.png")
    plt.savefig(output_path, dpi=100)  # Save with 100 dpi to match the size
    plt.close()

    print(f"Saved timeline to: {output_path}")

# Function to pad arrays to match the longest length
def pad_arrays_to_length(*arrays):
    max_length = max(len(arr) for arr in arrays)

    # Pad all arrays to the same length as the maximum length
    def pad(arr, max_len):
        return arr + [np.nan] * (max_len - len(arr))

    return [pad(arr, max_length) for arr in arrays]

# Function to export the data to CSV or Excel format
def export_to_csv_xlsx(
    media_times, attention_values, valence_values, arousal_values, file_name, output_dir
):
    # Ensure that arrays are of the same length
    (
        media_times,
        attention_values,
        valence_values,
        arousal_values,
    ) = pad_arrays_to_length(
        media_times, attention_values, valence_values, arousal_values
    )

    # Combine data into a pandas DataFrame
    data = {
        "Media Time (seconds)": media_times,
        "Attention (%)": attention_values,
        "Valence (%)": valence_values,
        "Arousal (%)": arousal_values,
    }
    df = pd.DataFrame(data)

    # Export to CSV
    csv_output_path = os.path.join(output_dir, f"{file_name}_data.csv")
    df.to_csv(csv_output_path, index=False)

    # Export to Excel
    xlsx_output_path = os.path.join(output_dir, f"{file_name}_data.xlsx")
    df.to_excel(xlsx_output_path, index=False)

    print(f"Exported data to CSV and Excel for {file_name}")

# Function to create a summarized report combining all reports with grid cells for each 10% and 1-second step
def plot_summary(
    media_times_combined,
    attention_combined,
    valence_combined,
    arousal_combined,
    output_dir,
):
    plt.figure(figsize=(19.2, 10.8))  # Set horizontal size to 1920px

    # Set limits to ensure 0-100% is always visible
    plt.ylim(0, 100)

    # Plot each metric independently to avoid mismatched lengths
    plt.plot(
        media_times_combined, attention_combined, label="Attention", color="cyan", alpha=0.2
    )
    plt.plot(
        media_times_combined,
        valence_combined,
        label="Valence",
        color="orange",
        alpha=0.2,
    )
    plt.plot(
        media_times_combined, arousal_combined, label="Arousal", color="red", alpha=0.2
    )

    # Add grid cells for every 10% and 1-second mark
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.grid(
        True, which="both", axis="both", linestyle="--", linewidth=0.5, color="gray"
    )

    # Add labels and title
    plt.xlabel("Media Time (seconds)")
    plt.ylabel("Percentage (%)")
    plt.title("Summarized Emotion Tracking Timeline")
    plt.legend()

    # Save the plot
    output_path = os.path.join(output_dir, "summarized_timeline.png")
    plt.savefig(output_path, dpi=100)  # Save with 100 dpi for 1920px size
    plt.close()

    print(f"Saved summarized timeline to: {output_path}")

# Function to process multiple JSON files and generate both individual and summary reports
def process_all_json_files(directory):
    json_files = glob.glob(os.path.join(directory, "*.json"))

    # Lists to store combined data for the summary report
    media_times_combined = []
    attention_combined = []
    valence_combined = []
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
        (
            media_times, attention_values, valence_values, arousal_values 
        ) = process_report(file_path)

        # Plot individual report
        plot_timeline(
            media_times,
            attention_values,
            valence_values,
            arousal_values,
            file_name,
            output_dir,
        )

        # Export data to CSV and Excel
        export_to_csv_xlsx(
            media_times,
            attention_values,
            valence_values,
            arousal_values,
            file_name,
            output_dir,
        )

        # Pad arrays to the same length
        (
            media_times,
            attention_values,
            valence_values,
            arousal_values,
        ) = pad_arrays_to_length(
            media_times, attention_values, valence_values, arousal_values
        )

        # Append data to combined lists for summary report
        media_times_combined.append(media_times)
        attention_combined.append(attention_values)
        valence_combined.append(valence_values)
        arousal_combined.append(arousal_values)

    # Ensure all arrays within combined lists have the same length for the summary report
    media_times_combined = pad_arrays_to_length(*media_times_combined)
    attention_combined = pad_arrays_to_length(*attention_combined)
    valence_combined = pad_arrays_to_length(*valence_combined)
    arousal_combined = pad_arrays_to_length(*arousal_combined)

    # Convert lists to numpy arrays for easier manipulation
    media_times_combined = np.array(media_times_combined)
    attention_combined = np.array(attention_combined)
    valence_combined = np.array(valence_combined)
    arousal_combined = np.array(arousal_combined)

    # Plot summarized report
    plot_summary(
        media_times_combined,
        attention_combined,
        valence_combined,
        arousal_combined,
        output_dir,
    )

# Example usage:
json_directory = "reportsVideo1"  # Replace with the actual directory
process_all_json_files(json_directory)