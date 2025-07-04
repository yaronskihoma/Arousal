import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import interpolate
from scipy.signal import savgol_filter
from matplotlib.patches import Rectangle, Patch

# This will be updated based on the data
FIXED_TIMELINE_SECONDS = 30

def normalize_value(value, min_val=-1, max_val=1):
    try:
        return 100 * (value - min_val) / (max_val - min_val)
    except:
        return np.nan

def get_video_length(media_times):
    if len(media_times) == 0:
        return 30  # default length
    return int(np.ceil(max(media_times)))

def process_report(file_path):
    try:
        with open(file_path, 'r') as file:
            report_data = json.load(file)
        
        print(f"Processing file with {len(report_data)} entries")
        
        media_times = []
        arousal_values = []
        
        arousal_count = 0
        zero_count = 0
        error_count = 0
        
        for entry in report_data:
            if 'mediaTime' in entry and entry['type'] == 'FACE_AROUSAL_VALENCE':
                try:
                    media_time = float(entry['mediaTime'])
                    arousal = float(entry['arousal'])
                    
                    if arousal == 0:
                        zero_count += 1
                        
                    media_times.append(media_time)
                    arousal_values.append(normalize_value(arousal))
                    arousal_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Error processing entry: {entry}")
                    continue
        
        print(f"Found {arousal_count} arousal measurements")
        print(f"Zero values: {zero_count}")
        print(f"Errors: {error_count}")
        
        if zero_count == arousal_count and arousal_count > 0:
            print("WARNING: All values are zero in this file!")
        
        # Convert to numpy arrays
        media_times = np.array(media_times)
        arousal_values = np.array(arousal_values)
        
        # Sort by media_times if not already sorted
        if len(media_times) > 0:
            sort_idx = np.argsort(media_times)
            media_times = media_times[sort_idx]
            arousal_values = arousal_values[sort_idx]
        
        return media_times, arousal_values
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return np.array([]), np.array([])

def extend_data_to_timeline(media_times, arousal_values, timeline_length):
    if len(media_times) == 0:
        return np.arange(timeline_length), np.full(timeline_length, np.nan)
    
    # Convert to numpy arrays and ensure they're float type
    media_times = np.array(media_times, dtype=float)
    arousal_values = np.array(arousal_values, dtype=float)
    
    extended_times = np.arange(timeline_length)
    
    if len(media_times) == 1:
        extended_values = np.full(timeline_length, arousal_values[0])
    else:
        # Ensure media_times are unique for interpolation
        unique_times, unique_indices = np.unique(media_times, return_index=True)
        unique_values = arousal_values[unique_indices]
        
        if len(unique_times) < 2:
            extended_values = np.full(timeline_length, unique_values[0])
        else:
            try:
                f = interpolate.interp1d(unique_times, unique_values, kind='linear',
                                       bounds_error=False, fill_value=(unique_values[0], unique_values[-1]))
                extended_values = f(extended_times)
            except Exception as e:
                print(f"Interpolation error: {str(e)}")
                extended_values = np.full(timeline_length, np.nan)
    
    # Set values to NaN after the last actual data point
    last_actual_time = int(np.ceil(media_times[-1]))
    if last_actual_time < timeline_length:
        extended_values[last_actual_time+1:] = np.nan
    
    return extended_times, extended_values
