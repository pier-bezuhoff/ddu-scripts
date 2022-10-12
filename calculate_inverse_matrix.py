from __future__ import division
from sympy import *
from sympy.matrices import *
from sympy.physics.quantum import TensorProduct

# NOTE: reference
# http://www.r-5.org/files/books/computers/algo-list/image-processing/vision/Richard_Hartley_Andrew_Zisserman-Multiple_View_Geometry_in_Computer_Vision-EN.pdf
# page ~108

init_printing()

k = symbols("k:5", real=True)
(xa,ya,za) = symbols("x_a y_a z_a", real=True)
(x,y,z) = symbols("x y z", real=True)
M = Matrix(MatrixSymbol("M", 4, 4))

def vec(x,y,z,w=1):
    return Matrix([[x],[y],[z],[w]])

def act(v0, v):
    return TensorProduct(Matrix.hstack(-eye(3), v[:-1,:]), v0.T)

def fix(v0):
    return act(v0, v0)

O = vec(0,0,0) # center of the R=1 sphere
A = vec(xa,ya,za)
X = vec(x,y,z)

d = sqrt(xa*xa + ya*ya + za*za)
# I = A/d/d = p_A intersect AO
(xa0, ya0, za0) = (xa/d/d, ya/d/d, za/d/d)
P_left = vec(xa0 - ya, ya0 + xa, za0)
P_right = vec(xa0 + ya, ya0 - xa, za0)
P_top = vec(xa0, ya0 + za, za0 - ya)

# eq0 = Eq(M * vec(xa/d, ya/d, za/d), k[0] * vec(-xa/d, -ya/d, -za/d)) # 1 -> -1
# eq1 = fix(A, k[1])
# eq2 = fix(P_left, k[2])
# eq3 = fix(P_right, k[3])
# eq4 = fix(P_top, k[4])
# eqs = [eq0,eq1,eq2,eq3,eq4]

trans = Matrix.vstack(
    act(vec(xa/d, ya/d, za/d), vec(-xa/d, -ya/d, -za/d)),
    fix(A),
    fix(P_left),
    fix(P_right),
    fix(P_top)
)
M_v = Matrix(list(M))
eq = Eq(trans * M_v, zeros(15, 1))

r = solve(eq, list(M))
# M_result = M.xreplace(r).xreplace({ks[0],1})
