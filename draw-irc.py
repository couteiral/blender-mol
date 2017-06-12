import bpy
import math
import mathutils
import sys
import mendeleev
import functions

### STEP 1: Initializaton

# Get the IRC data
IRC = getIRC(filename + ".xyz", a)
#IRC = getIRC("IRC.allxyz")
print(IRC)

# Initialize the scene
bpy.ops.object.select_by_type(type='MESH') # Select cube
bpy.ops.object.delete() # Delete cube
bpy.context.scene.frame_start = 0 # Initial frame
bpy.context.scene.frame_end = len(IRC)*4 # Final frame
Materials = initMaterials() # Initialize materials

# Get coordinates of first frame
coords = IRC[0][1]

# Draw atoms
Atoms = [] # List of atoms
k = 0

for atom in coords:

	# Atom data
	k = k + 1 # Atom number
	(el, pos) = (atom[0], (atom[1], atom[2], atom[3])) # Coordinates
	name = el + str(k) # Identification
	rad = (mendeleev.element(el).covalent_radius_slater)/150 # Radius
	mat = getMaterial(el, Materials) # Material

	# Add sphere
	bpy.ops.mesh.primitive_uv_sphere_add(segments=200, ring_count=20, size=rad, location=pos, calc_uvs=True)
	Atoms.append(bpy.context.active_object)

	# Flatten sphere
	for i in range(len(bpy.context.active_object.data.polygons)):
		bpy.context.active_object.data.polygons[i].use_smooth = True

	# Rename sphere
	bpy.context.active_object.name = name

	# Apply material to sphere
	bpy.context.active_object.data.materials.append(mat)


# Draw bonds
Bonds = []
Bondslength = []
for i in range(0, len(coords)):

	for j in range(i+1, len(coords)):

		# Security check
		if (i == j):
			continue

		# Get pairs coordinates
		(el1, x1, y1, z1) = (mendeleev.element(coords[i][0]), coords[i][1], coords[i][2], coords[i][3])
		(el2, x2, y2, z2) = (mendeleev.element(coords[j][0]), coords[j][1], coords[j][2], coords[j][3])
		name = coords[i][0] + str(i) + "-" + coords[j][0] + str(j) # Bond ID 
		dist = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) # Interatomic distance
		vdW = (el1.vdw_radius_bondi + el2.vdw_radius_bondi)/200 # van der Waals radii sum
		loc = ((x2-x1)/2 + x1, (y2-y1)/2 + y2, (z2-z1)/2 + z2)

		# Generate a bond (even if it doesn't exist)
		bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=dist, location=loc) 
		Bond = bpy.context.active_object
		Bond.rotation_mode = 'QUATERNION'
		Bond.data.materials.append(Materials[3])
		rotateCyl(Bond, Atoms[i], Atoms[j], dist)
	
		# Check if the bond will be visible
		if (dist > vdW):

			Bond.hide_render = True
			Bond.hide = True

		Bonds.append(Bond)
		Bondslength.append(dist)

# Generate first keyframe	
for Atom in Atoms:

	Atom.keyframe_insert(data_path='location')

for Bond in Bonds:

	Bond.keyframe_insert(data_path='location')
	Bond.keyframe_insert(data_path='rotation_quaternion')
	Bond.keyframe_insert(data_path='scale')
	Bond.keyframe_insert(data_path='hide_render')
	Bond.keyframe_insert(data_path='hide')

### STEP 2: Update each frame
for step in IRC:

	# Do not repeat for the first frame
	if (step[0] == 1):
		continue

	# Set current frame
	bpy.context.scene.frame_set(step[0]*4)

	# Reduce to coordinates
	step = step[1]

	# Index for the atom
	k = 0

	# Move all atoms
	for Atom in Atoms:

		Atom.location = mathutils.Vector((step[k][1], step[k][2], step[k][3]))
		k += 1

	# Index for the bond array
	k = 0

	for i in range(0, len(step)):

		for j in range(i+1, len(step)):

			# Security check
			if (i == j):
				continue

			# Get pairs coordinates
			(el1, x1, y1, z1) = (mendeleev.element(step[i][0]), step[i][1], step[i][2], step[i][3])
			(el2, x2, y2, z2) = (mendeleev.element(step[j][0]), step[j][1], step[j][2], step[j][3])
			name = step[i][0] + str(i) + "-" + step[j][0] + str(j) # Bond ID 
			dist = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) # Interatomic distance
			vdW = (el1.vdw_radius_bondi + el2.vdw_radius_bondi)/200 # van der Waals radii sum

			# Take corresponding bond
			Bond = Bonds[k]
			rotateCyl(Bond, Atoms[i], Atoms[j], Bondslength[k])
			k += 1 # Increase index

			if (dist < vdW):

				Bond.hide_render = False
				Bond.hide = False

			else:

				Bond.hide_render = True
				Bond.hide = True

	# Insert keyframes

	for Atom in Atoms:

		Atom.keyframe_insert(data_path='location')

	for Bond in Bonds:

		Bond.keyframe_insert(data_path='location')
		Bond.keyframe_insert(data_path='rotation_quaternion')
		Bond.keyframe_insert(data_path='scale')
		Bond.keyframe_insert(data_path='hide_render')
		Bond.keyframe_insert(data_path='hide')

### STEP 3: Generate final file

#bpy.ops.wm.save_as_mainfile(filename + '.blend')
