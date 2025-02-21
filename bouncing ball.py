import tkinter as tk

class DraggableBallWithGravity:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        # Initial ball position and properties
        self.x, self.y = 100, 100
        self.radius = 30
        self.vx, self.vy = 0, 0  # velocity in x and y directions
        self.gravity = 0.5  # acceleration due to gravity
        self.friction = 0.98  # damping factor to simulate energy loss during bounce
        self.ground_y = self.height - 50  # position of the ground

        # Create the ball (circle)
        self.ball = self.canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                            self.x + self.radius, self.y + self.radius,
                                            fill='blue', outline='black')

        # Bind the mouse events to drag the ball
        self.canvas.tag_bind(self.ball, '<Button-1>', self.on_press)
        self.canvas.tag_bind(self.ball, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.ball, '<ButtonRelease-1>', self.on_release)

        # Start the gravity simulation
        self.update_gravity()

    def on_press(self, event):
        """Called when mouse is pressed on the ball."""
        # Record the offset to drag the ball
        self.offset_x = event.x - self.x
        self.offset_y = event.y - self.y
        self.vx, self.vy = 0, 0  # Stop gravity when dragging
        self.last_x, self.last_y = event.x, event.y  # Store last mouse position
        self.gravity = 0  # Stop gravity during drag

    def on_drag(self, event):
        """Called when mouse is dragged with button pressed."""
        # Update the ball's position while dragging
        self.x = event.x - self.offset_x
        self.y = event.y - self.offset_y

        # Calculate velocity based on the change in position
        self.vx = event.x - self.last_x
        self.vy = event.y - self.last_y
        self.last_x, self.last_y = event.x, event.y  # Update last position

        self.canvas.coords(self.ball, self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius)

    def on_release(self, event):
        """Called when mouse button is released."""
        # Resume gravity simulation after dragging
        self.gravity = 1  # Resume gravity
        self.friction = 0.8  # Restore friction

    def update_gravity(self):
        """Updates the position of the ball based on gravity and collision with boundaries."""
        # Apply gravity
        self.vy += self.gravity

        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Collision detection with the ground (bounce effect)
        if self.y + self.radius >= self.ground_y:
            self.y = self.ground_y - self.radius  # Place the ball on the ground
            self.vy = -self.vy * self.friction  # Reverse and reduce the vertical velocity (bounce)
            self.vx *= self.friction  # Apply friction to horizontal movement

        # Collision detection with walls (bounce effect)
        if self.x - self.radius <= 0:  # Left wall
            self.x = self.radius
            self.vx = -self.vx * self.friction
        elif self.x + self.radius >= self.width:  # Right wall
            self.x = self.width - self.radius
            self.vx = -self.vx * self.friction

        # Update the position of the ball in the canvas
        self.canvas.coords(self.ball, self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius)

        # Continue the gravity simulation by calling this method repeatedly
        self.canvas.after(20, self.update_gravity)

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Ball with Gravity and Throwing Physics")

    # Set the window size
    window_width = 500
    window_height = 500

    # Create a canvas to draw on
    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack()

    # Create the draggable ball with gravity
    ball_with_gravity = DraggableBallWithGravity(canvas, window_width, window_height)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
