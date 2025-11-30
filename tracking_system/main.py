import cv2
import time
import argparse
from tracking_system.camera import CameraInput
from tracking_system.processor import ImageProcessor
from tracking_system.controller import PIDController
from tracking_system.motor import MotorInterface
from tracking_system.simulation import Simulator

def main():
    parser = argparse.ArgumentParser(description='Black Tape Tracking System')
    parser.add_argument('--simulation', action='store_true', help='Run in simulation mode')
    args = parser.parse_args()

    # Initialize modules
    camera = None
    simulator = None
    
    if args.simulation:
        print("Running in SIMULATION mode.")
        simulator = Simulator()
    else:
        try:
            camera = CameraInput(source=0) # Use 0 for webcam, or path to video file
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return

    processor = ImageProcessor()
    # Tune PID values here
    controller = PIDController(kp=0.5, ki=0.0, kd=0.1)
    motor = MotorInterface()
    
    base_speed = 0.5
    
    print("Starting tracking system. Press 'q' to exit.")
    
    # Create window and trackbar
    cv2.namedWindow("Tracking View")
    def nothing(x):
        pass
    cv2.createTrackbar("Black Level", "Tracking View", 60, 255, nothing)
    cv2.createTrackbar("Min Area", "Tracking View", 1000, 10000, nothing)
    cv2.createTrackbar("Min Aspect Ratio", "Tracking View", 10, 100, nothing)
    
    try:
        while True:
            if args.simulation:
                frame = simulator.get_frame()
            else:
                frame = camera.read_frame()
                
            if frame is None:
                print("Failed to read frame or end of video.")
                break
            
            # Get threshold and min area from trackbars
            thresh_val = cv2.getTrackbarPos("Black Level", "Tracking View")
            min_area_val = cv2.getTrackbarPos("Min Area", "Tracking View")
            min_ar_val = cv2.getTrackbarPos("Min Aspect Ratio", "Tracking View") / 10.0
            
            error, processed_frame = processor.process(frame, threshold=thresh_val, min_area=min_area_val, min_aspect_ratio=min_ar_val)
            
            left_speed = 0.0
            right_speed = 0.0
            
            if error is not None:
                # Calculate steering adjustment
                steering = controller.compute(error)
                
                # Calculate motor speeds
                # If error is positive (line to right), we need to turn right.
                # Turn right -> Left motor faster, Right motor slower
                left_speed = base_speed + steering
                right_speed = base_speed - steering
                
                motor.set_speed(left_speed, right_speed)
            else:
                # No line detected - stop or spin to find line?
                # For safety, let's stop.
                print("No line detected.")
                motor.stop()
            
            # Update simulation if active
            if args.simulation:
                simulator.update(left_speed, right_speed)
                
                # Show map view
                map_view = simulator.get_map_with_robot()
                cv2.imshow("Simulation Map", map_view)
            
            # Display tracking view
            if processed_frame is not None:
                cv2.imshow("Tracking View", processed_frame)
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        motor.stop()
        if camera:
            camera.release()
        cv2.destroyAllWindows()
        print("System stopped.")

if __name__ == "__main__":
    main()
