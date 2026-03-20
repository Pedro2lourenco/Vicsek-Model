import numpy as np

# ============================
# Function to compute distance between particles i and j
# ============================
def dist(A,B,i,j):
    dx = A[j] - A[i]
    dy = B[j] - B[i]
    return np.sqrt(dx*dx + dy*dy)

# ============================
# Model parameters
# ============================
Num = [20,50,100]        # number of particles
etas = np.arange(0,1,0.05)  # noise strength
v0 = 0.2                 # constant particle speed
r0 = 1.                  # interaction radius
L = 10                   # system size (box length)

pol = []                 # list to store polarization values

# ============================
# Loop over different system sizes
# ============================
for idx, N in enumerate(Num):

    print(f'N = {N}')

    pol = []

    # ============================
    # Loop over noise values (η)
    # ============================
    for eta in etas:

        print(f'noise {eta}')

        phi = []  # polarization time series

        # Random initialization of particle positions
        x = np.random.rand(N)*L
        y = np.random.rand(N)*L

        # Random initialization of particle orientations
        theta = 2*np.pi*np.random.rand(N)

        dt = 0.1
        sim = np.arange(0,200,dt)

        # ============================
        # Time evolution loop
        # ============================
        for k in range(len(sim)):

            print(f'Step {k}')

            theta_new = np.zeros(N)

            # ============================
            # Update direction of each particle
            # ============================
            for i in range(N):

                neigb = []

                # Find neighbors within interaction radius r0
                for j in range(N):
                    if dist(x,y,i,j) < r0:
                        neigb.append(j)

                # Compute average direction of neighbors
                if len(neigb) > 0:
                    mean_sin = np.mean(np.sin(theta[neigb]))
                    mean_cos = np.mean(np.cos(theta[neigb]))

                    # Update direction with added noise
                    theta_new[i] = np.arctan2(mean_sin, mean_cos) + eta*(2*np.random.rand()-1)*np.pi
                else:
                    theta_new[i] = theta[i]

            theta = theta_new

            # ============================
            # Compute polarization (order parameter)
            # ============================
            vx = np.cos(theta)
            vy = np.sin(theta)
            phi.append(np.sqrt((np.sum(vx))**2 + (np.sum(vy))**2) / N)

            # ============================
            # Update particle positions with periodic boundary conditions
            # ============================
            x = (x + v0*np.cos(theta)*dt) % L
            y = (y + v0*np.sin(theta)*dt) % L

        # Compute average polarization in the steady-state regime (second half)
        pol.append(np.mean(phi[len(phi)//2:]))



