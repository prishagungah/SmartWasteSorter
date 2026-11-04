from itertools import permutations

towns = ["A", "B", "C", "D"]
dist = [
    [0, 10, 15, 20],
    [10, 0, 25, 12],
    [15, 25, 0, 18],
    [20, 12, 18, 0],
]

all_lengths = []          
best_length = 1000000
best_path = None

for order in permutations(range(len(towns))):            # every possible visiting order
       
    length = 0
    for i in range(len(order) - 1):              
        length += dist[order[i]][order[i + 1]]
    all_lengths.append(length)                           # keep total for this path
    print(" > ".join(towns[i] for i in order))
    if length < best_length:                    
        best_length = length
        best_path = order

print("Shortest path:", " > ".join(towns[i] for i in best_path))
print("Total distance travelled:", best_length, "km")