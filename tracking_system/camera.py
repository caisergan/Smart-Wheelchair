import cv2

class CameraInput:
    def __init__(self, source=0):
        """
        Initialize the camera input.
        
        Args:
            source (int or str): Camera index or video file path. Default is 0 (webcam).
        """
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open camera source: {source}")

    def read_frame(self):
        """
        Read a frame from the camera.
        
        Returns:
            frame (numpy.ndarray): The captured frame, or None if failed.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        """Release the camera resource."""
        self.cap.release()
