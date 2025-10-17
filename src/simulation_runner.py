    # src/simulation_runner.py
    import networkx as nx
    import urllib.request
    import io
    import gzip
    import zipfile
    import os
    from resilience_calculator import (
        run_single_strategy_simulation,
        pcm_strategy,
        betweenness_strategy,
        hub_strategy,
        random_strategy
    )
    from plotting import plot_and_save_results

    def load_network(network_name, data_dir="../data"):
        print(f"\n[INFO] در حال بارگذاری شبکه: {network_name.upper()}...")
        if network_name == 'ba': return nx.barabasi_albert_graph(n=1000, m=3, seed=42)
        elif network_name == 'er': return nx.erdos_renyi_graph(n=1000, p=0.006, seed=42)
        elif network_name == 'lattice': return nx.grid_2d_graph(32, 32)
        file_path = os.path.join(data_dir, f"{network_name}.gml")
        if network_name == 'power' and not os.path.exists(file_path):
            print(f"[INFO] فایل '{file_path}' یافت نشد. در حال دانلود از اینترنت...")
            url = "http://www-personal.umich.edu/~mejn/netdata/power.zip"
            try:
                with urllib.request.urlopen(url, timeout=30) as sock: s = io.BytesIO(sock.read())
                with zipfile.ZipFile(s) as zf:
                    gml_file = zf.open('power.gml', 'r')
                    lines = (line.decode('utf-8').strip() for line in gml_file)
                    clean_lines = [line for line in lines if not line.startswith('*')]
                    G = nx.parse_gml(clean_lines, label='id')
                    if not os.path.exists(data_dir): os.makedirs(data_dir)
                    nx.write_gml(G, file_path)
                    print(f"[INFO] شبکه برق در '{file_path}' ذخیره شد.")
                    return G
            except Exception as e:
                print(f"[ERROR] دانلود یا پردازش شبکه برق ناموفق بود: {e}")
                return None
        try:
            if file_path.endswith('.gml'): G = nx.read_gml(file_path, label='id')
            else: G = nx.read_edgelist(file_path.replace('.gml', '.edgelist'), nodetype=int)
            print(f"شبکه از فایل '{file_path}' با موفقیت بارگذاری شد.")
            return G
        except FileNotFoundError:
            print(f"[ERROR] فایل شبکه '{file_path}' پیدا نشد. لطفاً نام شبکه را بررسی کنید.")
            return None

    def main():
        NETWORK_CHOICE = 'power'
        NUM_EDGES_TO_ADD = 20
        G_original = load_network(NETWORK_CHOICE)
        if G_original is None: return
        if not nx.is_connected(G_original):
            print("[INFO] گراف اولیه همبند نیست. بزرگترین مولفه همبند استخراج می‌شود.")
            largest_cc_nodes = max(nx.connected_components(G_original), key=len)
            G_original = G_original.subgraph(largest_cc_nodes).copy()
        print(f"[INFO] مشخصات شبکه نهایی: {G_original.number_of_nodes()} گره و {G_original.number_of_edges()} یال.")
        strategies = {
            "PCM (Ours)": pcm_strategy,
            "High Betweenness": betweenness_strategy,
            "Hub (High Degree)": hub_strategy,
            "Random": random_strategy
        }
        results = {}
        for name, func in strategies.items():
            results[name] = run_single_strategy_simulation(G_original, NUM_EDGES_TO_ADD, func)
        print("\n[INFO] تمام شبیه‌سازی‌ها تکمیل شد. در حال تولید نمودار...")
        plot_and_save_results(
            results=results, network_name=NETWORK_CHOICE,
            num_nodes=G_original.number_of_nodes(), num_edges=G_original.number_of_edges(),
            num_edges_added=NUM_EDGES_TO_ADD, output_dir="../results"
        )

    if __name__ == "__main__":
        main()
