import networkx as nx
import matplotlib.pyplot as plt
import random
import copy

# --- بخش 1: توابع اصلی و کمکی ---

def create_complex_network(num_nodes=50, num_edges_to_add=3):
    """ایجاد یک شبکه پیچیده از نوع Barabási-Albert برای شبیه‌سازی دنیای واقعی."""
    G = nx.barabasi_albert_graph(num_nodes, num_edges_to_add, seed=42)
    print(f"شبکه اولیه با {G.number_of_nodes()} گره و {G.number_of_edges()} یال ساخته شد.")
    return G

def calculate_resilience_metrics(G):
    """محاسبه معیارهای کلیدی تاب‌آوری شبکه."""
    if not nx.is_connected(G):
        # اگر شبکه چند تکه شده باشد، بزرگترین قطعه را تحلیل می‌کنیم
        largest_cc_nodes = max(nx.connected_components(G), key=len)
        largest_cc = G.subgraph(largest_cc_nodes)
        connectivity = 0  # شبکه متصل نیست
        avg_shortest_path = nx.average_shortest_path_length(largest_cc)
        num_components = nx.number_connected_components(G)
    else:
        largest_cc = G
        connectivity = 1  # شبکه متصل است
        avg_shortest_path = nx.average_shortest_path_length(G)
        num_components = 1
        
    return {
        "is_connected": connectivity,
        "number_of_components": num_components,
        "largest_component_size": largest_cc.number_of_nodes(),
        "average_shortest_path": avg_shortest_path
    }

def visualize_network(G, title, pos=None, ax=None):
    """بصری‌سازی گراف شبکه."""
    if pos is None:
        pos = nx.spring_layout(G, seed=42)
    if ax is None:
        plt.figure(figsize=(10, 8))
        ax = plt.gca()
    
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray', ax=ax)
    ax.set_title(title, fontsize=16)
    return pos

# --- بخش 2: پیاده‌سازی سه استراتژی مختلف ---

# استراتژی 1: روش پیشنهادی شما (خرابی هدفمند + ترمیم هوشمند)
def simulate_proposed_method(G_original):
    """شبیه‌سازی خرابی گره بحرانی و ترمیم هوشمند."""
    G = G_original.copy()
    
    # پیدا کردن گره بحرانی
    centrality = nx.betweenness_centrality(G)
    critical_node = max(centrality, key=centrality.get)
    print(f"\n--- شروع روش پیشنهادی: گره بحرانی {critical_node} حذف می‌شود ---")
    
    neighbors = list(G.neighbors(critical_node))
    G.remove_node(critical_node)
    
    # استراتژی ترمیم: اتصال مجدد همسایگان گره حذف شده
    print("اجرای استراتژی ترمیم هوشمند...")
    for i in range(len(neighbors)):
        for j in range(i + 1, len(neighbors)):
            u, v = neighbors[i], neighbors[j]
            if not G.has_edge(u, v):
                # اگر مسیری بین دو همسایه وجود نداشته باشد، یک یال مستقیم اضافه کن
                if not nx.has_path(G, u, v):
                    print(f"ایجاد یال ترمیمی بین {u} و {v}")
                    G.add_edge(u, v)
    return G

# استراتژی 2: حمله به سبک مقاله Nature 2000 (حذف مهم‌ترین گره‌ها بدون ترمیم)
def simulate_nature_attack(G_original, num_nodes_to_remove=1):
    """شبیه‌سازی حمله هدفمند به گره‌های با بالاترین درجه (بدون ترمیم)."""
    G = G_original.copy()
    print(f"\n--- شروع حمله Nature: حذف {num_nodes_to_remove} گره با بالاترین درجه ---")
    
    # پیدا کردن گره‌ها با بالاترین درجه
    node_degrees = sorted(G.degree, key=lambda x: x[1], reverse=True)
    nodes_to_remove = [node for node, degree in node_degrees[:num_nodes_to_remove]]
    
    print(f"گره‌های هدف برای حذف: {nodes_to_remove}")
    G.remove_nodes_from(nodes_to_remove)
    return G

