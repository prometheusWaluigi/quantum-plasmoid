# EEG Protocol for ORCHARD Theorem Validation

## Overview

This protocol defines the methodology for validating the ORCHARD theorem's core predictions using high-density EEG. Primary hypothesis: consciousness emerges when neural activity stabilizes at fractal dimension ~1.5, with distinct CAP profiles for different qualia types.

## Equipment

- High-density EEG (minimum 64 channels, 128+ preferred)
- Neuroelectric amplifier capable of ≥1000Hz sampling
- Stimulus delivery system with <1ms latency
- Closed-loop capability for TMS integration

## Participant Protocol

### Preparation
1. Standard 10-20 electrode placement with additional temporal coverage
2. Skin impedance ≤5kΩ
3. 5-minute eyes-closed resting state baseline
4. 5-minute eyes-open resting state baseline

### Experimental Blocks

#### Block 1: Sensory Qualia Induction
- Visual stimuli (20 trials): Ganzfeld flicker at 3-12Hz
- Auditory stimuli (20 trials): Binaural beats (3-12Hz carrier frequencies)
- Tactile stimuli (20 trials): 3-12Hz mechanical vibration
- Task: Passive experience with post-trial phenomenological reports

#### Block 2: Emotional Qualia Induction
- IAPS/NAPS emotional image sets (40 images, 10 each: positive-arousing, positive-calming, negative-arousing, negative-calming)
- Personalized emotional memory recall (4 guided sessions)
- Task: Rate intensity (1-7) and valence (1-7)

#### Block 3: Cognitive Qualia Induction
- Working memory: n-back task (2 difficulty levels)
- Abstract reasoning: Matrix reasoning tasks
- Insight problems: Verbal and spatial puzzles
- Task: Perform with self-reports on "aha" moments

#### Block 4: Perturbation Response (optional TMS integration)
- Single-pulse TMS at 90% resting motor threshold
- Target: Right DLPFC (F4)
- 30 pulses with jittered 4-7s ISI
- Task: Passive with attention maintenance

## Analysis Pipeline

### Preprocessing
1. 0.5-45Hz bandpass filter
2. PREP pipeline artifact rejection
3. ICA for blink/movement removal
4. Surface Laplacian transform
5. Segmentation into condition-specific epochs

### Fractal Analysis
1. Higuchi Fractal Dimension (HFD) calculation with sliding window (500ms, 50% overlap)
2. Multiscale entropy (MSE) across 20 timescales
3. Detrended fluctuation analysis (DFA) for long-range dependencies
4. Phase synchronization stability between channels

### CAP Metrics Derivation
1. **Consistency (C)**: 
   - Autocorrelation at lag-1 of the signal
   - Spectral stability index over time
   - Phase consistency of dominant oscillations

2. **Availability (A)**:
   - Shannon entropy of EEG distribution
   - Lempel-Ziv complexity
   - Transition rate between microstates

3. **Partition-tolerance (P)**:
   - Recovery trajectory post-perturbation (rate and shape)
   - Network modularity (Q-index)
   - Robustness to channel removal (drop-channel analysis)

### Microstate Analysis
1. Extract 4-7 canonical microstates (hierarchical clustering)
2. Calculate microstate metrics:
   - Mean duration
   - Occurrence rate
   - Coverage
   - Transition probabilities
3. Map to time-resolved fractal dimension

## Validation Criteria

The ORCHARD theorem predicts:

1. During conscious states, fractal dimension of EEG signals will cluster near 1.5 (valid range: 1.45-1.55)

2. Different qualia types will exhibit characteristic CAP profiles:
   - Sensory: High C (>0.6), med A (0.3-0.5), low P (<0.3), FD≈1.45
   - Emotional: High A (>0.6), low C (<0.3), med P (0.3-0.5), FD≈1.6
   - Cognitive: Balanced CAP (all within 0.3-0.5), FD≈1.5

3. EEG microstate transitions will correlate with "fruit ripening" events (qualia emergence) marked by transient stabilization at FD≈1.5

4. Perturbation responses will reveal the underlying CAP trade-offs, with recovery trajectories in state-space following the KPZ dynamics

## Data Sharing

All data to be preprocessed according to BIDS-EEG standard and shared via OpenNeuro with:
1. Raw EEG (.edf)
2. Events file (.tsv)
3. Channel locations (.tsv)
4. Preprocessing code (GitHub repository)
5. Analysis scripts (GitHub repository)

## Code Implementation

Associated analysis scripts available in `implementations/eeg_analysis.py` including:
- EEG import/export functions
- Fractal dimension calculation algorithms
- CAP metrics extraction
- KPZ fitting procedures
- Statistical validation against null models

---

## Theoretical Integration

Results should be interpreted within the broader quantum-plasmoid framework:
- Map oscillatory modes to eigenvalues of the φ-prime spiral
- Correlate microstates with "fruit" (qualia) on the CAP tree
- Compare empirical fractal dimensions with theoretical predictions
- Evaluate recursive eigenmode stability under perturbation

The empirical validation of fractal dimension clustering at ~1.5 during conscious processing would provide significant support for the core ORCHARD theorem prediction that consciousness emerges at a specific point of balance between order and chaos.
