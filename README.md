# Social Network Analysis – Min Cut Comparison
This project is a Streamlit dashboard that uses NetworkX for graph analysis and Matplotlib for visualization.It finds weak links in a social network using Karger’s Randomized Min Cut and Stoer-Wagner Min Cut, then suggests new connections based on mutual friends.The results are displayed interactively with tables and network graphs for easy comparison.

# Overview :
This Streamlit app analyzes a social network to:
- Find the minimum cut edges using two algorithms: Karger’s Randomized Min Cut and Stoer-Wagner Min Cut
- Suggest new connections to strengthen the network based on mutual friends
- Compare both algorithms’ results side-by-side
  
# Requirements 
 ## Python version : 
     Python 3.8+
 ## Dependecies :
      Install the required packages with : 
      
      ```bash
      pip install streamlit networkx matplotlib pandas
      ```
Required Libraries
1. streamlit – for interactive dashboard
2. networkx – for graph creation and algorithms
3. matplotlib – for visualizing the network
4. pandas – for comparison tables

# How to run  
 - Save the script as app.py
 - Install all dependencies.
 - Run the app. py file
```
streamlit run app.py
```
  ## Input format 
  Users: Comma-separated list
  Connections: Semicolon-separated list of User1-User2 pairs
# Output 
The output displays the weakest links in red and it also suggests potential connections based on mutual connections to make the graph connections stronger. It also provides a comparison table to evaluate the performance of both algorithms.

![image](https://github.com/user-attachments/assets/cde8f589-ea7c-4d93-b8b6-20b792872d45)

![image](https://github.com/user-attachments/assets/656aa427-63bb-4c46-81e0-9e64d24dd28e)
