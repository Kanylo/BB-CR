# Blender Batch Camera Rendering 
## This addon will 
###  Let you batch render files from multiple angles 
###  Addon will set your camera empty to object origin
###  Addon can work with collections 

# Addon must work in this order: 

-1 User select collection to be batch rendered: 

-2 User pressing button "Set up camera":

-3 User pressing button "Start Batch Render" then:

-4 addon must hide viewport and render visibility for objects in selected earlier collection: 

-5 addon must create an empty and camera parented to empty:  

-6 addon must make created camera as active camera:

-7 camera empty location must be transformed for location of first object in collection:

-8 Start blender render:

-9 When blender render is ended change empty location for next object in collection:

-10 Start blender render: 

-11 repeat 9 and 10 until end of collection;
