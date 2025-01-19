import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Declare global variables 
line = None
fig = None
angle_text = None
ax = None

slider = None

def createCircle():
    global line, fig, ax, angle_text  # Declare these variables as global

    # Create the circle
    theta = np.linspace(0, 2 * np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)

    # Set up the plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y)  # Circle, by default draws line between points
    ax.axhline(0, color='black',linewidth=1)  # X-axis
    ax.axvline(0, color='black',linewidth=1)  # Y-axis
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # Add line and angle text
    line, = ax.plot([0, 1], [0, 0], color='red', lw=2)  # Initial line
    angle_text = ax.text(1.1, 0, 'Angle: 0°', fontsize=12)

    # Set equal scaling
    ax.set_aspect('equal', adjustable='box')

    # Add labels
    ax.set_title("Circle with Radius 1 and Rotating Line")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

# Function to update the line position
def update(val):
    global line, angle_text  # Declare line and angle_text as global to modify them

    angle = slider.val
    angle_rad = np.deg2rad(angle)
    
    # Update line
    x_end = np.cos(angle_rad)
    y_end = np.sin(angle_rad)
    line.set_data([0, x_end], [0, y_end])
    
    # Update angle text
    angle_text.set_text(f'Angle: {angle:.1f}°')

    # Redraw the plot
    fig.canvas.draw_idle()
    
def createSlider():
   global slider # Declare slider as global to modify them
   # Slider for angle control
   ax_slider = plt.axes([0.2, 0.01, 0.65, 0.02], facecolor='lightgoldenrodyellow')
   slider = Slider(ax_slider, 'Angle', 0, 360, valinit=0, valstep=1)
   slider.on_changed(update)

createCircle()
createSlider()


# Show the plot with the slider
plt.grid(True)
plt.show()