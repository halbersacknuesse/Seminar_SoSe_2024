#!/usr/bin/env python
# coding: utf-8

# Imports
import sys
import globals
import cv2 as cv
import numpy as np
import csv
from scipy.spatial.transform import Rotation as R

# Custom exception for no matches found
class NoMatchesError(Exception):
    pass

# Paths
intrinsic_path = globals.intrinsic_path
imported_pose_relative_path = globals.imported_pose_relative_path
imported_pose_absolute_path = globals.imported_pose_absolute_path

# Define the correction angles in degrees
correction_angles = [0, 0, 0]  # [x, y, z] in degrees

# Convert correction angles to radians
correction_angles_rad = np.radians(correction_angles)

# Create the correction rotation matrix
correction_rotation = R.from_euler('xyz', correction_angles_rad)

# Function to read intrinsic parameters from a file
def read_intrinsic():
    try:
        intrinsic = np.loadtxt(intrinsic_path, dtype=float)
        if intrinsic.size == 0:
            raise ValueError("File is empty or does not contain a matrix.")
        elif intrinsic.shape != (4, 3):
            raise ValueError("intrinsic.txt does not contain a 3x4 matrix")
        return intrinsic

    except IOError:
        print("Intrinsic File not found.")
        sys.exit()
    except ValueError as e:
        print(e)
        sys.exit()
    except:
        print("An unknown error occurred, exiting the program")
        sys.exit()

# Function to create a camera matrix from intrinsic parameters
def create_camera_matrix(intrinsic):
    fx = fy = intrinsic[1, 0]
    cx = cy = intrinsic[1, 2]
    cameraMatrix = np.array([[fx, 0, cx],
                             [0, fy, cy],
                             [0, 0, 1]])
    return cameraMatrix

# Function to estimate the pose (rotation and translation) between two sets of keypoints
def estimate_pose(keypoints1, keypoints2, matches, camera_matrix):
    # Extract corresponding points
    pts1 = np.float32([keypoints1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([keypoints2[m.trainIdx].pt for m in matches])
    
    # Compute the Essential Matrix
    E, mask = cv.findEssentialMat(pts1, pts2, camera_matrix)
    if E is None:
        print("Essential matrix could not be computed. Return 0-matrices")
        R = np.eye(3)
        t = np.zeros((3, 1))
        return R, t
    rows, cols = (np.array(E)).shape
    if rows % 3 != 0:
        raise NoMatchesError("Error: The number of rows of the essential matrix is not a multiple of 3.")
    
    elif rows == 3:
        try:
            pts1 = pts1[mask.ravel() == 1]
            pts2 = pts2[mask.ravel() == 1]
        except:
            print('\n ERROR: No matches possible')
            R_corrected = np.eye(3)
            t_corrected = np.zeros((3, 1))
            raise NoMatchesError
        
        _, R, t, mask = cv.recoverPose(E, pts1, pts2, camera_matrix)
    else:
        # Compute the arithmetic mean of the corresponding rows
        E_3x3 = np.zeros((3, 3))
        for i in range(3):
            E_3x3[i, :] = np.mean(E[i::3, :], axis=0)
        _, R, t, mask = cv.recoverPose(E_3x3, pts1, pts2, camera_matrix)
        print("arithmetic mean of essential matrix is used!")
    
    # Apply the correction rotation
    R_corrected = correction_rotation.as_matrix() @ R
    
    # Apply the correction to the translation
    t_corrected = correction_rotation.apply(t.ravel())
    
    # Reshape t_corrected to match the format of t
    t_corrected = t_corrected.reshape(3, 1)
    return R_corrected, t_corrected


# Functions to read the paths from the files
def read_relative_path():
    with open(imported_pose_relative_path, 'r') as f:
        lines = list(csv.reader(f, delimiter=' '))
    return lines

def read_absolute_path():
    with open(imported_pose_absolute_path, 'r') as f:
        lines = list(csv.reader(f, delimiter=' '))
    return lines

# Function to convert the position and orientation from Euler angles in two arrays
def pos_euler(lines, i):
    line = lines[i]
    x = float(line[1])
    y = float(line[2])
    z = float(line[3])
    rot_x = float(line[4])
    rot_y = float(line[5])
    rot_z = float(line[6])

    t_total_imported = np.array([x, y, z])
    R_total_imported = R.from_euler('xyz', [rot_x, rot_y, rot_z])

    return t_total_imported, R_total_imported

# Function to normalize the path
def normalize_pos_euler(lines, i):
    line = lines[i]
    x = float(line[1])
    y = -float(line[3])
    z = -float(line[2])
    rot_x = float(line[4])
    rot_y = -float(line[6])
    rot_z = -float(line[5])
    initial_line = lines[0]
    initial_x = float(initial_line[1])
    initial_y = -float(initial_line[3])
    initial_z = -float(initial_line[2])
    initial_rot_x = float(initial_line[4])
    initial_rot_y = -float(initial_line[6])
    initial_rot_z = -float(initial_line[5])
    
    t_total_imported_normalized = np.array([x - initial_x, y - initial_y, z - initial_z])
    R_total_imported_normalized = R.from_euler('xyz', [rot_x - initial_rot_x, rot_y - initial_rot_y, rot_z - initial_rot_z])

    return t_total_imported_normalized, R_total_imported_normalized