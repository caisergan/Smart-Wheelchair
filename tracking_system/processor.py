import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        pass

    def process(self, frame, threshold=60, min_area=1000, min_aspect_ratio=1.0):
        """
        Process the frame to detect the black tape.
        
        Args:
            frame (numpy.ndarray): The input image frame.
            threshold (int): Upper bound for black color (0-255).
            min_area (int): Minimum contour area to be considered a line.
            min_aspect_ratio (float): Minimum aspect ratio (long side / short side) to be considered a line.
            
        Returns:
            tuple: (error, processed_frame)
                error (float): Deviation from center (normalized -1 to 1). None if no line found.
                processed_frame (numpy.ndarray): Frame with visualization.
        """
        if frame is None:
            return None, None

        # Resize for faster processing and consistent coordinates
        height, width = frame.shape[:2]
        
        # Define color range for black
        low_b = np.array([0, 0, 0], dtype=np.uint8)
        high_b = np.array([threshold, threshold, threshold], dtype=np.uint8)
        
        # Create mask
        mask = cv2.inRange(frame, low_b, high_b)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        processed_frame = frame.copy()
        
        valid_contours = []
        for c in contours:
            area = cv2.contourArea(c)
            if area > min_area:
                # Check aspect ratio
                rect = cv2.minAreaRect(c)
                (x, y), (w, h), angle = rect
                
                # Avoid division by zero
                if w == 0 or h == 0:
                    ar = 0
                else:
                    ar = max(w, h) / min(w, h)
                
                if ar >= min_aspect_ratio:
                    valid_contours.append(c)
                    # Draw the actual contour (high detail)
                    # Approximate the contour to make it a "polygon" but keep high detail (epsilon small)
                    epsilon = 0.005 * cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, epsilon, True)
                    cv2.drawContours(processed_frame, [approx], 0, (0, 255, 0), 2)
                else:
                    # Rejected by aspect ratio
                    cv2.drawContours(processed_frame, [c], -1, (0, 255, 255), 1) # Yellow for bad shape
            else:
                # Rejected by area
                cv2.drawContours(processed_frame, [c], -1, (0, 0, 255), 1) # Red for small area
        
        if valid_contours:
            # Assume the largest valid contour is the tape
            c = max(valid_contours, key=cv2.contourArea)
            
            # Calculate moments to find centroid
            M = cv2.moments(c)
            
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Draw centroid
                cv2.circle(processed_frame, (cx, cy), 5, (0, 0, 255), -1)
                
                # Calculate error
                # Center of image is width / 2
                # Error is (cx - center) / (width / 2) -> range -1 to 1
                center = width / 2
                error = (cx - center) / center
                
                # Visualize error
                cv2.line(processed_frame, (int(center), cy), (cx, cy), (255, 0, 0), 2)
                
                return error, processed_frame
        
        return None, processed_frame
