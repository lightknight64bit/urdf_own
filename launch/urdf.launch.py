from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
import os
def generate_launch_description():
    urdf = '/home/govind/ros_ws/src/urdf_own/urdf/robot.urdf.xacro'
    urdf_ = os.popen(f'xacro {urdf}').read()
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    return LaunchDescription([
        
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name = 'robot_state_publisher',
            parameters=[{'use_sim_time':use_sim_time,'robot_description':urdf_}],
            arguments=[urdf]
            

        )
        ]
    )