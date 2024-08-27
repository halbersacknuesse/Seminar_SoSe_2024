#!/usr/bin/env python
# coding: utf-8

# Feature Description, Matching and Visual Odometry

# Imports
import os
import sys
import argparse
import time
import globals
import features
import save_figures
import outputs
import cv2 as cv
import numpy as np
from tqdm import tqdm
import visual_odometry
from scipy.spatial.transform import Rotation as R


# Initializing global variables
globals.initialize()

# Paths
image_folder_path = globals.image_folder_path
outputs.check_and_create_directories()

# Lists to store trajectories
traj_computed = []
traj_computed_total = []
traj_computed_relative = []
traj_imported = []
traj_imported_abs = []
traj_difference = []

# Initializing benchmark     
times = []
start_time = time.time()

# Read intrinsic parameters for the camera
intrinsic = visual_odometry.read_intrinsic()

# Read the absolute position and orientation from the imported data
abs_path = visual_odometry.read_absolute_path()

# Create camera matrix from intrinsic parameters
camera_matrix = visual_odometry.create_camera_matrix(intrinsic)

# Initialize total rotation and translation matrices for estimation
R_total_est = np.eye(3)
t_total_est = np.zeros((3, 1))

# Initialize total rotation and translation matrices for imported data
R_total_imported = R.identity()
t_total_imported = np.zeros(3,)

t_total_imported_abs = np.zeros(3,)
R_total_imported_abs = R.identity()

# Usage message for the script
message = '''main.py [-h]

             --detector     {SIFT, SURF, KAZE, ORB, BRISK, AKAZE}
             --descriptor   {SIFT, SURF, KAZE, BRIEF, ORB, BRISK, AKAZE, FREAK}
             --matcher      {BF, FLANN}'''

# Create the argument parser
parser = argparse.ArgumentParser(description='Feature Description and Matching.',
                                 usage=message)

# Argument --detector
parser.add_argument('--detector',
                    action='store',
                    choices=['SIFT', 'SURF', 'KAZE', 'ORB', 'BRISK', 'AKAZE'],
                    required=True,
                    metavar='',
                    dest='detector',
                    help='select the detector to be used in this experiment')

# Argument --descriptor
parser.add_argument('--descriptor',
                    action='store',
                    choices=['SIFT', 'SURF', 'KAZE', 'BRIEF', 'ORB', 'BRISK', 'AKAZE', 'FREAK'],
                    required=True,
                    metavar='',
                    dest='descriptor',
                    help='select the descriptor to be used in this experiment')

# Argument --matcher
parser.add_argument('--matcher',
                    action='store',
                    choices=['BF', 'FLANN'],
                    required=True,
                    metavar='',
                    dest='matcher',
                    help='select the matcher to be used in this experiment')

# Execute the parse_args() method to parse the arguments
arguments = parser.parse_args()

# Initialize the selected detector
if arguments.detector == 'SIFT':
    globals.detector = features.SIFT()
elif arguments.detector == 'SURF':
    globals.detector = features.SURF()
elif arguments.detector == 'KAZE':
    globals.detector = features.KAZE()
elif arguments.detector == 'ORB':
    globals.detector = features.ORB()
elif arguments.detector == 'BRISK':
    globals.detector = features.BRISK()
elif arguments.detector == 'AKAZE':
    globals.detector = features.AKAZE()

# Initialize the selected descriptor
if arguments.descriptor == 'SIFT':
    globals.descriptor = features.SIFT()
elif arguments.descriptor == 'SURF':
    globals.descriptor = features.SURF()
elif arguments.descriptor == 'KAZE':
    globals.descriptor = features.KAZE()
elif arguments.descriptor == 'BRIEF':
    globals.descriptor = features.BRIEF()
elif arguments.descriptor == 'ORB':
    globals.descriptor = features.ORB()
elif arguments.descriptor == 'BRISK':
    globals.descriptor = features.BRISK()
elif arguments.descriptor == 'AKAZE':
    globals.descriptor = features.AKAZE()
elif arguments.descriptor == 'FREAK':
    globals.descriptor = features.FREAK()

# Function to read images from a folder
def read_images(image_folder_path):
    # List of image paths in the folder
    image_paths = sorted([os.path.join(image_folder_path, img) for img in os.listdir(image_folder_path) if img.endswith(".png")])

    # List to store the images
    images = []

    # Iterate through the images in the folder
    for image_path in image_paths:
        # Open and convert the image from BGR to GRAYSCALE
        image = cv.imread(filename=image_path, flags=cv.IMREAD_GRAYSCALE)

        # If the image could not be opened or found
        if image is None:
            print(f'\nCould not open or find the image {image_path}.')
            continue

        # Add the image to the list
        images.append(image)

    return images

def compute_differences(array1, array2):
    difference = array1.copy()
    difference[:, 1:] = array1[:, 1:] - array2[:, 1:]
    return difference

def benchmark(times, end_time, traj_difference):
    total_time = end_time - start_time
    fastest_time = min(times)
    slowest_time = max(times)
    average_time = sum(times) / len(times)
    total_images = len(images) - 1
    outputs.save_benchmark(fastest_time, slowest_time, average_time, total_time, total_images, traj_difference, 
                            matcher = arguments.matcher, 
                            detector = arguments.detector,
                            descriptor = arguments.descriptor)
    
# Read the images from the specified folder
images = read_images(image_folder_path)

# Check if any images were read
if not images:
    print('\nNo images were read.')
    exit(0)

