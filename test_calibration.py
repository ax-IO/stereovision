import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import codecs, json, math


# with open('calibration.txt', 'r') as f:
#     pos = json.load(f)
np.set_printoptions(precision=3, suppress=True, linewidth=100)

obj_text = codecs.open("calibration.txt", "r", encoding="utf-8").read()
pos = json.loads(obj_text)
# print("[%s]" % ", ".join(map(str, pos)))
xList = pos[0]
yList = pos[1]
zList = pos[2]
u_GList = pos[3]
v_GList = pos[4]
u_DList = pos[5]
v_DList = pos[6]

x = np.asarray(xList, dtype=float).reshape((len(xList), 1))
y = np.asarray(yList, dtype=float).reshape((len(yList), 1))
z = np.asarray(zList, dtype=float).reshape((len(zList), 1))
u_G = np.asarray(u_GList, dtype=float).reshape((len(u_GList), 1))
v_G = np.asarray(v_GList, dtype=float).reshape((len(v_GList), 1))
u_D = np.asarray(u_DList, dtype=float).reshape((len(u_DList), 1))
v_D = np.asarray(v_DList, dtype=float).reshape((len(v_DList), 1))

# nombre de point de calibration
n = len(xList)
# print("Nombre de point de calibration : " + str(n))

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

# Vecteur B_D
# B_D = np.array([u_DList + v_DList], dtype=float).T
# print("Dimension de u_D : " + str(u_D.shape))
# print("Dimension de v_D : " + str(v_D.shape))
B_D = np.append(u_D, v_D, axis=0)

# print("Dimension de B_D : " + str(B_D.shape))
# print(B_D)

# Matrice A_D
A_D_1 = np.concatenate(
    (
        x,
        y,
        z,
        np.ones((n, 1)),
        np.zeros((n, 4)),
        np.negative(u_D) * x,
        np.negative(u_D) * y,
        np.negative(u_D) * z,
    ),
    axis=1,
)
A_D_2 = np.concatenate(
    (
        np.zeros((n, 4)),
        x,
        y,
        z,
        np.ones((n, 1)),
        np.negative(v_D) * x,
        np.negative(v_D) * y,
        np.negative(v_D) * z,
    ),
    axis=1,
)

A_D = np.concatenate((A_D_1, A_D_2), axis=0)

# print("Dimension de A_D : " + str(A_D.shape))
# print(A_D)

X_D = np.linalg.pinv(A_D) @ B_D
# print("Dimension de X_D : " + str(X_D.shape))
# print(X_D)

H_D = np.resize(X_D, (3, 4))
H_D[2, 3] = 1
# print("Dimension de H_D : " + str(H_D.shape))
print(H_D)


# pour tous les points
uvs_rec_D = H_D @ np.concatenate((x.T, y.T, z.T, np.ones((1, n))), axis=0)
# print(H_D)
print(x.T.shape)
print(np.ones((1, n)).shape)
# suivant u
u_rec_D = (uvs_rec_D[0, :] * (1 / uvs_rec_D[2, :])).T
# suivant v
v_rec_D = (uvs_rec_D[1, :] * (1 / uvs_rec_D[2, :])).T

print(uvs_rec_D)
# print(u_rec_D)
# print(u_D.T)
# print(v_rec_D)
# print(v_D.T)


# CALCUL ERREURS

# # # erreur suivant u
# Err_u_D = u_D.T - u_rec_D
# # # erreur suivant v
# Err_v_D = v_D.T - v_rec_D

# # # erreur maximale u_D
# # print("Erreur maximale u_D : " + str(round(np.max(Err_u_D), 5)))
# # # erreur maximale v_D
# # print("Erreur maximale v_D : " + str(round(np.max(Err_v_D), 5)))

# # # erreur.minimale.u_D
# # print("Erreur minimale u_D : " + str(round(np.min(Err_u_D), 5)))
# # # erreur minimale v_D
# # print("Erreur minimale v_D : " + str(round(np.min(Err_v_D), 5)))


# # # erreur moyenne u_D
# # print("Erreur moyenne u_D : " + str(round(np.mean(Err_u_D), 5)))
# # # erreur moyenne v_D
# # print("Erreur moyenne v_D : " + str(round(np.mean(Err_v_D), 5)))


# # # erreur ecart-type u_D
# # print("Erreur écart-type u_D : " + str(round(np.std(Err_u_D), 5)))
# # # erreur ecart-type v_D
# # print("Erreur écart-type v_D : " + str(round(np.std(Err_v_D), 5)))


# Test  points (Mire Droite)
obj_text = codecs.open("test_points.txt", "r", encoding="utf-8").read()
pos_points_test = json.loads(obj_text)
# print("[%s]" % ", ".join(map(str, pos_points_test)))

