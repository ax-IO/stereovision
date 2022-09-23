import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import codecs, json, math
import glob


np.set_printoptions(precision=3, suppress=True, linewidth=100)

# stop the iteration when specified
# accuracy, epsilon, is reached or
# specified number of iterations are completed.
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = []  # 3d point in real world space
# imgpoints_D = []  # 2d points in image plane.
grid_size = 0.03  # 3cm
rows, cols = 4, 11

for i in range(cols):
    for j in range(rows):
        objpoints.append((i * grid_size, (2 * j + i % 2) * grid_size, 0))

objpoints = np.array(objpoints).astype("float32").reshape((1, rows * cols, 3))
# print(objpoints.shape)
# print(objpoints)
# xy = objpoints[:, 0:2]
# plt.scatter(objpoints[:, 0], objpoints[:, 1])
# plt.show()


#######################################################################################################
#
#  #####                                               ######
# #     #    ##    #    #  ######  #####     ##        #     #  #####    ####   #  #####  ######
# #         #  #   ##  ##  #       #    #   #  #       #     #  #    #  #    #  #    #    #
# #        #    #  # ## #  #####   #    #  #    #      #     #  #    #  #    #  #    #    #####
# #        ######  #    #  #       #####   ######      #     #  #####   #    #  #    #    #
# #     #  #    #  #    #  #       #   #   #    #      #     #  #   #   #    #  #    #    #
#  #####   #    #  #    #  ######  #    #  #    #      ######   #    #   ####   #    #    ######
#
#######################################################################################################

# Extracting path of individual image stored
# in a given directory.
images_D = glob.glob("etallonage/mire2/mire2_D_*.bmp")

# Vector for 3D points
points_3D_D = []

# Vector for 2D points
points_2D_D = []


for filename in images_D:

    # Etallonage automatique sur la 2ème mire
    mire_D = cv.imread(filename)
    gray = cv.cvtColor(mire_D, cv.COLOR_BGR2GRAY)

    params = cv.SimpleBlobDetector_Params()
    params.minArea = 10
    params.minDistBetweenBlobs = 5
    detector = cv.SimpleBlobDetector_create(params)

    keypoints = detector.detect(gray)  # Detect blobs.

    # Draw detected blobs as red circles. This helps cv2.findCirclesGrid() .
    im_with_keypoints = cv.drawKeypoints(
        mire_D,
        keypoints,
        np.array([]),
        (0, 255, 0),
        cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    )
    im_with_keypoints_gray = cv.cvtColor(im_with_keypoints, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findCirclesGrid(
        im_with_keypoints, (4, 11), None, flags=cv.CALIB_CB_ASYMMETRIC_GRID
    )  # Find the circle grid

    # If desired number of corners can be detected then,
    # refine the pixel coordinates and display
    # them on the images of checker board
    if ret == True:
        points_3D_D.append(objpoints)

        # Refining pixel coordinates
        # for given 2d points.
        corners2 = cv.cornerSubPix(
            im_with_keypoints_gray, corners, (11, 11), (-1, -1), criteria
        )

        u_D = corners2[:, 0, 0]
        u_D = u_D.reshape((len(u_D), 1))
        v_D = corners2[:, 0, 1]
        v_D = v_D.reshape((len(v_D), 1))
        uvs_D = (
            np.concatenate((u_D, v_D), axis=1)
            .astype("float32")
            .reshape((1, rows * cols, 2))
        )

        points_2D_D.append(uvs_D)

        # Draw and display the corners
        image = cv.drawChessboardCorners(mire_D, (4, 11), corners2, ret)

        # # print(uvs_D)
        # print(uvs_D.shape)
        # print(uvs_D)
    else:
        image = cv.imread(filename)

    # while True:
    #     cv.imshow("Mire 2 Droite : Calibration", image)
    #     k = cv.waitKey(200) & 0xFF
    #     # print(k)
    #     if k == 27 or k == 113:
    #         cv.destroyAllWindows()
    #         break

    cv.imshow("Mire 2 Droite : Calibration", image)
    cv.waitKey(100)
    cv.destroyAllWindows()

# print(len(points_2D_D))
# print(points_2D_D[0])

# print(len(points_3D_D))
# print(points_3D_D[0])


ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    points_3D_D, points_2D_D, gray.shape[::-1], None, None
)

