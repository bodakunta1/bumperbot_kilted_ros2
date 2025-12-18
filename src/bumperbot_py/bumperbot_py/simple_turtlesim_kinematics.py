import rclpy    # Import rclpy library
import math  # Import math library
from rclpy.node import Node     # Import Node class from rclpy
from turtlesim.msg import Pose  # Import Pose message from turtlesim

class SimpleTurtlesimKinematics(Node):
    def __init__(self):
        super().__init__("simple_turtlesim_kinematics") # Initialize the node with the name "simple_turtlesim_kinematics"

        self.turtle1_pose_sub_ = self.create_subscription(Pose, "turtle1/pose", self.turtle1PoseCallback, 10) # Subscribe to turtle1/pose topic
        self.turtle2_pose_sub_ = self.create_subscription(Pose, "turtle2/pose", self.turtle2PoseCallback, 10) # Subscribe to turtle2/pose topic

        self.last_turtle1_pose_ = Pose() # Initialize last_turtle1_pose_ with a default Pose
        self.last_turtle2_pose_ = Pose() # Initialize last_turtle2_pose_ with a default Pose

    def turtle1PoseCallback(self, msg):  # Callback function for turtle1 pose
        self.last_turtle1_pose_ = msg    # Update last_turtle1_pose_ with the received message


    def turtle2PoseCallback(self, msg):  # Callback function for turtle2 pose
        self.last_turtle2_pose_ = msg    # Update last_turtle2_pose_ with the received message

        Tx = self.last_turtle2_pose_.x - self.last_turtle1_pose_.x  # Calculate translation in x
        Ty = self.last_turtle2_pose_.y - self.last_turtle1_pose_.y  # Calculate translation in y

        theta_rad = self.last_turtle2_pose_.theta - self.last_turtle1_pose_.theta  # Calculate rotation in radians
        theta_deg = math.degrees(theta_rad)                                        # Convert rotation to degrees

        self.get_logger().info("""\n
        Translation Vector turtle1 -> turtle2\n
                               Tx: %f \n
                               Ty: %f \n 
                               Rotation Matrix turtle1 -> turtle2 \n
                               theta(rad): %f\n
                               theta(deg): %f\n
                               |R11     R12| : |%f      %f|\n
                               |R21     R22| : |%f      %f|\n""" % (Tx, Ty, theta_rad, theta_deg, math.cos(theta_rad),
                                                                    -math.sin(theta_rad), math.sin(theta_rad), math.cos(theta_rad))) # Log the translation and rotation information
        
def main():
    rclpy.init()          # Initialize rclpy
    simple_turtlesim_kinematics = SimpleTurtlesimKinematics()  # Create an instance of SimpleTurtlesimKinematics
    rclpy.spin(simple_turtlesim_kinematics)  # Spin the node to keep it alive and processing callbacks
    simple_turtlesim_kinematics.destroy_node()  # Destroy the node after spinning
    rclpy.shutdown()   # Shutdown rclpy

if __name__ == '__main__':      
    main()  # Call the main function if this script is executed directly
