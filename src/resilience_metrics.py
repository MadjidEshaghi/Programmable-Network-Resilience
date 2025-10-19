    # resilience_metrics.py
    import networkx as nx
    import numpy as np
    import scipy.sparse as sp
    from scipy.stats import entropy

    def calculate_omega_betweenness(G):
        """Calculates Network Resistance based on edge betweenness centrality."""
        if G.number_of_nodes() == 0 or G.number_of_edges() == 0:
            return 0.0
        
        try:
            # Normalize='overall' to get probabilities summing to 1
            edge_bc = nx.edge_betweenness_centrality(G, normalized=False)
            flow_values = np.array(list(edge_bc.values()))
            
            # If all flows are zero (e.g., a disconnected graph with no paths)
            if np.sum(flow_values) == 0:
                 # In this case, distribute flow uniformly as a fallback
                 flow_values = np.ones(G.number_of_edges())
            
            # Convert to probability distribution
            probabilities = flow_values / np.sum(flow_values)
            
            # Calculate normalized entropy (Omega)
            h_max = np.log(G.number_of_edges()) if G.number_of_edges() > 1 else 1.0
            h_actual = entropy(probabilities, base=np.e)
            
            return h_actual / h_max
        except Exception:
            # Handles cases where calculation might fail (e.g., very large or disconnected graphs)
            return np.nan


    def calculate_omega_electrical(G):
        """Calculates Network Resistance based on electrical current flow."""
        if G.number_of_nodes() < 2 or G.number_of_edges() == 0:
            return 0.0

        # Ensure graph is connected
        if not nx.is_connected(G):
            # Work with the largest connected component
            giant_nodes = max(nx.connected_components(G), key=len)
            G = G.subgraph(giant_nodes).copy()
            if G.number_of_nodes() < 2 or G.number_of_edges() == 0:
                return 0.0

        L = nx.laplacian_matrix(G).astype(np.float64)
        # Use pseudo-inverse for robustness, handles singular matrices
        L_pinv = np.linalg.pinv(L.toarray())
        
        effective_resistances = []
        for i, j in G.edges():
            # Need to map node labels to integer indices if they are not already
            node_list = list(G.nodes())
            u, v = node_list.index(i), node_list.index(j)
            # Kirchhoff's formula for effective resistance
            R_eff = L_pinv[u, u] + L_pinv[v, v] - 2 * L_pinv[u, v]
            effective_resistances.append(R_eff)
            
        currents = 1.0 / np.array(effective_resistances)
        
        # Power dissipated in each edge is P = I^2 * R = (1/R_eff)^2 * R_eff = 1/R_eff
        # Total power is sum of currents
        total_power = np.sum(currents)
        
        # Probability distribution of flow (power)
        probabilities = currents / total_power
        
        h_max = np.log(G.number_of_edges()) if G.number_of_edges() > 1 else 1.0
        h_actual = entropy(probabilities, base=np.e)
        
        return h_actual / h_max

    def simulate_targeted_attack(G):
        """
        Simulates a targeted attack on high-degree nodes and returns the AUC.
        """
        if G.number_of_nodes() == 0:
            return 0.0

        temp_G = G.copy()
        initial_gcc_size = len(max(nx.connected_components(temp_G), key=len, default=[]))
        if initial_gcc_size == 0:
            return 0.0

        # Sort nodes by degree (descending)
        nodes_sorted_by_degree = sorted(temp_G.nodes(), key=lambda n: temp_G.degree(n), reverse=True)
        
        gcc_sizes = [initial_gcc_size]
        
        for node_to_remove in nodes_sorted_by_degree:
            if temp_G.has_node(node_to_remove):
                temp_G.remove_node(node_to_remove)
                if temp_G.number_of_nodes() > 0:
                    # Find the largest connected component
                    largest_comp = max(nx.connected_components(temp_G), key=len, default=[])
                    gcc_sizes.append(len(largest_comp))
                else:
                    gcc_sizes.append(0)
        
        # Normalize sizes by initial size
        normalized_sizes = np.array(gcc_sizes) / initial_gcc_size
        
        # Calculate AUC (Area Under the Curve) using trapezoidal rule
        auc = np.trapz(normalized_sizes, dx=1/len(normalized_sizes))
        
        return auc
