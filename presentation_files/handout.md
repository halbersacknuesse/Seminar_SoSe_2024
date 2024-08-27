## Comparison of feature-based pose estimation and localization methods in dark environments

Lecturer: Jonas Fleicher 
Date: 06-04-2024

#### What is it about?

- Area in computer vision
- Deals with the prediction and reconstruction of the pose (describes the position and orientation of an object in space) of an object/ subject in $ \mathbb{R}^3 $.
<center><img src="assets/Matches.png" alt="Matchings_Features" title="{1}{Matchings based on features in an image sequence[^1]}" style="zoom:50%;" /></center>
#### Importance
- can be used:
  - to determine the **pose** of **object(s)** in space
  - to determine your **own position/ orientation** in space
  - for **SLAM** in conjunction with autonomous vehicles/ robots
  - for orientation and navigation in areas where navigation with **GNSS** alone is not sufficient (-> accuracy, availability)
- Possibility to fuse sensors and methodologies
=> **Environment Detection and Awareness**

#### Approaches
```mermaid
graph LR
    A[1. Data Capture] --> B[2. Pre-Processing]
    B --> C[3. Model Selection and Application]
    C --> D[4. Feature Extraction]
    D --> E[5. Pose Estimation]
	E --> F[6. Action]
	F --> A
```

#### Discussion
##### Requirements for SLAM
- Accuracy of pose estimation
- Processing speed/ Performance
- Reliability/ Robustness
##### Ideal Scenario
Sensor and Model **Fusion**
- Redundancy
- Complementarity
##### 3D Depth Images
- Radar
- ToF
- LiDAR
- Structured Light Sensor
#### Comparison
##### Criteria/ Metrics
- Performance
- Robustness/ Accuracy
- Simplicity of Implementation
##### Potential problems
- Procurement of different sensors (cost, time)
- Use of the approaches to be investigated may require adaptation/ self-implementation 
- Availability of the necessary software/ hardware not necessarily given 
- Testing only possible with given hardware & softwareware
#### Procedure
1. Selection/ creation of a test scenario

     - only synthetic
     - e.g. path in a Blender scene
2. Selection of considered selected models

     - Restriction to approaches that can recognize general features in the data 
     - Avoidance of own implementations (time, scope)
3. Application of selected models to the data from the test scenario
4. Measurement of processing times for the scenario
5. Measuring the deviation of the estimation from the absolute position
6. Extension of the comparison by pre-processing the depth data

     - Flexion images

     - Bearing-Angel images

#### Appendix
##### Flexion Images
- Input: depth image
  - Depth image has to be in specific format (-> camera intrinsic)
- Calculating Flexion:
  - Angle between normals $\vec{n_1}$ and $\vec{n_2}$ of (horizontal and vertical) neighbors and diagonal neighbors
  - Consideration: nearest or next-neighbor

<center><img src="assets/flexion_toth_2.png" alt="Toth" title="{1}{The estimated normals span an angle depending on the local shape of the measured surface.[^12]}" style="zoom:50%;" /></center>


##### (Multi-Directional) Bearing-Angle Images
- Input: depth image 
  - Depth image has to be in specific format (-> camera intrinsic)
- Calculation Bearing-Angle:
  - Angle between two neighboring pixels ($\beta$ and $\gamma$)
  - 0 $\le$ **angle** $\le$ $\pi$
  - Angle represents color in resulting image
- Problem:
  - Rotation invariance not given for BA images
  - Rotation invariance given for MDBA images
  - MDBA images contain only outlines of objects
<center><img src="assets/Toth_MDBA.jpg" alt="Toth" title="{1}{Schematic representation of the Multi-Directional Bearing-Angle image. The Multi-Directional Bearing-Angle image composes two Bearing-Angles in vertical, horizontal, diagonal and anti-diagonal direction. The maximum angle is then selected as pixel value[^12]}" style="zoom:50%;" /></center>
