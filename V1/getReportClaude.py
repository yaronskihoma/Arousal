import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import interpolate
from scipy.signal import savgol_filter
from matplotlib.patches import Rectangle, Patch

FIXED_TIMELINE_SECONDS = 30

def normalize_value(value, min_val=-1, max_val=1):
    return 100 * (value - min_val) / (max_val - min_val)

def process_report(file_path):
    with open(file_path, 'r') as file:
        report_data = json.load(file)
    
    media_times = []
    arousal_values = []
    
    for entry in report_data['trackingData']:
        if 'mediaTime' in entry and entry['type'] == 'FACE_AROUSAL_VALENCE':
            media_times.append(entry['mediaTime'])
            arousal_values.append(normalize_value(entry['arousal']))

    return media_times, arousal_values

def extend_data_to_60_seconds(media_times, arousal_values):
    if len(media_times) == 0:
        return np.array([]), np.array([])
    
    extended_times = np.arange(FIXED_TIMELINE_SECONDS)
    
    if len(media_times) == 1:
        extended_values = np.full(FIXED_TIMELINE_SECONDS, arousal_values[0])
    else:
        f = interpolate.interp1d(media_times, arousal_values, kind='linear', bounds_error=False, fill_value=(arousal_values[0], arousal_values[-1]))
        extended_values = f(extended_times)
    
    # Set values to NaN after the last actual data point
    last_actual_time = int(media_times[-1])
    extended_values[last_actual_time+1:] = np.nan
    
    return extended_times, extended_values

