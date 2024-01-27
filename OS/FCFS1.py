n = int(input("Enter the number of processes: "))

burst_times = []
arrival_times = []

for i in range(1, n + 1):
    burst_time = int(input(f"Enter burst time for process {i}: "))
    arrival_time = int(input(f"Enter arrival time for process {i}: "))

    burst_times.append(burst_time)
    arrival_times.append(arrival_time)

print(burst_times)
print(arrival_times)

waiting_times = [0] * n

# Calculate waiting times
for i in range(1, n):
    waiting_times[i] = waiting_times[i - 1] + burst_times[i - 1]


# Display waiting times for each process
for i in range(n):
    print(f"Waiting time for P{i + 1}: {waiting_times[i]}")

# Calculate and display average waiting time
avg_waiting_time = sum(waiting_times) / n
print("\nAverage Waiting Time:", avg_waiting_time)