# pointx=[x y z u_D v_D]
pos_point1_D = [
    pos_points_test[0][0],
    pos_points_test[1][0],
    pos_points_test[2][0],
    pos_points_test[5][0],
    pos_points_test[6][0],
]

pos_point2_D = [
    pos_points_test[0][1],
    pos_points_test[1][1],
    pos_points_test[2][1],
    pos_points_test[5][1],
    pos_points_test[6][1],
]

pos_point3_D = [
    pos_points_test[0][2],
    pos_points_test[1][2],
    pos_points_test[2][2],
    pos_points_test[5][2],
    pos_points_test[6][2],
]

pos_point4_D = [
    pos_points_test[0][3],
    pos_points_test[1][3],
    pos_points_test[2][3],
    pos_points_test[5][3],
    pos_points_test[6][3],
]

point1_D = np.asarray(pos_point1_D, dtype=float).reshape((len(pos_point1_D), 1))
point2_D = np.asarray(pos_point2_D, dtype=float).reshape((len(pos_point2_D), 1))
point3_D = np.asarray(pos_point3_D, dtype=float).reshape((len(pos_point3_D), 1))
point4_D = np.asarray(pos_point4_D, dtype=float).reshape((len(pos_point4_D), 1))

# POINT 1
uvrec1_D = H_D @ np.asarray(
    [point1_D[0, 0], point1_D[1, 0], point1_D[2, 0], 1]
).reshape(4, 1)
# u
# print(point1_D[3])
# u reconstruite
u_rec1_D = uvrec1_D[0, 0] / uvrec1_D[2, 0]
# v
# point1_D[4,0]
# v reconstruite
v_rec1_D = uvrec1_D[1, 0] / uvrec1_D[2, 0]

# POINT 2
uvrec2_D = H_D @ np.asarray(
    [point2_D[0, 0], point2_D[1, 0], point2_D[2, 0], 1]
).reshape(4, 1)
# u
# point2_D[3,0]
# u reconstruite
u_rec2_D = uvrec2_D[0, 0] / uvrec2_D[2, 0]
# v
# point2_D[4, 0]
# v reconstruite
v_rec2_D = uvrec2_D[1, 0] / uvrec2_D[2, 0]

# POINT 3
uvrec3_D = H_D @ np.asarray(
    [point3_D[0, 0], point3_D[1, 0], point3_D[2, 0], 1]
).reshape(4, 1)
# u
# point3_D[3,0]
# u reconstruite
u_rec3_D = uvrec3_D[0, 0] / uvrec3_D[2, 0]
# v
# point3_D[4, 0]
# v reconstruite
v_rec3_D = uvrec3_D[1, 0] / uvrec3_D[2, 0]

# POINT 4
uvrec4_D = H_D @ np.asarray(
    [point4_D[0, 0], point4_D[1, 0], point4_D[2, 0], 1]
).reshape(4, 1)
# u
# point4_D[3, 0]
# u reconstruite
u_rec4_D = uvrec4_D[0, 0] / uvrec4_D[2, 0]
# v
# point4_D[5, 0]
# v reconstruite
v_rec4_D = uvrec4_D[1, 0] / uvrec4_D[2, 0]

Err_u_D = np.array(
    [
        point1_D[3, 0] - u_rec1_D,
        point2_D[3, 0] - u_rec2_D,
        point3_D[3, 0] - u_rec3_D,
        point4_D[3, 0] - u_rec4_D,
    ]
)
Err_v_D = np.array(
    [
        point1_D[4, 0] - v_rec1_D,
        point2_D[4, 0] - v_rec2_D,
        point3_D[4, 0] - v_rec3_D,
        point4_D[4, 0] - v_rec4_D,
    ]
)
# print("Erreur reconstruction suivant u (mire Droite): " + str(Err_u_D))
# print("Erreur reconstruction suivant v (mire Droite): " + str(Err_v_D))

#######################################################################################################
#
#  ####                                                #####
# #     #   ##    #    #  ######  #####     ##        #     #    ##    #    #   ####   #    #  ######
# #        #  #   ##  ##  #       #    #   #  #       #         #  #   #    #  #    #  #    #  #
# #       #    #  # ## #  #####   #    #  #    #      #  ####  #    #  #    #  #       ######  #####
# #       ######  #    #  #       #####   ######      #     #  ######  #    #  #       #    #  #
# #     # #    #  #    #  #       #   #   #    #      #     #  #    #  #    #  #    #  #    #  #
#  ####   #    #  #    #  ######  #    #  #    #       #####   #    #   ####    ####   #    #  ######
#
#######################################################################################################

