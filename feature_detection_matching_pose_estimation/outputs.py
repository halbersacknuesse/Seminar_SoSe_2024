#!/usr/bin/env python
# coding: utf-8

# Imports
import os
import globals
import numpy as np

# Paths
benchmark_path = globals.benchmark_path
keypts_and_descr_path = globals.keypts_and_descr_path
traj_computed_path = globals.traj_computed_path

def check_and_create_directories():
    # Liste der erforderlichen Ordner
    directories = [
        'Outputs/Benchmark',
        'Outputs/Figures',
        'Outputs/KeypointsAndDescriptors',
        'Outputs/TrajectoryComputed'
    ]

    # Überprüfe und erstelle die Ordner bei Bedarf
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Folder '{directory}' created.")
        else:
            print(f"Folder '{directory}' exists.")

# Call function saveKeypointsAndDescriptors
def saveKeypointsAndDescriptors(keypoints,
								descriptors,
								matcher,
                                descriptor,
                                flags,
								image_num):
	# flags = 1: input image or queryDescriptors
	# flags = 2: training-set image trainDescriptors
	
	# File name
	filename1 = os.path.join(keypts_and_descr_path, '%s-with-%s-keypoints%s-%04d.txt' % (matcher, descriptor, flags, image_num))
	filename2 = os.path.join(keypts_and_descr_path, '%s-with-%s-descriptors%s-%04d.txt' % (matcher, descriptor, flags, image_num))

	# Delete a file if it exists
	if os.path.exists(filename1):
		os.remove(filename1)

	elif os.path.exists(filename2):
		os.remove(filename2)

	# Save keypoints into a file
	np.savetxt(fname = filename1,
				X = keypoints,
				fmt='%s')

	# Save descriptors into a file
	np.savetxt(fname = filename2,
			   X = descriptors,
			   fmt = "%d")
# Call funktion save_traj_computed	
def save_traj_computed(traj_computed_total, traj_computed_relative, traj_difference, 
					   matcher, 
					   detector,
					   descriptor):
	filename1 = os.path.join(traj_computed_path, 'traj_computed_total-%s-%s-%s.txt' % (matcher, detector, descriptor))
	filename2 = os.path.join(traj_computed_path, 'traj_computed_relative-%s-%s-%s.txt' % (matcher, detector, descriptor))
	filename3 = os.path.join(traj_computed_path, 'traj_computed_difference-%s-%s-%s.txt' % (matcher, detector, descriptor))

	# Delete a file if it exists
	if os.path.exists(filename1):
		os.remove(filename1)

	elif os.path.exists(filename2):
		os.remove(filename2)

	elif os.path.exists(filename3):
		os.remove(filename3)

	# Save traj_computed_total into a file
	np.savetxt(fname = filename1,
			   X = traj_computed_total,
			   fmt='%d %.8f %.8f %.8f %.8f %.8f %.8f')
	
	# Save traj_computed_relative into a file
	np.savetxt(fname = filename2,
			   X = traj_computed_relative,
			   fmt='%d %.8f %.8f %.8f %.8f %.8f %.8f')
	
	# Save traj_computed_difference into a file
	np.savetxt(fname = filename3,
			   X = traj_difference,
			   fmt='%d %.8f %.8f %.8f')
	
# Call function save_benchmark
def save_benchmark(fastest_time, slowest_time, average_time, total_time, total_images, traj_difference,
					matcher, 
					detector, 
					descriptor):
	
	filename = os.path.join(benchmark_path, 'benchmark-%s-%s-%s.txt' % (matcher, detector, descriptor))

	# Delete a file if it exists
	if os.path.exists(filename):
		os.remove(filename)

	# Compute abs of column 2 to 4 of traj_difference
	abs_data = np.abs(traj_difference[:, 1:4])

	# Compute cumulative error
	cumulative_error = np.sum(abs_data, axis=0)

	# Compute max, min, avg of the abs
	max_values = np.max(abs_data, axis=0)
	min_values = np.min(abs_data, axis=0)
	mean_values = np.mean(abs_data, axis=0)

	# Save benchmark data into a file
	with open(filename, 'w') as f:
		f.write(f"Fastest image processing time:\t{fastest_time:.8f} seconds\n")
		f.write(f"Slowest image processing time:\t{slowest_time:.8f} seconds\n")
		f.write(f"Average image processing time:\t{average_time:.8f} seconds\n")
		f.write(f"Total processing time:\t\t{total_time:.8f} seconds\n")
		f.write(f"Total images processed:\t\t{total_images}\n\n\n")
		f.write("Cumulative error:\n")
		f.write(f"\tx: {cumulative_error[0]:.8f}\n")
		f.write(f"\ty: {cumulative_error[1]:.8f}\n")
		f.write(f"\tz: {cumulative_error[2]:.8f}\n")
		f.write("Maximum error:\n")
		f.write(f"\tx: {max_values[0]:.8f}\n")
		f.write(f"\ty: {max_values[1]:.8f}\n")
		f.write(f"\tz: {max_values[2]:.8f}\n")
		f.write("Minimum error:\n")
		f.write(f"\tx: {min_values[0]:.8f}\n")
		f.write(f"\ty: {min_values[1]:.8f}\n")
		f.write(f"\tz: {min_values[2]:.8f}\n")
		f.write("Average error:\n")
		f.write(f"\tx: {mean_values[0]:.8f}\n")
		f.write(f"\ty: {mean_values[1]:.8f}\n")
		f.write(f"\tz: {mean_values[2]:.8f}\n")