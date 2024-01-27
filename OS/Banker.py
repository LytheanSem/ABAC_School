def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    resources = list(map(int, lines[1].strip().split()))
    allocation_matrix = [list(map(int, line.strip().split())) for line in lines[3:8]]
    max_matrix = [list(map(int, line.strip().split())) for line in lines[9:]]

    return resources, allocation_matrix, max_matrix

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

def print_need_table(processes, need_matrix):
    print("\n{:10} {:10} {:10} {:10}".format("Process", "Resource 1", "Resource 2", "Resource 3"))
    for i in range(processes):
        print("{:10} {:10} {:10} {:10}".format(
            f"P{i}",
            *need_matrix[i]
        ))

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
        print_need_table(processes, need_matrix)

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
                break

        if not found:
            break

    return safe_sequence, iteration



def main():
    filename = input("Please enter the .txt file for your inputs: ")
    resources, allocation_matrix, max_matrix = read_input(filename)

    safe_sequence, iteration = bankers_algorithm(resources, allocation_matrix, max_matrix)

    if len(safe_sequence) == len(allocation_matrix):
        print("\nSystem is in a safe state.")
        print("Safe sequence:", safe_sequence)
    else:
        print("\nDeadlock occurred in iteration", iteration)

if __name__ == "__main__":
    main()
