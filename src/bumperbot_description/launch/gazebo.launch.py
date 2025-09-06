import os
from pathlib import Path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    # Paths
    bumperbot_description = get_package_share_directory("bumperbot_description")
    urdf_file = os.path.join(bumperbot_description, "urdf", "bumperbot.urdf.xacro")
    
    # ROS distro & ignition flag
    ros_distro = os.environ.get("ROS_DISTRO", "humble")
    is_ignition = "True" if ros_distro in ["humble", "iron"] else "False"

    # Launch argument for model path
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=urdf_file,
        description="Absolute path to robot URDF file"
    )

    # Robot description parameter
    robot_description = ParameterValue(
        Command([
            "xacro ", LaunchConfiguration("model"),
            " is_ignition:=", is_ignition
        ]),
        value_type=str
    )

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": robot_description},
            {"use_sim_time": True}
        ]
    )

    # Set Gazebo resource path (CRITICAL FIX)
    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=str(Path(bumperbot_description).parent.resolve())  # Parent directory of package
    )

    # Launch Gazebo (empty world)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": "-v 4 -r empty.sdf"
        }.items()
    )

    # Spawn robot in Gazebo (after 3.5s delay)
    gz_spawn_entity = TimerAction(
        period=3.5,
        actions=[
            Node(
                package="ros_gz_sim",
                executable="create",
                output="screen",
                arguments=[
                    "-topic", "robot_description",
                    "-name", "bumperbot",
                    "-x", "0",
                    "-y", "0",
                    "-z", "0.5"
                ],
                parameters=[{"use_sim_time": True}]
            )
        ]
    )

    return LaunchDescription([
        model_arg,
        gazebo_resource_path,
        robot_state_publisher_node,
        gazebo,
        gz_spawn_entity
    ])
