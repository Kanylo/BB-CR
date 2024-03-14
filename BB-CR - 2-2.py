import bpy
import os
from mathutils import Vector

# Function to check the existence of objects
def check_objects(names):
    for name in names:
        if not bpy.data.objects.get(name):
            return False
    return True

# Add-on information
bl_info = {
    "name": "Batch Camera Rendering",
    "author": "Kanylo n52",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > My Tab",
    "description": "Batch render objects with a camera empty set to each object's origin",
    "category": "3D View",
}

# Operator for batch rendering
class BatchRenderOperator(bpy.types.Operator):
    bl_idname = "render.batch_render"
    bl_label = "Start Batch Render"

    def execute(self, context):
        # Check the existence of necessary objects
        if not check_objects(['Empty', 'Camera']):
            self.report({'ERROR'}, "Camera setup not found.")
            return {'CANCELLED'}

        # Check the output directory
        base_output_dir = context.scene.render.filepath
        if not os.path.isdir(base_output_dir) or not os.access(base_output_dir, os.W_OK):
            self.report({'ERROR'}, "Output directory not found or not writable.")
            return {'CANCELLED'}

        # Save the original visibility of objects
        original_visibility = dict((obj, obj.hide_viewport) for obj in bpy.data.objects)

        # Render each object in the collection
        for i, obj in enumerate(context.scene.batch_render_collection.objects):
            # Hide all other objects
            for other_obj in bpy.data.objects:
                other_obj.hide_viewport = other_obj != obj

            # Calculate the object's bounding box center
            bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
            global_bbox_center = obj.matrix_world @ bbox_center

            # Set the empty object to the object's bounding box center
            bpy.data.objects['Empty'].location = global_bbox_center

            # Set the output file path
            context.scene.render.filepath = f"{base_output_dir}/output/{obj.name}"

            # Render the scene
            try:
                bpy.ops.render.render(write_still=True)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to render the scene: {str(e)}")
                return {'CANCELLED'}

            # Report the render progress
            self.report({'INFO'}, f"Render progress: {i+1}/{len(context.scene.batch_render_collection.objects)}")

        # Restore the original output file path and visibility of objects
        context.scene.render.filepath = base_output_dir
        for obj, visibility in original_visibility.items():
            obj.hide_viewport = visibility

        return {'FINISHED'}

# Operator for setting up the camera
class SetupCameraOperator(bpy.types.Operator):
    bl_idname = "render.setup_camera"
    bl_label = "Set up camera"

    def execute(self, context):
        # Remove the existing camera setup collection if it exists
        camera_setup_collection = bpy.data.collections.get('Camera Setup')
        if camera_setup_collection:
            for obj in camera_setup_collection.objects:
                bpy.context.scene.collection.objects.unlink(obj)
                bpy.data.objects.remove(obj)
            bpy.data.collections.remove(camera_setup_collection)

        # Create a new camera setup collection
        camera_setup_collection = bpy.data.collections.new('Camera Setup')
        bpy.context.scene.collection.children.link(camera_setup_collection)

        # Add an empty object and a camera object to the scene
        bpy.ops.object.empty_add(location=(0, 0, 0))
        empty = bpy.context.object
        bpy.ops.object.camera_add(location=(0, -20, 0))
        camera = bpy.context.object

        # Parent the camera to the empty object
        camera.parent = empty

        # Link the empty object and the camera to the camera setup collection
        camera_setup_collection.objects.link(empty)
        camera_setup_collection.objects.link(camera)

        # Unlink the empty object and the camera from the scene collection
        bpy.context.scene.collection.objects.unlink(empty)
        bpy.context.scene.collection.objects.unlink(camera)

        # Add a 'TRACK_TO' constraint to the camera
        constraint = camera.constraints.new('TRACK_TO')
        constraint.target = empty
        constraint.up_axis = 'UP_Y'
        constraint.track_axis = 'TRACK_NEGATIVE_Z'

        return {'FINISHED'}

# Panel for batch rendering
class BatchRenderPanel(bpy.types.Panel):
    bl_label = "Batch Render"
    bl_idname = "OBJECT_PT_batch_render"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Batch Render"

    def draw(self, context):
        layout = self.layout

        # Draw the collection property
        row = layout.row()
        row.prop(context.scene, "batch_render_collection")

        # Draw the output directory property
        row = layout.row()
        row.prop(context.scene.render, "filepath")

        # Draw the image file format property
        row = layout.row()
        row.prop(context.scene.render.image_settings, "file_format")

        # Draw the 'Set up camera' operator button
        row = layout.row()
        row.operator("render.setup_camera")

        # Draw the 'Start Batch Render' operator button
        row = layout.row()
        row.operator("render.batch_render")

# Register the operators and the panel
def register():
    bpy.utils.register_class(BatchRenderOperator)
    bpy.utils.register_class(SetupCameraOperator)
    bpy.utils.register_class(BatchRenderPanel)
    bpy.types.Scene.batch_render_collection = bpy.props.PointerProperty(type=bpy.types.Collection)

# Unregister the operators and the panel
def unregister():
    bpy.utils.unregister_class(BatchRenderOperator)
    bpy.utils.unregister_class(SetupCameraOperator)
    bpy.utils.unregister_class(BatchRenderPanel)
    del bpy.types.Scene.batch_render_collection

# Run the register function if the script is run directly
if __name__ == "__main__":
    register()
