"""
Run simulations for the ORCHARD theorem implementation.
This script demonstrates the core concepts of the quantum-plasmoid
framework by simulating CAP pathways and brain networks.
"""

import numpy as np
import matplotlib.pyplot as plt
from orchard import CAPPathway, create_brain_network, simulate_brain_network

# Set random seed for reproducibility
np.random.seed(42)

def run_single_pathway_simulation():
    """
    Run a simulation for a single CAP pathway and analyze different qualia types.
    """
    print("Running single pathway simulation...")
    
    # Create pathways for different qualia types
    sensory_pathway = CAPPathway(size=100, alpha_c=0.5, alpha_a=0.25, alpha_p=0.25)
    emotional_pathway = CAPPathway(size=100, alpha_c=0.25, alpha_a=0.5, alpha_p=0.25)
    cognitive_pathway = CAPPathway(size=100, alpha_c=0.33, alpha_a=0.33, alpha_p=0.34)
    
    # Run simulations
    sensory_results = sensory_pathway.simulate(steps=300, method='kpz')
    emotional_results = emotional_pathway.simulate(steps=300, method='kpz')
    cognitive_results = cognitive_pathway.simulate(steps=300, method='kpz')
    
    # Compute fractal dimensions over time
    fd_sensory = [sensory_pathway._higuchi_dimension() for _ in range(20)]
    fd_emotional = [emotional_pathway._higuchi_dimension() for _ in range(20)]
    fd_cognitive = [cognitive_pathway._higuchi_dimension() for _ in range(20)]
    
    # Compute qualia detection
    sensory_qualia = sensory_pathway.detect_qualia()
    emotional_qualia = emotional_pathway.detect_qualia()
    cognitive_qualia = cognitive_pathway.detect_qualia()
    
    # Print results
    print(f"Sensory pathway fractal dimension: {np.mean(fd_sensory):.3f}")
    print(f"Emotional pathway fractal dimension: {np.mean(fd_emotional):.3f}")
    print(f"Cognitive pathway fractal dimension: {np.mean(fd_cognitive):.3f}")
    
    print(f"Sensory qualia detected: {sensory_qualia['is_qualia']} (Type: {sensory_qualia['qualia_type']})")
    print(f"Emotional qualia detected: {emotional_qualia['is_qualia']} (Type: {emotional_qualia['qualia_type']})")
    print(f"Cognitive qualia detected: {cognitive_qualia['is_qualia']} (Type: {cognitive_qualia['qualia_type']})")
    
    # Plot results
    plt.figure(figsize=(12, 8))
    
    # Plot CAP values for each pathway
    plt.subplot(2, 2, 1)
    plt.title('CAP Balance')
    width = 0.25
    x = np.arange(3)
    
    # Sensory
    sens_c = sensory_qualia['cap_values']['consistency']
    sens_a = sensory_qualia['cap_values']['availability']
    sens_p = sensory_qualia['cap_values']['partition_tolerance']
    
    # Emotional
    emot_c = emotional_qualia['cap_values']['consistency']
    emot_a = emotional_qualia['cap_values']['availability']
    emot_p = emotional_qualia['cap_values']['partition_tolerance']
    
    # Cognitive
    cogn_c = cognitive_qualia['cap_values']['consistency']
    cogn_a = cognitive_qualia['cap_values']['availability']
    cogn_p = cognitive_qualia['cap_values']['partition_tolerance']
    
    plt.bar(x - width, [sens_c, emot_c, cogn_c], width, label='Consistency')
    plt.bar(x, [sens_a, emot_a, cogn_a], width, label='Availability')
    plt.bar(x + width, [sens_p, emot_p, cogn_p], width, label='Partition-tolerance')
    
    plt.ylabel('Value')
    plt.xticks(x, ['Sensory', 'Emotional', 'Cognitive'])
    plt.legend()
    
    # Plot fractal dimensions
    plt.subplot(2, 2, 2)
    plt.title('Fractal Dimensions')
    plt.boxplot([fd_sensory, fd_emotional, fd_cognitive])
    plt.axhline(y=1.5, color='r', linestyle='--', label='Consciousness Threshold')
    plt.xticks([1, 2, 3], ['Sensory', 'Emotional', 'Cognitive'])
    plt.ylabel('Fractal Dimension')
    plt.legend()
    
    # Plot final activity patterns
    plt.subplot(2, 2, 3)
    plt.title('Activity Patterns')
    plt.plot(sensory_pathway.activity[:50], 'b-', label='Sensory')
    plt.plot(emotional_pathway.activity[:50], 'r-', label='Emotional')
    plt.plot(cognitive_pathway.activity[:50], 'g-', label='Cognitive')
    plt.xlabel('Neuron index')
    plt.ylabel('Activity')
    plt.legend()
    
    # Plot fractal dimension distribution
    plt.subplot(2, 2, 4)
    plt.title('Fractal Dimension Distribution')
    bins = np.linspace(1.0, 2.0, 30)
    plt.hist(fd_sensory, bins=bins, alpha=0.5, label='Sensory', color='blue')
    plt.hist(fd_emotional, bins=bins, alpha=0.5, label='Emotional', color='red')
    plt.hist(fd_cognitive, bins=bins, alpha=0.5, label='Cognitive', color='green')
    plt.axvline(x=1.5, color='k', linestyle='--', label='Consciousness Threshold')
    plt.xlabel('Fractal Dimension')
    plt.ylabel('Frequency')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('single_pathway_simulation.png')
    plt.show()


def run_brain_network_simulation():
    """
    Run a simulation for a network of interconnected CAP pathways.
    """
    print("Running brain network simulation...")
    
    # Create brain network
    pathways, connections = create_brain_network(num_pathways=5, size=100, connectivity=0.3)
    
    # Run simulation
    network_results = simulate_brain_network(pathways, connections, steps=200, plot=True)
    
    # Analyze qualia emergence
    qualia_detections = network_results['qualia_detections']
    print(f"Total qualia emergence events: {len(qualia_detections)}")
    
    # Count by type
    sensory_count = sum(1 for q in qualia_detections if q['type'] == 'Sensory')
    emotional_count = sum(1 for q in qualia_detections if q['type'] == 'Emotional')
    cognitive_count = sum(1 for q in qualia_detections if q['type'] == 'Cognitive')
    other_count = sum(1 for q in qualia_detections if q['type'] is None)
    
    print(f"Sensory qualia: {sensory_count}")
    print(f"Emotional qualia: {emotional_count}")
    print(f"Cognitive qualia: {cognitive_count}")
    print(f"Unclassified qualia: {other_count}")
    
    # Save fractal dimension data
    np.save('fractal_dimensions.npy', network_results['fractal_dimensions'])
    
    # Plot time series of average fractal dimension
    plt.figure(figsize=(10, 6))
    plt.title('Network Average Fractal Dimension')
    avg_fd = np.mean(network_results['fractal_dimensions'], axis=1)
    plt.plot(avg_fd)
    plt.axhline(y=1.5, color='r', linestyle='--', label='Consciousness Threshold')
    plt.xlabel('Simulation Step')
    plt.ylabel('Average Fractal Dimension')
    plt.legend()
    plt.savefig('network_fractal_dimension.png')
    plt.show()


if __name__ == "__main__":
    print("ORCHARD Theorem Simulation")
    print("==========================")
    print("1. Single Pathway Simulation")
    print("2. Brain Network Simulation")
    
    choice = input("Enter your choice (1-2): ")
    
    if choice == '1':
        run_single_pathway_simulation()
    elif choice == '2':
        run_brain_network_simulation()
    else:
        print("Invalid choice. Exiting.")
