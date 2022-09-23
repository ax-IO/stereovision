import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import math
import pymesh

# import pywavefront
# from pywavefront import visualization

np.set_printoptions(precision=3, suppress=True, linewidth=100)


def rescaleFrame(frame, scale=0.75):
    """
    Rescale Photos, Videos and Live Videos
    """
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_CUBIC)


def clickCameraGauche(event, u_G, v_G, flags, param):
    global u_GList, v_GList, mire_G_resized
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.drawMarker(
            mire_G_resized, (u_G, v_G), (0, 0, 255), cv.MARKER_TILTED_CROSS, thickness=1
        )

        u_GList.append(u_G)
        v_GList.append(v_G)


def clickCameraDroite(event, u_D, v_D, flags, param):
    global u_DList, v_DList, mire_D_resized
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.drawMarker(
            mire_D_resized, (u_D, v_D), (0, 0, 255), cv.MARKER_TILTED_CROSS, thickness=1
        )

        u_DList.append(u_D)
        v_DList.append(v_D)
        print(f"Point calibré !\n")


def camera_2D_3D(H_G, H_D, u_G, v_G, u_D, v_D):
    """
    Reconstruit un point 3D en passant le modèle de Gauche (H_G),
    le modèle de Droite (H_D) ainsi que les coordonnées de l'image de Gauche (u_v, v_G)
    et les coordonnées de l'image de Droite (u_D, v_D)
    """
    A = np.asarray(
        [
            [
                (H_G[0, 0] - H_G[2, 0] * u_G),
                (H_G[0, 1] - H_G[2, 1] * u_G),
                (H_G[0, 2] - H_G[2, 2] * u_G),
            ],
            [
                (H_G[1, 0] - H_G[2, 0] * v_G),
                (H_G[1, 1] - H_G[2, 1] * v_G),
                (H_G[1, 2] - H_G[2, 2] * v_G),
            ],
            [
                (H_D[0, 0] - H_D[2, 0] * u_D),
                (H_D[0, 1] - H_D[2, 1] * u_D),
                (H_D[0, 2] - H_D[2, 2] * u_D),
            ],
            [
                (H_D[1, 0] - H_D[2, 0] * v_D),
                (H_D[1, 1] - H_D[2, 1] * v_D),
                (H_D[1, 2] - H_D[2, 2] * v_D),
            ],
        ],
    ).reshape(4, 3)
    B = np.asarray(
        [
            H_G[2, 3] * u_G - H_G[0, 3],
            H_G[2, 3] * v_G - H_G[1, 3],
            H_D[2, 3] * u_D - H_D[0, 3],
            H_D[2, 3] * v_D - H_D[1, 3],
        ]
    ).reshape(4, 1)
    #  Points 3D reconstruits
    X = np.linalg.pinv(A) @ B
    return X


def chessboard(mire):
    uList = []
    vList = []
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    gray = cv.cvtColor(mire, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(
        gray,
        (6, 6),
        None,
        flags=cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE,
    )  # Find the grid

    # If desired number of corners can be detected then,
    # refine the pixel coordinates and display
    # them on the images of checker board
    if ret == True:
        # Refining pixel coordinates
        # for given 2d points.
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        uList = corners2[:, 0, 0]
        uList = uList.reshape((len(uList), 1))
        # print(uList)
        vList = corners2[:, 0, 1]
        vList = vList.reshape((len(vList), 1))
        # print(vList)
        uvsList = (
            np.concatenate((uList, vList), axis=1)
            .astype("float32")
            .reshape((1, 6 * 6, 2))
        )
        # print(uvsList)

        image = cv.drawChessboardCorners(mire, (6, 6), corners2, ret)

        while True:
            cv.imshow("Mire 2 : Calibration", image)
            k = cv.waitKey(200) & 0xFF
            # print(k)
            if k == 27 or k == 113:
                cv.destroyAllWindows()
                break
    else:
        print("Erreur detection Chessboard")
    return ret, uList, vList


def main():

    cv.namedWindow("Mire Gauche")
    cv.setMouseCallback("Mire Gauche", clickCameraGauche)

    cv.namedWindow("Mire Droite")
    cv.setMouseCallback("Mire Droite", clickCameraDroite)

    while True:
        cv.imshow("Mire Gauche", mire_G_resized)
        cv.imshow("Mire Droite", mire_D_resized)
        k = cv.waitKey(200) & 0xFF
        # print(k)
        if k == 27 or k == 113:
            cv.destroyAllWindows()
            break

    # while True:
    #     cv.imshow("Mire 2 : Calibration", mire_G_resized[250:429, 320:655])
    #     k = cv.waitKey(200) & 0xFF
    #     # print(k)
    #     if k == 27 or k == 113:
    #         cv.destroyAllWindows()
    #         break

    # ret_G, u_GList, v_GList = chessboard(mire_G_resized[18:294, 464:673])
    # ret_G, u_GList, v_GList = chessboard(mire_G_resized[40:350, 278:468])
    # ret_G, u_GList, v_GList = chessboard(mire_G_resized[250:429, 320:655])
    # if ret_G == True:
    #     print(u_GList)
    #     print(v_GList)

    # ret_D, u_DList, v_DList = chessboard(mire_D_resized)
    # if ret_D == True:
    #     print(u_DList)
    #     print(v_DList)
    if len(u_GList) == len(v_GList) == len(u_DList) == len(v_DList):
        n = len(u_GList)
        X = np.zeros((n, 3))
        for i in range(n):
            a = camera_2D_3D(H_G, H_D, u_GList[i], v_GList[i], u_DList[i], v_DList[i])
            X[i, 0] = a[0]
            X[i, 1] = a[1]
            X[i, 2] = a[2]
        print(X)
        # np.save("obj.npy", X)
    else:
        print(f"{len(u_GList)}≠{len(v_GList)}≠{len(u_DList)}≠{len(v_DList)}")
        quit()


if __name__ == "__main__":
    # print(__doc__)
    H_G = np.load("H_G.npy")
    # print(H_G)
    H_D = np.load("H_D.npy")
    # print(H_D)

    # mire_G = cv.imread("etallonage/tennis/mire_G_tennis_0056.bmp")
    mire_G = cv.imread("etallonage/mire_G_00146.jpg")

    mire_G_resized = rescaleFrame(mire_G, scale=0.6)
    u_GList = []
    v_GList = []

    # mire_D = cv.imread("etallonage/tennis/mire_D_tennis_0056.bmp")
    mire_D = cv.imread("etallonage/mire_D_00146.jpg")

    mire_D_resized = rescaleFrame(mire_D, scale=0.6)
    u_DList = []
    v_DList = []
    main()
    cv.destroyAllWindows()