def plot_comprehensive_summary(all_media_times, all_arousal_values, output_dir, timeline_length):
    # Generate extended data for each dataset
    extended_data = [extend_data_to_timeline(mt, av, timeline_length) 
                    for mt, av in zip(all_media_times, all_arousal_values)]
    
    # Create a matrix of the interpolated values, padding with NaN where necessary
    interpolated_values = np.full((len(extended_data), timeline_length), np.nan)
    
    for i, (_, values) in enumerate(extended_data):
        if len(values) > 0:  # Only process non-empty arrays
            interpolated_values[i, :len(values)] = values[:timeline_length]
    
    if len(interpolated_values) > 0:
        average_arousal = np.nanmean(interpolated_values, axis=0)
        
        if np.all(np.isnan(average_arousal)):
            print("Warning: All values are NaN. Unable to generate visualization.")
            return

        # Calculate smoothed trend with better handling of window length
        non_nan_count = np.sum(~np.isnan(average_arousal))
        window_length = min(11, non_nan_count)
        if window_length % 2 == 0:
            window_length -= 1
        if window_length < 3:
            window_length = 3
        poly_order = min(3, window_length - 1)
        
        # Replace NaN with interpolated values for smoothing
        non_nan_idx = ~np.isnan(average_arousal)
        if np.any(non_nan_idx):
            temp_arousal = average_arousal.copy()
            x = np.arange(len(average_arousal))
            non_nan_x = x[non_nan_idx]
            non_nan_y = average_arousal[non_nan_idx]
            if len(non_nan_x) > 1:
                f = interpolate.interp1d(non_nan_x, non_nan_y, bounds_error=False, fill_value='extrapolate')
                temp_arousal = f(x)
                smoothed_arousal = savgol_filter(temp_arousal, window_length, poly_order)
            else:
                smoothed_arousal = average_arousal
        else:
            smoothed_arousal = average_arousal
        
        # Create plot
        fig, ax = plt.subplots(figsize=(20, 12))
        
        # Add guide cells
        for i in range(timeline_length):
            for j in range(10):
                ax.add_patch(Rectangle((i, j*10), 1, 10, fill=False, edgecolor='gray', lw=0.5, alpha=0.15))
        
        # Plot heatmap
        masked_values = np.ma.masked_invalid(interpolated_values)
        heatmap = sns.heatmap(masked_values.T, cmap='YlOrRd', 
                             cbar_kws={'label': 'Arousal Match Frequency'}, 
                             xticklabels=False, yticklabels=False, 
                             vmin=0, vmax=100, cbar=False, ax=ax, alpha=0.7)
        
        # Add color bar
        sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=0, vmax=100))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, label='Arousal Match Frequency', aspect=30)
        cbar.set_ticks(np.linspace(0, 100, 5))
        cbar.set_ticklabels(['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        
        ax.invert_yaxis()
        
        time_axis = np.arange(timeline_length)
        ax2 = ax.twinx()
        
        # Plot average and smoothed lines
        valid_arousal = ~np.isnan(average_arousal)
        if np.any(valid_arousal):
            min_val = np.nanmin(average_arousal[valid_arousal])
            max_val = np.nanmax(average_arousal[valid_arousal])
            if min_val != max_val:
                scaled_average = np.interp(average_arousal, (min_val, max_val), (0, 100))
                scaled_smoothed = np.interp(smoothed_arousal, (min_val, max_val), (0, 100))
            else:
                scaled_average = average_arousal
                scaled_smoothed = smoothed_arousal
            
            ax2.plot(time_axis, scaled_average, color='blue', linewidth=2, label='Average Arousal (Scaled)')
            ax2.plot(time_axis, scaled_smoothed, color='green', linewidth=2, label='Smoothed Trend (Scaled)')
            ax2.plot(time_axis, average_arousal, color='purple', linewidth=2, linestyle='--', label='Average Arousal (No Scale)')
        
        # Set labels and title
        ax.set_xlabel("Media Time (seconds)")
        ax.set_ylabel("Arousal Match Frequency")
        ax2.set_ylabel("Arousal (%)")
        ax.set_title(f"Heatmap of Arousal Values with Average and Smoothed Trends\nVideo Length: {timeline_length}s")
        
        # Set ticks with better spacing for longer videos
        tick_spacing = max(1, timeline_length // 30)  # Adjust spacing based on length
        ax.set_xticks(np.arange(0, timeline_length + 1, tick_spacing))
        ax.set_xticklabels(np.arange(0, timeline_length + 1, tick_spacing), rotation=90)
        
        ax.set_yticks(np.linspace(0, 100, 11))
        ax.set_yticklabels(np.linspace(0, 100, 11).astype(int))
        ax2.set_ylim(0, 100)
        ax2.set_yticks(np.linspace(0, 100, 11))

        # Add annotations
        start_value = average_arousal[0]
        end_value = np.nanmean(interpolated_values[:, -1])
        
        if not np.isnan(start_value):
            ax2.annotate(f'Start: {start_value:.1f}%', xy=(0, start_value), xytext=(5, 5),
                        textcoords='offset points', ha='left', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        if not np.isnan(end_value):
            ax2.annotate(f'End: {end_value:.1f}%', xy=(timeline_length-1, end_value), xytext=(-5, 5),
                        textcoords='offset points', ha='right', va='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        # Add legend
        legend_elements = [
            Patch(facecolor='yellow', edgecolor='black', label='Start/End Arousal'),
            plt.Line2D([0], [0], color='blue', lw=2, label='Average Arousal (Scaled)'),
            plt.Line2D([0], [0], color='green', lw=2, label='Smoothed Trend (Scaled)'),
            plt.Line2D([0], [0], color='purple', lw=2, linestyle='--', label='Average Arousal (No Scale)'),
            Patch(facecolor='#FFA07A', edgecolor='black', label='Arousal Heatmap')
        ]
        
        leg = ax.legend(handles=legend_elements, loc='best', title="Legend", fontsize=8)
        
        plt.tight_layout()
        plt.subplots_adjust(right=0.85)
        plt.savefig(os.path.join(output_dir, "arousal_heatmap_timeline_combined.png"), dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved comprehensive summary visualizations to: {output_dir}")
    else:
        print("No valid data to plot.")

def process_all_json_files(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    if not json_files:
        print(f"No JSON files found in: {directory}")
        return
    
    print(f"Found {len(json_files)} JSON files")
    
    # First pass to determine video length and validate files
    max_video_length = 30  # default
    valid_files = []
    
    for file_name in json_files:
        file_path = os.path.join(directory, file_name)
        try:
            media_times, arousal_values = process_report(file_path)
            if len(media_times) > 0 and len(arousal_values) > 0:
                video_length = get_video_length(media_times)
                max_video_length = max(max_video_length, video_length)
                valid_files.append((file_path, media_times, arousal_values))
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    
    if not valid_files:
        print("No valid files found to process.")
        return
    
    print(f"Detected video length: {max_video_length} seconds")
    
    output_dir = os.path.join(directory, "reports")
    os.makedirs(output_dir, exist_ok=True)
    
    all_media_times = []
    all_arousal_values = []
    
    for file_path, media_times, arousal_values in valid_files:
        all_media_times.append(media_times)
        all_arousal_values.append(arousal_values)
    
    plot_comprehensive_summary(all_media_times, all_arousal_values, output_dir, max_video_length)
    print("Processing complete!")

if __name__ == "__main__":
    json_directory = 'TASK3'  # Set your folder path here
    process_all_json_files(json_directory)