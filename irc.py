def generateKeyframes(Atoms, Bonds):

	for Atom in Atoms:
		Atom.keyframe_insert(data_path='location')

	for Bond in Bonds:
		Bond.keyframe_insert(data_path='location')
		Bond.keyframe_insert(data_path='rotation_quaternion')
		Bond.keyframe_insert(data_path='scale')
		Bond.keyframe_insert(data_path='hide_render')
		Bond.keyframe_insert(data_path='hide')

	return
		
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
