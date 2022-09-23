import ctypes
import os
import pymesh
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
from matplotlib import cm

from pyglet.gl import *
from pywavefront import visualization, Wavefront

import plotly

#########################################################################################
#                                                                                       #
#   .d8888b.                                              888    d8b                    #
#  d88P  Y88b                                             888    Y8P                    #
#  888    888                                             888                           #
#  888         .d88b.  88888b.   .d88b.  888d888  8888b.  888888 888  .d88b.  88888b.   #
#  888  88888 d8P  Y8b 888 "88b d8P  Y8b 888P"       "88b 888    888 d88""88b 888 "88b  #
#  888    888 88888888 888  888 88888888 888     .d888888 888    888 888  888 888  888  #
#  Y88b  d88P Y8b.     888  888 Y8b.     888     888  888 Y88b.  888 Y88..88P 888  888  #
#   "Y8888P88  "Y8888  888  888  "Y8888  888     "Y888888  "Y888 888  "Y88P"  888  888  #
#                                                                                       #
#########################################################################################

np.set_printoptions(precision=3, suppress=True, linewidth=100)


obj = np.load("obj.npy")
print(obj)
vraixyz = np.load("xyz.npy")
print(vraixyz)
vraix = vraixyz[:, 0]
vraiy = vraixyz[:, 1]
vraiz = vraixyz[:, 2]
# print(obj)
x = obj[:, 0]
y = obj[:, 1]
z = obj[:, 2]


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")
ax.scatter(x, z, y, c="blue", s=100)
ax.scatter(vraix, vraiz, vraiy, c="red", s=700, marker="x")
ax.view_init(22, 45)

# ax.plot_surface(x, y, z)


# def f(x, y):
#     return np.sin(np.sqrt(x ** 2 + y ** 2))


# X, Y = np.meshgrid(x, y)
# Z = f(X, Y)
# ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

# ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)
# plt.show()

# tri = pymesh.triangle()
# tri.points = obj
# tri.max_area = 0.05
# tri.split_boundary = False
# tri.verbosity = 0
# tri.run()
# # Execute triangle.
# mesh = tri.mesh
# # output triangulation.
# pymesh.save_mesh("test.obj", mesh)

# tetgen = pymesh.tetgen()
# tetgen.points = obj
# tetgen.verbosity = 1
# # tetgen.keep_convex_hull = False
# tetgen.split_boundary = False
# # tetgen.max_radius_edge_ratio = 2000
# # tetgen.min_dihedral_angle = 0.1
# # tetgen.coplanar_tolerance = 0.9
pymesh.tetrahedralize(
    obj,
    cell_size=0.5,
    radius_edge_ratio=2.0,
    facet_distance=-1.0,
    feature_angle=120,
    engine="auto",
    with_timing=False,
)

tetgen.run()  # Execute tetgen

mesh = tetgen.mesh  # Extract output tetrahedral mesh.
# mesh.add_attribute("voxel_volume")
# volumes = mesh.get_attribute("voxel_volume")
# print(len(tetgen.vertices))
# print(volumes)
pymesh.save_mesh("test.obj", mesh)

# from vedo import *
# data = np.stack((x, y, z), axis=1)

########################################################################################################
#                                                                                                      #
#  888     888 d8b                            888 d8b                   888    d8b                     #
#  888     888 Y8P                            888 Y8P                   888    Y8P                     #
#  888     888                                888                       888                            #
#  Y88b   d88P 888 .d8888b  888  888  8888b.  888 888 .d8888b   8888b.  888888 888  .d88b.  88888b.    #
#   Y88b d88P  888 88K      888  888     "88b 888 888 88K          "88b 888    888 d88""88b 888 "88b   #
#    Y88o88P   888 "Y8888b. 888  888 .d888888 888 888 "Y8888b. .d888888 888    888 888  888 888  888   #
#     Y888P    888      X88 Y88b 888 888  888 888 888      X88 888  888 Y88b.  888 Y88..88P 888  888   #
#      Y8P     888  88888P'  "Y88888 "Y888888 888 888  88888P' "Y888888  "Y888 888  "Y88P"  888  888   #
#                                                                                                      #
########################################################################################################


# window = pyglet.window.Window(width=1280, height=720, resizable=True)
# root_path = os.path.dirname(__file__)
# tennis = Wavefront(os.path.join(root_path, "test.obj"))
# rotation = 0.0
# lightfv = ctypes.c_float * 4


# @window.event
# def on_resize(width, height):
#     viewport_width, viewport_height = window.get_framebuffer_size()
#     glViewport(0, 0, viewport_width, viewport_height)

#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(45.0, float(width) / height, 1.0, 100.0)
#     glMatrixMode(GL_MODELVIEW)
#     return True


# @window.event
# def on_draw():
#     window.clear()
#     glLoadIdentity()

#     glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))

#     draw_box(tennis, 0.0, 0.0)


# def draw_box(object, x, y):
#     glLoadIdentity()
#     glTranslated(x, y, -10.0)
#     glRotatef(rotation, 0.0, 1.0, 0.0)
#     glRotatef(-25.0, 1.0, 0.0, 0.0)
#     glRotatef(45.0, 0.0, 0.0, 1.0)

#     visualization.draw(object)


# def update(dt):
#     global rotation
#     rotation += 90.0 * dt

#     if rotation > 720.0:
#         rotation = 0.0


# pyglet.clock.schedule(update)
# pyglet.app.run()
