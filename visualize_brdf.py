"""
BEM3D BRDF Binary File Visualization Tool
Usage: python visualize_brdf.py <filename> [output_image]
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

def load_brdf(filename, shape=None):
    """Load BRDF binary file"""
    with open(filename, 'rb') as f:
        data = np.fromfile(f, dtype=np.float32)
    
    if shape is None:
        # Assume square matrix
        size = int(np.sqrt(len(data)))
        if size * size != len(data):
            print(f"Warning: data length {len(data)} is not a perfect square")
            return data
        shape = (size, size)
    
    return data.reshape(shape)

def visualize_brdf(filename, output=None):
    """Visualize BRDF data"""
    print(f"Loading: {filename}")
    brdf = load_brdf(filename)
    
    print(f"Shape: {brdf.shape}")
    print(f"Range: [{brdf.min():.6f}, {brdf.max():.6f}]")
    print(f"Mean: {brdf.mean():.6f}")
    print(f"Std Dev: {brdf.std():.6f}")
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. BRDF Heatmap (log scale)
    ax = axes[0, 0]
    im = ax.imshow(brdf, cmap='hot', norm='log')
    ax.set_title('BRDF (Log Scale)')
    ax.set_xlabel('Azimuth (phi)')
    ax.set_ylabel('Zenith (theta)')
    plt.colorbar(im, ax=ax)
    
    # 2. BRDF Heatmap (linear scale)
    ax = axes[0, 1]
    im = ax.imshow(brdf, cmap='hot')
    ax.set_title('BRDF (Linear Scale)')
    ax.set_xlabel('Azimuth (phi)')
    ax.set_ylabel('Zenith (theta)')
    plt.colorbar(im, ax=ax)
    
    # 3. Histogram
    ax = axes[1, 0]
    ax.hist(brdf.flatten(), bins=100, edgecolor='black')
    ax.set_xlabel('BRDF Value')
    ax.set_ylabel('Frequency')
    ax.set_title('BRDF Value Distribution')
    ax.set_yscale('log')
    
    # 4. Center line slices
    ax = axes[1, 1]
    center = brdf.shape[0] // 2
    ax.plot(brdf[center, :], label='Horizontal (center row)', linewidth=2)
    ax.plot(brdf[:, center], label='Vertical (center col)', linewidth=2)
    ax.set_xlabel('Pixel Position')
    ax.set_ylabel('BRDF Value')
    ax.set_title('Center Line Slices')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output:
        plt.savefig(output, dpi=150, bbox_inches='tight')
        print(f"Image saved to: {output}")
    else:
        plt.show()
    
    return brdf

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python visualize_brdf.py <filename> [output_image]")
        print("Example: python visualize_brdf.py data/test/BRDF_wvl0_wi0.binary brdf_output.png")
        sys.exit(1)
    
    filename = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(filename).exists():
        print(f"Error: File not found {filename}")
        sys.exit(1)
    
    visualize_brdf(filename, output)
