import random
import copy
import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def add_edge(edges, u, v):
    edges.append([u, v])

def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

def karger_min_cut(vertices, edges):
    edges_copy = copy.deepcopy(edges)
    parent = []
    rank = []
    
    for node in range(vertices):
        parent.append(node)
        rank.append(0)

    remaining_vertices = vertices
    
    while remaining_vertices > 2:
        i = random.randrange(len(edges_copy))
        u, v = edges_copy[i]

        set1 = find(parent, u)
        set2 = find(parent, v)

        if set1 != set2:
            remaining_vertices -= 1
            union(parent, rank, set1, set2)

        edges_copy.pop(i)  

    cut_edges = []
    for u, v in edges:
        if find(parent, u) != find(parent, v):
            cut_edges.append([u, v])

    return cut_edges

def suggest_new_connections(user_names, edges, min_cut_edges):
    connections = {i: set() for i in range(len(user_names))}
    
    for u, v in edges:
        connections[u].add(v)
        connections[v].add(u)
    
    recommendations = {}    
    for u, v in min_cut_edges:
        u_suggestions = set()
        v_suggestions = set()
        
        for friend in connections[u]:
            for potential in connections[friend]:
                if potential != u and potential != v and potential not in connections[u]:
                    u_suggestions.add(potential)
        
        # Suggest friends for v
        for friend in connections[v]:
            for potential in connections[friend]:
                if potential != v and potential != u and potential not in connections[v]:
                    v_suggestions.add(potential)

        recommendations[user_names[u]] = [user_names[p] for p in u_suggestions]
        recommendations[user_names[v]] = [user_names[p] for p in v_suggestions]

    return recommendations


def plot_full_graph(user_names, edges, cut_edges=None):
    plt.clf()  
    fig, ax = plt.subplots(figsize=(8, 6))

    n = len(user_names)
    angle_step = 360 / n
    positions = {}

    for i, user in enumerate(user_names):
        angle = i * angle_step
        x = 10 * (1 + 0.9 * np.cos(np.radians(angle)))
        y = 10 * (1 + 0.9 * np.sin(np.radians(angle)))
        positions[user] = (x, y)
        ax.text(x, y, user, fontsize=12, ha='center')

    for u, v in edges:
        u_name = user_names[u]
        v_name = user_names[v]
        x_values = [positions[u_name][0], positions[v_name][0]]
        y_values = [positions[u_name][1], positions[v_name][1]]
        if cut_edges and ([u, v] in cut_edges or [v, u] in cut_edges):
            ax.plot(x_values, y_values, 'red', linestyle='-', lw=4)  
        else:
            ax.plot(x_values, y_values, 'gray', linestyle='-', lw=2) 

    ax.set_title("Social Network with Minimum Cut Highlighted")
    ax.axis('off')
    return fig

def display_plot_window(user_names, edges, min_cut_edges):
    new_window = Toplevel(root)
    new_window.title("Network Plot")

    fig = plot_full_graph(user_names, edges, cut_edges=min_cut_edges)
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def run_algorithm():
    user_names = entry_users.get().split(",")
    friendships = entry_edges.get().split(";")

    if not user_names or not friendships:
        messagebox.showerror("Input Error", "Please enter users and friendships.")
        return

    user_names = [name.strip() for name in user_names]
    edges = []

    for friendship in friendships:
        try:
            u_name, v_name = friendship.split("-")
            u_name, v_name = u_name.strip(), v_name.strip()
            if u_name in user_names and v_name in user_names:
                u = user_names.index(u_name)
                v = user_names.index(v_name)
                add_edge(edges, u, v)
            else:
                messagebox.showerror("Input Error", f"User {u_name} or {v_name} not found in users list.")
                return
        except ValueError:
            messagebox.showerror("Input Error", f"Friendship {friendship} is not in the correct format.")
            return

    min_cut_edges = None
    min_cut_size = float('inf')

    for _ in range(200): 
        cut_edges = karger_min_cut(len(user_names), edges)
        if len(cut_edges) < min_cut_size:
            min_cut_size = len(cut_edges)
            min_cut_edges = cut_edges

    result = "\nWeakest connections in the network (minimum cut):\n"
    for u, v in min_cut_edges:
        result += f"{user_names[u]} - {user_names[v]}\n"
    
    result += f"\nSize of the minimum cut (weak connections): {min_cut_size}"

    suggestions = suggest_new_connections(user_names, edges, min_cut_edges)

    result += "\n\nSuggestions to strengthen weak connections:\n"
    for person, suggestions_list in suggestions.items():
        if suggestions_list:
            result += f"{person} can connect with: {', '.join(suggestions_list)}\n"
        else:
            result += f"{person} has no new suggestions.\n"

    result_label.config(text=result)

    display_plot_window(user_names, edges, min_cut_edges)