# # Displayig required output
# print(" Camera matrix:")
# print(mtx)

# print("\n Distortion coefficient:")
# print(dist)

# print("\n Rotation Vectors:")
# print(rvecs)

# print("\n Translation Vectors:")
# print(tvecs)

# Converts a rotation matrix to a rotation vector or vice versa.
# print(rvecs[0])
Rmtx = []
for i in range(len(rvecs)):
    rotmtx, _ = cv.Rodrigues((rvecs[i]), jacobian=None)
    Rmtx.append(rotmtx)
# print("\n Rotation Matrices (3x3):")
# print(Rmtx)

# Concatenate rotation matrix (3x3) and translation vector (3x1)
RTmtx = []
for i in range(len(rvecs)):
    rottransmtx = np.concatenate((Rmtx[i], tvecs[i]), axis=1)
    RTmtx.append(rottransmtx)
# print("\n RT Matrices (3x4):")
# print(RTmtx)

# Projection matrices (3x4) = camera Matrices (3x3) @ RT (3x4)
Pmtx = []
for i in range(len(rvecs)):
    projmtx = mtx @ RTmtx[i]
    Pmtx.append(projmtx)
# print("\n Projection matrix (3x4):")
# print(Pmtx)
# print()


# pour tous les points
# print(objpoints.shape)
n = objpoints[0, :, 0].size
x = objpoints[0, :, 0].reshape((n, 1))
# print(x)
y = objpoints[0, :, 1].reshape((n, 1))
z = objpoints[0, :, 2].reshape((n, 1))

for i in range(len(rvecs)):
    uvs_rec_D = Pmtx[i] @ np.concatenate((x.T, y.T, z.T, np.ones((1, n))), axis=0)
    # print(Pmtx)
    # print(x.T.shape)
    # print(np.ones((1, n)).shape)

    # suivant u
    u_rec_D = (uvs_rec_D[0, :] * (1 / uvs_rec_D[2, :])).T
    # suivant v
    v_rec_D = (uvs_rec_D[1, :] * (1 / uvs_rec_D[2, :])).T

    # print(uvs_rec_D)

    u_D = points_2D_D[i][0, :, 0]
    # print("u_D = ")
    # print(u_D)
    # print("u_rec_D = ")
    # print(u_rec_D)

    v_D = points_2D_D[i][0, :, 1]
    # print("v_D = ")
    # print(v_D)
    # print("v_rec_D = ")
    # print(v_rec_D)

    # CALCUL ERREURS

    # # erreur suivant u
    Err_u_D = u_D.T - u_rec_D
    # # erreur suivant v
    Err_v_D = v_D.T - v_rec_D

    # erreur maximale u_D
    # print("Erreur maximale u_D : " + str(round(np.max(Err_u_D), 5)))
    # # erreur maximale v_D
    # print("Erreur maximale v_D : " + str(round(np.max(Err_v_D), 5)))

    # # erreur.minimale.u_D
    # print("Erreur minimale u_D : " + str(round(np.min(Err_u_D), 5)))
    # # erreur minimale v_D
    # print("Erreur minimale v_D : " + str(round(np.min(Err_v_D), 5)))

    # erreur moyenne u_D
    print(
        "[image "
        + str(i + 1)
        + "] "
        + "Erreur moyenne u_D : "
        + str(round(np.mean(Err_u_D), 5))
    )
    # erreur moyenne v_D
    print(
        "[image "
        + str(i + 1)
        + "] "
        + "Erreur moyenne v_D : "
        + str(round(np.mean(Err_v_D), 5))
    )

    # erreur ecart-type u_D
    print(
        "[image "
        + str(i + 1)
        + "] "
        + "Erreur écart-type u_D : "
        + str(round(np.std(Err_u_D), 5))
    )
    # erreur ecart-type v_D
    print(
        "[image "
        + str(i + 1)
        + "] "
        + "Erreur écart-type v_D : "
        + str(round(np.std(Err_v_D), 5))
    )

    if (
        abs(np.mean(Err_u_D)) < 2
        and abs(np.mean(Err_v_D)) < 2
        and abs(np.std(Err_u_D)) < 2
        and abs(np.std(Err_v_D)) < 2
    ):
        print("[image " + str(i + 1) + "] : Wow!")

    print()
