"""
EEG Analysis Pipeline for ORCHARD Theorem Validation
----------------------------------------------------
Core implementation of the EEG analysis pipeline for testing ORCHARD theorem 
predictions, focusing on fractal dimension calculation and CAP metrics extraction.
"""

import numpy as np
import scipy.signal as sig
import mne
from mne.preprocessing import ICA
from mne_bids import BIDSPath, read_raw_bids
import pandas as pd
from scipy.stats import entropy
from scipy.ndimage import gaussian_filter1d
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import networkx as nx
from pathlib import Path
import warnings

# Configure MNE
mne.set_log_level('WARNING')
warnings.filterwarnings('ignore', category=RuntimeWarning)

class ORCHARDAnalyzer:
    """
    Implements analysis methods for validating ORCHARD theorem predictions
    using EEG data.
    """
    
    def __init__(self, sampling_rate=1000, window_size=500, window_overlap=0.5):
        """
        Initialize the analyzer with parameters.
        
        Parameters:
        -----------
        sampling_rate : int
            Sampling rate in Hz
        window_size : int
            Window size for sliding window analysis in ms
        window_overlap : float
            Overlap between consecutive windows (0-1)
        """
        self.fs = sampling_rate
        self.window_size = window_size
        self.window_overlap = window_overlap
        self.window_samples = int(window_size * sampling_rate / 1000)
        self.step_samples = int(self.window_samples * (1 - window_overlap))
        
    def load_bids_data(self, bids_root, subject, task, session=None, run=None):
        """
        Load EEG data from BIDS-formatted dataset.
        
        Parameters:
        -----------
        bids_root : str
            Path to BIDS dataset root
        subject : str
            Subject ID
        task : str
            Task name
        session : str, optional
            Session ID
        run : str, optional
            Run number
            
        Returns:
        --------
        raw : mne.io.Raw
            Raw EEG data
        """
        bids_path = BIDSPath(
            root=bids_root,
            subject=subject,
            task=task,
            session=session,
            run=run,
            suffix='eeg',
            extension='.edf'
        )
        
        raw = read_raw_bids(bids_path=bids_path, verbose=False)
        return raw
    
    def preprocess(self, raw, filter_range=(0.5, 45), ica_components=20, 
                   reference='average', apply_laplacian=True):
        """
        Preprocess raw EEG data.
        
        Parameters:
        -----------
        raw : mne.io.Raw
            Raw EEG data
        filter_range : tuple
            (high_pass, low_pass) filter cutoff frequencies
        ica_components : int
            Number of ICA components to extract
        reference : str
            Reference to use ('average' or None)
        apply_laplacian : bool
            Whether to apply surface Laplacian transform
            
        Returns:
        --------
        processed : mne.io.Raw
            Preprocessed EEG data
        """
        # Copy to avoid modifying original
        processed = raw.copy()
        
        # Filter
        processed.filter(filter_range[0], filter_range[1], 
                         method='fir', phase='zero-double')
        
        # Re-reference
        if reference:
            processed.set_eeg_reference(reference, projection=False)
        
        # Run ICA for artifact removal
        ica = ICA(n_components=ica_components, random_state=42)
        ica.fit(processed)
        
        # Auto-detect and remove eye blinks
        eog_indices, eog_scores = ica.find_bads_eog(processed)
        if eog_indices:
            ica.exclude = eog_indices
        
        ica.apply(processed)
        
        # Apply surface Laplacian for improved spatial resolution
        if apply_laplacian:
            processed = mne.preprocessing.compute_current_source_density(processed)
        
        return processed
    
    def extract_epochs(self, raw, events, event_ids, tmin=-0.2, tmax=1.0):
        """
        Extract epochs from continuous data.
        
        Parameters:
        -----------
        raw : mne.io.Raw
            Preprocessed EEG data
        events : ndarray
            Events array (N x 3)
        event_ids : dict
            Dictionary mapping event names to IDs
        tmin : float
            Start time of epoch relative to event
        tmax : float
            End time of epoch relative to event
            
        Returns:
        --------
        epochs : mne.Epochs
            Extracted epochs
        """
        epochs = mne.Epochs(raw, events, event_id=event_ids, tmin=tmin, tmax=tmax, 
                            baseline=(tmin, 0), preload=True)
        return epochs
    
    def compute_higuchi_fd(self, signal, kmax=10):
        """
        Compute Higuchi Fractal Dimension of a signal.
        
        Parameters:
        -----------
        signal : ndarray
            1D signal
        kmax : int
            Maximum k value
            
        Returns:
        --------
        hfd : float
            Higuchi Fractal Dimension
        """
        N = len(signal)
        L = np.zeros(kmax)
        x = np.arange(1, kmax + 1)
        
        for k in range(1, kmax + 1):
            Lk = np.zeros(k)
            
            for m in range(k):
                indices = np.arange(m, N, k)
                Lmk = np.sum(np.abs(np.diff(signal[indices])))
                Lmk = Lmk * (N - 1) / (((N - m) // k) * k) / k
                Lk[m] = Lmk
                
            L[k-1] = np.mean(Lk)
            
        # Linear regression on log-log scale
        log_x = np.log(x)
        log_L = np.log(L)
        
        # Fit line: log(L) = -D * log(k) + b
        A = np.vstack([log_x, np.ones(len(log_x))]).T
        D, b = np.linalg.lstsq(A, log_L, rcond=None)[0]
        
        return -D  # Negative slope is the dimension
    
    def compute_box_counting_fd(self, signal, epsilons=None):
        """
        Compute Box-Counting Fractal Dimension of a signal.
        
        Parameters:
        -----------
        signal : ndarray
            1D signal
        epsilons : ndarray, optional
            Array of box sizes
            
        Returns:
        --------
        fd : float
            Box-Counting Fractal Dimension
        """
        if epsilons is None:
            epsilons = np.logspace(-3, 0, 20)
            
        # Normalize signal to [0, 1]
        sig_min = np.min(signal)
        sig_max = np.max(signal)
        if sig_max > sig_min:
            normalized = (signal - sig_min) / (sig_max - sig_min)
        else:
            return 1.0  # Not fractal
        
        # Count boxes at different scales
        N = np.zeros(len(epsilons))
        
        for i, eps in enumerate(epsilons):
            # Count boxes needed to cover the signal
            boxes = np.ceil(normalized / eps)
            N[i] = len(np.unique(boxes))
            
        # Linear regression on log-log scale
        log_eps = np.log(epsilons)
        log_N = np.log(N)
        
        # Fit line: log(N) = -D * log(eps) + b
        A = np.vstack([log_eps, np.ones(len(log_eps))]).T
        D, b = np.linalg.lstsq(A, log_N, rcond=None)[0]
        
        return -D  # Negative slope is the dimension
    
    def compute_dfa(self, signal, scales=None):
        """
        Compute Detrended Fluctuation Analysis.
        
        Parameters:
        -----------
        signal : ndarray
            1D signal
        scales : ndarray, optional
            Array of window sizes
            
        Returns:
        --------
        alpha : float
            DFA scaling exponent
        """
        if scales is None:
            scales = np.logspace(1, np.log10(len(signal) // 4), 20).astype(int)
            
        # Compute cumulative sum of mean-subtracted signal
        y = np.cumsum(signal - np.mean(signal))
        
        # Compute fluctuation at different scales
        F = np.zeros(len(scales))
        
        for i, scale in enumerate(scales):
            # Number of windows
            num_windows = len(y) // scale
            
            if num_windows < 1:
                continue
                
            # Reshape signal into windows
            windows = y[:num_windows * scale].reshape((num_windows, scale))
            
            # Compute local trend (polynomial fit)
            x = np.arange(scale)
            X = np.vstack([x, np.ones(len(x))]).T
            
            # Compute fluctuation for each window
            fluctuation = np.zeros(num_windows)
            
            for j in range(num_windows):
                # Fit linear trend
                a, b = np.linalg.lstsq(X, windows[j], rcond=None)[0]
                trend = a * x + b
                
                # Compute RMS fluctuation
                fluctuation[j] = np.sqrt(np.mean((windows[j] - trend) ** 2))
                
            F[i] = np.mean(fluctuation)
            
        # Linear regression on log-log scale
        valid = F > 0  # Avoid log(0)
        log_scales = np.log(scales[valid])
        log_F = np.log(F[valid])
        
        # Fit line: log(F) = alpha * log(scale) + b
        A = np.vstack([log_scales, np.ones(len(log_scales))]).T
        alpha, b = np.linalg.lstsq(A, log_F, rcond=None)[0]
        
        return alpha