def open_input_window(action, input_type):
    input_window = Toplevel(root)
    input_window.title(action)

    label = Label(input_window, text=f"Enter {input_type}:")
    label.grid(row=0, column=0, padx=10, pady=10)
    entry = Entry(input_window)
    entry.grid(row=0, column=1, padx=10, pady=10)

    if input_type == "person":
        Button(input_window, text="Submit", command=lambda: process_person(action, entry.get(), input_window)).grid(row=1, columnspan=2, pady=10)
    else:
        Button(input_window, text="Submit", command=lambda: process_friendship(action, entry.get(), input_window)).grid(row=1, columnspan=2, pady=10)


def process_person(action, name, window):
    user_names = entry_users.get().split(",")
    user_names = [name.strip() for name in user_names]

    if action == "Add Person":
        if name in user_names:
            messagebox.showerror("Error", "Person already exists.")
        else:
            user_names.append(name)
            entry_users.delete(0, tk.END)
            entry_users.insert(0, ", ".join(user_names))
            messagebox.showinfo("Success", f"{name} added successfully.")

    elif action == "Remove Person":
        if name not in user_names:
            messagebox.showerror("Error", "Person not found.")
        else:
            remove_friendships(name, user_names)

            user_names.remove(name)
            entry_users.delete(0, tk.END)
            entry_users.insert(0, ", ".join(user_names))
            messagebox.showinfo("Success", f"{name} removed successfully.")

    window.destroy()
    

def remove_friendships(person, user_names):
    edges = entry_edges.get().split(";")
    edges = [edge.strip() for edge in edges]
    updated_edges = []

    for friendship in edges:
        u_name, v_name = friendship.split("-")
        if u_name.strip() != person and v_name.strip() != person:
            updated_edges.append(friendship)

    entry_edges.delete(0, tk.END)
    entry_edges.insert(0, "; ".join(updated_edges))




def process_friendship(action, friendship, window):
    try:
        u_name, v_name = friendship.split("-")
        u_name, v_name = u_name.strip(), v_name.strip()
    except ValueError:
        messagebox.showerror("Input Error", "Friendship must be in format User1-User2.")
        return

    user_names = entry_users.get().split(",")
    user_names = [name.strip() for name in user_names]

    if u_name not in user_names or v_name not in user_names:
        messagebox.showerror("Error", "One or both users not found.")
        return

    edges = entry_edges.get().split(";")
    edges = [edge.strip() for edge in edges]

    if action == "Add Friendship":
        if f"{u_name}-{v_name}" in edges or f"{v_name}-{u_name}" in edges:
            messagebox.showerror("Error", "Friendship already exists.")
        else:
            edges.append(f"{u_name}-{v_name}")
            entry_edges.delete(0, tk.END)
            entry_edges.insert(0, "; ".join(edges))
            messagebox.showinfo("Success", f"Friendship between {u_name} and {v_name} added.")
    
    elif action == "Remove Friendship":
        if f"{u_name}-{v_name}" not in edges and f"{v_name}-{u_name}" not in edges:
            messagebox.showerror("Error", "Friendship not found.")
        else:
            edges.remove(f"{u_name}-{v_name}")
            entry_edges.delete(0, tk.END)
            entry_edges.insert(0, "; ".join(edges))
            messagebox.showinfo("Success", f"Friendship between {u_name} and {v_name} removed.")

    window.destroy()


root = tk.Tk()
root.title("Social Network Min Cut Algorithm")


label_users = Label(root, text="Enter users (comma separated):")
label_users.grid(row=0, column=0, padx=10, pady=10)
entry_users = Entry(root, width=50)
entry_users.grid(row=0, column=1, padx=10, pady=10)


label_edges = Label(root, text="Enter friendships (User1-User2; comma separated):")
label_edges.grid(row=1, column=0, padx=10, pady=10)
entry_edges = Entry(root, width=50)
entry_edges.grid(row=1, column=1, padx=10, pady=10)

button_run = Button(root, text="Find Minimum Cut", command=run_algorithm)
button_run.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

result_label = Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


button_add_person = Button(root, text="Add Person", command=lambda: open_input_window("Add Person", "person"))
button_add_person.grid(row=4, column=0, padx=10, pady=10)

button_remove_person = Button(root, text="Remove Person", command=lambda: open_input_window("Remove Person", "person"))
button_remove_person.grid(row=4, column=1, padx=10, pady=10)

button_add_friendship = Button(root, text="Add Friendship", command=lambda: open_input_window("Add Friendship", "friendship"))
button_add_friendship.grid(row=5, column=0, padx=10, pady=10)

button_remove_friendship = Button(root, text="Remove Friendship", command=lambda: open_input_window("Remove Friendship", "friendship"))
button_remove_friendship.grid(row=5, column=1, padx=10, pady=10)

root.mainloop()


