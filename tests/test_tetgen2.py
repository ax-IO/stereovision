import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import math
import pymesh

np.set_printoptions(precision=3, suppress=True, linewidth=100)


def rescaleFrame(frame, scale=0.75):
    """
    Rescale Photos, Videos and Live Videos
    """
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_CUBIC)


H_G = np.load("H_G.npy")
# print(H_G)
H_D = np.load("H_D.npy")
# print(H_D)

# mire_G = cv.imread("etallonage/tennis/mire_G_tennis_0056.bmp")
mire_G = cv.imread("etallonage/mire_G_00146.jpg")

mire_G_resized = rescaleFrame(mire_G, scale=0.9)
u_GList = []
v_GList = []


def clickCameraGauche(event, u_G, v_G, flags, param):
    global u_GList, v_GList, mire_G_resized
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.drawMarker(
            mire_G_resized, (u_G, v_G), (0, 0, 255), cv.MARKER_TILTED_CROSS, thickness=1
        )

        u_GList.append(u_G)
        v_GList.append(v_G)


# mire_D = cv.imread("etallonage/tennis/mire_D_tennis_0056.bmp")
mire_D = cv.imread("etallonage/mire_D_00146.jpg")

mire_D_resized = rescaleFrame(mire_D, scale=0.9)
u_DList = []
v_DList = []


def clickCameraDroite(event, u_D, v_D, flags, param):
    global u_DList, v_DList, mire_D_resized
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.drawMarker(
            mire_D_resized, (u_D, v_D), (0, 0, 255), cv.MARKER_TILTED_CROSS, thickness=1
        )

        u_DList.append(u_D)
        v_DList.append(v_D)
        print(f"Point calibré !\n")


input_mesh = pymesh.generate_icosphere(1.0, [0.0, 0.0, 0.0])
tetgen = pymesh.tetgen()
tetgen.points = input_mesh.vertices  # Input points.
tetgen.triangles = input_mesh.faces  # Input triangles
tetgen.max_tet_volume = 0.01
tetgen.verbosity = 1
tetgen.run()  # Execute tetgen
mesh = tetgen.mesh  # Extract output tetrahedral mesh.
pymesh.save_mesh("test.obj", mesh)
