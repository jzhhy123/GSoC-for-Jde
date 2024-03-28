import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
arena_size = 100
step_size = 1
num_steps = 1000

# Initialize the robot's position and direction
robot_position = np.array([arena_size / 2, arena_size / 2])
robot_direction = np.random.rand() * 2 * np.pi

# Store the positions for plotting
positions = [robot_position.copy()]

def update_position():
    global robot_position, robot_direction
    # Move robot
    robot_position += np.array([np.cos(robot_direction), np.sin(robot_direction)]) * step_size

    # Check for boundary collision
    if not (0 <= robot_position[0] <= arena_size) or not (0 <= robot_position[1] <= arena_size):
        # Reflect the direction if it hits a boundary
        robot_direction += np.pi + np.random.uniform(-0.1, 0.1)

    # Ensure the robot stays within bounds
    robot_position = np.clip(robot_position, 0, arena_size)
    positions.append(robot_position.copy())

# Update the robot's position for a number of steps
for _ in range(num_steps):
    update_position()

# Plotting
fig, ax = plt.subplots()
ax.set_xlim(0, arena_size)
ax.set_ylim(0, arena_size)
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return (line,)

def animate(i):
    x = [p[0] for p in positions[:i]]
    y = [p[1] for p in positions[:i]]
    line.set_data(x, y)
    return (line,)

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(positions), interval=50, blit=False)

plt.show()

