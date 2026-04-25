import numpy as np
import matplotlib.pyplot as plt

# 13 nodes
N = 13
feedback = 1  ## communication graph feedback (1 or -1) 
b= 0.1 ##  external push at nodes ( 0.1 or 0.3) 
noise_level = 0.02  
steps = 120   ## total step of simulations (one step =0.1 s)

# communication graph: 1= connected agents
edges = [
    (1,2), (1,3), (1,7), (1,12), (1,13),
    (2,3), (2,4), (2,8), (2,13),
    (3,10), 
    (4,5), (4,6), (4,10),
    (5,6), (5,11), (5,13),
    (6,8), (6,10), (6,12),
    (7,11),
    (8,9),
    (9,10), (9,11), (9,12),
    (10,13),
    (11,13)
]

# Build A Matrix
A = np.zeros((N, N), dtype=float)
for u, v in edges: 
    A[u-1, v-1] = feedback  
    A[v-1, u-1] = feedback  
  
# diagonal entries: A(i,i) = 1
for i in range(N):
    A[i, i] = 1

# Print matrix
print("\nMatrix A:")
print(A)

#normalize the matrix using the largest eigenvalue 
eigenvalues = np.linalg.eigvals(A)
largest = np.max(np.abs(eigenvalues))
A = A / largest
     
#print("\nLargest eigenvalue of Matrix A:", largest)


# initialize x 
x = np.zeros(N)


print("use x = Ax + noise to update the system: \n")
history = [x.flatten()]   ## for plotting  
for i in range(1, steps):
    noise = noise_level * np.random.randn(N)  # Add random noise to x
    x = x + noise
    ## add input (push) at step 70-80 (0.7-0.8s) to agent 3, 6 , 10 11
    if 70<=i<=80 :  
      x[2] =  x[2] - b  
      x[5] = x[5]  + b 
      x[9] = x[9]  + b 
      x[10] = x[10] - b  
    x = A @ x 

    
    history.append(x.flatten()) # for plotting 
    
## end of simulation 

## plotting:
history = np.array(history)  # shape: (steps+1, N) for plotting

# Plot each node's value over time in different colors
colors = plt.cm.tab20(np.linspace(0, 1, N))

plt.figure(figsize=(10, 6))
for node in range(N):
    plt.plot(history[:, node], marker='', color=colors[node], label=f'agent{node+1}')

plt.xlabel('Step (n)')
plt.xlim(0, 120)
plt.ylim(-0.2, 0.5)
plt.ylabel('Value')
plt.title(f"feedback={feedback}    b={b}    noise={noise_level}")
plt.legend(loc='upper left', fontsize=8, ncol=2)
plt.xticks()
plt.tight_layout()
plt.show()

