import bpy
import math
import mathutils
import sys
import mendeleev
import draw
import irc
import functions

def plotMolecule(Molecule, output):
  
  draw.initialize()
  draw.drawAtoms(Molecule)
  draw.drawBonds(Molecule)
  bpy.ops.wm.save_as_mainfile(output)
  
  return None

# Plot a molecule
HCN = functions.getMolecule('molecule.dat', 3)
plotMolecule(HCN, 'molecule.blend')
