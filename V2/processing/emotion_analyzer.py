"""
Emotion Tracking Data Analyzer V2
=================================

This script processes emotion tracking data from Morphcast and generates comprehensive reports.
Features:
- 60-second fixed timeline normalization
- Advanced heatmap visualizations
- Cross-participant analysis
- Professional reporting
- Multiple export formats

Author: Emotion Tracking V2 System
"""

import os
import json
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import interpolate
from scipy.signal import savgol_filter
from scipy.stats import zscore
from matplotlib.patches import Rectangle, Patch
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class EmotionAnalyzer:
    def __init__(self, config_path=None):
        """
        Initialize the Emotion Analyzer with configuration.
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.data_cache = {}
        self.analysis_results = {}
        
        # Set up matplotlib for high-quality plots
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        
    def _load_config(self, config_path):
        """Load configuration or use defaults."""
        default_config = {
            'FIXED_TIMELINE_SECONDS': 60,
            'OUTPUT_FORMAT': 'png',
            'FIGURE_SIZE': (19.2, 10.8),
            'HEATMAP_COLORS': 'YlOrRd',
            'SMOOTHING_WINDOW': 11,
            'HIGH_AROUSAL_THRESHOLD': 75,
            'NORMALIZATION_RANGE': (-1, 1),
            'EXPORT_FORMATS': ['csv', 'xlsx', 'json']
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
            default_config.update(user_config)
            
        return default_config
    
    def normalize_value(self, value, min_val=-1, max_val=1):
        """Normalize values to 0-100% scale."""
        if value is None or np.isnan(value):
            return np.nan
        return 100 * (value - min_val) / (max_val - min_val)
    
    def load_participant_data(self, file_path):
        """Load and parse participant data from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Handle different data formats
            if 'trackingData' in data:
                tracking_data = data['trackingData']
                metadata = data.get('metadata', {})
            elif isinstance(data, list):
                tracking_data = data
                metadata = {}
            else:
                tracking_data = data
                metadata = {}
            
            # Extract metrics
            arousal_values = []
            valence_values = []
            attention_values = []
            emotion_data = []
            
            for entry in tracking_data:
                if 'mediaTime' in entry:
                    media_time = entry['mediaTime']
                    
                    if entry.get('type') == 'FACE_AROUSAL_VALENCE':
                        arousal_values.append({
                            'time': media_time,
                            'value': self.normalize_value(entry.get('arousal', 0))
                        })
                        valence_values.append({
                            'time': media_time,
                            'value': self.normalize_value(entry.get('valence', 0))
                        })
                    
                    elif entry.get('type') == 'FACE_ATTENTION':
                        attention_values.append({
                            'time': media_time,
                            'value': entry.get('attention', 0) * 100
                        })
                    
                    elif entry.get('type') == 'FACE_EMOTION':
                        emotion_data.append({
                            'time': media_time,
                            'dominant': entry.get('dominantEmotion', 'Unknown'),
                            'emotions': entry.get('emotions', {})
                        })
            
            return {
                'participant_id': os.path.splitext(os.path.basename(file_path))[0],
                'arousal': arousal_values,
                'valence': valence_values,
                'attention': attention_values,
                'emotions': emotion_data,
                'metadata': metadata,
                'raw_data': tracking_data
            }
            
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def interpolate_to_fixed_timeline(self, data_points, timeline_seconds=None):
        """Interpolate data to fixed timeline."""
        if timeline_seconds is None:
            timeline_seconds = self.config['FIXED_TIMELINE_SECONDS']
        
        if not data_points:
            return np.full(timeline_seconds, np.nan)
        
        # Extract times and values
        times = [point['time'] for point in data_points]
        values = [point['value'] for point in data_points]
        
        # Create fixed timeline
        fixed_timeline = np.arange(timeline_seconds)
        
        if len(times) == 1:
            # Single data point - use constant value
            interpolated = np.full(timeline_seconds, values[0])
        else:
            # Interpolate data
            f = interpolate.interp1d(
                times, values, 
                kind='linear', 
                bounds_error=False, 
                fill_value=(values[0], values[-1])
            )
            interpolated = f(fixed_timeline)
        
        # Set values to NaN after the last actual data point
        if times:
            last_time = int(max(times))
            if last_time < timeline_seconds - 1:
                interpolated[last_time + 1:] = np.nan
        
        return interpolated
    
    def process_participant(self, participant_data):
        """Process individual participant data."""
        if not participant_data:
            return None
        
        # Interpolate metrics to fixed timeline
        arousal_timeline = self.interpolate_to_fixed_timeline(participant_data['arousal'])
        valence_timeline = self.interpolate_to_fixed_timeline(participant_data['valence'])
        attention_timeline = self.interpolate_to_fixed_timeline(participant_data['attention'])
        
        # Calculate engagement metrics
        engagement_score = np.nanmean([
            np.nanmean(arousal_timeline),
            np.nanmean(attention_timeline)
        ])
        
        # Identify high arousal moments
        high_arousal_moments = np.where(arousal_timeline > self.config['HIGH_AROUSAL_THRESHOLD'])[0]
        
        return {
            'participant_id': participant_data['participant_id'],
            'arousal_timeline': arousal_timeline,
            'valence_timeline': valence_timeline,
            'attention_timeline': attention_timeline,
            'engagement_score': engagement_score,
            'high_arousal_moments': high_arousal_moments,
            'metadata': participant_data['metadata']
        }
    
    def create_individual_report(self, processed_data, output_dir):
        """Create individual participant report."""
        participant_id = processed_data['participant_id']
        
        # Create figure with subplots
        fig, axes = plt.subplots(3, 1, figsize=self.config['FIGURE_SIZE'])
        fig.suptitle(f'Emotion Tracking Report - {participant_id}', fontsize=16, fontweight='bold')
        
        timeline = np.arange(self.config['FIXED_TIMELINE_SECONDS'])
        
        # Arousal plot
        axes[0].plot(timeline, processed_data['arousal_timeline'], 
                    color='red', linewidth=2, label='Arousal')
        axes[0].set_title('Arousal Over Time')
        axes[0].set_ylabel('Arousal (%)')
        axes[0].set_ylim(0, 100)
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        
        # Valence plot
        axes[1].plot(timeline, processed_data['valence_timeline'], 
                    color='orange', linewidth=2, label='Valence')
        axes[1].set_title('Valence Over Time')
        axes[1].set_ylabel('Valence (%)')
        axes[1].set_ylim(0, 100)
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
        
        # Attention plot
        axes[2].plot(timeline, processed_data['attention_timeline'], 
                    color='cyan', linewidth=2, label='Attention')
        axes[2].set_title('Attention Over Time')
        axes[2].set_ylabel('Attention (%)')
        axes[2].set_xlabel('Time (seconds)')
        axes[2].set_ylim(0, 100)
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()
        
        # Format x-axis for all plots
        for ax in axes:
            ax.set_xlim(0, self.config['FIXED_TIMELINE_SECONDS'])
            ax.set_xticks(np.arange(0, self.config['FIXED_TIMELINE_SECONDS'] + 1, 5))
        
        plt.tight_layout()
        
        # Save individual report
        output_path = os.path.join(output_dir, f"{participant_id}_individual_report.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Individual report saved: {output_path}")
        return output_path
    
    def create_heatmap_analysis(self, all_processed_data, output_dir):
        """Create comprehensive heatmap analysis."""
        if not all_processed_data:
            return None
        
        # Prepare data for heatmap
        arousal_matrix = []
        participant_ids = []
        
        for data in all_processed_data:
            arousal_matrix.append(data['arousal_timeline'])
            participant_ids.append(data['participant_id'])
        
        arousal_matrix = np.array(arousal_matrix)
        
        # Calculate statistics
        average_arousal = np.nanmean(arousal_matrix, axis=0)
        std_arousal = np.nanstd(arousal_matrix, axis=0)
        
        # Apply smoothing
        window_length = min(self.config['SMOOTHING_WINDOW'], len(average_arousal) - 1)
        if window_length % 2 == 0:
            window_length -= 1
        if window_length >= 3:
            smoothed_arousal = savgol_filter(
                average_arousal, 
                window_length, 
                min(3, window_length - 1)
            )
        else:
            smoothed_arousal = average_arousal
        
        # Create comprehensive figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 12))
        
        # Heatmap
        im = ax1.imshow(arousal_matrix, cmap=self.config['HEATMAP_COLORS'], 
                       aspect='auto', vmin=0, vmax=100)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax1, aspect=30)
        cbar.set_label('Arousal (%)', rotation=270, labelpad=20)
        
        # Format heatmap
        ax1.set_title('Arousal Heatmap Across Participants', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Participants')
        ax1.set_yticks(range(len(participant_ids)))
        ax1.set_yticklabels([pid[:15] + '...' if len(pid) > 15 else pid for pid in participant_ids])
        ax1.set_xticks(np.arange(0, self.config['FIXED_TIMELINE_SECONDS'] + 1, 5))
        ax1.set_xticklabels(np.arange(0, self.config['FIXED_TIMELINE_SECONDS'] + 1, 5))
        
        # Summary statistics plot
        timeline = np.arange(self.config['FIXED_TIMELINE_SECONDS'])
        
        ax2.fill_between(timeline, 
                        average_arousal - std_arousal, 
                        average_arousal + std_arousal, 
                        alpha=0.3, color='red', label='±1 Standard Deviation')
        
        ax2.plot(timeline, average_arousal, 
                color='red', linewidth=3, label='Average Arousal')
        ax2.plot(timeline, smoothed_arousal, 
                color='blue', linewidth=2, linestyle='--', label='Smoothed Trend')
        
        # Highlight high arousal moments
        high_moments = np.where(average_arousal > self.config['HIGH_AROUSAL_THRESHOLD'])[0]
        if len(high_moments) > 0:
            ax2.scatter(high_moments, average_arousal[high_moments], 
                       color='orange', s=50, zorder=5, label='High Arousal Moments')
        
        ax2.set_title('Summary Statistics', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Arousal (%)')
        ax2.set_ylim(0, 100)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        
        # Save heatmap
        output_path = os.path.join(output_dir, "arousal_heatmap_analysis.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Heatmap analysis saved: {output_path}")
        return output_path
    
    def analyze_directory(self, input_dir, output_dir=None):
        """Analyze all JSON files in a directory."""
        if output_dir is None:
            output_dir = os.path.join(input_dir, "analysis_results")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all JSON files
        json_files = glob.glob(os.path.join(input_dir, "*.json"))
        
        if not json_files:
            print(f"No JSON files found in {input_dir}")
            return None
        
        print(f"Found {len(json_files)} JSON files")
        
        # Process all participants
        all_processed_data = []
        failed_files = []
        
        for json_file in json_files:
            print(f"Processing: {os.path.basename(json_file)}")
            
            # Load participant data
            participant_data = self.load_participant_data(json_file)
            if not participant_data:
                failed_files.append(json_file)
                continue
            
            # Process participant
            processed_data = self.process_participant(participant_data)
            if processed_data:
                all_processed_data.append(processed_data)
                
                # Create individual report
                self.create_individual_report(processed_data, output_dir)
        
        if not all_processed_data:
            print("No valid data processed")
            return None
        
        print(f"Successfully processed {len(all_processed_data)} participants")
        if failed_files:
            print(f"Failed to process {len(failed_files)} files")
        
        # Create heatmap analysis
        self.create_heatmap_analysis(all_processed_data, output_dir)
        
        return {
            'processed_participants': len(all_processed_data),
            'failed_files': failed_files,
            'output_directory': output_dir
        }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Emotion Tracking Data Analyzer V2')
    parser.add_argument('input_dir', help='Input directory containing JSON files')
    parser.add_argument('--output-dir', '-o', help='Output directory for results')
    parser.add_argument('--config', '-c', help='Configuration file path')
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = EmotionAnalyzer(args.config)
    
    # Analyze directory
    results = analyzer.analyze_directory(args.input_dir, args.output_dir)
    
    if results:
        print(f"\nAnalysis complete!")
        print(f"Results saved to: {results['output_directory']}")
        print(f"Processed {results['processed_participants']} participants")
    else:
        print("Analysis failed") 