# Vecteur B_G
# B_G = np.array([u_GList + v_GList], dtype=float).T
# print("Dimension de u_G : " + str(u_G.shape))
# print("Dimension de v_G : " + str(v_G.shape))
B_G = np.append(u_G, v_G, axis=0)

# print("Dimension de B_G : " + str(B_G.shape))
# print(B_G)

# Matrice A_G
A_G_1 = np.concatenate(
    (
        x,
        y,
        z,
        np.ones((n, 1)),
        np.zeros((n, 4)),
        np.negative(u_G) * x,
        np.negative(u_G) * y,
        np.negative(u_G) * z,
    ),
    axis=1,
)
A_G_2 = np.concatenate(
    (
        np.zeros((n, 4)),
        x,
        y,
        z,
        np.ones((n, 1)),
        np.negative(v_G) * x,
        np.negative(v_G) * y,
        np.negative(v_G) * z,
    ),
    axis=1,
)

A_G = np.concatenate((A_G_1, A_G_2), axis=0)

# print("Dimension de A_G : " + str(A_G.shape))
# print(A_G)

X_G = np.linalg.pinv(A_G) @ B_G
# print("Dimension de X_G : " + str(X_G.shape))
# print(X_G)

H_G = np.resize(X_G, (3, 4))
H_G[2, 3] = 1
# print("Dimension de H_G : " + str(H_G.shape))
# print(H_G)

# pour tous les points
uvs_rec_G = H_G @ np.concatenate((x.T, y.T, z.T, np.ones((1, n))), axis=0)
# suivant u
u_rec_G = uvs_rec_G[0, :] * (1 / uvs_rec_G[2, :])
u_rec_G = u_rec_G.T
# suivant v
v_rec_G = uvs_rec_G[1, :] * (1 / uvs_rec_G[2, :])
v_rec_G = v_rec_G.T

# print(u_rec_G)
# print(u_G.T)
# print(v_rec_G)
# print(v_G.T)


# CALCUL ERREURS

# # erreur suivant u
Err_u_G = u_G.T - u_rec_G
# # erreur suivant v
Err_v_G = v_G.T - v_rec_G

# # erreur maximale u_G
# print("Erreur maximale u_G : " + str(round(np.max(Err_u_G), 5)))
# # erreur maximale v_G
# print("Erreur maximale v_G : " + str(round(np.max(Err_v_G), 5)))

# # erreur.minimale.u_G
# print("Erreur minimale u_G : " + str(round(np.min(Err_u_G), 5)))
# # erreur minimale v_G
# print("Erreur minimale v_G : " + str(round(np.min(Err_v_G), 5)))


# # erreur moyenne u_G
# print("Erreur moyenne u_G : " + str(round(np.mean(Err_u_G), 5)))
# # erreur moyenne v_G
# print("Erreur moyenne v_G : " + str(round(np.mean(Err_v_G), 5)))


# # erreur ecart-type u_G
# print("Erreur écart-type u_G : " + str(round(np.std(Err_u_G), 5)))
# # erreur ecart-type v_G
# print("Erreur écart-type v_G : " + str(round(np.std(Err_v_G), 5)))

# Test  points (Mire Gauche)
obj_text = codecs.open("test_points.txt", "r", encoding="utf-8").read()
pos_points_test = json.loads(obj_text)
# print("[%s]" % ", ".join(map(str, pos_points_test)))

# pointx=[x y z u_G v_G]
pos_point1_G = [
    pos_points_test[0][0],
    pos_points_test[1][0],
    pos_points_test[2][0],
    pos_points_test[3][0],
    pos_points_test[4][0],
]

pos_point2_G = [
    pos_points_test[0][1],
    pos_points_test[1][1],
    pos_points_test[2][1],
    pos_points_test[3][1],
    pos_points_test[4][1],
]

pos_point3_G = [
    pos_points_test[0][2],
    pos_points_test[1][2],
    pos_points_test[2][2],
    pos_points_test[3][2],
    pos_points_test[4][2],
]

pos_point4_G = [
    pos_points_test[0][3],
    pos_points_test[1][3],
    pos_points_test[2][3],
    pos_points_test[3][3],
    pos_points_test[4][3],
]

point1_G = np.asarray(pos_point1_G, dtype=float).reshape((len(pos_point1_G), 1))
point2_G = np.asarray(pos_point2_G, dtype=float).reshape((len(pos_point2_G), 1))
point3_G = np.asarray(pos_point3_G, dtype=float).reshape((len(pos_point3_G), 1))
point4_G = np.asarray(pos_point4_G, dtype=float).reshape((len(pos_point4_G), 1))

