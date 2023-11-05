import random
import time


def main():
    total_switch = 0
    total_restart = 0
    # Print a header for the output
    print("Node".ljust(30), "Restart Counts".ljust(20), "Switch Counts".ljust(20), "Time")
    print("-"*81)
    total_start = time.time()   # Start a timer to measure the total running time of the program
    for i in range(9):
        start = time.time()  # Start a timer to measure the time it takes to find a solution in this iteration
        node = [0] * 8  # Initialize the state of the problem to a random initial state
        # Initialize variables to keep track of the number of restarts and switches
        h = 9999
        restart_counter = -1
        switch_counter = 0
        while h != 0:  # Continue generating new states until a solution is found
            restart_counter += 1
            node, switch_counter = hill_climbing(node, switch_counter)
            h = calc_h(node)
        stop = time.time()  # Stop the timer for this iteration
        # Update total switch and restart counts
        total_switch += switch_counter
        total_restart += restart_counter
        print(str(node).ljust(30), str(restart_counter).ljust(20), str(switch_counter).ljust(20),
              "{:.6f}".format(stop - start))
    total_stop = time.time()  # Stop the timer for the entire program
    print("-"*81)
    print("Averages:".ljust(30), "{:.2f}".format(total_restart / 15).ljust(20),
          "{:.2f}".format(total_switch / 15).ljust(20), "{:.2f}".format((total_stop - total_start) / 15))


def random_node():
    node = []
    for i in range(8):
        node.append(random.randint(1, 8))  # List indexes represent rows random values represent columns
    return node


def select_best_node(neighbors):  # Return best node index and best node's h value
    best_indices = [i for i in range(len(neighbors)) if neighbors[i] == min(neighbors)]
    best_index = random.choice(best_indices)
    best_node = neighbors[best_index]
    return best_index, best_node


def calc_h(node):  # Calculate h value for a given node
    h = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if node[i] == node[j] or abs(node[i] - node[j]) == abs(i - j):
                h += 1
    return h


def generate_neighbors(node):
    neighbors = [0] * 64  # Create an empty list to hold the h values of each neighbor
    for i in range(64):  # Loop through each index in the range 0 to 63
        # Calculate the row and column of the current index
        col = i % 8
        row = i // 8
        temp = node.copy()  # Create a copy of the current node
        self = node[row]  # Store the current value in the row to be modified
        temp[row] = col + 1  # Update the value in the current row to the new column value
        if col + 1 == self:   # Check if the new value is the same as the old value
            # If the value is the same, set the neighbor h value to a high number (9999)
            neighbors[i] = 9999
        else:
            neighbors[i] = calc_h(temp)  # If the value is different, calculate the h value for the new node
    return neighbors


def hill_climbing(node, switch_counter):
    main_node = random_node()
    switch_counter = 0
    while True:
        if calc_h(main_node) == 0:  # Check if current node is the goal state
            return main_node, switch_counter
        neighbors = generate_neighbors(main_node)  # Generate neighbors and select the best one
        best_index, best_value = select_best_node(neighbors)
        current_value = calc_h(main_node)
        if best_value >= current_value:  # Check if the best neighbor is worse than the current node
            return main_node, switch_counter
        main_node[best_index // 8] = (best_index % 8) + 1  # Move to the best neighbor and increment the switch counter
        switch_counter += 1


main()
