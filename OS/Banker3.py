def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Read the number of instances for each initial resource
    initial_resources = list(map(int, lines[1].strip().split()))

    # Read the allocation matrix
    allocation_matrix = [list(map(int, line.strip().split())) for line in lines[3:8]]

    # Read the max matrix
    max_matrix = [list(map(int, line.strip().split())) for line in lines[9:]]

    return initial_resources, allocation_matrix, max_matrix

def print_resource_instances(resources):
    header = ["R{}".format(i) for i in range(len(resources))]
    print("\nResource Instances:")
    for i in range(len(resources)):
        print("{:<3} = {}".format(header[i], resources[i]), end=", ")
    print()

def print_matrix(matrix, header, label):
    print("\n{}:".format(label))
    
    # Calculate the maximum width of each column
    max_widths = [max(len(str(matrix[i][j])) for i in range(len(matrix))) for j in range(len(header))]
    
    # Print the header
    print("{:10}".format("Process"), end=" ")
    for i in range(len(header)):
        print("{:>{width}}".format(header[i], width=max_widths[i] + 1), end=" ")
    print()
    
    # Print the matrix
    for i in range(len(matrix)):
        print("{:10}".format(f"P{i}"), end=" ")
        for j in range(len(header)):
            print("{:>{width}}".format(matrix[i][j], width=max_widths[j] + 1), end=" ")
        print()


def calculate_need_matrix(allocation_matrix, max_matrix):
    return [[max_matrix[i][j] - allocation_matrix[i][j] for j in range(len(allocation_matrix[0]))] for i in range(len(allocation_matrix))]

def calculate_available(resources, allocation_matrix):
    total_resources = list(resources)
    for i in range(len(allocation_matrix)):
        for j in range(len(allocation_matrix[0])):
            total_resources[j] -= allocation_matrix[i][j]

    return total_resources

def is_less_than_or_equal(a, b):
    for ai, bi in zip(a, b):
        if ai > bi:
            return False
    return True


def bankers_algorithm(resources, allocation_matrix, max_matrix):
    need_matrix = calculate_need_matrix(allocation_matrix, max_matrix)
    available_resources = calculate_available(resources, allocation_matrix)

    processes = len(allocation_matrix)
    resources_count = len(resources)
    safe_sequence = []
    iteration = 0

    while safe_sequence != list(range(processes)):
        iteration += 1
        found = False

        print("\nIteration:", iteration)
        print("Available Resources:", available_resources)
        
        # Print Max Matrix
        print_matrix(max_matrix, ["R{}".format(i) for i in range(len(max_matrix[0]))], "Max Matrix")
        
        # Print Allocation Matrix
        print_matrix(allocation_matrix, ["R{}".format(i) for i in range(len(allocation_matrix[0]))], "Allocation Matrix")
        
        # Print Need Matrix
        print("\nNeed Matrix:")
        header = ["R{}".format(i) for i in range(resources_count)]
        print("{:10} {}".format("Process", " ".join(header)))
        for i in range(processes):
            print("{:10} {}".format(
                f"P{i}",
                " ".join("{:>2}".format(str(need_matrix[i][j])) for j in range(resources_count))
            ))

        for i in range(processes):
            if i not in safe_sequence and is_less_than_or_equal(need_matrix[i], available_resources):
                found = True
                safe_sequence.append(i)

                # Mark the resources as released by the completed process
                available_resources = [available_resources[j] + allocation_matrix[i][j] for j in range(resources_count)]
                # Mark the resources as allocated by the completed process
                allocation_matrix[i] = [0] * resources_count
                # Update the need matrix to reflect the released resources
                need_matrix[i] = [0] * resources_count
                # Update the max matrix to reflect the released resources
                max_matrix[i] = [0] * resources_count
                break

        if not found:
            break

    return safe_sequence, iteration


def main():
    processes = int(input("Enter the number of processes: "))
    num_resources = int(input("Enter the number of resources: "))   
    
    filename = input("Please enter the .txt file for your inputs: ")
    initial_resources, allocation_matrix, max_matrix = read_input(filename)

    # Print resource instances
    print_resource_instances(initial_resources)

    # Print Allocation Matrix from input file
    print_matrix(allocation_matrix, ["R{}".format(i) for i in range(len(allocation_matrix[0]))], "Allocation Matrix (From Input File)")

    # Print Max Matrix from input file
    print_matrix(max_matrix, ["R{}".format(i) for i in range(len(max_matrix[0]))], "Max Matrix (From Input File)")

    safe_sequence, iteration = bankers_algorithm(initial_resources, allocation_matrix, max_matrix)

    if len(safe_sequence) == len(allocation_matrix):
        print("\nSystem is in a safe state.")
        # print("Safe sequence:", safe_sequence)
        print("Safe sequence: P" + ", P".join(map(str, safe_sequence)))
            
    else:
        print("\nDeadlock occurred in iteration", iteration)

if __name__ == "__main__":
    main()
