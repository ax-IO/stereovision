import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import codecs
import json


def rescaleFrame(frame, scale=0.75):
    """
    Rescale Photos, Videos and Live Videos
    """
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_CUBIC)


def printL(myList):
    print("[%s]" % ", ".join(map(str, myList)))


mire_G = cv.imread("etallonage/mire_G_00146.jpg")
mire_G_resized = rescaleFrame(mire_G, scale=0.6)
# posList_G = []
# posList_3D = []
xList = []
yList = []
zList = []
u_GList = []
v_GList = []


def clickCameraGauche(event, u_G, v_G, flags, param):
    global xList, yList, zList, u_GList, v_GList, mire_G_resized
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.drawMarker(
            mire_G_resized, (u_G, v_G), (0, 0, 255), cv.MARKER_TILTED_CROSS, thickness=1
        )
        x = input("Coordonnée en x ? ")
        xList.append(x)
        y = input("Coordonnée en y ? ")
        yList.append(y)
        z = input("Coordonnée en z ? ")
        zList.append(z)

        # posList_3D.append((x, y, z))
        # posList_G.append((u_G, v_G))
        u_GList.append(u_G)
        v_GList.append(v_G)


mire_D = cv.imread("etallonage/mire_D_00146.jpg")
mire_D_resized = rescaleFrame(mire_D, scale=0.6)
# posList_D = []
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


# posList = posList_3D + posList_G + posList_D
# print("[%s]" % ", ".join(map(str, posList)))
# print(posList[1][0])

printL(xList)
printL(yList)
printL(zList)
printL(u_GList)
printL(v_GList)
printL(u_DList)
printL(v_DList)
posNp = np.array(
    [xList, yList, zList, u_GList, v_GList, u_DList, v_DList]
)  # conversion en Numpy Array
print("Numpy Array :")
print(posNp)

position = posNp.tolist()  # nested lists with same data, indices

print("List of Lists :")
printL(position)

# with open("calibration.txt", "w") as f:
#     json.dump(posNp, f)

# file_path = "calibration.txt"  ## your path variable
# json.dump(
#     position,
#     codecs.open(file_path, "w", encoding="utf-8"),
#     separators=(",", ":"),
#     sort_keys=True,
#     indent=4,
# )  ### this saves the array in .json format

# file_path = "test_points.txt"  ## your path variable
# json.dump(
#     position,
#     codecs.open(file_path, "w", encoding="utf-8"),
#     separators=(",", ":"),
#     sort_keys=True,
#     indent=4,
# )  ### this saves the array in .json format
