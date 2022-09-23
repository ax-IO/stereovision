#!/usr/bin/env python

"""
Simple example of stereo image matching and point cloud generation.

Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )
"""

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def round_down(num, divisor):
    return num - (num % divisor)


ply_header = """ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
"""


print("loading images...")
cv.samples.addSamplesDataSearchPath(
    "/home/axiom/Documents/Source_Davy_fevrier_2020/python/etallonage"
)
imgL = cv.pyrDown(
    cv.imread(cv.samples.findFile("mire_G_00146.jpg"))
)  # downscale images for faster processing
imgR = cv.pyrDown(cv.imread(cv.samples.findFile("mire_D_00146.jpg")))


window_size = 3
# num_disp = 96
disp = []
min_disp = 16
max_disp = 112
block_size = 16


def computeDisp(img_G, img_D):
    global disp, num_disp
    num_disp = max_disp - min_disp
    stereo = cv.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        P1=8 * 3 * window_size ** 2,
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32,
    )

    # print("computing disparity...")
    disp = stereo.compute(img_G, img_D).astype(np.float32) / 16.0


def windowSize(x):
    global window_size
    window_size = x
    # print("window_size = " + str(window_size))
    computeDisp(imgL, imgR)


def minDisp(x):
    global min_disp
    min_disp = round_down(x, 16)
    # print("min_disp = " + str(min_disp))
    computeDisp(imgL, imgR)


def maxDisp(x):
    global max_disp
    max_disp = round_down(x, 16)
    # print("max_disp = " + str(max_disp))
    computeDisp(imgL, imgR)


def blockSize(x):
    global block_size
    block_size = round_down(x, 2) + 1
    # print("max_disp = " + str(max_disp))
    computeDisp(imgL, imgR)


def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, "wb") as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode("utf-8"))
        np.savetxt(f, verts, fmt="%f %f %f %d %d %d ")


def main():

    # Create window
    cv.namedWindow("Test")

    # Add a slider
    cv.createTrackbar("window_size", "Test", 3, 21, windowSize)
    cv.createTrackbar("min_disp", "Test", 16, 160, minDisp)
    cv.createTrackbar("max_disp", "Test", 112, 320, maxDisp)
    cv.createTrackbar("block_size", "Test", 2, 15, blockSize)

    # disparity range is tuned for 'aloe' image pair
    # print("Window size = " + str(window_size))

    computeDisp(imgL, imgR)

    # cv.imshow("left", imgL)
    while True:
        # Show an image in the window
        # print("disp = " + str(disp))
        # print("block_size = " + str(block_size))
        # print("min_disp = " + str(min_disp))
        # print("max_disp = " + str(max_disp))
        # print(num_disp)

        cv.imshow("Test", (disp - min_disp) / (num_disp))

        k = cv.waitKey(500) & 0xFF
        # print(k)
        if k == 27 or k == 113:
            cv.destroyAllWindows()
            break
    print("Done")

    plt.imshow(disp, cmap="plasma")
    plt.colorbar()
    plt.show()

    print(
        "generating 3d point cloud...",
    )
    h, w = imgL.shape[:2]
    f = 0.8 * w  # guess for focal length
    Q = np.float32(
        [
            [1, 0, 0, -0.5 * w],
            [0, -1, 0, 0.5 * h],  # turn points 180 deg around x-axis,
            [0, 0, 0, -f],  # so that y-axis looks up
            [0, 0, 1, 0],
        ]
    )
    points = cv.reprojectImageTo3D(disp, Q)
    colors = cv.cvtColor(imgL, cv.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    out_fn = "out.ply"
    write_ply(out_fn, out_points, out_colors)
    print("%s saved" % out_fn)


if __name__ == "__main__":
    print(__doc__)
    main()
    cv.destroyAllWindows()
