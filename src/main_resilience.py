    # main.py
    import networks
    import resilience_metrics
    import pandas as pd

    def run_analysis():
        """
        Runs the full analysis for all benchmark networks and prints the results table.
        """
        network_constructors = {
            "Karate Club": networks.create_karate_club,
            "Star Graph (N=20)": networks.create_star_graph,
            "Complete Graph (N=20)": networks.create_complete_graph,
            "Grid 2D (5x5)": networks.create_grid_2d_graph,
            "ER (N=100, p=0.04)": networks.create_er_graph,
            "BA (N=100, m=2)": networks.create_ba_graph,
            "WS (N=100, k=4, p=0.1)": networks.create_ws_graph,
            # "US Power Grid": networks.load_power_grid, # Uncomment if you have the data file
            # "Yeast": networks.load_yeast_protein, # Uncomment if you have the data file
        }

        results = []

        for name, constructor_func in network_constructors.items():
            print(f"Analyzing {name}...")
            G = constructor_func()
            
            auc = resilience_metrics.simulate_targeted_attack(G)
            omega_btn = resilience_metrics.calculate_omega_betweenness(G)
            omega_elec = resilience_metrics.calculate_omega_electrical(G)
            
            results.append({
                "Network": name,
                "AUC": f"{auc:.6f}",
                "Omega_btn": f"{omega_btn:.6f}" if not pd.isna(omega_btn) else "NaN",
                "Omega_elec": f"{omega_elec:.6f}"
            })
        
        # Create and print a pandas DataFrame for nice formatting
        df = pd.DataFrame(results)
        print("\n" + "="*60)
        print("           Final Resilience Metrics Results")
        print("="*60)
        print(df.to_string(index=False))
        print("="*60)

    if __name__ == "__main__":
        # Ensure you have the necessary libraries installed:
        # pip install networkx numpy scipy pandas
        run_analysis()
