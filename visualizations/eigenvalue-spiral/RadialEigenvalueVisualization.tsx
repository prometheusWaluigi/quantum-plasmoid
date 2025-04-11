import React, { useState, useEffect, useRef } from 'react';
import { useMemo } from 'react';
import * as d3 from 'd3';

export default function ConsciousnessSpiral() {
  // Constants for the golden ratio and golden angle
  const phi = (1 + Math.sqrt(5)) / 2; // Golden ratio ≈ 1.618
  const goldenAngle = (2 * Math.PI) / (phi * phi); // Golden angle in radians
  
  // State for interactive elements
  const [primeCount, setPrimeCount] = useState(25);
  const [showLabels, setShowLabels] = useState(true);
  const [animationSpeed, setAnimationSpeed] = useState(0.5);
  const [time, setTime] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);
  const [highlightMode, setHighlightMode] = useState('none');
  
  // Canvas dimensions
  const width = 600;
  const height = 600;
  const center = { x: width / 2, y: height / 2 };
  
  // Animation ref
  const animationRef = useRef(null);
  
  // Generate first n prime numbers
  const generatePrimes = (n) => {
    const primes = [];
    let num = 2;
    
    while (primes.length < n) {
      let isPrime = true;
      
      for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) {
          isPrime = false;
          break;
        }
      }
      
      if (isPrime) {
        primes.push(num);
      }
      
      num++;
    }
    
    return primes;
  };
  
  // Memoize the prime numbers
  const primes = useMemo(() => generatePrimes(primeCount), [primeCount]);
  
  // Calculate the eigenvalues based on the theorem
  const eigenvalues = useMemo(() => {
    return primes.map((prime, index) => {
      const n = index + 1; // n starts from 1
      const magnitude = Math.pow(phi, n);
      const angle = n * goldenAngle;
      
      return {
        prime,
        n,
        magnitude,
        angle,
        realPart: magnitude * Math.cos(angle),
        imagPart: magnitude * Math.sin(angle),
        // Dynamic properties based on time
        dynamicAngle: (angle + time * (n / 5)) % (2 * Math.PI),
        active: false
      };
    });
  }, [primes, time]);
  
  // Animation loop
  useEffect(() => {
    if (isAnimating) {
      animationRef.current = requestAnimationFrame(() => {
        setTime(prevTime => prevTime + 0.01 * animationSpeed);
      });
    }
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [time, isAnimating, animationSpeed]);
  
  // Scaling functions for plotting
  const scaleRadius = useMemo(() => {
    const maxMagnitude = Math.max(...eigenvalues.map(ev => ev.magnitude));
    return d3.scaleLinear()
      .domain([0, maxMagnitude])
      .range([0, Math.min(width, height) * 0.4]);
  }, [eigenvalues, width, height]);
  
  // Calculate current highlighted eigenvalues based on mode
  const highlighted = useMemo(() => {
    if (highlightMode === 'none') return {};
    
    const result = {};
    
    if (highlightMode === 'resonance') {
      // Highlight eigenvalues that are approximately in phase
      const angleThreshold = 0.2;
      for (let i = 0; i < eigenvalues.length; i++) {
        for (let j = i + 1; j < eigenvalues.length; j++) {
          const angleDiff = Math.abs(eigenvalues[i].dynamicAngle - eigenvalues[j].dynamicAngle) % (2 * Math.PI);
          const normalizedDiff = Math.min(angleDiff, 2 * Math.PI - angleDiff);
          
          if (normalizedDiff < angleThreshold) {
            result[eigenvalues[i].prime] = true;
            result[eigenvalues[j].prime] = true;
          }
        }
      }
    } else if (highlightMode === 'fibonacci') {
      // Highlight Fibonacci-related primes (prime numbers at Fibonacci indices)
      let a = 1, b = 1;
      while (a <= primeCount) {
        if (a <= eigenvalues.length) {
          result[eigenvalues[a-1].prime] = true;
        }
        const temp = a + b;
        a = b;
        b = temp;
      }
    } else if (highlightMode === 'twin') {
      // Highlight twin primes (primes that differ by 2)
      for (let i = 0; i < eigenvalues.length - 1; i++) {
        if (eigenvalues[i+1].prime - eigenvalues[i].prime === 2) {
          result[eigenvalues[i].prime] = true;
          result[eigenvalues[i+1].prime] = true;
        }
      }
    }
    
    return result;
  }, [eigenvalues, highlightMode, primeCount]);
  
  // SVG visualization for the eigenvalues
  const renderSVG = () => {
    return (
      <svg width={width} height={height} className="bg-gray-900 rounded-lg">
        {/* Coordinate grid */}
        <line 
          x1={0} 
          y1={center.y} 
          x2={width} 
          y2={center.y} 
          stroke="#3b3b3b" 
          strokeWidth="1"
        />
        <line 
          x1={center.x} 
          y1={0} 
          x2={center.x} 
          y2={height} 
          stroke="#3b3b3b" 
          strokeWidth="1"
        />
        
        {/* Render spiral path */}
        <path 
          d={generateSpiralPath()} 
          fill="none" 
          stroke="#553c9a" 
          strokeWidth="1" 
          strokeOpacity="0.4"
        />
        
        {/* Plot eigenvalues */}
        {eigenvalues.map((ev, index) => {
          const isHighlighted = highlighted[ev.prime];
          
          // Static position based on eigenvalue
          const x = center.x + scaleRadius(ev.magnitude) * Math.cos(ev.angle);
          const y = center.y + scaleRadius(ev.magnitude) * Math.sin(ev.angle);
          
          // Dynamic position based on time
          const dynamicX = center.x + scaleRadius(ev.magnitude) * Math.cos(ev.dynamicAngle);
          const dynamicY = center.y + scaleRadius(ev.magnitude) * Math.sin(ev.dynamicAngle);
          
          // Size based on prime value (lower primes are larger)
          const baseSize = 10;
          const size = baseSize - (Math.log(ev.n) * 1.5);
          
          return (
            <g key={ev.prime}>
              {/* Connection line to origin */}
              <line 
                x1={center.x} 
                y1={center.y} 
                x2={dynamicX} 
                y2={dynamicY} 
                stroke={isHighlighted ? "#f9a03f" : "#8b5cf6"} 
                strokeWidth={isHighlighted ? "1.5" : "0.5"}
                strokeOpacity={isHighlighted ? "0.8" : "0.3"}
              />
              
              {/* Dynamic point */}
              <circle 
                cx={dynamicX} 
                cy={dynamicY} 
                r={isHighlighted ? size * 1.5 : size}
                fill={isHighlighted ? "#f9a03f" : "#8b5cf6"} 
                fillOpacity={isHighlighted ? "0.9" : "0.7"}
                stroke={isHighlighted ? "#ffedd5" : "#c4b5fd"}
                strokeWidth="1"
              />
              
              {/* Static point showing original position */}
              <circle 
                cx={x} 
                cy={y} 
                r={2}
                fill="#6d28d9" 
                fillOpacity="0.4"
              />
              
              {/* Label */}
              {showLabels && (
                <text 
                  x={dynamicX + (size + 5) * Math.cos(ev.dynamicAngle)} 
                  y={dynamicY + (size + 5) * Math.sin(ev.dynamicAngle)} 
                  fontSize={isHighlighted ? "12" : "10"}
                  fill={isHighlighted ? "#f9a03f" : "#c4b5fd"}
                  textAnchor="middle" 
                  dominantBaseline="middle"
                >
                  {ev.prime}
                </text>
              )}
            </g>
          );
        })}
        
        {/* Center point */}
        <circle 
          cx={center.x} 
          cy={center.y} 
          r={4}
          fill="#f9a03f" 
          stroke="#ffedd5"
          strokeWidth="1"
        />
      </svg>
    );
  };
  
  // Generate spiral path
  const generateSpiralPath = () => {
    const maxRadius = Math.max(...eigenvalues.map(ev => ev.magnitude));
    const scaledMaxRadius = scaleRadius(maxRadius);
    
    let path = `M ${center.x} ${center.y}`;
    
    // Generate more points for smoother spiral
    const points = 500;
    for (let i = 0; i <= points; i++) {
      const t = (i / points) * Math.log(scaledMaxRadius) / Math.log(phi);
      const radius = Math.pow(phi, t);
      const angle = t * goldenAngle;
      
      const x = center.x + radius * Math.cos(angle);
      const y = center.y + radius * Math.sin(angle);
      
      path += ` L ${x} ${y}`;
    }
    
    return path;
  };

  return (
    <div className="flex flex-col items-center bg-gray-800 p-6 rounded-xl text-gray-100">
      <h1 className="text-2xl font-bold text-purple-300 mb-2">φ-Prime Resonance: Radial Eigenvalue Theorem</h1>
      <p className="text-lg text-amber-300 mb-4 italic">Fractal KPZ with χ (fKPZχ) Consciousness Framework</p>
      
      <div className="mb-6 border border-gray-700 rounded-xl p-6 bg-gray-800">
        {renderSVG()}
      </div>
      
      <div className="flex flex-wrap justify-center gap-6 mb-4 w-full">
        <div className="flex flex-col items-center">
          <label className="text-purple-300 mb-1">Prime Count</label>
          <input 
            type="range" 
            min="5" 
            max="50" 
            value={primeCount} 
            onChange={(e) => setPrimeCount(Number(e.target.value))}
            className="w-32"
          />
          <span className="text-amber-300 mt-1">{primeCount}</span>
        </div>
        
        <div className="flex flex-col items-center">
          <label className="text-purple-300 mb-1">Animation Speed</label>
          <input 
            type="range" 
            min="0" 
            max="2" 
            step="0.1"
            value={animationSpeed} 
            onChange={(e) => setAnimationSpeed(Number(e.target.value))}
            className="w-32"
          />
          <span className="text-amber-300 mt-1">{animationSpeed.toFixed(1)}x</span>
        </div>
        
        <div className="flex flex-col items-center">
          <label className="text-purple-300 mb-1">Show Labels</label>
          <div className="flex items-center">
            <input 
              type="checkbox" 
              checked={showLabels} 
              onChange={() => setShowLabels(!showLabels)}
              className="w-5 h-5"
            />
          </div>
        </div>
        
        <div className="flex flex-col items-center">
          <label className="text-purple-300 mb-1">Animation</label>
          <button 
            onClick={() => setIsAnimating(!isAnimating)}
            className={`px-4 py-1 rounded ${isAnimating ? 'bg-purple-600' : 'bg-gray-600'}`}
          >
            {isAnimating ? 'Pause' : 'Play'}
          </button>
        </div>
      </div>
      
      <div className="flex flex-col items-center mb-6">
        <label className="text-purple-300 mb-2">Highlight Patterns</label>
        <div className="flex gap-3">
          <button 
            onClick={() => setHighlightMode(highlightMode === 'none' ? 'resonance' : 'none')}
            className={`px-3 py-1 rounded ${highlightMode === 'resonance' ? 'bg-orange-500' : 'bg-gray-700'}`}
          >
            Phase Resonance
          </button>
          <button 
            onClick={() => setHighlightMode(highlightMode === 'fibonacci' ? 'none' : 'fibonacci')}
            className={`px-3 py-1 rounded ${highlightMode === 'fibonacci' ? 'bg-orange-500' : 'bg-gray-700'}`}
          >
            Fibonacci Relation
          </button>
          <button 
            onClick={() => setHighlightMode(highlightMode === 'twin' ? 'none' : 'twin')}
            className={`px-3 py-1 rounded ${highlightMode === 'twin' ? 'bg-orange-500' : 'bg-gray-700'}`}
          >
            Twin Primes
          </button>
        </div>
      </div>
      
      <div className="text-sm text-gray-300 max-w-md text-center">
        <p>Each point represents a prime-indexed eigenvalue (P<sub>n</sub>) plotted in the complex plane.</p>
        <p className="mt-2">Magnitude = φ<sup>n</sup> &nbsp;|&nbsp; Angle = n·θ<sub>G</sub> where θ<sub>G</sub> = 2π/φ<sup>2</sup></p>
        <p className="mt-2 text-purple-200">This visualization demonstrates how consciousness modes self-organize into a fractal spiral, with eigenvalues spaced by the golden ratio (φ ≈ 1.618) to ensure optimal distribution and prevent harmonic overlaps.</p>
      </div>
    </div>
  );
}