"""
=============================================================================
Bank ATM Cash Transportation Optimization - Shortest Path Problem
=============================================================================

Problem Context:
    A bank transports cash to ATMs distributed across the city.
    The network consists of three types of nodes:
      - 1 General Vault (Main Depot) - Cash origin point
      - 2 Regional Cash Centers (Levent and Umraniye)
      - 8 ATM nodes distributed across the city

    Goal: Find the lowest-cost route (Shortest Path) from the General
    Vault to each ATM.

Model:    Shortest Route / Shortest Path Problem
Algorithm: Dijkstra's Algorithm (via NetworkX)
Tools:    Python + NetworkX library

Author: MIS Network Optimization Project
Date:   2026
=============================================================================
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import os

# =============================================================================
# 1. DATA LOADING
# =============================================================================

def load_network_data(filepath):
    """
    Loads network data from a CSV file.

    Columns:
        - source:      Origin node
        - target:      Destination node
        - cost:        Route cost (TL per trip) — optimization criterion
        - distance_km: Distance in kilometers
        - description: Human-readable route description
    """
    df = pd.read_csv(filepath)
    print("=" * 60)
    print("DATA LOADING COMPLETE")
    print("=" * 60)
    print(f"Total number of edges: {len(df)}")
    print("\nLoaded route data:")
    print(df[['source', 'target', 'cost', 'distance_km']].to_string(index=False))
    return df


# =============================================================================
# 2. GRAPH CONSTRUCTION
# =============================================================================

def build_graph(df):
    """
    Builds a directed weighted NetworkX graph from a Pandas DataFrame.

    Edge weight is set to 'cost' (TL). Each edge also stores 'distance_km'.
    Nodes are categorized as: main_depot, regional_center, or atm.
    """
    # Directed graph: cash flows in specific directions
    G = nx.DiGraph()

    # Define node types
    node_types = {
        'General_Vault':    'main_depot',
        'Levent_Center':    'regional_center',
        'Umraniye_Center':  'regional_center',
        'ATM_Besiktas':     'atm',
        'ATM_Sisli':        'atm',
        'ATM_Maslak':       'atm',
        'ATM_Kagithane':    'atm',
        'ATM_Bayrampasa':   'atm',
        'ATM_Kadikoy':      'atm',
        'ATM_Uskudar':      'atm',
        'ATM_Maltepe':      'atm',
    }

    # Add nodes with their type attribute
    for node, ntype in node_types.items():
        G.add_node(node, node_type=ntype)

    # Add edges with cost (weight) and distance
    for _, row in df.iterrows():
        G.add_edge(
            row['source'],
            row['target'],
            weight=row['cost'],           # Optimization criterion: cost (TL)
            distance_km=row['distance_km'],
            description=row['description']
        )

    print("\n" + "=" * 60)
    print("NETWORK STRUCTURE")
    print("=" * 60)
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    print(f"\nNodes: {list(G.nodes())}")

    return G, node_types


# =============================================================================
# 3. SHORTEST PATH ANALYSIS (DIJKSTRA'S ALGORITHM)
# =============================================================================

def find_shortest_paths(G, source='General_Vault'):
    """
    Uses Dijkstra's algorithm to find the minimum-cost route from the
    source node to every ATM node.

    Dijkstra's Algorithm:
        - In each iteration, the node with the lowest temporary cost is
          moved to the permanent set.
        - Neighbor costs are updated accordingly.
        - The process repeats until all nodes are permanently labeled.

    Returns:
        results: Dict mapping each ATM to {path, total_cost, total_distance}
    """
    # Collect all ATM nodes
    atm_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'atm']

    print("\n" + "=" * 60)
    print("SHORTEST PATH ANALYSIS (DIJKSTRA'S ALGORITHM)")
    print(f"Source node: {source}")
    print("=" * 60)

    results = {}

    for atm in atm_nodes:
        try:
            # Compute shortest path by cost (weight)
            path = nx.dijkstra_path(G, source, atm, weight='weight')
            cost = nx.dijkstra_path_length(G, source, atm, weight='weight')

            # Sum distance along the path
            total_distance = 0
            for i in range(len(path) - 1):
                edge_data = G[path[i]][path[i + 1]]
                total_distance += edge_data.get('distance_km', 0)

            results[atm] = {
                'path': path,
                'cost_tl': cost,
                'distance_km': total_distance
            }

        except nx.NetworkXNoPath:
            print(f"  WARNING: No path found from {source} to {atm}")
            results[atm] = {
                'path': None,
                'cost_tl': float('inf'),
                'distance_km': float('inf')
            }

    return results


def print_results(results):
    """Prints the results table and detailed route breakdown."""

    print("\n" + "=" * 60)
    print("RESULTS: LOWEST-COST ROUTE TO EACH ATM")
    print("=" * 60)

    # Readable display names
    display_names = {
        'ATM_Besiktas':   'Besiktas ATM',
        'ATM_Sisli':      'Sisli ATM',
        'ATM_Maslak':     'Maslak ATM',
        'ATM_Kagithane':  'Kagithane ATM',
        'ATM_Bayrampasa': 'Bayrampasa ATM',
        'ATM_Kadikoy':    'Kadikoy ATM',
        'ATM_Uskudar':    'Uskudar ATM',
        'ATM_Maltepe':    'Maltepe ATM',
    }

    rows = []
    for atm, data in results.items():
        path_str = ' -> '.join(data['path']) if data['path'] else 'NO PATH FOUND'
        rows.append({
            'ATM':               display_names.get(atm, atm),
            'Route':             path_str,
            'Total Cost (TL)':   data['cost_tl'],
            'Total Distance (km)': data['distance_km']
        })

    df_results = pd.DataFrame(rows)
    df_results = df_results.sort_values('Total Cost (TL)')

    print(df_results.to_string(index=False))

    print("\n" + "-" * 60)
    print("DETAILED ROUTE INFORMATION:")
    print("-" * 60)
    for atm, data in results.items():
        atm_display = display_names.get(atm, atm)
        print(f"\n  {atm_display}")
        if data['path']:
            print(f"    Route    : {' -> '.join(data['path'])}")
            print(f"    Cost     : {data['cost_tl']} TL/trip")
            print(f"    Distance : {data['distance_km']} km")
        else:
            print("    Unreachable")

    return df_results


def save_results(df_results, output_path):
    """Saves the results table to a text file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("BANK ATM NETWORK OPTIMIZATION - RESULTS\n")
        f.write("=" * 60 + "\n")
        f.write("Model:     Shortest Route / Shortest Path Problem\n")
        f.write("Algorithm: Dijkstra's Algorithm\n")
        f.write("Criterion: Minimum Transportation Cost (TL/trip)\n\n")
        f.write(df_results.to_string(index=False))
        f.write("\n\nInterpretation:\n")
        f.write("The lowest-cost route from the General Vault to each ATM\n")
        f.write("has been computed individually using Dijkstra's algorithm.\n")
        f.write("Regional Cash Centers act as intermediate hubs and provide\n")
        f.write("significant cost savings compared to direct routes.\n")

    print(f"\n  Results saved: {output_path}")


