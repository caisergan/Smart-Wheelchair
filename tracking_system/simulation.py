import cv2
import numpy as np
import math

class Simulator:
    def __init__(self, width=800, height=600):
        """
        Initialize the simulator with a track map.
        """
        self.width = width
        self.height = height
        self.map = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Draw a track (black line)
        # Simple loop: oval shape
        center_x, center_y = width // 2, height // 2
        axes = (width // 3, height // 3)
        cv2.ellipse(self.map, (center_x, center_y), axes, 0, 0, 360, (0, 0, 0), 20)
        
        # Robot state
        # Start on the track (Top of oval)
        self.x = center_x
        self.y = center_y - axes[1]
        self.theta = 0.0 # Facing right
        
        self.robot_width = 40 # pixels (distance between wheels)
        self.max_speed = 5.0 # pixels per frame
        
        # Viewport parameters
        self.view_width = 160
        self.view_height = 120

    def update(self, left_speed, right_speed):
        """
        Update robot pose based on wheel speeds.
        Speeds are -1.0 to 1.0
        """
        # Differential drive kinematics
        v_left = left_speed * self.max_speed
        v_right = right_speed * self.max_speed
        
        v = (v_left + v_right) / 2.0
        omega = (v_right - v_left) / self.robot_width
        
        self.x += v * math.cos(self.theta)
        self.y += v * math.sin(self.theta)
        self.theta += omega
        
        # Keep theta normalized
        self.theta = (self.theta + np.pi) % (2 * np.pi) - np.pi

    def get_frame(self):
        """
        Get the camera view from the current robot pose.
        """
        # Define the viewport rectangle centered at robot
        # We need to extract a rotated rectangle
        
        # Create a rotation matrix
        M = cv2.getRotationMatrix2D((self.x, self.y), np.degrees(self.theta) - 90, 1.0)
        
        # We want the camera to look "ahead". 
        # In our map, theta is the direction of movement.
        # The camera view should be aligned such that "up" in the image is "forward" in the world.
        # So we rotate the map around the robot by -theta + 90 degrees?
        # Let's try extracting a larger patch and rotating it.
        
        patch_size = max(self.view_width, self.view_height) * 2
        
        # Extract patch (clipping to bounds)
        x_min = int(self.x - patch_size / 2)
        y_min = int(self.y - patch_size / 2)
        x_max = x_min + patch_size
        y_max = y_min + patch_size
        
        # Pad map if needed (simple way: just clip and maybe get black borders)
        # Better: warpAffine the whole map (slow) or just handle boundaries carefully.
        # For simplicity, let's assume we stay in bounds or just pad with white.
        
        map_padded = cv2.copyMakeBorder(self.map, patch_size, patch_size, patch_size, patch_size, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        
        # Adjust coordinates for padded map
        x_p = self.x + patch_size
        y_p = self.y + patch_size
        
        M = cv2.getRotationMatrix2D((x_p, y_p), np.degrees(self.theta) + 90, 1.0)
        rotated = cv2.warpAffine(map_padded, M, (map_padded.shape[1], map_padded.shape[0]))
        
        # Crop the center of the rotated image
        crop_x = int(x_p - self.view_width / 2)
        crop_y = int(y_p - self.view_height) # Camera looks ahead, so robot is at bottom
        
        # Actually, let's put robot at bottom center of view
        # So we crop from [x_p - w/2, y_p - h] to [x_p + w/2, y_p]
        
        view = rotated[crop_y:crop_y+self.view_height, crop_x:crop_x+self.view_width]
        
        return view

    def get_map_with_robot(self):
        """Return the global map with robot drawn on it for visualization."""
        vis_map = self.map.copy()
        cv2.circle(vis_map, (int(self.x), int(self.y)), 5, (0, 0, 255), -1)
        
        # Draw heading
        end_x = int(self.x + 20 * math.cos(self.theta))
        end_y = int(self.y + 20 * math.sin(self.theta))
        cv2.line(vis_map, (int(self.x), int(self.y)), (end_x, end_y), (0, 0, 255), 2)
        
        return vis_map
