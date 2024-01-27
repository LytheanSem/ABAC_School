n = int(input("Enter the number of processes: "))

burst_times = []
arrival_times = []

for i in range(1, n + 1):
    burst_time = int(input(f"Enter burst time for P{i}: "))
    arrival_time = int(input(f"Enter arrival time for P{i}: "))

    burst_times.append(burst_time)
    arrival_times.append(arrival_time)

print(burst_times)
print(arrival_times)

waiting_times = [0] * n

# Cal waiting time
for i in range(1, n):
    waiting_times[i] = waiting_times[i - 1] + burst_times[i - 1]

    
# Sub arrival times
for i in range(1, n):
    waiting_times[i] -= arrival_times[i]

# Display waiting times
for i in range(n):
    print(f"Waiting time for P{i + 1}: {waiting_times[i]}")
    
    
    

# cal and display avg waiting time
avg_waiting_time = sum(waiting_times) / n
print("\nAverage Waiting Time:", avg_waiting_time)