def plot_comprehensive_summary(all_media_times, all_arousal_values, output_dir):
    extended_data = [extend_data_to_60_seconds(mt, av) for mt, av in zip(all_media_times, all_arousal_values)]
    interpolated_values = np.array([data[1] for data in extended_data])
    
    if len(interpolated_values) > 0:
        average_arousal = np.nanmean(interpolated_values, axis=0)
        
        # Handle cases where all values might be NaN
        if np.all(np.isnan(average_arousal)):
            print("Warning: All values are NaN. Unable to generate visualization.")
            return

        # Smoothed trend
        window_length = min(11, len(average_arousal) - 1)
        if window_length % 2 == 0:
            window_length -= 1
        poly_order = min(3, window_length - 1)
        smoothed_arousal = savgol_filter(average_arousal, window_length, poly_order)
        
        fig, ax = plt.subplots(figsize=(20, 12))
        
        # Add guide cells
        for i in range(FIXED_TIMELINE_SECONDS):
            for j in range(10):
                ax.add_patch(Rectangle((i, j*10), 1, 10, fill=False, edgecolor='gray', lw=0.5, alpha=0.15))
        
        # Plot heatmap with increased contrast
        heatmap = sns.heatmap(interpolated_values.T, cmap='YlOrRd', cbar_kws={'label': 'Arousal Match Frequency'}, 
                    xticklabels=False, yticklabels=False, vmin=0, vmax=100, cbar=False, ax=ax, alpha=0.7)
        
        # Add color bar manually for more control
        sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=0, vmax=100))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, label='Arousal Match Frequency', aspect=30)
        cbar.set_ticks(np.linspace(0, 100, 5))
        cbar.set_ticklabels(['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        
        ax.invert_yaxis()
        
        time_axis = np.arange(FIXED_TIMELINE_SECONDS)
        
        # Create a twin axis for the line plots
        ax2 = ax.twinx()
        
        # Overlay average arousal (scaled)
        scaled_average = np.interp(average_arousal, (np.nanmin(average_arousal), np.nanmax(average_arousal)), (0, 100))
        ax2.plot(time_axis, scaled_average, color='blue', linewidth=2, label='Average Arousal (Scaled)')
        
        # Overlay smoothed trend (scaled)
        scaled_smoothed = np.interp(smoothed_arousal, (np.nanmin(smoothed_arousal), np.nanmax(smoothed_arousal)), (0, 100))
        ax2.plot(time_axis, scaled_smoothed, color='green', linewidth=2, label='Smoothed Trend (Scaled)')
        
        # Overlay "no scale" line
        ax2.plot(time_axis, average_arousal, color='purple', linewidth=2, linestyle='--', label='Average Arousal (No Scale)')
        
        ax.set_xlabel("Media Time (seconds)")
        ax.set_ylabel("Arousal Match Frequency")
        ax2.set_ylabel("Arousal (%)")
        ax.set_title("Heatmap of Arousal Values with Average and Smoothed Trends")
        
        ax.set_xticks(np.arange(0, FIXED_TIMELINE_SECONDS + 1, 1))
        ax.set_xticklabels(np.arange(0, FIXED_TIMELINE_SECONDS + 1, 1), rotation=90)
        
        ax.set_yticks(np.linspace(0, 100, 11))
        ax.set_yticklabels(np.linspace(0, 100, 11).astype(int))
        
        ax2.set_ylim(0, 100)
        ax2.set_yticks(np.linspace(0, 100, 11))
        
        # Add annotations for start and end values
        start_value = average_arousal[0]
        end_value = np.nanmean(interpolated_values[:, -1])  # Use the last non-NaN value
        if not np.isnan(start_value):
            ax2.annotate(f'Start: {start_value:.1f}%', xy=(0, start_value), xytext=(5, 5), 
                        textcoords='offset points', ha='left', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
        if not np.isnan(end_value):
            ax2.annotate(f'End: {end_value:.1f}%', xy=(FIXED_TIMELINE_SECONDS-1, end_value), xytext=(-5, 5), 
                        textcoords='offset points', ha='right', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
        
        # Find and annotate all matches greater than 75% (aligned with no scale line)
        high_matches = np.where(interpolated_values > 75)
        annotated_times = set()  # To keep track of times we've already annotated
        for time, report_index in zip(high_matches[1], high_matches[0]):
            if time not in annotated_times and not np.isnan(average_arousal[time]):
                match_value = np.nanmax(interpolated_values[:, time])  # Get max non-NaN value for this time across all reports
                ax2.annotate(f'{match_value:.1f}%', 
                            xy=(time, average_arousal[time]), 
                            xytext=(0, 10), textcoords='offset points',
                            ha='center', va='bottom',
                            bbox=dict(boxstyle='round,pad=0.3', fc='red', alpha=0.5),
                            fontsize=8)
                annotated_times.add(time)
        
        # Add visual legend with examples
        legend_elements = [
            Patch(facecolor='yellow', edgecolor='black', label='Start/End Arousal'),
            Patch(facecolor='red', edgecolor='black', label='High Arousal (>75%)'),
            plt.Line2D([0], [0], color='blue', lw=2, label='Average Arousal (Scaled)'),
            plt.Line2D([0], [0], color='green', lw=2, label='Smoothed Trend (Scaled)'),
            plt.Line2D([0], [0], color='purple', lw=2, linestyle='--', label='Average Arousal (No Scale)'),
            Patch(facecolor='#FFA07A', edgecolor='black', label='Arousal Heatmap')
        ]
        
        # Add legend inside the plot
        leg = ax.legend(handles=legend_elements, loc='best', 
                        title="Legend", fontsize=8, bbox_to_anchor=(0.02, 0.98))
        
        # Add short descriptions for each element
        descriptions = [
            "Initial and final engagement levels",
            "Moments of high engagement across viewers",
            "Overall arousal trend (scaled)",
            "Smoothed average arousal trend (scaled)",
            "Actual average arousal values",
            "Intensity of arousal across all viewers"
        ]
        
        # Add descriptions next to legend items
        for txt, desc in zip(leg.get_texts(), descriptions):
            txt.set_multialignment('left')
            txt.set_text(f"{txt.get_text()}\n{desc}")
        
        plt.tight_layout()
        plt.subplots_adjust(right=0.85)
        plt.savefig(os.path.join(output_dir, "arousal_heatmap_timeline_combined.png"), dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved comprehensive summary visualizations to: {output_dir}")
    else:
        print("No valid data to plot.")

def process_all_json_files(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    all_media_times = []
    all_arousal_values = []
    
    if not json_files:
        print(f"No JSON files found in: {directory}")
        return
    
    output_dir = os.path.join(directory, "reports")
    os.makedirs(output_dir, exist_ok=True)
    
    for file_name in json_files:
        file_path = os.path.join(directory, file_name)
        print(f"Processing file: {file_name}")
        
        media_times, arousal_values = process_report(file_path)
        all_media_times.append(media_times)
        all_arousal_values.append(arousal_values)
    
    plot_comprehensive_summary(all_media_times, all_arousal_values, output_dir)

    print("Processing complete!")

# Run the script
if __name__ == "__main__":
    json_directory = 'reportsVideo1_60s'  # Set your folder path here
    process_all_json_files(json_directory)