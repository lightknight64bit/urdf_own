import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='urdf_own' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch/urdf.launch.py'
                )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control':'true'}.items()
    )
    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])
    controller_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'my_controller.yaml')
    controller_manager = Node(package='controller_manager', executable='ros2_control_node',
                        parameters=[{'robot_description': robot_description}, controller_params_file],
                        remappings=[('/cmd_vel', '/diff_cont/cmd_vel_unstamped')]
                        )
    d_controller_manager = TimerAction(period=3.0, actions=[controller_manager])
    
    diff_drive_spawner = Node(package='controller_manager', executable='spawner.py',
                        arguments=['diff_cont'],
                        )
    d_diff_drive_spawner = RegisterEventHandler(event_handler=OnProcessStart(target_action=controller_manager, on_start=[diff_drive_spawner]))
    joint_cont_spawner = Node(package='controller_manager', executable='spawner.py',
                        arguments=['joint_broad'],
                        )
    d_joint_cont_spawner = RegisterEventHandler(event_handler=OnProcessStart(target_action=diff_drive_spawner, on_start=[joint_cont_spawner]))



    # Launch them all!
    return LaunchDescription([
        rsp,
        d_controller_manager,
        d_diff_drive_spawner,
        d_joint_cont_spawner
    ])
