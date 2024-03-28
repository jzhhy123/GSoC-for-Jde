import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
arena_size = 100
step_size = 1
num_steps = 1000
marker_size = 50  # Increase the size of the marker representing the robot

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
line, = ax.plot([], [], 'r-', linewidth=1)  # 'r-' creates a red line for the trajectory
point, = ax.plot([], [], 'o', markersize=marker_size)

# Initialize
arrow = ax.arrow(robot_position[0], robot_position[1], 0, 0, head_width=3, head_length=6, fc='k',
                 length_includes_head=True)
trace, = ax.plot([], [], '-', lw=3, color='red')

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point, arrow

def animate(i):
    global arrow
    x = positions[i][0]
    y = positions[i][1]

    # Update the point position
    point.set_data([x], [y])

    # Add the current position to the trace
    trace_x, trace_y = trace.get_data()
    trace.set_data(np.append(trace_x, x), np.append(trace_y, y))

    # Update the arrow to show direction
    arrow.remove()  # Remove the old arrow
    dx = np.cos(robot_direction) * 5  # Length of the arrow along x (scaled for visibility)
    dy = np.sin(robot_direction) * 5  # Length of the arrow along y (scaled for visibility)
    arrow = ax.arrow(x, y, dx, dy, head_width=3, head_length=6, fc='k', length_includes_head=True)

    return point, arrow, trace


ani = animation.FuncAnimation(fig, animate, init_func=init, frames=num_steps, interval=50, blit=False)

plt.show()

