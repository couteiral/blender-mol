import bpy
import math
import mathutils
import sys
import mendeleev

def getIRC(filename, a):

	pointer = open(filename, "r+")
	data = pointer.readlines()
	
	IRC = []
	amount = math.ceil(len(data) / a)
	for i in range(amount):

		coords = []
		for j in range(a-1):

			line = data[a*i + j + 1]
			coords.append([line.split()[0], float(line.split()[1]), float(line.split()[2]), float(line.split()[3])])

		IRC.append([i+1, coords])

	return IRC

def initMaterials():

	path = "Materials.blend"
	
	with bpy.data.libraries.load(path) as (data_from, data_to):
		data_to.materials = data_from.materials

	Hydrogen = bpy.data.materials['Hydrogen']
	Nitrogen = bpy.data.materials['Nitrogen']
	Carbon = bpy.data.materials['Carbon']
	Metal = bpy.data.materials['Metal']
	Materials = [Hydrogen, Carbon, Nitrogen, Metal]

	return Materials

def getMaterial(element, Materials):

	if (element == "H"):
		mat = Materials[0]

	elif (element == "C"):
		mat = Materials[1]

	elif (element == "N"):
		mat = Materials[2]

	else:
		
		mat = Materials[1]	

	return mat

def rotateCyl(Bond, o1, o2, prevdist):

	dx = o2.location[0] - o1.location[0]
	dy = o2.location[1] - o1.location[1]
	dz = o2.location[2] - o1.location[2]
	dist = math.sqrt(dx**2 + dy**2 + dz**2)
	bpy.ops.object.select_all(action='DESELECT')
	Bond.select = True

	Bond.location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)

	theta = math.atan2(dy, dx)
	phi = math.acos(dz/dist)

	x = math.cos(phi/2)*math.cos(theta/2)
	y = -math.sin(phi/2)*math.sin(theta/2)
	z = math.sin(phi/2)*math.cos(theta/2)
	w = math.cos(phi/2)*math.sin(theta/2)

	Bond.rotation_quaternion = (x, y, z, w)
	Bond.scale[2] = dist/prevdist 

	return Bond	
