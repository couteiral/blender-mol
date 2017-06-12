import bpy
import math
import mathutils
import sys
import mendeleev
import functions

def initialize():
	
	bpy.ops.object.select_by_type(type='MESH')
	bpy.ops.object.delete()
	bpy.context.scene.frame_start = 0
	bpy.context.scene.frame_end = len(IRC)*4
	Materials = initMaterials()
	
	return None

def drawAtoms(coords):
	
	Atoms = [] # List of atoms
	k = 0
	for atom in coords:

		k = k + 1 # Atom number
		(el, pos) = (atom[0], (atom[1], atom[2], atom[3])) # Coordinates
		name = el + str(k) # Identification
		rad = (mendeleev.element(el).covalent_radius_slater)/150 # Radius
		mat = getMaterial(el, Materials) # Material
		# Add sphere
		bpy.ops.mesh.primitive_uv_sphere_add(segments=200, ring_count=20, size=rad, location=pos, calc_uvs=True)
		Atoms.append(bpy.context.active_object)
		for i in range(len(bpy.context.active_object.data.polygons)):
			bpy.context.active_object.data.polygons[i].use_smooth = True
		bpy.context.active_object.name = name
		bpy.context.active_object.data.materials.append(mat)

	return Atoms

# Draw bonds
def drawBonds(coords):
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
			
		return Bonds, Bondslength


