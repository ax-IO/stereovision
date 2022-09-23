//TP Calibration
//Novembre 2020
//J. Triboulet

clear;//nettoyage variable
clc;//page blanche 

//donnees 3D de calibration en metres
x=[0	0	0	0	0	0	0.03	0.27	0.03	0.27	0.03	0.27]';
y=[0.36	0.36	0.18	0.18	0	0	0.36	0.36	0.18	0.18	0	0]';
z=[0.27	0.03	0.27	0.03	0.27	0.03	0	0	0	0	0	0]';

//donnees 2D de calibration en pixels camera DROITE
u_D=[260	649	262	650	265	651	731	1122	732	1125	732	1123]';
v_D=[54	111	459	456	861	799	111	52	456	456	799	858]';

//donnees 2D de calibration en pixels camera GAUCHE
u_G=[190	567	193	569	197	570	649	1054	651	1057	652	1056]';
v_G=[61	123	473	470	882	814	123	68	469	469	813	867]';

// construction des elements associes au systeme
// A_D.X_D=B_D
//A..
//B...
// X les inconnues du modele global

// nombre de point de calibration
n=size(x,1);
// vecteur B_D
B_D=[u_D;v_D];

//Matrice A_D
A_D=[x,y,z,ones(n,1),zeros(n,4),-u_D.*x,-u_D.*y,-u_D.*z;
    zeros(n,4),x,y,z,ones(n,1),-v_D.*x,-v_D.*y,-v_D.*z];

// Calcul de X=pinv(A).B
X_D=pinv(A_D)*B_D;

// Modele global de la camera D