# Iterate through the images
for i in tqdm(range(len(images) - 1), desc="Processing images: ", unit=" Images"):
    try:
        # Set the input image and the training image
        image1 = images[i]
        image2 = images[i + 1]

        # Could not open or find the images
        if image1 is None or image2 is None:
            print('\nCould not open or find the images.')
            exit(0)

        image_start_time = time.time()

        # Find the keypoints and compute the descriptors for input image
        globals.keypoints1, globals.descriptors1 = features.features(image1)

        # Find the keypoints and compute the descriptors for training-set image
        globals.keypoints2, globals.descriptors2 = features.features(image2)

        # Match the descriptors between the two images
        output, good_matches, no_matches_found = features.matcher(image1=image1,
                                                                  image2=image2,
                                                                  keypoints1=globals.keypoints1,
                                                                  keypoints2=globals.keypoints2,
                                                                  descriptors1=globals.descriptors1,
                                                                  descriptors2=globals.descriptors2,
                                                                  matcher=arguments.matcher,
                                                                  descriptor=arguments.descriptor)

        # Save the matcher output figure
        # If you want to save the figures, just uncomment the following lines
        save_figures.saveMatcher(output=output,
                                 matcher=arguments.matcher,
                                 descriptor=arguments.descriptor,
                                 image_num=i)
        
        # Save keypoints and descriptors into a file
        # from input image,
        # If you want to save the keypoints and descriptors, just uncomment the following lines
        outputs.saveKeypointsAndDescriptors(keypoints = globals.keypoints1,
        								    descriptors = globals.descriptors1,
                                            matcher = arguments.matcher,
                                            descriptor = arguments.descriptor,
                                            flags = 1,
                                            image_num=i)

        # Save keypoints and descriptors into a file
        # from training-set image
        # If you want to save the keypoints and descriptors, just uncomment the following lines
        outputs.saveKeypointsAndDescriptors(keypoints = globals.keypoints2,
                						    descriptors = globals.descriptors2,
                                            matcher = arguments.matcher,
                                            descriptor = arguments.descriptor,
                                            flags = 2,
                                            image_num=i)

        keypoints1 = globals.keypoints1
        keypoints2 = globals.keypoints2

        # Estimate the pose (rotation and translation) between the two images
        R_est, t_est = visual_odometry.estimate_pose(keypoints1, keypoints2, good_matches, camera_matrix)
        R_total_est = R_est @ R_total_est
        t_total_est = t_total_est + R_total_est @ t_est


        # Stop timer for the current image pair
        image_end_time = time.time()
        times.append(image_end_time - image_start_time)

        t_total_imported_abs, R_total_imported_abs = visual_odometry.normalize_pos_euler(abs_path, i)

        # Copy data into different arrays for further methods
        traj_computed.append([i, t_total_est[0, 0], t_total_est[1, 0], t_total_est[2, 0]])
        traj_computed_total.append([i, t_total_est[0, 0], t_total_est[1, 0], t_total_est[2, 0], R_total_est[0,0], R_total_est[1,0], R_total_est[2,0]])
        traj_computed_relative.append([i, t_est[0, 0], t_est[1, 0], t_est[2, 0], R_est[0, 0], R_est[1, 0], R_est[2, 0] ])

        # Read the relative position and orientation from the imported data
        #t_imported, R_imported = visual_odometry.pos_euler(visual_odometry.read_relative_path(), i)
          
        # Update the total pose for the imported rel data
        #R_total_imported = R_imported * R_total_imported
        #t_total_imported += R_total_imported.apply(t_imported)
    
        # Save the current position for the imported abs data
        #traj_imported.append([i, t_total_imported[0], t_total_imported[1], t_total_imported[2]])
        traj_imported_abs.append([i, t_total_imported_abs[0], t_total_imported_abs[1], t_total_imported_abs[2]])
        
    except visual_odometry.NoMatchesError:
        # If no matches are found, plot the trajectories and exit

        # Benchmarking
        end_time = time.time()

        # Convert the trajectories to numpy arrays
        traj_computed = np.array(traj_computed)
        print(traj_computed)
        traj_computed_total = np.array(traj_computed_total)
        #traj_computed_relative = np.array(traj_computed_relative)
        #traj_imported = np.array(traj_imported)
        traj_imported_abs = np.array(traj_imported_abs)
        traj_difference = compute_differences(traj_computed, traj_imported_abs)
        traj_difference = np.array(traj_difference)

        benchmark(times, end_time, traj_difference)
        
        outputs.save_traj_computed(traj_computed_total, traj_computed_relative, traj_difference, 
                                   matcher = arguments.matcher, 
                                   detector = arguments.detector,
                                   descriptor = arguments.descriptor)

        save_figures.plot_movement_and_rotation(traj_computed, traj_imported_abs, traj_difference)
        sys.exit()


# Benchmarking
end_time = time.time()

# Convert the trajectories to numpy arrays
traj_computed = np.array(traj_computed)
traj_computed_total = np.array(traj_computed_total)
#traj_computed_relative = np.array(traj_computed_relative)
#traj_imported = np.array(traj_imported)
traj_imported_abs = np.array(traj_imported_abs)
traj_difference = compute_differences(traj_computed, traj_imported_abs)
traj_difference = np.array(traj_difference)
benchmark(times, end_time, traj_difference)

outputs.save_traj_computed(traj_computed_total, traj_computed_relative, traj_difference, 
                           matcher = arguments.matcher, 
                           detector = arguments.detector,
                           descriptor = arguments.descriptor)

# Plot the movement and rotation trajectories
save_figures.plot_movement_and_rotation(traj_computed, traj_imported_abs, traj_difference)