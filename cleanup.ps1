# PowerShell script to reorganize the quantum-plasmoid repository
# Set the root directory of the repository
$repoRoot = "C:\dev\quantum-plasmoid"
$unifiedTheories = "$repoRoot\unifiedTheories"

# Create the new directory structure
Write-Host "Creating new directory structure..." -ForegroundColor Green
$directories = @(
    "docs",
    "core-concepts\fractal-systems",
    "core-concepts\quantum-dynamics",
    "core-concepts\recursive-systems",
    "core-concepts\consciousness",
    "theorems\eigenmode-theory",
    "theorems\orchard-theorem",
    "theorems\zeta-correspondence",
    "time-models",
    "applications\computational",
    "applications\health",
    "applications\integrative"
)

foreach ($dir in $directories) {
    $path = Join-Path -Path $repoRoot -ChildPath $dir
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType Directory | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Yellow
    }
}

# Function to move files
function Move-File {
    param (
        [string]$source,
        [string]$destination
    )
    
    if (Test-Path $source) {
        $destDir = Split-Path -Parent $destination
        if (-not (Test-Path $destDir)) {
            New-Item -Path $destDir -ItemType Directory -Force | Out-Null
        }
        
        # Check if destination exists
        if (Test-Path $destination) {
            Write-Host "WARNING: Destination file already exists: $destination" -ForegroundColor Red
        } else {
            Move-Item -Path $source -Destination $destination
            Write-Host "Moved: $source -> $destination" -ForegroundColor Cyan
        }
    } else {
        Write-Host "ERROR: Source file not found: $source" -ForegroundColor Red
    }
}

# Move files from root to docs
Write-Host "Moving documentation files..." -ForegroundColor Green
Move-File -source "$repoRoot\INTRODUCTION.md" -destination "$repoRoot\docs\INTRODUCTION.md"
Move-File -source "$repoRoot\MATHEMATICAL_FOUNDATIONS.md" -destination "$repoRoot\docs\MATHEMATICAL_FOUNDATIONS.md"
Move-File -source "$repoRoot\RESEARCH_ROADMAP.md" -destination "$repoRoot\docs\RESEARCH_ROADMAP.md"

# Move files to core-concepts
Write-Host "Moving core concept files..." -ForegroundColor Green
# Fractal systems
Move-File -source "$repoRoot\celestialFRACTAL.md" -destination "$repoRoot\core-concepts\fractal-systems\celestialFRACTAL.md"
Move-File -source "$repoRoot\multidisciplinaryFRACTAL.md" -destination "$repoRoot\core-concepts\fractal-systems\multidisciplinaryFRACTAL.md"
Move-File -source "$unifiedTheories\FRACTAL.md" -destination "$repoRoot\core-concepts\fractal-systems\FRACTAL.md"

# Quantum dynamics
Move-File -source "$unifiedTheories\cosmicTensegrity.md" -destination "$repoRoot\core-concepts\quantum-dynamics\cosmicTensegrity.md"
Move-File -source "$unifiedTheories\Quantum Spectral Fractal Weaving.md" -destination "$repoRoot\core-concepts\quantum-dynamics\Quantum Spectral Fractal Weaving.md"

# Recursive systems
Move-File -source "$unifiedTheories\meta_theory_of_recursion.md" -destination "$repoRoot\core-concepts\recursive-systems\meta_theory_of_recursion.md"
Move-File -source "$unifiedTheories\meta_theory_recursion_whitepaper.md" -destination "$repoRoot\core-concepts\recursive-systems\meta_theory_recursion_whitepaper.md"
Move-File -source "$unifiedTheories\recursive_lattice_network.md" -destination "$repoRoot\core-concepts\recursive-systems\recursive_lattice_network.md"

# Consciousness
Move-File -source "$unifiedTheories\Consciousness Function.md" -destination "$repoRoot\core-concepts\consciousness\Consciousness Function.md"
Move-File -source "$unifiedTheories\Consciousness Function and more.md" -destination "$repoRoot\core-concepts\consciousness\Consciousness Function and more.md"
Move-File -source "$unifiedTheories\UnconsciousSemanticLattice.md" -destination "$repoRoot\core-concepts\consciousness\UnconsciousSemanticLattice.md"

