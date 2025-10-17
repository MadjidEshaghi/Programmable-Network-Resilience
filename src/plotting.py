    # src/plotting.py
    import matplotlib.pyplot as plt
    import os

    def plot_and_save_results(results, network_name, num_nodes, num_edges, num_edges_added, output_dir="results"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"[INFO] پوشه '{output_dir}' برای ذخیره نتایج ایجاد شد.")
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(14, 9))
        markers = ['o', 's', 'D', '^']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        strategy_order = ["PCM (Ours)", "High Betweenness", "Hub (High Degree)", "Random"]
        for i, name in enumerate(strategy_order):
            if name in results:
                history = results[name]
                plot_range = range(min(len(history), num_edges_added + 1))
                ax.plot(plot_range, history[:len(plot_range)], marker=markers[i], linestyle='-', label=name, color=colors[i], markersize=8, linewidth=2.5)
        ax.set_xlabel("تعداد یال‌های اضافه شده (هزینه)", fontsize=16, fontweight='bold')
        ax.set_ylabel("اتصال جبری (λ₂) - مقاومت شبکه", fontsize=16, fontweight='bold')
        title = f"مقایسه استراتژی‌های مقاوم‌سازی برای شبکه {network_name.upper()}\n" \
                f"({num_nodes} گره, {num_edges} یال اولیه)"
        ax.set_title(title, fontsize=18, fontweight='bold')
        ax.legend(fontsize=14, title="استراتژی‌ها", title_fontsize='15')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.xticks(range(0, num_edges_added + 1, max(1, num_edges_added // 10)))
        plt.tight_layout()
        output_filename = os.path.join(output_dir, f"simulation_results_{network_name}.png")
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        print(f"\n[SUCCESS] نمودار نتایج در فایل '{output_filename}' ذخیره شد.")
        plt.show()
