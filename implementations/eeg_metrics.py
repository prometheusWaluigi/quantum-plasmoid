"""
EEG Metrics for ORCHARD Theorem Validation
------------------------------------------
Implements CAP (Consistency-Availability-Partition tolerance) metrics
and microstate analysis to identify qualia emergence in EEG data.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.ndimage import gaussian_filter1d
import mne

class CAPMetrics:
    """
    Implements CAP metrics calculation (Consistency, Availability, Partition-tolerance)
    for EEG data analysis.
    """
    
    def __init__(self, eeg_analyzer):
        """
        Initialize with reference to the EEG analyzer.
        
        Parameters:
        -----------
        eeg_analyzer : ORCHARDAnalyzer
            Reference to the EEG analyzer
        """
        self.analyzer = eeg_analyzer
    
    def compute_cap_metrics(self, epochs, sfreq=None):
        """
        Compute CAP metrics (Consistency, Availability, Partition-tolerance).
        
        Parameters:
        -----------
        epochs : mne.Epochs or ndarray
            EEG epochs (channels x time) or raw data
        sfreq : float, optional
            Sampling frequency (required if epochs is ndarray)
            
        Returns:
        --------
        cap_metrics : dict
            Dictionary with CAP metrics
        """
        if isinstance(epochs, mne.Epochs):
            data = epochs.get_data()
            sfreq = epochs.info['sfreq']
        else:
            data = epochs
            if sfreq is None:
                sfreq = self.analyzer.fs
                
        n_epochs, n_channels, n_times = data.shape
        
        # Initialize metrics
        consistency = np.zeros((n_epochs, n_channels))
        availability = np.zeros((n_epochs, n_channels))
        partition_tolerance = np.zeros((n_epochs, n_channels))
        
        for e in range(n_epochs):
            for c in range(n_channels):
                signal = data[e, c, :]
                
                # Consistency (C): Autocorrelation at lag-1
                acf = np.correlate(signal, signal, mode='full') / np.sum(signal**2)
                acf = acf[len(acf)//2:]  # Keep only positive lags
                consistency[e, c] = acf[1]  # Lag-1 autocorrelation
                
                # Availability (A): Shannon entropy (normalized)
                # Convert to histogram
                hist, _ = np.histogram(signal, bins=20, density=True)
                hist = hist / np.sum(hist)
                hist = hist[hist > 0]  # Remove zeros
                availability[e, c] = entropy(hist) / np.log(len(hist))
                
                # Partition-tolerance (P): Signal robustness to noise
                # Add Gaussian noise and measure effect on FD
                noise_level = 0.1 * np.std(signal)
                noisy_signal = signal + np.random.normal(0, noise_level, len(signal))
                
                fd_original = self.analyzer.compute_higuchi_fd(signal)
                fd_noisy = self.analyzer.compute_higuchi_fd(noisy_signal)
                
                # Measure relative change (lower is better = higher P)
                if fd_original > 0:
                    rel_change = np.abs(fd_noisy - fd_original) / fd_original
                    partition_tolerance[e, c] = np.exp(-rel_change)  # Transform to [0, 1]
                else:
                    partition_tolerance[e, c] = 0
                    
        # Average over channels
        c_mean = np.mean(consistency, axis=1)
        a_mean = np.mean(availability, axis=1)
        p_mean = np.mean(partition_tolerance, axis=1)
        
        # Epoch-wise metrics
        cap_metrics = {
            'consistency': consistency,
            'availability': availability,
            'partition_tolerance': partition_tolerance,
            'c_mean': c_mean,
            'a_mean': a_mean,
            'p_mean': p_mean,
            'c_global': np.mean(c_mean),
            'a_global': np.mean(a_mean),
            'p_global': np.mean(p_mean)
        }
        
        return cap_metrics
    
    def classify_qualia_type(self, cap_metrics, fd_value):
        """
        Classify qualia type based on CAP metrics and fractal dimension.
        
        Parameters:
        -----------
        cap_metrics : dict
            Dictionary with CAP metrics
        fd_value : float
            Fractal dimension value
            
        Returns:
        --------
        qualia_type : str
            Classified qualia type
        confidence : float
            Confidence level (0-1)
        """
        # Extract metrics
        c = cap_metrics['c_global']
        a = cap_metrics['a_global']
        p = cap_metrics['p_global']
        
        # Sensory qualia: High C, med A, low P, FD≈1.45
        sensory_match = (c > 0.6) and (0.3 < a < 0.5) and (p < 0.3) and (abs(fd_value - 1.45) < 0.1)
        
        # Emotional qualia: High A, low C, med P, FD≈1.6
        emotional_match = (a > 0.6) and (c < 0.3) and (0.3 < p < 0.5) and (abs(fd_value - 1.6) < 0.1)
        
        # Cognitive qualia: Balanced CAP, FD≈1.5
        cognitive_match = (0.3 < c < 0.5) and (0.3 < a < 0.5) and (0.3 < p < 0.5) and (abs(fd_value - 1.5) < 0.05)
        
        # Determine type and confidence
        if sensory_match and not emotional_match and not cognitive_match:
            return "Sensory", 0.8
        elif emotional_match and not sensory_match and not cognitive_match:
            return "Emotional", 0.8
        elif cognitive_match and not sensory_match and not emotional_match:
            return "Cognitive", 0.8
        else:
            # Compute weighted match
            weights = {'Sensory': 0.0, 'Emotional': 0.0, 'Cognitive': 0.0}
            
            # Sensory weight
            if c > 0.6:
                weights['Sensory'] += 0.4
            if 0.3 < a < 0.5:
                weights['Sensory'] += 0.3
            if p < 0.3:
                weights['Sensory'] += 0.3
                
            # Apply FD factor
            weights['Sensory'] *= max(0, 1 - abs(fd_value - 1.45) * 5)
            
            # Emotional weight
            if a > 0.6:
                weights['Emotional'] += 0.4
            if c < 0.3:
                weights['Emotional'] += 0.3
            if 0.3 < p < 0.5:
                weights['Emotional'] += 0.3
                
            # Apply FD factor
            weights['Emotional'] *= max(0, 1 - abs(fd_value - 1.6) * 5)
            
            # Cognitive weight
            if 0.3 < c < 0.5:
                weights['Cognitive'] += 0.33
            if 0.3 < a < 0.5:
                weights['Cognitive'] += 0.33
            if 0.3 < p < 0.5:
                weights['Cognitive'] += 0.34
                
            # Apply FD factor
            weights['Cognitive'] *= max(0, 1 - abs(fd_value - 1.5) * 7)
            
            # Find highest weight
            qualia_type = max(weights, key=weights.get)
            confidence = weights[qualia_type]
            
            return qualia_type, confidence
    
    def plot_cap_balance(self, cap_metrics, condition=None):
        """
        Plot CAP balance.
        
        Parameters:
        -----------
        cap_metrics : dict
            Dictionary with CAP metrics
        condition : str, optional
            Condition name for title
            
        Returns:
        --------
        fig : matplotlib.figure.Figure
            Figure object
        """
        # Get epoch-wise CAP values
        c_mean = cap_metrics['c_mean']
        a_mean = cap_metrics['a_mean']
        p_mean = cap_metrics['p_mean']
        
        n_epochs = len(c_mean)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        width = 0.25
        x = np.arange(n_epochs)
        
        ax.bar(x - width, c_mean, width, label='Consistency')
        ax.bar(x, a_mean, width, label='Availability')
        ax.bar(x + width, p_mean, width, label='Partition-tolerance')
        
        # Add labels
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Value')
        ax.set_title(f'CAP Balance{" - " + condition if condition else ""}')
        ax.set_xticks(x)
        ax.set_xticklabels([str(i+1) for i in range(n_epochs)])
        ax.legend()
        
        return fig


class MicrostateAnalyzer:
    """
    Implements microstate analysis for EEG data.
    """
    
    def __init__(self, eeg_analyzer):
        """
        Initialize with reference to the EEG analyzer.
        
        Parameters:
        -----------
        eeg_analyzer : ORCHARDAnalyzer
            Reference to the EEG analyzer
        """
        self.analyzer = eeg_analyzer
    
    def extract_microstates(self, epochs, n_states=4):
        """
        Extract EEG microstates using k-means clustering.
        
        Parameters:
        -----------
        epochs : mne.Epochs
            EEG epochs
        n_states : int
            Number of microstates to extract
            
        Returns:
        --------
        microstates : dict
            Dictionary with microstate templates and assignments
        """
        # Get data and reshape
        data = epochs.get_data()
        n_epochs, n_channels, n_times = data.shape
        X = data.reshape(n_epochs * n_times, n_channels).T  # channels x (epochs*times)
        
        # Normalize (GFP-normalized maps)
        X_norm = X / np.sqrt(np.sum(X**2, axis=0))
        
        # Run PCA for dimensionality reduction
        pca = PCA(n_components=min(15, n_channels))
        X_pca = pca.fit_transform(X_norm.T).T
        
        # K-means clustering
        kmeans = KMeans(n_clusters=n_states, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_pca.T)
        
        # Get template maps for each microstate
        templates = kmeans.cluster_centers_
        templates = pca.inverse_transform(templates).T  # channels x states
        
        # Reshape labels back to epochs x times
        labels = labels.reshape(n_epochs, n_times)
        
        # Calculate microstate metrics
        duration = np.zeros((n_epochs, n_states))
        occurrence = np.zeros((n_epochs, n_states))
        coverage = np.zeros((n_epochs, n_states))
        
        for e in range(n_epochs):
            for s in range(n_states):
                # Get indices for this state
                indices = np.where(labels[e, :] == s)[0]
                
                if len(indices) == 0:
                    continue
                    
                # Calculate duration
                diff = np.diff(indices)
                runs = np.split(indices, np.where(diff > 1)[0] + 1)
                duration[e, s] = np.mean([len(r) for r in runs]) / epochs.info['sfreq'] * 1000  # ms
                
                # Calculate occurrence
                occurrence[e, s] = len(runs) / (n_times / epochs.info['sfreq'])  # per second
                
                # Calculate coverage
                coverage[e, s] = len(indices) / n_times
                
        # Calculate transition matrix
        transition_matrix = np.zeros((n_states, n_states))
        
        for e in range(n_epochs):
            for t in range(n_times - 1):
                from_state = labels[e, t]
                to_state = labels[e, t + 1]
                
                if from_state != to_state:
                    transition_matrix[from_state, to_state] += 1
                    
        # Normalize transition matrix
        row_sums = transition_matrix.sum(axis=1, keepdims=True)
        transition_matrix = np.divide(transition_matrix, row_sums, 
                                     where=row_sums!=0)
        
        microstates = {
            'templates': templates,
            'labels': labels,
            'duration': duration,
            'occurrence': occurrence,
            'coverage': coverage,
            'transition_matrix': transition_matrix
        }
        
        return microstates
    
    def correlate_microstates_with_fd(self, microstates, fd_values, epochs):
        """
        Correlate microstate transitions with fractal dimension.
        
        Parameters:
        -----------
        microstates : dict
            Dictionary with microstate information
        fd_values : ndarray
            Fractal dimension values (epochs x channels x windows)
        epochs : mne.Epochs
            EEG epochs
            
        Returns:
        --------
        correlation : dict
            Dictionary with correlation results
        """
        labels = microstates['labels']
        n_epochs, n_times = labels.shape
        n_states = len(microstates['duration'][0])
        
        # Compute mean FD across channels
        fd_mean = np.mean(fd_values, axis=1)  # epochs x windows
        
        # Interpolate FD to match microstate time resolution
        fd_interp = np.zeros((n_epochs, n_times))
        for e in range(n_epochs):
            # Create interpolation function
            x_orig = np.linspace(0, 1, fd_mean.shape[1])
            x_new = np.linspace(0, 1, n_times)
            fd_interp[e, :] = np.interp(x_new, x_orig, fd_mean[e, :])
            
        # Find microstate transitions
        transitions = np.zeros((n_epochs, n_times), dtype=bool)
        for e in range(n_epochs):
            transitions[e, 1:] = labels[e, 1:] != labels[e, :-1]
            
        # Window around transitions
        window_size = 30  # samples
        fd_around_transitions = []
        
        for e in range(n_epochs):
            trans_indices = np.where(transitions[e, :])[0]
            
            for idx in trans_indices:
                start = max(0, idx - window_size // 2)
                end = min(n_times, idx + window_size // 2)
                
                # Center and align
                segment = fd_interp[e, start:end]
                
                if len(segment) == window_size:
                    fd_around_transitions.append(segment)
                    
        # Convert to array
        if fd_around_transitions:
            fd_around_transitions = np.array(fd_around_transitions)
            
            # Compute mean and std
            fd_mean_around_trans = np.mean(fd_around_transitions, axis=0)
            fd_std_around_trans = np.std(fd_around_transitions, axis=0)
            
            # Center of window
            center = window_size // 2
            
            # Check if FD peaks around transitions
            pre_trans = np.mean(fd_mean_around_trans[:center])
            post_trans = np.mean(fd_mean_around_trans[center:])
            at_trans = fd_mean_around_trans[center]
            
            # Compute state-to-state correlation
            state_pairs = []
            fd_at_transitions = []
            
            for e in range(n_epochs):
                for t in range(1, n_times):
                    if transitions[e, t]:
                        from_state = labels[e, t-1]
                        to_state = labels[e, t]
                        fd_val = fd_interp[e, t]
                        
                        state_pairs.append((from_state, to_state))
                        fd_at_transitions.append(fd_val)
            
            correlation = {
                'fd_around_transitions': fd_around_transitions,
                'fd_mean_around_trans': fd_mean_around_trans,
                'fd_std_around_trans': fd_std_around_trans,
                'pre_trans_fd': pre_trans,
                'at_trans_fd': at_trans,
                'post_trans_fd': post_trans,
                'state_pairs': state_pairs,
                'fd_at_transitions': fd_at_transitions
            }
        else:
            correlation = {
                'fd_around_transitions': None
            }
            
        return correlation
    
    def plot_microstate_topographies(self, microstates, epochs, condition=None):
        """
        Plot microstate topographic maps.
        
        Parameters:
        -----------
        microstates : dict
            Dictionary with microstate information
        epochs : mne.Epochs
            EEG epochs
        condition : str, optional
            Condition name for title
            
        Returns:
        --------
        fig : matplotlib.figure.Figure
            Figure object
        """
        templates = microstates['templates']
        n_states = templates.shape[1]
        
        # Create figure
        fig, axes = plt.subplots(1, n_states, figsize=(4 * n_states, 4))
        
        # Create montage info
        info = epochs.info
        
        # Plot each microstate
        for s in range(n_states):
            map_data = templates[:, s]
            
            if n_states == 1:
                ax = axes
            else:
                ax = axes[s]
                
            mne.viz.plot_topomap(map_data, info, axes=ax, show=False)
            ax.set_title(f'Microstate {s+1}')
            
        fig.suptitle(f'Microstate Topographies{" - " + condition if condition else ""}')
        plt.tight_layout()
        
        return fig
