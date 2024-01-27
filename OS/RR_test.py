n = int(input("Enter the number of processes: "))
time_quantum = int(input("Please enter the time quantum: "))

burst_times = []
arrival_times = []

for i in range(1, n + 1):
    burst_time = int(input(f"Enter burst time for process {i}: "))
    arrival_time = int(input(f"Enter arrival time for process {i}: "))

    burst_times.append(burst_time)
    arrival_times.append(arrival_time)

print(burst_times)
print(arrival_times)

flag = burst_times.copy()
waiting_times = [0] * n
queue = list(range(n))
time = 0

while queue:
    process = queue.pop(0)
    if flag[process] <= time_quantum:
        # Process completes within time quantum
        time += flag[process]
        waiting_times[process] += time - burst_times[process]
        flag[process] = 0
    else:
        # Process needs more than time quantum
        time += time_quantum
        flag[process] -= time_quantum
        queue.append(process)
        
print(waiting_times)

# Subtract arrival times
for i in range(1, n):
    waiting_times[i] -= arrival_times[i]

# Display waiting times for each process
for i in range(n):
    print(f"Waiting time for P{i + 1}: {waiting_times[i]} ms")

# Calculate and print average waiting time
avg_waiting_time = sum(waiting_times) / n
print(f"Average Waiting Time: {avg_waiting_time:.2f} ms")