# POINT 1
uvrec1_G = H_G @ np.asarray(
    [point1_G[0, 0], point1_G[1, 0], point1_G[2, 0], 1]
).reshape(4, 1)
# u
# print(point1_G[3])
# u reconstruite
u_rec1_G = uvrec1_G[0, 0] / uvrec1_G[2, 0]
# v
# point1_G[4,0]
# v reconstruite
v_rec1_G = uvrec1_G[1, 0] / uvrec1_G[2, 0]

# POINT 2
uvrec2_G = H_G @ np.asarray(
    [point2_G[0, 0], point2_G[1, 0], point2_G[2, 0], 1]
).reshape(4, 1)
# u
# point2_G[3,0]
# u reconstruite
u_rec2_G = uvrec2_G[0, 0] / uvrec2_G[2, 0]
# v
# point2_G[4, 0]
# v reconstruite
v_rec2_G = uvrec2_G[1, 0] / uvrec2_G[2, 0]

# POINT 3
uvrec3_G = H_G @ np.asarray(
    [point3_G[0, 0], point3_G[1, 0], point3_G[2, 0], 1]
).reshape(4, 1)
# u
# point3_G[3,0]
# u reconstruite
u_rec3_G = uvrec3_G[0, 0] / uvrec3_G[2, 0]
# v
# point3_G[4, 0]
# v reconstruite
v_rec3_G = uvrec3_G[1, 0] / uvrec3_G[2, 0]

# POINT 4
uvrec4_G = H_G @ np.asarray(
    [point4_G[0, 0], point4_G[1, 0], point4_G[2, 0], 1]
).reshape(4, 1)
# print(uvrec4_G)
# u
# print(point4_G[3, 0])
# u reconstruite
u_rec4_G = uvrec4_G[0, 0] / uvrec4_G[2, 0]
# print(u_rec4_G)
# v
# print(point4_G[4, 0])
# v reconstruite
v_rec4_G = uvrec4_G[1, 0] / uvrec4_G[2, 0]
# print(v_rec4_G)

Err_u_G = np.array(
    [
        point1_G[3, 0] - u_rec1_G,
        point2_G[3, 0] - u_rec2_G,
        point3_G[3, 0] - u_rec3_G,
        point4_G[3, 0] - u_rec4_G,
    ]
)
Err_v_G = np.array(
    [
        point1_G[4, 0] - v_rec1_G,
        point2_G[4, 0] - v_rec2_G,
        point3_G[4, 0] - v_rec3_G,
        point4_G[4, 0] - v_rec4_G,
    ]
)
# print("Erreur reconstruction suivant u (mire Gauche): " + str(Err_u_G))
# print("Erreur reconstruction suivant v (mire Gauche): " + str(Err_v_G))


#######################################################################################################
#
#  .d8888b.  888                                                d8b          d8b
# d88P  Y88b 888                                                Y8P          Y8P
# Y88b.      888
#  "Y888b.   888888  .d88b.  888d888  .d88b.   .d88b.  888  888 888 .d8888b  888  .d88b.  88888b.
#     "Y88b. 888    d8P  Y8b 888P"   d8P  Y8b d88""88b 888  888 888 88K      888 d88""88b 888 "88b
#       "888 888    88888888 888     88888888 888  888 Y88  88P 888 "Y8888b. 888 888  888 888  888
# Y88b  d88P Y88b.  Y8b.     888     Y8b.     Y88..88P  Y8bd8P  888      X88 888 Y88..88P 888  888
#  "Y8888P"   "Y888  "Y8888  888      "Y8888   "Y88P"    Y88P   888  88888P' 888  "Y88P"  888  888
#
#######################################################################################################


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


# objet 1 (point 1)
point1 = camera_2D_3D(
    H_G, H_D, point1_G[3, 0], point1_G[4, 0], point1_D[3, 0], point1_D[4, 0]
)
print(point1)
# objet 2 (point 2)
point2 = camera_2D_3D(
    H_G, H_D, point2_G[3, 0], point2_G[4, 0], point2_D[3, 0], point2_D[4, 0]
)

# distance entre les 2 points de la mire
distance1_2 = math.sqrt(
    (point1[0, 0] - point2[0, 0]) ** 2
    + (point1[1, 0] - point2[1, 0]) ** 2
    + (point1[2, 0] - point2[2, 0]) ** 2
)
print(
    "Distance réelle entre les point 1 et 2 : "
    + str(round(math.sqrt((3 * 0.03) ** 2 + (3 * 0.03) ** 2), 4) * 100)
    + " cm"
)
print(
    "Distance reconstruite entre les point 1 et 2 : "
    + str(round(distance1_2, 4) * 100)
    + " cm"
)

print(H_G)
# np.save("H_G.npy", H_G)
print(H_D)
# np.save("H_D.npy", H_D)
xyz = np.concatenate((x, y, z), axis=1)
# np.save("xyz.npy", xyz)
