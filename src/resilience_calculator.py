    # src/resilience_calculator.py
    import networkx as nx
    import numpy as np
    import random
    import time

    def calculate_algebraic_connectivity(G):
        if not nx.is_connected(G):
            return 0.0
        try:
            laplacian = nx.laplacian_matrix(G).asfptype()
            eigenvalues = np.linalg.eigvalsh(laplacian.toarray())
            return max(0, eigenvalues[1])
        except Exception as e:
            print(f"  [Warning] خطا در محاسبه λ₂: {e}. مقدار 0.0 برگردانده شد.")
            return 0.0

    def pcm_strategy(G_in):
        G = G_in.copy()
        if G.number_of_nodes() < 2: return None
        subgraph = G
        if not nx.is_connected(G):
            largest_cc_nodes = max(nx.connected_components(G), key=len)
            subgraph = G.subgraph(largest_cc_nodes).copy()
        if subgraph.number_of_nodes() < 2: return None
        all_paths_lengths = dict(nx.all_pairs_shortest_path_length(subgraph))
        max_len, start_node, end_node = -1, -1, -1
        for source, paths in all_paths_lengths.items():
            for target, length in paths.items():
                if length > max_len and not G.has_edge(source, target):
                    max_len, start_node, end_node = length, source, target
        if start_node != -1 and end_node != -1:
            return (start_node, end_node)
        else:
            return random_strategy(G)

    def random_strategy(G_in):
        G = G_in.copy()
        nodes = list(G.nodes())
        if len(nodes) < 2: return None
        max_attempts = min(100 * G.number_of_nodes(), G.number_of_nodes()**2) 
        for _ in range(max_attempts):
            u, v = random.sample(nodes, 2)
            if u != v and not G.has_edge(u, v):
                return (u, v)
        return None

    def hub_strategy(G_in):
        G = G_in.copy()
        if G.number_of_nodes() < 2: return None
        sorted_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)
        if len(sorted_nodes) < 2: return None
        for i in range(len(sorted_nodes)):
            for j in range(i + 1, len(sorted_nodes)):
                u, v = sorted_nodes[i][0], sorted_nodes[j][0]
                if u != v and not G.has_edge(u, v):
                    return (u, v)
        return random_strategy(G)

    def betweenness_strategy(G_in):
        G = G_in.copy()
        if G.number_of_nodes() < 2: return None
        k = min(200, G.number_of_nodes()) if G.number_of_nodes() > 200 else None
        betweenness = nx.betweenness_centrality(G, k=k, normalized=True)
        sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_nodes) < 2: return None
        for i in range(len(sorted_nodes)):
            for j in range(i + 1, len(sorted_nodes)):
                u, v = sorted_nodes[i][0], sorted_nodes[j][0]
                if u != v and not G.has_edge(u, v):
                    return (u, v)
        return random_strategy(G)

    def run_single_strategy_simulation(G_original, num_edges_to_add, strategy_func):
        G = nx.convert_node_labels_to_integers(G_original.copy(), first_label=0)
        connectivity_history = [calculate_algebraic_connectivity(G)]
        print(f"--- شروع شبیه‌سازی برای: {strategy_func.__name__} ---")
        print(f"اتصال جبری اولیه (λ₂): {connectivity_history[0]:.5f}")
        for i in range(num_edges_to_add):
            start_time = time.time()
            edge_to_add = strategy_func(G)
            if edge_to_add is None:
                print(f"مرحله {i+1}: استراتژی نتوانست یالی پیدا کند. شبیه‌سازی متوقف شد.")
                connectivity_history.extend([connectivity_history[-1]] * (num_edges_to_add - i))
                break
            u, v = edge_to_add
            G.add_edge(u, v)
            new_connectivity = calculate_algebraic_connectivity(G)
            connectivity_history.append(new_connectivity)
            end_time = time.time()
            print(f"مرحله {i+1}/{num_edges_to_add}: یال {edge_to_add} اضافه شد. λ₂ جدید: {new_connectivity:.5f}. (زمان: {end_time - start_time:.2f} ثانیه)")
        return connectivity_history