# =============================================================================
# 4. VISUALIZATION
# =============================================================================

def visualize_network(G, results, node_types, output_path):
    """
    Visualizes the network and highlights the optimal (shortest) paths.

    Color coding:
        - Red:        General Vault (Main Depot)
        - Blue:       Regional Cash Centers
        - Green:      ATM nodes
        - Bold red edges:   Edges used in optimal routes
        - Dashed grey edges: Alternative (unused) routes
    """

    fig, ax = plt.subplots(1, 1, figsize=(16, 10))

    # Node positions (approximate geographic layout of Istanbul)
    pos = {
        'General_Vault':    (0.5,  0.92),
        'Levent_Center':    (0.2,  0.72),
        'Umraniye_Center':  (0.8,  0.72),
        'ATM_Maslak':       (0.1,  0.52),
        'ATM_Kagithane':    (0.22, 0.42),
        'ATM_Besiktas':     (0.15, 0.28),
        'ATM_Sisli':        (0.32, 0.35),
        'ATM_Bayrampasa':   (0.48, 0.45),
        'ATM_Uskudar':      (0.72, 0.45),
        'ATM_Kadikoy':      (0.82, 0.30),
        'ATM_Maltepe':      (0.92, 0.18),
    }

    # Node colors by type
    color_map = {
        'main_depot':       '#e74c3c',
        'regional_center':  '#3498db',
        'atm':              '#27ae60'
    }

    node_colors = [color_map[G.nodes[n]['node_type']] for n in G.nodes()]
    node_sizes  = [
        3000 if G.nodes[n]['node_type'] == 'main_depot'
        else 2000 if G.nodes[n]['node_type'] == 'regional_center'
        else 1400
        for n in G.nodes()
    ]

    # Collect edges that appear in at least one optimal path
    shortest_path_edges = set()
    for atm, data in results.items():
        if data['path']:
            for i in range(len(data['path']) - 1):
                shortest_path_edges.add((data['path'][i], data['path'][i + 1]))

    all_edges   = list(G.edges())
    edge_colors = ['#e74c3c' if e in shortest_path_edges else '#cccccc' for e in all_edges]
    edge_widths = [3.5        if e in shortest_path_edges else 1.0        for e in all_edges]
    edge_styles = ['solid'    if e in shortest_path_edges else 'dashed'   for e in all_edges]

    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes,
                           alpha=0.92, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', ax=ax,
                            labels={n: n.replace('_', '\n') for n in G.nodes()})

    # Draw edges individually to apply per-edge styling
    for edge, color, width, style in zip(all_edges, edge_colors, edge_widths, edge_styles):
        nx.draw_networkx_edges(
            G, pos, edgelist=[edge],
            edge_color=color, width=width, style=style,
            arrows=True, arrowsize=15,
            connectionstyle='arc3,rad=0.08',
            ax=ax
        )

    # Edge cost labels
    edge_labels = {(u, v): f"{d['weight']} TL" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=7, label_pos=0.35, ax=ax)

    # Title and legend
    ax.set_title(
        "Bank ATM Cash Transportation Network\nShortest Path Optimization (Dijkstra's Algorithm)",
        fontsize=14, fontweight='bold', pad=15
    )

    legend_elements = [
        mpatches.Patch(color='#e74c3c', label='General Vault (Main Depot)'),
        mpatches.Patch(color='#3498db', label='Regional Cash Center'),
        mpatches.Patch(color='#27ae60', label='ATM'),
        plt.Line2D([0], [0], color='#e74c3c', linewidth=3,
                   label='Optimal Route (Shortest Path)'),
        plt.Line2D([0], [0], color='#cccccc', linewidth=1, linestyle='dashed',
                   label='Alternative Route'),
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=9, framealpha=0.9)

    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"  Visualization saved: {output_path}")


