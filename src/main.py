import networkx as nx
import matplotlib.pyplot as plt
import random

def create_complex_network(nodes=20, edge_prob=0.2):
    """ایجاد یک گراف پیچیده با استفاده از مدل Erdős-Rényi"""
    G = nx.erdos_renyi_graph(nodes, edge_prob, seed=42, directed=False)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(nodes, edge_prob, seed=random.randint(0, 1000), directed=False)
    return G

def find_critical_nodes(G, top_n=3):
    """پیدا کردن مهم‌ترین گره‌ها بر اساس معیار مرکزیت بینابینی (Betweenness Centrality)"""
    centrality = nx.betweenness_centrality(G)
    # مرتب‌سازی گره‌ها بر اساس مقدار مرکزیت به صورت نزولی
    sorted_nodes = sorted(centrality.items(), key=lambda item: item[1], reverse=True)
    # برگرداندن N گره برتر
    critical_nodes = [node for node, score in sorted_nodes[:top_n]]
    return critical_nodes

def simulate_failure_and_reroute(G, failed_node):
    """
    شبیه‌سازی خرابی یک گره و تلاش برای یافتن مسیر جایگزین
    بین همسایگان گره خراب شده.
    """
    if failed_node not in G:
        print(f"گره {failed_node} در شبکه وجود ندارد.")
        return G, False, []

    neighbors = list(G.neighbors(failed_node))
    print(f"گره {failed_node} خراب شد. همسایگان آن عبارتند از: {neighbors}")

    G_resilient = G.copy()
    G_resilient.remove_node(failed_node)
    print(f"گره {failed_node} و تمام یال‌های متصل به آن حذف شدند.")

    rerouted_paths = []
    # تلاش برای ایجاد مسیر جایگزین بین هر جفت از همسایگان گره خراب
    for i in range(len(neighbors)):
        for j in range(i + 1, len(neighbors)):
            u, v = neighbors[i], neighbors[j]
            # اگر مسیری بین دو همسایه وجود نداشته باشد، یک یال مستقیم اضافه می‌کنیم
            if not nx.has_path(G_resilient, u, v):
                print(f"هیچ مسیری بین {u} و {v} وجود ندارد. ایجاد یال مستقیم برای بازیابی اتصال.")
                G_resilient.add_edge(u, v)
                rerouted_paths.append((u, v))

    is_connected_after = nx.is_connected(G_resilient)
    return G_resilient, is_connected_after, rerouted_paths

def visualize_network(G, title, critical_nodes=None, failed_node=None, rerouted_edges=None):
    """نمایش گرافیکی شبکه"""
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 12))
    
    node_colors = []
    for node in G.nodes():
        if node == failed_node:
            node_colors.append('red')
        elif critical_nodes and node in critical_nodes:
            node_colors.append('orange')
        else:
            node_colors.append('skyblue')
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_size=10, font_color='black')

    if rerouted_edges:
        nx.draw_networkx_edges(G, pos, edgelist=rerouted_edges, edge_color='green', width=2.5, style='dashed')

    plt.title(title, size=15)
    plt.show()

if __name__ == '__main__':
    # 1. ایجاد و نمایش شبکه اولیه
    original_network = create_complex_network(nodes=15, edge_prob=0.3)
    print("شبکه اولیه ایجاد شد.")
    visualize_network(original_network, "شبکه اصلی و پیچیده")

    # 2. پیدا کردن و نمایش گره‌های حیاتی
    critical_nodes = find_critical_nodes(original_network, top_n=3)
    print(f"گره‌های حیاتی شناسایی شدند: {critical_nodes}")
    visualize_network(original_network, "شناسایی گره‌های حیاتی (نارنجی)", critical_nodes=critical_nodes)

    # 3. شبیه‌سازی خرابی یکی از گره‌های حیاتی
    node_to_fail = critical_nodes[0]
    print(f"\n--- شبیه‌سازی خرابی گره حیاتی: {node_to_fail} ---")
    
    resilient_network, is_connected, rerouted = simulate_failure_and_reroute(original_network, node_to_fail)

    # 4. نمایش شبکه پس از خرابی و بازیابی
    status = "متصل" if is_connected else "غیرمتصل (Partitioned)"
    visualize_network(resilient_network, 
                      f"شبکه پس از خرابی گره {node_to_fail} و بازیابی (وضعیت: {status})",
                      failed_node=node_to_fail, 
                      critical_nodes=critical_nodes,
                      rerouted_edges=rerouted)
    
    if is_connected:
        print(f"موفقیت: شبکه پس از خرابی گره {node_to_fail} و اعمال مسیرهای جایگزین، همچنان متصل باقی ماند.")
    else:
        print(f"هشدار: با وجود تلاش برای بازیابی، شبکه به چند بخش تقسیم شده است.")
