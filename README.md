# Blender Batch Camera Rendering 
## This addon will 
###  Let you batch-render objects 
###  Addon work with collections 

# Addon must work in this order: 

-1 User selects a collection to be batch rendered: 

-2 User pressing button "Set up camera":

-3 User pressing button "Start Batch Render" then:

-4 addon hides viewport and renders visibility for objects in selected earlier collection: 

-5 addon creates an empty and camera parented to empty:  

-6 addon makes the created camera an active camera:

-7 camera empty location must be transformed for the location of the first object in the collection:

-8 Start blender render:

-9 On the blender render end change the empty location for the next object in the collection:

-10 Start blender render: 

-11 addon will repeat 9 and 10 until the end of collection;