H_D=[X_D(1:4)';
X_D(5:8)';
X_D(9:11)',1]

// pour tous les points
uvs_rec_D=H_D*[x';y';z';ones(1,12)];
//suivant u
u_rec_D=uvs_rec_D(1,1:n)./uvs_rec_D(3,1:n);
u_rec_D=u_rec_D'
//suivant v
v_rec_D=uvs_rec_D(2,1:n)./uvs_rec_D(3,1:n);
v_rec_D=v_rec_D'

// CALCUL ERREURS

// erreur suivant u
Err_u_D=u_D-u_rec_D;

// erreur suivant v
Err_v_D=v_D-v_rec_D;

// erreur maximale u_D
max(Err_u_D)

// erreur maximale v_D
max(Err_v_D)

//.erreur.minimale.u_D
min(Err_u_D)

// erreur minimale v_D
min(Err_v_D)

// erreur moyenne u_D
mean(Err_u_D)

// erreur moyenne v_D
mean(Err_v_D)

// erreur ecart-type u_D
stdev(Err_u_D)

// erreur ecart-type v_D
stdev(Err_v_D)

// Erreur moyenne suivant u
mean(Err_u_D)

// Erreur moyenne suivant v
mean(Err_v_D)

// Ecart-type suivant u
stdev(Err_u_D)

// Ecart-type suivant v
stdev(Err_v_D)

// Test  points (Mire Droite)
// pointx=[x y z u_D v_D]
point1=[0 0.12 0.15 472 581];
point2=[0.15 0.24 0 913 332];
point3=[0 0.3 0.21 370 199];
point4=[0.21 0.06 0 1014 714];


// POINT 1
uvrec1_D=H_D*[point1(1);point1(2);point1(3);1];
//u
point1(4)
//u reconstruite
u_rec1_D=uvrec1_D(1)/uvrec1_D(3)
//v
point1(5)
//v reconstruite
v_rec1_D=uvrec1_D(2)/uvrec1_D(3)

// POINT 2
uvrec2_D=H_D*[point2(1);point2(2);point2(3);1];
//u
point2(4)
//u reconstruite
u_rec2_D=uvrec2_D(1)/uvrec2_D(3)
//v
point2(5)
//v reconstruite
v_rec2_D=uvrec2_D(2)/uvrec2_D(3)

// POINT 3
uvrec3_D=H_D*[point3(1);point3(2);point3(3);1];
//u
point3(4)
//u reconstruite
u_rec3_D=uvrec3_D(1)/uvrec3_D(3)
//v
point3(5)
//v reconstruite
v_rec3_D=uvrec3_D(2)/uvrec3_D(3)

// POINT 4
uvrec4_D=H_D*[point4(1);point4(2);point4(3);1];
//u
point4(4)
//u reconstruite
u_rec4_D=uvrec4_D(1)/uvrec4_D(3)
//v
point4(5)
//v reconstruite
v_rec4_D=uvrec4_D(2)/uvrec4_D(3)

Err_u=[point1(4) - u_rec1_D; point2(4) - u_rec2_D ; 
       point3(4) - u_rec3_D;point4(4) - u_rec4_D]
Err_v=[point1(5) - v_rec1_D;point2(5) - v_rec2_D;
       point3(5) - v_rec3_D;point4(5) - v_rec4_D]

// construction des elements associes au systeme
// A_G.X_G=B_G
//A..
//B...
// X les inconnues du modele global

// nombre de point de calibration
n=size(x,1);
// vecteur B_G
B_G=[u_G;v_G];

//Matrice A_G
A_G=[x,y,z,ones(n,1),zeros(n,4),-u_G.*x,-u_G.*y,-u_G.*z;
    zeros(n,4),x,y,z,ones(n,1),-v_G.*x,-v_G.*y,-v_G.*z];

// Calcul de X=pinv(A).B
X_G=pinv(A_G)*B_G;

// Modele global de la camera G

H_G=[X_G(1:4)';
X_G(5:8)';
X_G(9:11)',1]

// pour tous les points
uvrec_G=H_G*[x';y';z';ones(1,12)];
//suivant u
u_rec_G=uvrec_G(1,1:n)./uvrec_G(3,1:n)

//suivant v
v_rec_G=uvrec_G(2,1:n)./uvrec_G(3,1:n)


// CALCUL ERREURS

// erreur suivant u
Err_u_G=u_G-u_rec_G';

// erreur suivant v
Err_v_G=v_G-v_rec_G';

// erreur maximale u_G
max(Err_u_G)

// erreur maximale v_G
max(Err_v_G)

//.erreur.minimale.u_G
min(Err_u_G)

// erreur minimale v_G
min(Err_v_G)

// erreur moyenne u_G
mean(Err_u_G)

// erreur moyenne v_G
mean(Err_v_G)

// erreur ecart-type u_G
stdev(Err_u_G)

// erreur ecart-type v_G
stdev(Err_v_G)

// Test  points (Mire Gauche)
// pointx=[x y z u_G v_G]
point1=[0 0.12 0.15 398 596];
point2=[0.15 0.24 0 839 345];
point3=[0 0.3 0.21 298 210];
point4=[0.21 0.06 0 944 725];

// POINT 1
uvrec1_G=H_G*[point1(1);point1(2);point1(3);1];
//u
point1(4)
//u reconstruite
u_rec1_G=uvrec1_G(1)/uvrec1_G(3)
//v
point1(5)
//v reconstruite
v_rec1_G=uvrec1_G(2)/uvrec1_G(3)

// POINT 2
uvrec2_G=H_G*[point2(1);point2(2);point2(3);1];
//u
point2(4)
//u reconstruite
u_rec2_G=uvrec2_G(1)/uvrec2_G(3)
//v
point2(5)
//v reconstruite
v_rec2_G=uvrec2_G(2)/uvrec2_G(3)

// POINT 3
uvrec3_G=H_G*[point3(1);point3(2);point3(3);1];
//u
point3(4)
//u reconstruite
u_rec3_G=uvrec3_G(1)/uvrec3_G(3)
//v
point3(5)
//v reconstruite
v_rec3_G=uvrec3_G(2)/uvrec3_G(3)

// POINT 4
uvrec4_G=H_G*[point4(1);point4(2);point4(3);1];
//u
point4(4)
//u reconstruite
u_rec4_G=uvrec4_G(1)/uvrec4_G(3)
//v
point4(5)
//v reconstruite
v_rec4_G=uvrec4_G(2)/uvrec4_G(3)

Err_u=[point1(4) - u_rec1_G; point2(4) - u_rec2_G ; 
       point3(4) - u_rec3_G;point4(4) - u_rec4_G]
Err_v=[point1(5) - v_rec1_G;point2(5) - v_rec2_G;
       point3(5) - v_rec3_G;point4(5) - v_rec4_G]

// STEREOVISION

function [x,y,z]=camera_2D_3D(H_G,H_D,u_G,v_G,u_D,v_D)
 A(1,:)=[(H_G(1,1)-H_G(3,1)*u_G),(H_G(1,2)-H_G(3,2)*u_G),(H_G(1,3)-H_G(3,3)*u_G)];
 A(2,:)=[(H_G(2,1)-H_G(3,1)*v_G),(H_G(2,2)-H_G(3,2)*v_G),(H_G(2,3)-H_G(3,3)*v_G)];
 A(3,:)=[(H_D(1,1)-H_D(3,1)*u_D),(H_D(1,2)-H_D(3,2)*u_D),(H_D(1,3)-H_D(3,3)*u_D)];
 A(4,:)=[(H_D(2,1)-H_D(3,1)*v_D),(H_D(2,2)-H_D(3,2)*v_D),(H_D(2,3)-H_D(3,3)*v_D)];

 B(1)=[H_G(3,4)*u_G-H_G(1,4)];
 B(2)=[H_G(3,4)*v_G-H_G(2,4)] ;   
 B(3)=[H_D(3,4)*u_D-H_D(1,4)];
 B(4)=[H_D(3,4)*v_D-H_D(2,4)] ;   

// Points 3D reconstruits
 X=pinv(A)*B;
 x=X(1);
 y=X(2);
 z=X(3);
endfunction

//objet 1 (point 1)
[xrec1, yrec1, zrec1]=camera_2D_3D(H_G,H_D,190, 61,260,54)
obj_1=[xrec1 yrec1 zrec1]

//objet 2 (point 2)
[xrec2, yrec2, zrec2]=camera_2D_3D(H_G,H_D,567, 123,649, 111)
obj_2=[xrec2 yrec2 zrec2]

// distance entre les 2 points de la mire
distance1_2=sqrt((obj_1(1)-obj_2(1))^2+(obj_1(2)-obj_2(2))^2+(obj_1(3)-obj_2(3))^2)
    
//objet 3 (point 1 boite)
[xrec3, yrec3, zrec3]=camera_2D_3D(H_G,H_D,555, 583,619,569)
obj_3=[xrec3 yrec3 zrec3]

//objet 4 (point 2 boite)
[xrec4, yrec4, zrec4]=camera_2D_3D(H_G,H_D,717, 569,792, 557)
obj_4=[xrec4 yrec4 zrec4]

// distance entre les 2 points sur la boite(calcul d'arrête)
// vraie longueur = 0.13m
arrete3_4=sqrt((obj_3(1)-obj_4(1))^2+(obj_3(2)-obj_4(2))^2+(obj_3(3)-obj_4(3))^2)

//objet 5 (point 1 pikachu)
[xrec5, yrec5, zrec5]=camera_2D_3D(H_G,H_D,556, 586,618,572)
obj_5=[xrec5 yrec5 zrec5]

//objet 6 (point 2 pikachu)
[xrec6, yrec6, zrec6]=camera_2D_3D(H_G,H_D,720, 573,794, 559)
obj_6=[xrec6 yrec6 zrec6]

// distance entre les 2 points sur le pikachu(calcul d'arrête)
// vraie longueur = m
arrete5_6=sqrt((obj_5(1)-obj_6(1))^2+(obj_5(2)-obj_6(2))^2+(obj_5(3)-obj_6(3))^2)
