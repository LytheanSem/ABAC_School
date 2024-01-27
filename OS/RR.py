n = int(input("Enter the number of processes: "))
time_quantum = int(input("Please enter the time quantum: "))

burst_times = []
arrival_times = []

for i in range(1, n + 1):
    burst_time = int(input(f"Enter burst time for P{i}: "))
    arrival_time = int(input(f"Enter arrival time for P{i}: "))

    burst_times.append(burst_time)
    arrival_times.append(arrival_time)

print(f"\nburst time in list form: {burst_times}")
print(f"arrival time in list form: {arrival_times}")

# flag=remainingBurstTime
flag = burst_times.copy()
waiting_times = [0] * n
queue = list(range(n))
time = 0

while queue:
    process = queue.pop(0)
    if flag[process] <= time_quantum:
        time += flag[process]
        waiting_times[process] += time - burst_times[process]
        flag[process] = 0
    else:
        time += time_quantum
        flag[process] -= time_quantum
        queue.append(process) 

print(f"\nwaiting time in list form (without substracting the arrival time yet): {waiting_times}\n")

# Subtract arrival times
for i in range(1, n):
    waiting_times[i] -= arrival_times[i]

# Display waiting times
for i in range(n):
    print(f"Waiting time for P{i + 1}: {waiting_times[i]} ms")

# Cal and display avg waiting time
avg_waiting_time = sum(waiting_times) / n
print(f"\nAverage Waiting Time: {avg_waiting_time:.2f} ms")