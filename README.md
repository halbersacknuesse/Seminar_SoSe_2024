# Seminar_SoSe_2024

## Content

- Python tool for feature detection and matching and pose estimation
- Paper
- Presentation

### Python Tool

This tool uses a depth or flexion image sequence to estimate the poses of image pairs to estimate the path treaded in the sequence

#### Inputs

- place image sequence in 'Dataset/InputImages' (remove file 'place depth images here' before use)
- place the ground truth with Euler angles in 'Dataset/CameraPose'
  - examples given in the folder
- place camera intrinsic matrix in 'Dataset/Intrinsic'
  - example given in the folder
  - further information can be found in [this repo](https://github.com/TUBAF-IFI-VR/Projektseminar22-23)
- Example data set is provided in 'Dataset/blender_test_data/blender_testmap'

#### Execution

Run a terminal with the following commands:

`pip install -r requirements.txt`

to install the dependencies.

To run the program:

`python main.py --detector DETECTOR --descriptor DESCRIPTOR --matcher MATCHER`

Choose your preferred parameters. Help is given with the following command:
`python main.py --help`



#### Remark #1

The program was written under Linux. Accordingly, some paths were integrated directly into the program. These have the typical path structure used under Linux. An adjustment is necessary if the program is to be started under Windows.

#### Outputs

The program creates the necessary folders (if not already existent). The output consists of the following:

- Benchmark:
  - durations for processing
  - accuracy
- Figures:
  - visualization of the matchings between consecutive image pairs of the image sequence
- Keypoints and Descriptors:
  - keypoints of each image in '.txt'-format
  - descriptors of each image in '.txt'-format
- Trajectory:
  - computed trajectory of the ground truth, the estimation and the difference between both
- Plot:
  - the 'InteractivePlot.html' contains an interactive 3D visualization of all the trajectory.

#### Remark #2

The framework of the tool was taken from [this](https://github.com/whoisraibolt/Feature-Detection-and-Matching.git) GitHub-Repo. The original README.md can be found under 'README_from_Repo.md' in the main folder of the program.

### Paper

This folder contains all the source files for LATEX and the rendered 'paper.pdf'. It is written according to a template given by Robert Lösch via OPAL (access restricted for public). It follows the IEEE-standard.

### Presentation

This folder contains a handout ('handout.pdf') and the 'presentation.md'. The 'presentation.md'-file is written in markdown with specific syntax for use with LiaScript. The Link to the renderer can be found on the first page of the file ('course on LiaScript').
