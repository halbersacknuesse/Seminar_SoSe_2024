# Kamera Pose Ausgabeformate

## 1. camera_pose_euler.txt

Muster: 

```
Frame frame: Position: <Vector (x, y, z)>, Rotation: <Euler (x= , y= , z= ), order='XYZ'>
```

Beispiel: 

```
Frame 0: Position: <Vector (-84.9387, -18.4300, 3.3100)>, Rotation: <Euler (x=1.5708, y=0.0000, z=-6.2832), order='XYZ'>
```

## 2. camera_pose_quat.txt

Muster: 

```
Frame frame: Position: <Vector (x, y, z)>, Rotation: <Quaternion (x= , y= , z= , w= )>
```

Beispiel: 

```
Frame 0: Position: <Vector (-84.9387, -18.4300, 3.3100)>, Rotation: <Quaternion (x=0.0000, y=0.0000, z=0.0000, w=1.0000)>
```

## 3. relative_pose_euler.txt

Muster: 

```
Frame frame: Relative Position: <Vector (x, y, z)>, Relative Rotation: <Euler (x= , y= , z= ), order='XYZ'>
```

Beispiel: 

```
Frame 1: Relative Position: <Vector (0.0000, 0.0000, 0.0000)>, Relative Rotation: <Euler (x=0.0000, y=0.0000, z=0.0000), order='XYZ'>
```
## 4. relative_pose_quat.txt

Muster:

```
Frame frame: Relative Position: <Vector (x, y, z)>, Relative Rotation: <Quaternion (x= , y= , z= , w= )>
```

Beispiel:

```
Frame 1: Relative Position: <Vector (0.0000, 0.0000, 0.0000)>, Relative Rotation: <Quaternion (x=0.0000, y=0.0000, z=0.0000, w=1.0000)
```

