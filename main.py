import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import copy
import time

# Karger’s Algorithm
def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    xr, yr = find(parent, x), find(parent, y)
    if rank[xr] < rank[yr]:
        parent[xr] = yr
    elif rank[xr] > rank[yr]:
        parent[yr] = xr
    else:
        parent[yr] = xr
        rank[xr] += 1

def karger_min_cut(n, edges):
    e = copy.deepcopy(edges)
    parent = list(range(n))
    rank = [0] * n
    verts = n
    while verts > 2:
        u, v = random.choice(e)
        s1, s2 = find(parent, u), find(parent, v)
        if s1 != s2:
            verts -= 1
            union(parent, rank, s1, s2)
        e.remove((u, v))
    cut = [(u, v) for (u, v) in edges if find(parent, u) != find(parent, v)]
    return cut

# Stoer–Wagner Algorithm
def stoer_wagner_min_cut(G):
    val, part = nx.stoer_wagner(G)
    cut = [(u, v) for u in part[0] for v in part[1] if G.has_edge(u, v)]
    return val, cut

# Suggestions for strengthening network
def suggest_connections(G):
    suggestions = []
    for node in G.nodes():
        for other in G.nodes():
            if node != other and not G.has_edge(node, other):
                common = len(set(G.neighbors(node)) & set(G.neighbors(other)))
                if common >= 2:  # adjustable
                    suggestions.append((node, other, common))
    suggestions.sort(key=lambda x: -x[2])
    return suggestions

# Plot Graph
def plot_graph(G, cut_edges, title):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=800)
    nx.draw_networkx_edges(G, pos, edgelist=cut_edges, edge_color="red", width=2)
    plt.title(title)
    st.pyplot(plt)

st.title("Social Strength Analyzer: Karger vs Stoer–Wagner")

# Inputs
users_input = st.sidebar.text_input("Users (comma separated)",
    "Alice, Bob, Charlie, David, Eve, Frank, Grace, Helen, Ian, Julia")
edges_input = st.sidebar.text_area("Edges (U1-U2 per line)", """Alice-Bob
Alice-Charlie
Alice-David
Bob-Charlie
Bob-Eve
Charlie-David
Charlie-Frank
David-Eve
Eve-Frank
Eve-Grace
Frank-Grace
Grace-Helen
Helen-Ian
Ian-Julia
Julia-Alice
Julia-Frank
David-Helen
Bob-Helen
Charlie-Ian""")
iterations = st.sidebar.slider("Karger Trials", 50, 1000, 200)

# Parse
names = [u.strip() for u in users_input.split(",") if u.strip()]
idx = {name: i for i, name in enumerate(names)}
edges = []
for line in edges_input.splitlines():
    if "-" in line:
        u, v = line.strip().split("-")
        if u in idx and v in idx:
            edges.append((idx[u], idx[v]))

# Graph
G = nx.Graph()
G.add_nodes_from(names)
for u, v in edges:
    G.add_edge(names[u], names[v])

# Karger
start_k = time.time()
best_cut, min_size = None, float("inf")
for _ in range(iterations):
    cut = karger_min_cut(len(names), edges)
    if len(cut) < min_size:
        min_size, best_cut = len(cut), cut
end_k = time.time()
best_cut_named = [(names[u], names[v]) for u, v in best_cut]

# Stoer–Wagner
start_s = time.time()
sw_val, sw_cut = stoer_wagner_min_cut(G)
end_s = time.time()

# Show graphs
st.subheader("Karger Result")
plot_graph(G, best_cut_named, f"Size: {min_size}")

st.subheader("Stoer–Wagner Result")
plot_graph(G, sw_cut, f"Size: {sw_val}")

# Suggestions
st.subheader("Suggested Connections to Strengthen Network")
st.caption("Numbers in parentheses show how many mutual friends the two people share.")

suggestions = suggest_connections(G)

# Group by person
suggestion_dict = {person: [] for person in G.nodes()}
for u, v, common in suggestions:
    suggestion_dict[u].append(f"{v} ({common})")

# Display per person
for person, suggestion_list in suggestion_dict.items():
    if suggestion_list:
        st.write(f"{person} can connect with: {', '.join(suggestion_list)}")
    else:
        st.write(f"{person} has no new suggestions.")

# Comparison
st.subheader("Comparison Table")
comparison_data = {
    "Algorithm": ["Karger", "Stoer–Wagner"],
    "Cut Size": [min_size, sw_val],
    "Cut Edges": [
        ", ".join(f"{u}–{v}" for u, v in best_cut_named),
        ", ".join(f"{u}–{v}" for u, v in sw_cut)
    ],
    "Time (s)": [round(end_k - start_k, 4), round(end_s - start_s, 4)]
}
st.table(comparison_data)