# Move files to theorems
Write-Host "Moving theorem files..." -ForegroundColor Green
# Eigenmode theory
Move-File -source "$unifiedTheories\Recursive Eigenmode Theory and Fractal CAP Dynamics.md" -destination "$repoRoot\theorems\eigenmode-theory\Recursive Eigenmode Theory and Fractal CAP Dynamics.md"
Move-File -source "$unifiedTheories\Neural Eigenmodes of Consciousness.md" -destination "$repoRoot\theorems\eigenmode-theory\Neural Eigenmodes of Consciousness.md"
Move-File -source "$unifiedTheories\radialEigenvalueTheorem.md" -destination "$repoRoot\theorems\eigenmode-theory\radialEigenvalueTheorem.md"
Move-File -source "$unifiedTheories\Quantum Spectral Fractal Weaving Multi Scale Eigenmode.md" -destination "$repoRoot\theorems\eigenmode-theory\Quantum Spectral Fractal Weaving Multi Scale Eigenmode.md"

# ORCHARD theorem
Move-File -source "$unifiedTheories\ORCHARD Theorem.md" -destination "$repoRoot\theorems\orchard-theorem\ORCHARD Theorem.md"
Move-File -source "$unifiedTheories\ORCHARD Theorem Formalized.md" -destination "$repoRoot\theorems\orchard-theorem\ORCHARD Theorem Formalized.md"
Move-File -source "$unifiedTheories\ORCHARD Theorem Extended.md" -destination "$repoRoot\theorems\orchard-theorem\ORCHARD Theorem Extended.md"
Move-File -source "$unifiedTheories\ORCHARD Theorem Research.md" -destination "$repoRoot\theorems\orchard-theorem\ORCHARD Theorem Research.md"
Move-File -source "$unifiedTheories\ORCHARD Summary.md" -destination "$repoRoot\theorems\orchard-theorem\ORCHARD Summary.md"
Move-File -source "$unifiedTheories\ORCHARD Recursive Consciousness Dynamics.md" -destination "$repoRoot\theorems\orchard-theorem\ORCHARD Recursive Consciousness Dynamics.md"
Move-File -source "$unifiedTheories\ORCHARD Geometry as Retrocausal Spectral Manifold.md" -destination "$repoRoot\theorems\orchard-theorem\ORCHARD Geometry as Retrocausal Spectral Manifold.md"
Move-File -source "$unifiedTheories\ORCHARD vs Recursive Eigenmode vs Plasma.md" -destination "$repoRoot\theorems\orchard-theorem\ORCHARD vs Recursive Eigenmode vs Plasma.md"

# Zeta correspondence
Move-File -source "$unifiedTheories\The ζ-Orchard Correspondence.md" -destination "$repoRoot\theorems\zeta-correspondence\The ζ-Orchard Correspondence.md"
Move-File -source "$unifiedTheories\Comparing ζ-Orchard Correspondence Ψζ Hypothesis.md" -destination "$repoRoot\theorems\zeta-correspondence\Comparing ζ-Orchard Correspondence Ψζ Hypothesis.md"

# Move files to time-models
Write-Host "Moving time model files..." -ForegroundColor Green
Move-File -source "$unifiedTheories\Fractal Time and CSCM Framework.md" -destination "$repoRoot\time-models\Fractal Time and CSCM Framework.md"
Move-File -source "$unifiedTheories\fractalTimeRecursiveMind.md" -destination "$repoRoot\time-models\fractalTimeRecursiveMind.md"
Move-File -source "$unifiedTheories\CAP and Fractal Time.md" -destination "$repoRoot\time-models\CAP and Fractal Time.md"

# Move files to applications
Write-Host "Moving application files..." -ForegroundColor Green
# Computational
Move-File -source "$unifiedTheories\Ruliad Traversal System.md" -destination "$repoRoot\applications\computational\Ruliad Traversal System.md"

