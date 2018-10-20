import os
import csv
import math

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, FloatProperty

bl_info = {
    "name": "Export > Drone Swarm animation Export(.csv)",
    "author": "Dmitry Shorokhov",
    "version": (2, 5, 1),
    "blender": (2, 6, 3),
    "api": 36079,
    "location": "File > Export > Drone Swarm animation Export(.csv)",
    "description": "Export > Drone Swarm animation Export(.csv)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}


class ExportCsv(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.folder"
    bl_label = "Export"
    filename_ext = ''
    use_filter_folder = True

    filepath = StringProperty(
        name="File Path",
        description="File path used for exporting csv files",
        maxlen=1024,
        subtype='DIR_PATH',
        default=""
    )

    def execute(self, context):
        save_chan(context, self.filepath)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(
        ExportCsv.bl_idname,
        text="Drone Swarm Exporter (.csv)"
    )


def register():
    bpy.utils.register_class(ExportCsv)
    bpy.types.INFO_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ExportCsv)
    bpy.types.INFO_MT_file_export.remove(menu_func)


def calc_speed(start_point, end_point):
    time_delta = 0.1
    distance = math.sqrt(
        (start_point[0] - end_point[0]) ** 2 +
        (start_point[1] - end_point[1]) ** 2 +
        (start_point[2] - end_point[2]) ** 2
    )
    return distance / time_delta


def save_chan(context, folder_path):
    scene = context.scene
    objects = []
    for obj in context.visible_objects:
        if 'drone' in obj.name.lower():
            objects.append(obj)

    frame_start = scene.frame_start
    frame_end = scene.frame_end

    drone_number = 1
    for obj in objects:
        with open(
            os.path.join(folder_path, 'drone{}.csv'.format(drone_number)), 'w'
        ) as csv_file:
            animation_file_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
            )

            prev_x, prev_y, prev_z = 0, 0, 0
            for frame in range(frame_start, frame_end + 1, 1):
                row = [
                    str(frame),
                ]
                if len(obj.data.materials) == 1:
                    material = obj.data.materials[0]
                else:
                    # TODO: choose material by name
                    material = obj.data.materials[0]
                print(dir(material))
                scene.frame_set(frame)
                mat = obj.matrix_world.copy()
                t = mat.to_translation()
                x, y, z = t[:]
                row += [x, y, z]
                speed = calc_speed(
                    (x, y, z),
                    (prev_x, prev_y, prev_z)
                ) if frame != frame_start else 1
                prev_x, prev_y, prev_z = x, y, z
                row.append(speed)
                rgb = []
                for u in range(3):
                    rgb.append(
                        int(material.diffuse_color[u] * 255)
                    )
                row += rgb
                animation_file_writer.writerow(row)
        drone_number += 1
    return {'FINISHED'}


if __name__ == "__main__":
    register()
