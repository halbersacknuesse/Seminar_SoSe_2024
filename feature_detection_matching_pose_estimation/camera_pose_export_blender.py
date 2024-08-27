import bpy
import os
import mathutils

# Name der Kamera
camera_name = "Camera"

# Pfad zur Ausgabedatei relativ zur .blend-Datei
blend_file_path = bpy.data.filepath
project_dir = os.path.dirname(blend_file_path)
output_dir = os.path.join(project_dir, "camera_pose")

# Sicherstellen, dass der Ordner existiert
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Ordner '{output_dir}' erstellt.")

# Dateinamen
output_file_euler = os.path.join(output_dir, "camera_pose_euler.txt")
output_file_quat = os.path.join(output_dir, "camera_pose_quat.txt")
output_file_relative_euler = os.path.join(output_dir, "relative_pose_euler.txt")
output_file_relative_quat = os.path.join(output_dir, "relative_pose_quat.txt")

# Kamera-Objekt holen
camera = bpy.data.objects.get(camera_name)
if camera is None:
    print(f"Kamera '{camera_name}' nicht gefunden.")
else:
    print(f"Kamera '{camera_name}' gefunden.")

# Sicherstellen, dass die Dateien existieren
for file in [output_file_euler, output_file_quat, output_file_relative_euler, output_file_relative_quat]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write("")
        print(f"Datei '{file}' erstellt.")

# Keyframes durchlaufen und Pose speichern
previous_position = None
previous_rotation_euler = None
previous_rotation_quat = None

with open(output_file_euler, 'a') as f_euler, open(output_file_quat, 'a') as f_quat, open(output_file_relative_euler, 'a') as f_rel_euler, open(output_file_relative_quat, 'a') as f_rel_quat:
    for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
        bpy.context.scene.frame_set(frame)
        
        # Position und Rotation der Kamera holen
        position = camera.location
        rotation_euler = camera.rotation_euler
        rotation_quat = camera.rotation_quaternion
        
        # Pose in das gewünschte Format bringen
        position_str = f"{position.x:.4f} {position.y:.4f} {position.z:.4f}"
        rotation_euler_str = f"{rotation_euler.x:.4f} {rotation_euler.y:.4f} {rotation_euler.z:.4f}"
        rotation_quat_str = f"{rotation_quat.x:.4f} {rotation_quat.y:.4f} {rotation_quat.z:.4f} {rotation_quat.w:.4f}"
        
        # Absolute Posen speichern
        f_euler.write(f"{frame} {position_str} {rotation_euler_str}\n")
        f_quat.write(f"{frame} {position_str} {rotation_quat_str}\n")
        
        # Relative Posen berechnen und speichern
        if previous_position is not None and previous_rotation_euler is not None and previous_rotation_quat is not None:
            relative_position = position - previous_position
            relative_rotation_euler = mathutils.Vector((rotation_euler.x, rotation_euler.y, rotation_euler.z)) - mathutils.Vector((previous_rotation_euler.x, previous_rotation_euler.y, previous_rotation_euler.z))
            relative_rotation_quat = rotation_quat @ previous_rotation_quat.inverted()
            
            relative_position_str = f"{relative_position.x:.4f} {relative_position.y:.4f} {relative_position.z:.4f}"
            relative_rotation_euler_str = f"{relative_rotation_euler.x:.4f} {relative_rotation_euler.y:.4f} {relative_rotation_euler.z:.4f}"
            relative_rotation_quat_str = f"{relative_rotation_quat.x:.4f} {relative_rotation_quat.y:.4f} {relative_rotation_quat.z:.4f} {relative_rotation_quat.w:.4f}"
            
            f_rel_euler.write(f"{frame} {relative_position_str} {relative_rotation_euler_str}\n")
            f_rel_quat.write(f"{frame} {relative_position_str} {relative_rotation_quat_str}\n")
        
        # Aktuelle Position und Rotation speichern
        previous_position = position.copy()
        previous_rotation_euler = rotation_euler.copy()
        previous_rotation_quat = rotation_quat.copy()
        
        print(f"Frame {frame}: Position: {position_str}, Rotation Euler: {rotation_euler_str}, Rotation Quat: {rotation_quat_str}")

print(f"Alle Dateien wurden erfolgreich im Ordner '{output_dir}' erstellt und gespeichert.")
