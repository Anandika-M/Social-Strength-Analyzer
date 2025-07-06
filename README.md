# Social Strength Analyzer
This Python application provides an interactive way to analyze a social network's weakest connections using Karger’s Minimum Cut algorithm, along with Tkinter for the GUI and Matplotlib for visualizing the graph.

# Overview :
The tool:
- Allows you to input people and their friendships.
- Uses Karger's  min cut algorithm to identify weak connections in the network.
- Suggests potential new friendships to strengthen the network.
- Visualizes the social network and highlights the minimum cut edges.

# Requirements 
- Python 3.x
- matplotlib
- numpy
- tkinter

# Input Format 
 - Users  (comma-separated)
    Example: Alice, Bob, Charlie, David, Gary
 - Friendships (semicolon-separated pairs)
    Example: Alice-Bob; Bob-Charlie; Charlie-David; Alice-David; Charlie-Alice; Alice-Gary

# Additional Features
1. Add/Remove People
2. Add/Remove Friendships

# Output 
The output displays the weakest links in red and it also suggests potential connections based on mutual connections to make the graph connections stronger.

![image](https://github.com/user-attachments/assets/cde8f589-ea7c-4d93-b8b6-20b792872d45)

![image](https://github.com/user-attachments/assets/656aa427-63bb-4c46-81e0-9e64d24dd28e)
