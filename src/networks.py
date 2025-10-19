    # networks.py
    import networkx as nx

    def create_karate_club():
        """Returns the Zachary's Karate Club graph."""
        return nx.karate_club_graph()

    def create_star_graph(n=20):
        """Creates a Star graph with n nodes."""
        return nx.star_graph(n - 1)

    def create_complete_graph(n=20):
        """Creates a Complete graph with n nodes."""
        return nx.complete_graph(n)

    def create_grid_2d_graph(m=5, n=5):
        """Creates a 2D Grid graph of size m x n."""
        return nx.grid_2d_graph(m, n)

    def create_er_graph(n=100, p=0.04, seed=42):
        """Creates an Erdős-Rényi (ER) graph."""
        return nx.erdos_renyi_graph(n, p, seed=seed)

    def create_ba_graph(n=100, m=2, seed=42):
        """Creates a Barabási-Albert (BA) scale-free graph."""
        return nx.barabasi_albert_graph(n, m, seed=seed)

    def create_ws_graph(n=100, k=4, p=0.1, seed=42):
        """Creates a Watts-Strogatz (WS) small-world graph."""
        return nx.watts_strogatz_graph(n, k, p, seed=seed)

    def load_power_grid():
        """
        Loads the US Power Grid network.
        This is a simplified version of the network for demonstration.
        Requires 'power_grid.edgelist' file.
        """
        # Create a dummy graph if the file doesn't exist.
        # For real use, you would download and provide the edgelist file.
        try:
            G = nx.read_edgelist('power_grid.edgelist', nodetype=int)
            return G
        except FileNotFoundError:
            print("Warning: 'power_grid.edgelist' not found. Creating a placeholder BA graph instead.")
            return create_ba_graph(4941, 2, seed=42) # Placeholder

    def load_yeast_protein():
        """
        Loads a Yeast protein interaction network.
        Requires 'yeast.edgelist' file.
        """
        # Create a dummy graph if the file doesn't exist.
        try:
            G = nx.read_edgelist('yeast.edgelist', nodetype=str)
            # The real yeast dataset might have multiple components, get the giant component
            giant = max(nx.connected_components(G), key=len)
            return G.subgraph(giant).copy()
        except FileNotFoundError:
            print("Warning: 'yeast.edgelist' not found. Creating a placeholder BA graph instead.")
            return create_ba_graph(2361, 3, seed=42) # Placeholder
