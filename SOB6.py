'''This program calculates the shortest route to visit 5 towns (A, B, C, D, E). 
It generates all possible permutations of the towns and calculating the total distance for each route based on a distance table.
The program keeps track of the shortest route found and its corresponding distance, which is printed at the end.
The trip starts at the first and ends at the last town. It does not return to the starting point.'''

from itertools import permutations               # Import the permutations function from the itertools module to generate all possible visiting orders of the towns

towns = ["A", "B", "C", "D", "E"]                # Name of the 5 towns
dist = [
    [0, 10, 15, 20, 5],
    [10, 0, 25, 12, 8],
    [15, 25, 0, 18, 4],
    [20, 12, 18, 0, 6],
    [5, 8, 4, 6, 0],
]                                                # Distance table in km between towns

all_lengths = []                                 # Keeps the length of all possible paths
best_length = 1000000
best_path = None                                 # Will hold the best visiting order once found

for order in permutations(range(len(towns))):    # Every possible visiting order
    length = 0                                   # Start the length of the current path at 0
    for i in range(len(order) - 1):              
        length += dist[order[i]][order[i + 1]]   # Add the distance between the current town and the next town in the order
    all_lengths.append(length)                   # Keep total for this path
    print(" > ".join(towns[i] for i in order))   # Print the  order of the route in terms of town names
    if length < best_length:                     # If the current path is shorter than the best path found so far, update the best path and length
        best_length = length
        best_path = order

print("Shortest path:", " > ".join(towns[i] for i in best_path))  # After checking all possible routes, print the shortest one
print("Total distance travelled:", best_length, "km")             # Print the total distance of the shortest path found