# Health
Move-File -source "$unifiedTheories\duckslapProtocol.md" -destination "$repoRoot\applications\health\duckslapProtocol.md"
Move-File -source "$unifiedTheories\EBVReactivationMECFS.md" -destination "$repoRoot\applications\health\EBVReactivationMECFS.md"

# Integrative
Move-File -source "$unifiedTheories\primeRecursionCodex.md" -destination "$repoRoot\applications\integrative\primeRecursionCodex.md"
Move-File -source "$unifiedTheories\primeRecursionProtocol.md" -destination "$repoRoot\applications\integrative\primeRecursionProtocol.md"
Move-File -source "$unifiedTheories\FRACTALQuantumAstrology.md" -destination "$repoRoot\applications\integrative\FRACTALQuantumAstrology.md"
Move-File -source "$unifiedTheories\publicationMythopoeticManifesto.md" -destination "$repoRoot\applications\integrative\publicationMythopoeticManifesto.md"

# Create README.md files for each directory
Write-Host "Creating README.md files for each directory..." -ForegroundColor Green

# Function to create README files
function Create-ReadmeFile {
    param (
        [string]$directory,
        [string]$title,
        [string]$description
    )
    
    $filePath = Join-Path -Path $repoRoot -ChildPath "$directory\README.md"
    if (-not (Test-Path $filePath)) {
        $content = @"
# $title

$description

## Contents

"@
        # Get all .md files in the directory except README.md
        $files = Get-ChildItem -Path (Join-Path -Path $repoRoot -ChildPath $directory) -Filter "*.md" | Where-Object { $_.Name -ne "README.md" }
        
        # Add each file to the contents section
        foreach ($file in $files) {
            $fileName = $file.Name
            $fileNameWithoutExtension = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
            $content += "`n- [$fileNameWithoutExtension](./$fileName)"
        }
        
        # Write the content to the README.md file
        $content | Out-File -FilePath $filePath -Encoding utf8
        Write-Host "Created README.md in $directory" -ForegroundColor Yellow
    } else {
        Write-Host "README.md already exists in $directory" -ForegroundColor Yellow
    }
}

# Create README files for each directory
$readmeConfigs = @(
    @{
        Directory = "docs"
        Title = "Documentation"
        Description = "Core documentation files for the Quantum-Plasmoid framework, providing introductions, mathematical foundations, and research roadmaps."
    },
    @{
        Directory = "core-concepts\fractal-systems"
        Title = "Fractal Systems"
        Description = "Explorations of fractal principles in consciousness, neural systems, and quantum phenomena."
    },
    @{
        Directory = "core-concepts\quantum-dynamics"
        Title = "Quantum Dynamics"
        Description = "Theoretical frameworks connecting quantum physics to consciousness and complex systems."
    },
    @{
        Directory = "core-concepts\recursive-systems"
        Title = "Recursive Systems"
        Description = "Meta-theoretical examinations of recursion as a fundamental principle across mathematical, physical, and cognitive domains."
    },
    @{
        Directory = "core-concepts\consciousness"
        Title = "Consciousness Theory"
        Description = "Foundational models of consciousness function, semantic processing, and unconscious dynamics."
    },
    @{
        Directory = "theorems\eigenmode-theory"
        Title = "Eigenmode Theory"
        Description = "Theoretical frameworks modeling consciousness as emerging from stable eigenmode solutions in neural systems."
    },
    @{
        Directory = "theorems\orchard-theorem"
        Title = "ORCHARD Theorem"
        Description = "A computational framework for consciousness emerging through recursive neural dynamics optimizing across consistency, availability, and partition-tolerance."
    },
    @{
        Directory = "theorems\zeta-correspondence"
        Title = "ζ-Orchard Correspondence"
        Description = "Theoretical work connecting the Riemann zeta function's spectral structure to the emergence of conscious experience."
    },
    @{
        Directory = "time-models"
        Title = "Fractal Time Models"
        Description = "Alternative conceptions of time as fractal, self-similar structures with implications for consciousness and physics."
    },
    @{
        Directory = "applications\computational"
        Title = "Computational Applications"
        Description = "Computational implementations and formalizations of the Quantum-Plasmoid framework."
    },
    @{
        Directory = "applications\health"
        Title = "Health Applications"
        Description = "Applying recursive and fractal frameworks to understanding and addressing health conditions."
    },
    @{
        Directory = "applications\integrative"
        Title = "Integrative Applications"
        Description = "Interdisciplinary applications bridging consciousness theory with astrology, mathematics, and publication strategies."
    }
)

