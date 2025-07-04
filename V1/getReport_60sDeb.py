import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import interpolate
from scipy.signal import savgol_filter
from matplotlib.patches import Rectangle, Patch

FIXED_TIMELINE_SECONDS = 60

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

def extend_data_to_actual_length(media_times, arousal_values):
    if len(media_times) == 0:
        return np.array([]), np.array([])
    
    max_time = np.ceil(media_times[-1]).astype(int)
    extended_times = np.arange(max_time + 1)  # +1 to include the last second
    
    if len(media_times) == 1:
        extended_values = np.full(len(extended_times), arousal_values[0])
    else:
        f = interpolate.interp1d(media_times, arousal_values, kind='linear', bounds_error=False, fill_value=(arousal_values[0], arousal_values[-1]))
        extended_values = f(extended_times)
    
    # Ensure the last value matches the actual last recorded value
    extended_values[-1] = arousal_values[-1]
    
    return extended_times, extended_values

def summarize_data(all_media_times, all_arousal_values):
    print("Data Summary:")
    print(f"Number of reports: {len(all_media_times)}")
    
    max_length = max(len(times) for times in all_media_times)
    print(f"Longest report duration: {max_length:.2f} seconds")
    
    avg_duration = np.mean([times[-1] for times in all_media_times])
    print(f"Average report duration: {avg_duration:.2f} seconds")
    
    # Print average arousal at start, middle, and end
    start_arousal = np.mean([values[0] for values in all_arousal_values])
    mid_point = max_length // 2
    mid_arousal = np.mean([values[min(mid_point, len(values) - 1)] for values in all_arousal_values])  # Fixed potential IndexError
    end_arousal = np.mean([values[-1] for values in all_arousal_values])
    
    print(f"Average arousal at start: {start_arousal:.2f}%")
    print(f"Average arousal at middle: {mid_arousal:.2f}%")
    print(f"Average arousal at end: {end_arousal:.2f}%")

def print_raw_data_sample(all_media_times, all_arousal_values, num_samples=5):
    print("\nRaw Data Sample:")
    for i in range(min(num_samples, len(all_media_times))):
        print(f"\nReport {i+1}:")
        for time, arousal in zip(all_media_times[i][:10], all_arousal_values[i][:10]):
            print(f"Time: {time:.2f}s, Arousal: {arousal:.2f}%")
        print("...")
        for time, arousal in zip(all_media_times[i][-10:], all_arousal_values[i][-10:]):
            print(f"Time: {time:.2f}s, Arousal: {arousal:.2f}%")

def plot_comprehensive_summary(all_media_times, all_arousal_values, output_dir):
    extended_data = [extend_data_to_actual_length(mt, av) for mt, av in zip(all_media_times, all_arousal_values)]
    interpolated_values = np.array([data[1] for data in extended_data])
    
    if len(interpolated_values) > 0:
        average_arousal = np.nanmean(interpolated_values, axis=0)
        
        # --- Debugging code starts here ---
        print("\nDebugging Information:")
        print("Shape of interpolated_values:", interpolated_values.shape)
        print("First 10 rows of interpolated_values:\n", interpolated_values[:10, :])
        print("...")
        print("Last 10 rows of interpolated_values:\n", interpolated_values[-10:, :])
        
        print("\nAverage arousal (first 10 values):", average_arousal[:10])
        print("Average arousal (last 10 values):", average_arousal[-10:])
        
        # Plot histograms of arousal values at specific times
        plt.figure(figsize=(10, 6))
        plt.hist(interpolated_values[:, 0], bins=10, alpha=0.5, label='Start') 
        plt.hist(interpolated_values[:, len(average_arousal)//2], bins=10, alpha=0.5, label='Middle')
        plt.hist(interpolated_values[:, -1], bins=10, alpha=0.5, label='End')
        plt.xlabel("Arousal Value")
        plt.ylabel("Frequency")
        plt.title("Histograms of Arousal Values at Start, Middle, and End")
        plt.legend()
        plt.savefig(os.path.join(output_dir, "arousal_histograms.png"))
        plt.close()
        # --- Debugging code ends here ---

        # Print key statistics
        print("\nKey Statistics:")
        print(f"Average arousal at start: {average_arousal[0]:.2f}%")
        print(f"Average arousal at middle: {average_arousal[len(average_arousal)//2]:.2f}%")
        print(f"Average arousal at end: {average_arousal[-1]:.2f}%")
        
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
        
        time_axis = np.arange(FIXED_TIMELINE_SECONDS)
        
        # Create a twin axis for the line plots
        ax2 = ax.twinx()
        
        # Overlay average arousal