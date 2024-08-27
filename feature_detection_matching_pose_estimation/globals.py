#!/usr/bin/env python
# coding: utf-8

# Paths
keypts_and_descr_path = "Outputs/KeypointsAndDescriptors/"
traj_computed_path = "Outputs/TrajectoryComputed/"
benchmark_path = "Outputs/Benchmark/"
image_folder_path = "Dataset/InputImages"
intrinsic_path = "Dataset/Intrinsic/intrinsic.txt"
imported_pose_relative_path = "Dataset/CameraPose/relative_pose_euler.txt"
imported_pose_absolute_path = "Dataset/CameraPose/camera_pose_euler.txt"
figure_path = "Outputs/Figures/"
interactive_plot_path = "Outputs/InteractivePlot.html"

def initialize():
	global descriptor
	global descriptors1
	global descriptors2
	global detector
	global keypoints1
	global keypoints2
	global outputs