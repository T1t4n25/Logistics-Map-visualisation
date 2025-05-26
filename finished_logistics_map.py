import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import time

class LogisticMapVisualizer:

    def __init__(self):
        self.fig_size = (12, 8)
        self.dpi = 100
        
    def logistic_map(self, x, a):
        return a * x * (1 - x)
    
    def plot_stability(self, a=2.5, x_range=(0, 1), n_points=1000):
        fig, ax = plt.subplots(figsize=(8, 6), dpi=self.dpi)
        
        # Generate x values for smooth curve
        x = np.linspace(x_range[0], x_range[1], n_points)
        
        y_logistic = self.logistic_map(x, a)
        
        # Plot the logistic map function and identity line
        ax.plot(x, y_logistic, 'b-', linewidth=2, label=f'f(x) = {a}x(1-x)')
        ax.plot(x, x, 'r--', linewidth=2, label='y = x (identity line)')

        fixed_points = [0]
        if a > 1:
            fixed_points.append((a - 1) / a)
        
        for fp in fixed_points:
            if x_range[0] <= fp <= x_range[1]:
                ax.plot(fp, fp, 'ro', markersize=8, 
                       label=f'Fixed point: x = {fp:.3f}')
        
        ax.set_xlabel('x_n', fontsize=12)
        ax.set_ylabel('x_{n+1}', fontsize=12)
        ax.set_title(f'Stability Plot: Logistic Map with a = {a}', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlim(x_range)
        ax.set_ylim(x_range)
        
        plt.tight_layout()
        plt.show()
    
    def plot_cobweb(self, a=3.2, x0=0.1, n_iter=50, x_range=(0, 1)):
        fig, ax = plt.subplots(figsize=(8, 8), dpi=self.dpi)
        
        x = np.linspace(x_range[0], x_range[1], 1000)
        y_logistic = self.logistic_map(x, a)
        
        ax.plot(x, y_logistic, 'b-', linewidth=2, label=f'f(x) = {a}x(1-x)')
        ax.plot(x, x, 'r--', linewidth=2, label='y = x')
        
        x_n = x0
        cobweb_x = []
        cobweb_y = []
        
        cobweb_x.append(x_n)
        cobweb_y.append(0)
        cobweb_x.append(x_n)
        cobweb_y.append(x_n)
        
        # Generate cobweb iterations
        for i in range(n_iter):
            x_next = self.logistic_map(x_n, a)
            
            cobweb_x.append(x_n)
            cobweb_y.append(x_next)
            
            cobweb_x.append(x_next)
            cobweb_y.append(x_next)
            
            x_n = x_next
            
            if x_n < x_range[0] or x_n > x_range[1]:
                break
        
        ax.plot(cobweb_x, cobweb_y, 'g-', linewidth=1, alpha=0.7, 
                label=f'Cobweb (x₀ = {x0})')
        
        ax.plot(x0, 0, 'go', markersize=8, label=f'Initial: x₀ = {x0}')
        
        ax.set_xlabel('x_n', fontsize=12)
        ax.set_ylabel('x_{n+1}', fontsize=12)
        ax.set_title(f'Cobweb Diagram: a = {a}, x₀ = {x0}, {n_iter} iterations', 
                    fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlim(x_range)
        ax.set_ylim(x_range)
        
        plt.tight_layout()
        plt.show()
    
    def generate_bifurcation_data(self, a_range=(0.5, 4.0), n_a=2000, 
                                 x0=0.5, n_iterations=1000, n_transient=500):
        print(f"Generating bifurcation data...")
        print(f"Parameter range: {a_range}")
        print(f"Number of a values: {n_a}")
        print(f"Iterations per a: {n_iterations} (discarding first {n_transient})")
        
        start_time = time.time()
        
        a_values = np.linspace(a_range[0], a_range[1], n_a)
        bifurcation_a = []
        bifurcation_x = []
        
        for i, a in enumerate(a_values):
            if i % (n_a // 20) == 0:  # Progress indicator
                progress = (i / n_a) * 100
                print(f"Progress: {progress:.1f}%")
            
            x = x0
            
            # Iterate and discard transients
            for _ in range(n_transient):
                x = self.logistic_map(x, a)
            
            # Collect asymptotic values
            for _ in range(n_iterations - n_transient):
                x = self.logistic_map(x, a)
                bifurcation_a.append(a)
                bifurcation_x.append(x)
        
        elapsed_time = time.time() - start_time
        print(f"Data generation complete in {elapsed_time:.2f} seconds")
        
        return np.array(bifurcation_a), np.array(bifurcation_x)
    
    def plot_bifurcation(self, a_range=(2.5, 4.0), n_a=2000, x0=0.5, 
                        n_iterations=1000, n_transient=500):

        a_vals, x_vals = self.generate_bifurcation_data(
            a_range, n_a, x0, n_iterations, n_transient)
        
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)
        
        ax.plot(a_vals, x_vals, ',k', alpha=0.25, markersize=0.1)
        
        ax.set_xlabel('Parameter a', fontsize=12)
        ax.set_ylabel('x_n', fontsize=12)
        ax.set_title('Bifurcation Diagram of Logistic Map', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        bifurcation_points = {
            3.0: 'Period-1 → Period-2',
            3.449: 'Period-2 → Period-4', 
            3.544: 'Period-4 → Period-8',
            3.57: 'Onset of Chaos'
        }
        
        for point, label in bifurcation_points.items():
            if a_range[0] <= point <= a_range[1]:
                ax.axvline(x=point, color='red', linestyle='--', alpha=0.7)
                ax.text(point, 0.9, label, rotation=90, fontsize=8, 
                       verticalalignment='bottom')
        
        ax.set_xlim(a_range)
        ax.set_ylim(0, 1)
        
        plt.tight_layout()
        plt.show()
    
    def comprehensive_analysis(self, a_values=[1.5, 2.8, 3.2, 3.5, 3.8]):
        n_plots = len(a_values)
        fig = plt.figure(figsize=(15, 10), dpi=self.dpi)
        gs = GridSpec(2, 3, figure=fig)
        
        # Plot cobweb diagrams for different a values
        for i, a in enumerate(a_values[:4]):
            row = i // 2
            col = i % 2
            ax = fig.add_subplot(gs[row, col])
            
            # Generate cobweb data
            x = np.linspace(0, 1, 1000)
            y_logistic = self.logistic_map(x, a)
            
            ax.plot(x, y_logistic, 'b-', linewidth=2)
            ax.plot(x, x, 'r--', linewidth=2)
            
            x0 = 0.1
            x_n = x0
            cobweb_x, cobweb_y = [], []
            
            for _ in range(30):
                x_next = self.logistic_map(x_n, a)
                cobweb_x.extend([x_n, x_n, x_next])
                cobweb_y.extend([x_n, x_next, x_next])
                x_n = x_next
            
            ax.plot(cobweb_x, cobweb_y, 'g-', linewidth=1, alpha=0.7)
            ax.set_title(f'a = {a}')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.grid(True, alpha=0.3)
        
        ax_bif = fig.add_subplot(gs[:, 2])
        
        # Generate bifurcation data (smaller range for speed)
        a_vals, x_vals = self.generate_bifurcation_data(
            a_range=(1.0, 4.0), n_a=1000, n_iterations=500, n_transient=250)
        
        ax_bif.plot(a_vals, x_vals, ',k', alpha=0.3, markersize=0.1)
        ax_bif.set_xlabel('Parameter a')
        ax_bif.set_ylabel('x_n')
        ax_bif.set_title('Bifurcation Diagram')
        ax_bif.grid(True, alpha=0.3)
        
        # Mark the a values being analyzed
        for a in a_values:
            ax_bif.axvline(x=a, color='red', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.show()

def analyze_parameter_regimes():

    print("Logistic Map Parameter Analysis")
    print("=" * 50)
    
    regimes = [
        (0.5, "Population dies out (x → 0)"),
        (1.5, "Stable fixed point"),
        (2.8, "Stable fixed point"),
        (3.1, "Period-2 cycle"),
        (3.5, "Period-4 cycle"),
        (3.7, "Chaotic behavior"),
        (3.83, "Period-3 window in chaos"),
        (4.0, "Full chaos")
    ]
    
    visualizer = LogisticMapVisualizer()
    
    for a, description in regimes:
        print(f"\na = {a}: {description}")
        
        # Calculate fixed points
        if a <= 1:
            print(f"  Fixed point: x = 0")
        else:
            fp1 = 0
            fp2 = (a - 1) / a
            print(f"  Fixed points: x = {fp1}, x = {fp2:.4f}")
        
        # Show first few iterations
        x = 0.5
        print(f"  First 10 iterations from x₀ = {x}:")
        iterations = [x]
        for i in range(10):
            x = visualizer.logistic_map(x, a)
            iterations.append(x)
        
        print(f"  {' → '.join([f'{val:.4f}' for val in iterations[:6]])}...")

def main():

    print("Logistic Map Visualization Suite")
    print("=" * 40)
    
    visualizer = LogisticMapVisualizer()
    
    # 1. Stability Plot
    print("\n1. Creating Stability Plot...")
    visualizer.plot_stability(a=2.5)
    
    # 2. Cobweb Diagrams for different behaviors
    print("\n2. Creating Cobweb Diagrams...")
    
    # Stable fixed point
    print("   - Stable fixed point (a = 2.8)")
    visualizer.plot_cobweb(a=2.8, x0=0.1, n_iter=20)
    
    # Period-2 cycle
    print("   - Period-2 cycle (a = 3.1)")
    visualizer.plot_cobweb(a=3.1, x0=0.1, n_iter=30)
    
    # Chaotic behavior
    print("   - Chaotic behavior (a = 3.7)")
    visualizer.plot_cobweb(a=3.7, x0=0.1, n_iter=50)
    
    # 3. Bifurcation Diagram
    print("\n3. Creating Bifurcation Diagram...")
    visualizer.plot_bifurcation(a_range=(2.5, 4.0), n_a=1500)
    
    # 4. Comprehensive Analysis
    print("\n4. Creating Comprehensive Analysis...")
    visualizer.comprehensive_analysis()
    
    # 5. Parameter Analysis
    print("\n5. Parameter Regime Analysis...")
    analyze_parameter_regimes()
    
    print("\nVisualization complete!")

if __name__ == "__main__":
    main()