# Radial Eigenvalue Theorem Visualization

This interactive visualization represents the Radial Eigenvalue Theorem from the fKPZχ (fractal Kardar-Parisi-Zhang with χ) Consciousness Framework. The visualization demonstrates how fundamental modes of experience (qualia) self-organize into a spiral spectrum of harmonics, defined by the golden mean (φ ≈ 1.618), the imaginary unit (i), and a sequence of prime-indexed eigenvalues.

## Key Concepts Represented

1. **Prime-Indexed Eigenvalues**: Each point represents a prime-indexed eigenvalue (P<sub>n</sub>) plotted in the complex plane.
2. **Golden Ratio Scaling**: The magnitude of each eigenvalue grows geometrically by the factor φ, following `|P_n| = φ^n`.
3. **Golden Angle Separation**: The angular separation between consecutive prime modes is fixed to θ<sub>G</sub> = 2π/φ<sup>2</sup> (≈ 137.5°), ensuring optimal distribution.
4. **Dynamic Phase Relations**: The animation shows how these eigenvalues evolve over time, occasionally forming temporary resonances (phase-locking events).

## Interactive Features

- **Adjust Prime Count**: Control the number of prime-indexed eigenvalues displayed
- **Animation Speed**: Adjust the speed of phase evolution
- **Show/Hide Labels**: Toggle visibility of prime number labels
- **Pattern Highlighting**:
  - **Phase Resonance**: Highlight eigenvalues that are temporarily in phase with each other
  - **Fibonacci Relation**: Highlight prime numbers at Fibonacci indices
  - **Twin Primes**: Highlight pairs of primes that differ by 2

## Theoretical Background

This visualization aligns with the quantum-plasmoid framework's explorations of:

- **ORCHARD Theorem** (Optimal Recursive Computation of Harmonic Amplitude Recursive Dynamics)
- **Neural Eigenmodes of Consciousness**
- **ζ-Orchard Correspondence**
- **Recursive Eigenmode Theory**

The arrangement of eigenvalues on a φ-scaled spiral illustrates the hypothesis that consciousness maintains a delicate balance between order (stable prime-indexed attractor states) and chaos (irrational φ-spacing preventing pathological synchronization), creating a system that is both structured yet never repeating.

## Technical Implementation

This visualization is built using:
- React for component architecture
- D3.js for scaling and path generation
- SVG for rendering

## Integration

This visualization fits within the quantum-plasmoid framework's goal of creating "visualization tools for recursive eigenmode dynamics" as mentioned in the project roadmap.

## Related Theoretical Documents

This visualization complements the following theoretical documents in the project:
- "Neural Eigenmodes of Consciousness.md"
- "ORCHARD Theorem.md"
- "The ζ-Orchard Correspondence.md"