# استراتژی 3: خرابی تصادفی (حذف 20% یال‌ها)
def simulate_random_failure(G_original, failure_percentage=0.20):
    """شبیه‌سازی خرابی تصادفی یال‌ها (بدون ترمیم)."""
    G = G_original.copy()
    num_edges_to_remove = int(G.number_of_edges() * failure_percentage)
    print(f"\n--- شروع خرابی تصادفی: حذف {num_edges_to_remove} یال ({failure_percentage*100}%) ---")
    
    edges_to_remove = random.sample(list(G.edges()), num_edges_to_remove)
    G.remove_edges_from(edges_to_remove)
    return G

# --- بخش 3: اجرای شبیه‌سازی و مقایسه نتایج ---

if __name__ == "__main__":
    # 1. ایجاد شبکه پایه
    original_network = create_complex_network()
    initial_pos = nx.spring_layout(original_network, seed=42) # موقعیت اولیه برای هماهنگی نمودارها
    
    # 2. کپی کردن شبکه برای هر سناریو
    network_proposed = original_network.copy()
    network_nature = original_network.copy()
    network_random = original_network.copy()

    # 3. اجرای هر سه شبیه‌سازی
    final_proposed = simulate_proposed_method(network_proposed)
    final_nature = simulate_nature_attack(network_nature, num_nodes_to_remove=1) # مقایسه حذف 1 گره
    final_random = simulate_random_failure(network_random, failure_percentage=0.20)
    
    # 4. ارزیابی نتایج
    print("\n\n" + "="*30)
    print(" نتایج ارزیابی تاب‌آوری ".center(30, "="))
    print("="*30)
    
    metrics_initial = calculate_resilience_metrics(original_network)
    metrics_proposed = calculate_resilience_metrics(final_proposed)
    metrics_nature = calculate_resilience_metrics(final_nature)
    metrics_random = calculate_resilience_metrics(final_random)

    print("\nوضعیت شبکه اولیه:")
    print(metrics_initial)
    
    print("\n۱. نتیجه روش پیشنهادی (ترمیم هوشمند):")
    print(metrics_proposed)

    print("\n۲. نتیجه حمله Nature (حذف گره مهم):")
    print(metrics_nature)
    
    print("\n۳. نتیجه خرابی تصادفی (حذف ۲۰٪ یال‌ها):")
    print(metrics_random)
    
    print("\n" + "="*30)
    print(" تحلیل مقایسه‌ای ".center(30, "="))
    print("="*30)
    if metrics_proposed["is_connected"]:
        print(">> موفقیت: روش پیشنهادی شما توانست اتصال شبکه را حفظ کند.")
    else:
        print(">> هشدار: حتی با روش پیشنهادی، شبکه چند تکه شد.")
        
    if not metrics_nature["is_connected"]:
        print(">> تحلیل: حمله Nature با حذف فقط یک گره، شبکه را از هم پاشید.")
        
    if not metrics_random["is_connected"]:
        print(">> تحلیل: حذف تصادفی ۲۰٪ یال‌ها نیز باعث از هم پاشیدگی شبکه شد.")

    # 5. بصری‌سازی نتایج
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle("مقایسه استراتژی‌های تاب‌آوری شبکه", fontsize=20)
    
    visualize_network(original_network, "شبکه اولیه", pos=initial_pos, ax=axes[0, 0])
    visualize_network(final_proposed, "1. پس از روش پیشنهادی (ترمیم هوشمند)", pos=initial_pos, ax=axes[0, 1])
    visualize_network(final_nature, "2. پس از حمله Nature (حذف گره مهم)", pos=initial_pos, ax=axes[1, 0])
    visualize_network(final_random, "3. پس از خرابی تصادفی (حذف 20% یال)", pos=initial_pos, ax=axes[1, 1])
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
