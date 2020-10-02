import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Define LaunchDescription variable
    ld = LaunchDescription()

    # use:
    #  - 'zed' for "ZED" camera
    #  - 'zedm' for "ZED mini" camera
    #  - 'zed2' for "ZED2" camera
    camera_model = 'zedm'

    # Camera name
    camera_name = 'zedm'

    # URDF file to be loaded by Robot State Publisher
    urdf = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'urdf', camera_model + '.urdf'
    )

    # ZED Configurations to be loaded by ZED Node
    config_common = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'config',
        'common.yaml'
    )

    config_camera = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'config',
        camera_model + '.yaml'
    )

    # Rviz2 Configurations to be loaded by ZED Node
    config_rviz2 = os.path.join(
        get_package_share_directory('zed_display_rviz2'),
        'rviz2',
        camera_model + '.rviz'
    )

    # Set LOG format
    os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time} [{name}] [{severity}] {message}'

    # Robot State Publisher node
    rsp_node = Node(
        package='robot_state_publisher',
        node_namespace=camera_name,
        node_executable='robot_state_publisher',
        node_name=camera_name+'_state_publisher',
        output='screen',
        arguments=[urdf],
    )

    # ZED Wrapper node
    zed_wrapper_node = Node(
        package='zed_wrapper',
        node_namespace=camera_name,
        node_executable='zed_wrapper',
        node_name='zed_node',
        output='screen',
        parameters=[
            config_common,  # Common parameters
            config_camera,  # Camera related parameters
        ]
    )

    # Rviz2 node
    rviz2_node = Node(
        package='rviz2',
        node_namespace=camera_name,
        node_executable='rviz2',
        node_name=camera_name+'_rviz2',
        output='screen',
        arguments=[["-d"],[config_rviz2]],
    )

    # Add noded to LaunchDescription
    ld.add_action(rsp_node)
    ld.add_action(zed_wrapper_node)
    ld.add_action(rviz2_node)

    return ld
