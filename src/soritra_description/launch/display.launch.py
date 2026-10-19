from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, UnsetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
	package_share = FindPackageShare("soritra_description")
	urdf_file = PathJoinSubstitution([package_share, "urdf", "soritra.urdf"])
	default_rviz_config = PathJoinSubstitution(
		[package_share, "rviz", "soritra.rviz"]
	)

	use_sim_time = LaunchConfiguration("use_sim_time")
	rviz_config = LaunchConfiguration("rviz_config")

	robot_description = ParameterValue(
		Command(["xacro ", urdf_file]), value_type=str
	)

	return LaunchDescription(
		[
			# VS Code installé via Snap transmet des chemins de modules GTK/GIO
			# incompatibles avec les bibliothèques système utilisées par ROS.
			UnsetEnvironmentVariable(name="GIO_MODULE_DIR"),
			UnsetEnvironmentVariable(name="GTK_PATH"),
			DeclareLaunchArgument(
				"use_sim_time",
				default_value="false",
				description="Utiliser l’horloge d’une simulation ROS.",
			),
			DeclareLaunchArgument(
				"rviz_config",
				default_value=default_rviz_config,
				description="Fichier de configuration RViz à charger.",
			),
			Node(
				package="robot_state_publisher",
				executable="robot_state_publisher",
				name="robot_state_publisher",
				output="screen",
				parameters=[
					{"robot_description": robot_description},
					{"use_sim_time": use_sim_time},
				],
			),
			Node(
				package="joint_state_publisher_gui",
				executable="joint_state_publisher_gui",
				name="joint_state_publisher_gui",
				output="screen",
				parameters=[
					{"robot_description": robot_description},
					{"use_sim_time": use_sim_time},
				],
			),
			Node(
				package="rviz2",
				executable="rviz2",
				name="rviz2",
				output="screen",
				arguments=["-d", rviz_config],
				parameters=[{"use_sim_time": use_sim_time}],
			),
		]
	)