foreach ($config in $readmeConfigs) {
    Create-ReadmeFile -directory $config.Directory -title $config.Title -description $config.Description
}

# Update main README.md to reflect the new structure
Write-Host "Updating main README.md..." -ForegroundColor Green
$mainReadmePath = Join-Path -Path $repoRoot -ChildPath "README.md"
$mainReadmeExists = Test-Path $mainReadmePath

if ($mainReadmeExists) {
    # Create a backup of the existing README.md
    Copy-Item -Path $mainReadmePath -Destination "$mainReadmePath.bak"
    Write-Host "Created backup of existing README.md as README.md.bak" -ForegroundColor Yellow
}

$mainReadmeContent = @"
# Quantum-Plasmoid Framework

A radical interdisciplinary approach to understanding complex systems through recursive, fractal principles.

## Repository Structure

- [Documentation](./docs/): Core framework documentation
  - Introduction
  - Mathematical Foundations
  - Research Roadmap

- [Core Concepts](./core-concepts/): Foundational theoretical concepts
  - [Fractal Systems](./core-concepts/fractal-systems/): Explorations of fractal principles
  - [Quantum Dynamics](./core-concepts/quantum-dynamics/): Quantum physics connections
  - [Recursive Systems](./core-concepts/recursive-systems/): Meta-theory of recursion
  - [Consciousness](./core-concepts/consciousness/): Consciousness function models

- [Theorems](./theorems/): Major theoretical formulations
  - [Eigenmode Theory](./theorems/eigenmode-theory/): Neural eigenmode models
  - [ORCHARD Theorem](./theorems/orchard-theorem/): Recursive neural dynamics
  - [ζ-Orchard Correspondence](./theorems/zeta-correspondence/): Zeta function connections

- [Time Models](./time-models/): Fractal time conceptions

- [Applications](./applications/): Applied theories and protocols
  - [Computational](./applications/computational/): Computational implementations
  - [Health](./applications/health/): Health-related applications
  - [Integrative](./applications/integrative/): Interdisciplinary extensions

- [Visualizations](./visualizations/): Visual representations of key concepts
"@

# Write the new content to README.md
if (-not $mainReadmeExists) {
    $mainReadmeContent | Out-File -FilePath $mainReadmePath -Encoding utf8
    Write-Host "Created new README.md" -ForegroundColor Yellow
} else {
    # Append a note about the reorganization
    $mainReadmeContent += @"

## Repository Reorganization

This repository was reorganized on $(Get-Date -Format "yyyy-MM-dd") to better reflect the conceptual relationships between different aspects of the Quantum-Plasmoid framework. The unifiedTheories folder has been replaced with a more structured hierarchy.
"@
    
    $mainReadmeContent | Out-File -FilePath $mainReadmePath -Encoding utf8
    Write-Host "Updated existing README.md" -ForegroundColor Yellow
}

# Check if unifiedTheories is now empty
$remainingFiles = Get-ChildItem -Path $unifiedTheories -File
if ($remainingFiles.Count -eq 0) {
    # Empty directory - safe to remove
    Remove-Item -Path $unifiedTheories -Force
    Write-Host "Removed empty unifiedTheories directory" -ForegroundColor Green
} else {
    # Directory still contains files
    Write-Host "WARNING: unifiedTheories directory still contains files and was not removed:" -ForegroundColor Red
    foreach ($file in $remainingFiles) {
        Write-Host "  - $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "Repository reorganization complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Review the new structure and make any manual adjustments" -ForegroundColor Cyan
Write-Host "2. Update any internal references between documents" -ForegroundColor Cyan
Write-Host "3. Commit the changes to Git" -ForegroundColor Cyan