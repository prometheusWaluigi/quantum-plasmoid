"""
ORCHARD Theorem Implementation
(Optimal Recursive Computation of Harmonic Amplitude Recursive Dynamics)

This module implements the core concepts of the ORCHARD theorem for consciousness modeling,
focusing on:
1. CAP Pathway dynamics (Consistency, Availability, Partition-tolerance)
2. KPZ growth equation for neural branches
3. Fractal dimension analysis for qualia emergence
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
from scipy.signal import correlate
from numpy.random import default_rng

# Initialize random number generator
rng = default_rng(42)

class CAPPathway:
    """
    Represents a neural branch or CAP Pathway as described in the ORCHARD theorem.
    """
    def __init__(self, size=100, initial_activity=None, alpha_c=0.33, alpha_a=0.33, alpha_p=0.34):
        """
        Initialize a CAP Pathway with specified parameters.
        
        Parameters:
        -----------
        size : int
            Size of the neural pathway
        initial_activity : array-like or None
            Initial neural activity pattern. If None, random values are generated.
        alpha_c : float
            Weight for consistency (stability) in the cost function
        alpha_a : float
            Weight for availability (entropy) in the cost function
        alpha_p : float
            Weight for partition-tolerance (resilience) in the cost function
        """
        # Validate alpha parameters
        assert abs(alpha_c + alpha_a + alpha_p - 1.0) < 1e-10, "Alpha values must sum to 1"
        assert all(a >= 0 for a in [alpha_c, alpha_a, alpha_p]), "Alpha values must be non-negative"
        
        self.size = size
        self.alpha_c = alpha_c
        self.alpha_a = alpha_a
        self.alpha_p = alpha_p
        
        # Initialize neural activity
        if initial_activity is None:
            self.activity = rng.normal(0, 1, size)
        else:
            self.activity = np.array(initial_activity)
            if len(self.activity) != size:
                raise ValueError(f"Initial activity must have length {size}")
        
        # Activity history for tracking changes
        self.history = [self.activity.copy()]
        
        # KPZ parameters
        self.nu = 0.1  # Synaptic stability
        self.lambda_ = 0.05  # Hebbian plasticity
        self.noise_amplitude = 0.2  # Amplitude of stochastic fluctuations
        
    def compute_consistency(self):
        """
        Compute the consistency (C) factor using autocorrelation.
        Higher values indicate more stable firing patterns.
        """
        if len(self.history) < 2:
            return 1.0  # Maximum consistency if no history
        
        # Use the mean autocorrelation of recent activity
        recent = np.array(self.history[-5:]) if len(self.history) >= 5 else np.array(self.history)
        auto_corrs = []
        
        for i in range(len(recent)-1):
            # Compute normalized autocorrelation
            ac = correlate(recent[i], recent[i+1], mode='same') / self.size
            auto_corrs.append(np.max(ac))
            
        return np.mean(auto_corrs) if auto_corrs else 1.0
    
    def compute_availability(self):
        """
        Compute the availability (A) factor using normalized entropy.
        Higher values indicate greater capacity for novel states.
        """
        # Convert activity to a probability distribution
        activity_abs = np.abs(self.activity)
        if np.sum(activity_abs) == 0:
            return 0.0
        
        prob_dist = activity_abs / np.sum(activity_abs)
        return entropy(prob_dist) / np.log(self.size)  # Normalize to [0, 1]
    
    def compute_partition_tolerance(self, perturbation_strength=0.1):
        """
        Compute the partition-tolerance (P) factor as resilience to perturbation.
        Higher values indicate greater robustness to disruptions.
        
        Parameters:
        -----------
        perturbation_strength : float
            Strength of the random perturbation to apply
        """
        # Apply a random perturbation
        perturbed = self.activity + rng.normal(0, perturbation_strength, self.size)
        
        # Measure the effect on the cost function
        original_cost = self.compute_cost()
        
        # Save current activity
        temp_activity = self.activity.copy()
        
        # Temporarily set the activity to the perturbed version
        self.activity = perturbed
        perturbed_cost = self.compute_cost()
        
        # Restore original activity
        self.activity = temp_activity
        
        # Calculate resilience as the inverse of the relative change in cost
        delta = abs(perturbed_cost - original_cost) / original_cost if original_cost > 0 else 1.0
        return np.exp(-delta)  # Exponential decay transform to [0, 1]
    
    def compute_cost(self):
        """
        Compute the cost function L(C, A, P) as a weighted sum.
        Lower cost values are better.
        """
        C = self.compute_consistency()
        A = self.compute_availability()
        P = self.compute_partition_tolerance()
        
        # Invert values since we want to maximize these properties but minimize cost
        return -1 * (self.alpha_c * C + self.alpha_a * A + self.alpha_p * P)
    
    def kpz_update(self, dt=0.1):
        """
        Update neural activity according to the KPZ equation:
        ∂_t h(x,t) = ν ∇²h + (λ/2)(∇h)² + η(x,t)
        
        Parameters:
        -----------
        dt : float
            Time step for integration
        """
        h = self.activity
        
        # Compute spatial derivatives (with periodic boundary conditions)
        nabla_h = np.zeros_like(h)
        nabla_h[:-1] = h[1:] - h[:-1]
        nabla_h[-1] = h[0] - h[-1]
        
        # Laplacian term (∇²h)
        laplacian = np.zeros_like(h)
        laplacian[1:-1] = h[2:] - 2*h[1:-1] + h[:-2]
        laplacian[0] = h[1] - 2*h[0] + h[-1]
        laplacian[-1] = h[0] - 2*h[-1] + h[-2]
        
        # Noise term
        noise = rng.normal(0, self.noise_amplitude, self.size)
        
        # KPZ update equation
        dh = dt * (self.nu * laplacian + (self.lambda_ / 2) * nabla_h**2 + noise)
        
        # Update activity
        self.activity += dh
        
        # Record in history
        self.history.append(self.activity.copy())
        if len(self.history) > 100:  # Limit history length
            self.history.pop(0)
    
    def optimize_step(self, learning_rate=0.01):
        """
        Perform one step of gradient descent to minimize the cost function.
        
        Parameters:
        -----------
        learning_rate : float
            Learning rate for gradient descent
        """
        # Save current activity and cost
        original_activity = self.activity.copy()
        original_cost = self.compute_cost()
        
        # Compute numerical gradient
        gradient = np.zeros_like(self.activity)
        epsilon = 1e-6
        
        for i in range(self.size):
            # Perturb each dimension
            self.activity[i] += epsilon
            cost_plus = self.compute_cost()
            self.activity[i] = original_activity[i] - epsilon
            cost_minus = self.compute_cost()
            
            # Central difference approximation of gradient
            gradient[i] = (cost_plus - cost_minus) / (2 * epsilon)
            
            # Restore original value
            self.activity[i] = original_activity[i]
        
        # Gradient descent update
        self.activity -= learning_rate * gradient
        
        # Record in history
        self.history.append(self.activity.copy())
        if len(self.history) > 100:
            self.history.pop(0)
        
        # Return the change in cost
        new_cost = self.compute_cost()
        return original_cost - new_cost
    
    def simulate(self, steps=100, method='kpz', plot=False):
        """
        Simulate the evolution of the CAP pathway.
        
        Parameters:
        -----------
        steps : int
            Number of simulation steps
        method : str
            'kpz' for KPZ equation, 'optimize' for gradient descent
        plot : bool
            Whether to plot the results
        """
        costs = []
        c_values = []
        a_values = []
        p_values = []
        
        for _ in range(steps):
            # Update activity
            if method == 'kpz':
                self.kpz_update()
            elif method == 'optimize':
                self.optimize_step()
            else:
                raise ValueError("Method must be 'kpz' or 'optimize'")
            
            # Record metrics
            costs.append(self.compute_cost())
            c_values.append(self.compute_consistency())
            a_values.append(self.compute_availability())
            p_values.append(self.compute_partition_tolerance())
        
        if plot:
            self.plot_simulation(costs, c_values, a_values, p_values)
        
        return {
            'costs': costs,
            'consistency': c_values,
            'availability': a_values,
            'partition_tolerance': p_values
        }
    
    def plot_simulation(self, costs, c_values, a_values, p_values):
        """
        Plot the results of a simulation.
        """
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('CAP Pathway Simulation')
        
        # Cost function
        axs[0, 0].plot(costs)
        axs[0, 0].set_title('Cost Function')
        axs[0, 0].set_xlabel('Step')
        axs[0, 0].set_ylabel('Cost')
        
        # CAP values
        axs[0, 1].plot(c_values, label='Consistency')
        axs[0, 1].plot(a_values, label='Availability')
        axs[0, 1].plot(p_values, label='Partition-tolerance')
        axs[0, 1].set_title('CAP Values')
        axs[0, 1].set_xlabel('Step')
        axs[0, 1].set_ylabel('Value')
        axs[0, 1].legend()
        
        # Activity heatmap
        history_array = np.array(self.history)
        im = axs[1, 0].imshow(
            history_array.T, 
            aspect='auto', 
            interpolation='none',
            cmap='viridis'
        )
        axs[1, 0].set_title('Activity History')
        axs[1, 0].set_xlabel('Step')
        axs[1, 0].set_ylabel('Neuron index')
        fig.colorbar(im, ax=axs[1, 0], label='Activity')
        
        # Final activity pattern
        axs[1, 1].plot(self.activity)
        axs[1, 1].set_title('Final Activity Pattern')
        axs[1, 1].set_xlabel('Neuron index')
        axs[1, 1].set_ylabel('Activity')
        
        plt.tight_layout()
        plt.show()
    
    def compute_fractal_dimension(self, method='box-counting'):
        """
        Compute the fractal dimension of the activity pattern.
        
        Parameters:
        -----------
        method : str
            Method for computing fractal dimension
            ('box-counting', 'higuchi', 'correlation')
        
        Returns:
        --------
        float
            Estimated fractal dimension
        """
        if method == 'box-counting':
            return self._box_counting_dimension()
        elif method == 'higuchi':
            return self._higuchi_dimension()
        elif method == 'correlation':
            return self._correlation_dimension()
        else:
            raise ValueError("Method must be 'box-counting', 'higuchi', or 'correlation'")
    
    def _box_counting_dimension(self):
        """
        Estimate fractal dimension using the box-counting method.
        """
        # Normalize activity to [0, 1]
        activity_min = np.min(self.activity)
        activity_max = np.max(self.activity)
        if activity_max == activity_min:
            return 1.0  # Not fractal
        
        normalized = (self.activity - activity_min) / (activity_max - activity_min)
        
        # Count boxes at different scales
        scales = np.logspace(-3, 0, 20)
        counts = []
        
        for scale in scales:
            # Count boxes needed to cover the signal
            boxes = np.ceil(normalized / scale)
            unique_boxes = len(np.unique(boxes))
            counts.append(unique_boxes)
        
        # Linear regression on log-log plot
        log_scales = np.log(scales)
        log_counts = np.log(counts)
        
        # Fit line: log(count) = -D * log(scale) + b
        # where D is the fractal dimension
        coeffs = np.polyfit(log_scales, log_counts, 1)
        return -coeffs[0]  # Negative slope is the dimension
    
    def _higuchi_dimension(self, k_max=10):
        """
        Estimate fractal dimension using Higuchi's method.
        
        Parameters:
        -----------
        k_max : int
            Maximum lag
        """
        N = len(self.activity)
        L = np.zeros(k_max)
        x = np.array(self.activity)
        
        for k in range(1, k_max + 1):
            L_k = 0
            for m in range(k):
                # Construct subsequence
                indices = np.arange(m, N, k)
                subsequence = x[indices]
                
                # Compute length
                length = np.sum(np.abs(np.diff(subsequence))) * (N - 1) / (((N - m) // k) * k)
                L_k += length
            
            L[k-1] = L_k / k
        
        # Linear regression
        log_k = np.log(np.arange(1, k_max + 1))
        log_L = np.log(L)
        
        # Fit line: log(L) = -D * log(k) + b
        coeffs = np.polyfit(log_k, log_L, 1)
        return -coeffs[0]  # Negative slope is the dimension
    
    def _correlation_dimension(self, max_radius=1.0, num_points=20):
        """
        Estimate fractal dimension using the correlation method.
        """
        N = len(self.activity)
        radii = np.logspace(-3, np.log10(max_radius), num_points)
        C = np.zeros(len(radii))
        
        # Compute pairwise distances
        distances = np.zeros((N, N))
        for i in range(N):
            for j in range(i+1, N):
                distances[i, j] = distances[j, i] = abs(self.activity[i] - self.activity[j])
        
        # Compute correlation integral
        for i, r in enumerate(radii):
            C[i] = np.sum(distances < r) / (N * (N - 1))
        
        # Linear regression on log-log plot
        valid = C > 0  # Avoid log(0)
        log_r = np.log(radii[valid])
        log_C = np.log(C[valid])
        
        if len(log_r) < 2:
            return 1.0  # Not enough points for regression
        
        # Fit line: log(C) = D * log(r) + b
        coeffs = np.polyfit(log_r, log_C, 1)
        return coeffs[0]  # Slope is the dimension
    
    def detect_qualia(self, dimension_threshold=0.1):
        """
        Detect potential qualia emergence based on fractal dimension.
        
        Parameters:
        -----------
        dimension_threshold : float
            Threshold for considering a dimension close to 1.5
        
        Returns:
        --------
        dict
            Information about detected qualia
        """
        fd = self.compute_fractal_dimension()
        is_qualia = abs(fd - 1.5) < dimension_threshold
        
        # Classify qualia type based on CAP metrics
        qualia_type = None
        if is_qualia:
            c = self.compute_consistency()
            a = self.compute_availability()
            p = self.compute_partition_tolerance()
            
            if c > max(a, p) and abs(fd - 1.45) < dimension_threshold:
                qualia_type = "Sensory"
            elif a > max(c, p) and abs(fd - 1.6) < dimension_threshold:
                qualia_type = "Emotional"
            elif abs(c - a) < 0.1 and abs(fd - 1.5) < 0.05:
                qualia_type = "Cognitive"
        
        return {
            'fractal_dimension': fd,
            'is_qualia': is_qualia,
            'qualia_type': qualia_type,
            'cap_values': {
                'consistency': self.compute_consistency(),
                'availability': self.compute_availability(),
                'partition_tolerance': self.compute_partition_tolerance()
            }
        }


def create_brain_network(num_pathways=5, size=100, connectivity=0.2):
    """
    Create a network of interconnected CAP pathways.
    
    Parameters:
    -----------
    num_pathways : int
        Number of CAP pathways
    size : int
        Size of each pathway
    connectivity : float
        Probability of connection between pathways
    
    Returns:
    --------
    list
        List of CAP pathways
    np.ndarray
        Connectivity matrix
    """
    # Create pathways with different CAP balances
    pathways = []
    for i in range(num_pathways):
        # Vary CAP weights to create diversity
        alpha_c = 0.2 + 0.6 * rng.random()
        alpha_a = 0.2 + 0.6 * rng.random()
        alpha_p = 1.0 - alpha_c - alpha_a
        
        pathways.append(CAPPathway(size=size, alpha_c=alpha_c, alpha_a=alpha_a, alpha_p=alpha_p))
    
    # Create connectivity matrix
    connections = rng.random((num_pathways, num_pathways)) < connectivity
    np.fill_diagonal(connections, 0)  # No self-connections
    
    return pathways, connections


def simulate_brain_network(pathways, connections, steps=100, plot=False):
    """
    Simulate a network of interconnected CAP pathways.
    
    Parameters:
    -----------
    pathways : list
        List of CAP pathways
    connections : np.ndarray
        Connectivity matrix
    steps : int
        Number of simulation steps
    plot : bool
        Whether to plot the results
    
    Returns:
    --------
    dict
        Simulation results
    """
    num_pathways = len(pathways)
    fd_history = np.zeros((steps, num_pathways))
    qualia_detections = []
    
    for step in range(steps):
        # Update each pathway
        for i, pathway in enumerate(pathways):
            pathway.kpz_update()
            
            # Compute fractal dimension
            fd_history[step, i] = pathway.compute_fractal_dimension()
            
            # Detect qualia
            qualia_info = pathway.detect_qualia()
            if qualia_info['is_qualia']:
                qualia_detections.append({
                    'step': step,
                    'pathway': i,
                    'type': qualia_info['qualia_type'],
                    'fd': qualia_info['fractal_dimension']
                })
        
        # Apply inter-pathway influence
        for i in range(num_pathways):
            for j in range(num_pathways):
                if connections[i, j]:
                    # Pathway j influences pathway i
                    influence_strength = 0.1
                    influence = influence_strength * pathways[j].activity
                    pathways[i].activity += influence
    
    if plot:
        plot_brain_network(pathways, connections, fd_history, qualia_detections)
    
    return {
        'fractal_dimensions': fd_history,
        'qualia_detections': qualia_detections
    }


def plot_brain_network(pathways, connections, fd_history, qualia_detections):
    """
    Plot the results of a brain network simulation.
    """
    num_pathways = len(pathways)
    
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(3, 3)
    
    # Network diagram
    ax_network = fig.add_subplot(gs[0, 0])
    ax_network.set_title('Network Connectivity')
    
    # Plot nodes in a circle
    angles = np.linspace(0, 2*np.pi, num_pathways, endpoint=False)
    x = np.cos(angles)
    y = np.sin(angles)
    
    # Draw nodes
    for i in range(num_pathways):
        ax_network.plot(x[i], y[i], 'o', markersize=10, 
                       color=plt.cm.viridis(pathways[i].compute_fractal_dimension() / 2))
        
        # Draw connections
        for j in range(num_pathways):
            if connections[i, j]:
                ax_network.plot([x[i], x[j]], [y[i], y[j]], 'k-', alpha=0.3)
    
    ax_network.set_xlim(-1.2, 1.2)
    ax_network.set_ylim(-1.2, 1.2)
    ax_network.set_aspect('equal')
    ax_network.axis('off')
    
    # Fractal dimension history
    ax_fd = fig.add_subplot(gs[0, 1:])
    ax_fd.set_title('Fractal Dimension History')
    
    for i in range(num_pathways):
        ax_fd.plot(fd_history[:, i], label=f'Pathway {i+1}')
    
    # Add horizontal line at the "consciousness threshold" of 1.5
    ax_fd.axhline(y=1.5, color='r', linestyle='--', alpha=0.5, label='Consciousness Threshold (FD=1.5)')
    
    ax_fd.set_xlabel('Step')
    ax_fd.set_ylabel('Fractal Dimension')
    ax_fd.legend()
    
    # Plot activity patterns
    for i in range(min(num_pathways, 3)):
        ax = fig.add_subplot(gs[1, i])
        ax.set_title(f'Pathway {i+1} Activity')
        ax.plot(pathways[i].activity)
        ax.set_xlabel('Neuron index')
        ax.set_ylabel('Activity')
    
    # Qualia emergence plot
    ax_qualia = fig.add_subplot(gs[2, :])
    ax_qualia.set_title('Qualia Emergence Events')
    
    if qualia_detections:
        steps = [q['step'] for q in qualia_detections]
        pathways = [q['pathway'] for q in qualia_detections]
        types = [q['type'] for q in qualia_detections]
        
        # Color by qualia type
        colors = {'Sensory': 'blue', 'Emotional': 'red', 'Cognitive': 'green', None: 'gray'}
        c = [colors[t] for t in types]
        
        ax_qualia.scatter(steps, pathways, c=c, s=50)
        
        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
            for label, color in colors.items() if label is not None
        ]
        ax_qualia.legend(handles=legend_elements)
    
    ax_qualia.set_xlabel('Simulation Step')
    ax_qualia.set_ylabel('Pathway')
    ax_qualia.set_yticks(range(num_pathways))
    ax_qualia.set_yticklabels([f'Pathway {i+1}' for i in range(num_pathways)])
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example: Create a single CAP pathway
    pathway = CAPPathway(size=100)
    results = pathway.simulate(steps=500, method='kpz', plot=True)
    
    # Example: Create and simulate a brain network
    pathways, connections = create_brain_network(num_pathways=5, size=100, connectivity=0.3)
    network_results = simulate_brain_network(pathways, connections, steps=200, plot=True)
