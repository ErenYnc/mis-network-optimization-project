# 🏦 Bank ATM Cash Transportation Network Optimization

**GitHub-Based Python Project Assignment**  
**Course:** Management Information Systems — Network Optimization Problems  
**Model:** Shortest Route / Shortest Path Problem  
**Algorithm:** Dijkstra's Algorithm

---

## 1. Real-World Problem Context

A bank regularly transports cash to its ATMs across Istanbul. In the current system, money flows from a **General Vault** (main depot) through **Regional Cash Centers** or directly to ATMs.

Management wants to determine the optimal route for delivering cash to each ATM using a network optimization method. The goal is to **minimize the total transportation cost**.

---

## 2. Problem Definition

| Feature | Value |
|---|---|
| **Model** | Shortest Route / Shortest Path Problem |
| **Decision Variable** | Which route to use for each ATM |
| **Objective** | Minimize total transportation cost |
| **Optimization Criterion** | Transportation cost (TL per trip) |

**Question:** Which route from the General Vault to each ATM results in the lowest cost?

---

## 3. Network Model

### Node Types

| Node Type | Examples | Description |
|---|---|---|
| **Main Depot** | General_Vault | Cash origin point |
| **Regional Cash Center** | Levent_Center, Umraniye_Center | Intermediate distribution hubs |
| **ATM** | 8 ATM nodes | Cash destination points |

### Graph Properties

- **Graph type:** Directed Graph
- **Number of nodes:** 11
- **Number of edges:** 15
- **Edge weight:** Transportation cost (TL per trip)

---

## 4. Nodes and Edges

### Nodes

| Node ID | Full Name | Type |
|---|---|---|
| General_Vault | General Vault (Main Depot) | Main Depot |
| Levent_Center | Levent Regional Cash Center | Regional Center |
| Umraniye_Center | Umraniye Regional Cash Center | Regional Center |
| ATM_Besiktas | Besiktas ATM | ATM |
| ATM_Sisli | Sisli ATM | ATM |
| ATM_Maslak | Maslak ATM | ATM |
| ATM_Kagithane | Kagithane ATM | ATM |
| ATM_Bayrampasa | Bayrampasa ATM | ATM |
| ATM_Kadikoy | Kadikoy ATM | ATM |
| ATM_Uskudar | Uskudar ATM | ATM |
| ATM_Maltepe | Maltepe ATM | ATM |

### Edges

Full data: `data/network_data.csv`

| Source | Target | Cost (TL) | Distance (km) |
|---|---|---|---|
| General_Vault | Levent_Center | 120 | 15 |
| General_Vault | Umraniye_Center | 140 | 22 |
| General_Vault | ATM_Besiktas | 200 | 18 |
| General_Vault | ATM_Sisli | 190 | 17 |
| General_Vault | ATM_Kadikoy | 230 | 30 |
| General_Vault | ATM_Maltepe | 280 | 38 |
| Levent_Center | ATM_Maslak | 45 | 5 |
| Levent_Center | ATM_Sisli | 50 | 3 |
| Levent_Center | ATM_Kagithane | 55 | 6 |
| Levent_Center | ATM_Besiktas | 60 | 4 |
| Levent_Center | ATM_Bayrampasa | 80 | 10 |
| Umraniye_Center | ATM_Uskudar | 55 | 5 |
| Umraniye_Center | ATM_Kadikoy | 65 | 8 |
| Umraniye_Center | ATM_Maltepe | 90 | 14 |
| Umraniye_Center | ATM_Bayrampasa | 110 | 18 |

### Column Descriptions

| Column | Unit | Description |
|---|---|---|
| `source` | — | Origin node of the route |
| `target` | — | Destination node of the route |
| `cost` | TL/trip | Transportation cost per trip |
| `distance_km` | km | Physical distance of the route |
| `description` | — | Human-readable route description |

---

## 5. Selected Algorithm

**Dijkstra's Algorithm** — Single-source shortest path algorithm.

### Algorithm Steps:
1. Add the source node (General_Vault) to the permanent set with cost 0
2. Calculate temporary costs for all neighboring nodes
3. Move the node with the lowest temporary cost to the permanent set
4. Update neighbors of the newly added node
5. Repeat until all nodes are in the permanent set

NetworkX functions `nx.dijkstra_path()` and `nx.dijkstra_path_length()` are used.

---

## 6. Python Implementation

```python
import networkx as nx

# Build the graph
G = nx.DiGraph()
G.add_edge('General_Vault', 'Levent_Center', weight=120)
# ... other edges

# Find shortest path
path = nx.dijkstra_path(G, 'General_Vault', 'ATM_Maslak', weight='weight')
cost = nx.dijkstra_path_length(G, 'General_Vault', 'ATM_Maslak', weight='weight')
# Result: ['General_Vault', 'Levent_Center', 'ATM_Maslak'], 165 TL
```

---

## 7. Results

| ATM | Optimal Route | Cost (TL) | Distance (km) |
|---|---|---|---|
| Maslak | General_Vault → Levent_Center → ATM_Maslak | 165 | 20 |
| Sisli | General_Vault → Levent_Center → ATM_Sisli | 170 | 18 |
| Kagithane | General_Vault → Levent_Center → ATM_Kagithane | 175 | 21 |
| Besiktas | General_Vault → Levent_Center → ATM_Besiktas | 180 | 19 |
| Uskudar | General_Vault → Umraniye_Center → ATM_Uskudar | 195 | 27 |
| Bayrampasa | General_Vault → Levent_Center → ATM_Bayrampasa | 200 | 25 |
| Kadikoy | General_Vault → Umraniye_Center → ATM_Kadikoy | 205 | 30 |
| Maltepe | General_Vault → Umraniye_Center → ATM_Maltepe | 230 | 36 |

**Total optimal daily cost: 1,520 TL**

---

## 8. Managerial Interpretation

### Key Findings

**Regional Cash Centers provide critical cost savings.**  
For the Besiktas ATM, the direct route costs 200 TL while routing via Levent Center costs only 180 TL — a **10% saving**. For ATMs with no direct access (Maslak, Kagithane, Uskudar, etc.), the savings are significantly higher.

**Geographic division is clearly observed:**
- **Levent Center** → European Side ATMs (5 ATMs)
- **Umraniye Center** → Anatolian Side ATMs (3 ATMs)

**Strategic Recommendation:**  
If demand increases in the Bayrampasa area, the bank should consider establishing an additional Regional Cash Center nearby. Currently, both existing centers serve this ATM at a relatively high cost (200 TL via Levent, 250 TL via Umraniye), making it the most expensive stop on the European side.

---

## 9. How to Run the Code

### Requirements

```bash
pip install -r requirements.txt
```

### Run

```bash
python src/solution.py
```

Outputs are saved to the `results/` folder:
- `results/solution_output.txt` — Results table
- `results/network_visualization.png` — Network visualization

### Jupyter Notebook

```bash
jupyter notebook notebooks/analysis.ipynb
```

---

## 10. References

See full bibliography: `references/references.md`

- Taylor, B.W. (2010). *Introduction to Management Science* (10th ed.). Prentice Hall. — Chapter 7: Network Flow Models
- NetworkX Documentation: https://networkx.org/documentation/stable/
- Dijkstra, E.W. (1959). A note on two problems in connexion with graphs. *Numerische Mathematik*, 1, 269–271.