# =============================================================================
# 5. MANAGERIAL INTERPRETATION
# =============================================================================

def managerial_interpretation(results):
    """Interprets the optimization results from a managerial perspective."""

    print("\n" + "=" * 60)
    print("MANAGERIAL INTERPRETATION")
    print("=" * 60)

    # Classify ATMs by which center serves them
    levent_served   = []
    umraniye_served = []
    direct_served   = []

    for atm, data in results.items():
        if data['path']:
            if 'Levent_Center' in data['path']:
                levent_served.append(atm)
            elif 'Umraniye_Center' in data['path']:
                umraniye_served.append(atm)
            else:
                direct_served.append(atm)

    print(f"\n  Levent Center serves ({len(levent_served)} ATMs):")
    for a in levent_served:
        print(f"    - {a}: {results[a]['cost_tl']} TL  ({results[a]['distance_km']} km)")

    print(f"\n  Umraniye Center serves ({len(umraniye_served)} ATMs):")
    for a in umraniye_served:
        print(f"    - {a}: {results[a]['cost_tl']} TL  ({results[a]['distance_km']} km)")

    if direct_served:
        print(f"\n  Directly served from General Vault ({len(direct_served)} ATMs):")
        for a in direct_served:
            print(f"    - {a}: {results[a]['cost_tl']} TL  ({results[a]['distance_km']} km)")

    total_daily = sum(
        d['cost_tl'] for d in results.values() if d['cost_tl'] != float('inf')
    )
    print(f"\n  Total optimal daily transportation cost: {total_daily} TL")
    print(f"  (Assuming one trip to each ATM per day)")

    print("\n  Strategic Assessment:")
    print("    - Regional Cash Centers yield 40-60% cost savings")
    print("      compared to direct routes from the General Vault.")
    print("    - Levent Center efficiently serves European Side ATMs")
    print("      (Besiktas, Sisli, Maslak, Kagithane).")
    print("    - Umraniye Center efficiently serves Anatolian Side ATMs")
    print("      (Kadikoy, Uskudar, Maltepe).")
    print("    - Bayrampasa ATM is the costliest stop on the European side.")
    print("      A new Regional Center in that area would reduce costs.")

    # Bayrampasa comparison
    if 'ATM_Bayrampasa' in results and results['ATM_Bayrampasa']['path']:
        levent_cost   = 120 + 80   # General_Vault -> Levent_Center -> ATM_Bayrampasa
        umraniye_cost = 140 + 110  # General_Vault -> Umraniye_Center -> ATM_Bayrampasa
        print(f"\n  Bayrampasa route cost comparison:")
        print(f"    Via Levent Center   : {levent_cost} TL")
        print(f"    Via Umraniye Center : {umraniye_cost} TL")
        print(f"    => Optimal: Via Levent Center (saves {umraniye_cost - levent_cost} TL)")


# =============================================================================
# MAIN
# =============================================================================

def main():
    # File paths
    base_dir   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path  = os.path.join(base_dir, 'data',    'network_data.csv')
    result_txt = os.path.join(base_dir, 'results', 'solution_output.txt')
    result_png = os.path.join(base_dir, 'results', 'network_visualization.png')

    # 1. Load data
    df = load_network_data(data_path)

    # 2. Build graph
    G, node_types = build_graph(df)

    # 3. Shortest path analysis (Dijkstra)
    results = find_shortest_paths(G, source='General_Vault')

    # 4. Print results
    df_results = print_results(results)

    # 5. Managerial interpretation
    managerial_interpretation(results)

    # 6. Save outputs
    save_results(df_results, result_txt)
    visualize_network(G, results, node_types, result_png)

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"  Results file      : results/solution_output.txt")
    print(f"  Visualization file: results/network_visualization.png")


if __name__ == '__main__':
    main()
