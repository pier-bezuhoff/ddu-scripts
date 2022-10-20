from __future__ import division
from sympy import *
from sympy.matrices import *
from sympy.physics.quantum import TensorProduct
import itertools as it

# NOTE: reference
# http://www.r-5.org/files/books/computers/algo-list/image-processing/vision/Richard_Hartley_Andrew_Zisserman-Multiple_View_Geometry_in_Computer_Vision-EN.pdf
# page ~108

init_printing()

k = symbols("k:5", real=True)
(xa,ya,za) = symbols("x_a y_a z_a", real=True)
(x,y,z) = symbols("x y z", real=True)
M = Matrix(MatrixSymbol("M", 4, 4))
ms = symbols("m:16", real=True)

def vec(x,y,z,w=1):
    return Matrix([[x],[y],[z],[w]])

def act(v0, v):
    return TensorProduct(Matrix.hstack(-eye(3), v[:-1,:]), v0.T)
# [3x16]

def fix(v0):
    return act(v0, v0)

O = vec(0,0,0) # the center of the R=1 sphere
A = vec(xa,ya,za)
X = vec(x,y,z)

d = sqrt(xa*xa + ya*ya + za*za)
# I = A/d/d = p_A intersects AO
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
    act(vec(xa/d, ya/d, za/d), vec(-xa/d, -ya/d, -za/d)), # NB: -v != v(-x,-y,-z) bc of w
    fix(A),
    fix(P_left),
    fix(P_right),
    fix(P_top)
) # [15x16]
M_v = Matrix(list(ms)) # [16x1]
res = trans * M_v # [15x1]
# eq = Eq(trans * M_v, zeros(15, 1))
# r = solve(eq, list(M))
eqs = [Eq(row, 0) for row in trans * M_v]
#r = solve(eqs, list(M[1:]))
#M_result = M.xreplace(r).xreplace({ks[0],1})


xs = symbols("x:4")
ys = symbols("y:4")
X = Array(xs, (4,))
Y = Array(ys, (4,))
H = Array(M.tolist(), (4, 4))
Hx = tensorcontraction(tensorproduct(H, X), (1, 2))
yHx = tensorproduct(Y[:-1], Hx[:-1]) # throw away 'w' cuz we only check collinearity
lc3 = Array((LeviCivita(i, j, k) for (i, j, k) in it.product(range(3), range(3), range(3))), (3, 3, 3))
vp = tensorcontraction(tensorcontraction(tensorproduct(lc3, yHx), (2, 4)), (1, 2))
# for every pair of points #n every entry in vp is 0
def rel(x0, y0, z0, x, y, z):
    return {xs[0]: x0, xs[1]: y0, xs[2]: z0, xs[3]: 1,
            ys[0]: x, ys[1]: y, ys[2]: z, ys[3]: 1}
def fixp(p):
    x, y, z, w = p
    return rel(x,y,z, x,y,z)
Ps = [
    rel(xa/d, ya/d, xa/d, -xa/d, -ya/d, -za/d),
    fixp(A),
    fixp(P_left),
    fixp(P_right),
    fixp(P_top)
]
eqs = []
for r in Ps:
    for row in vp:
        eqs.append(Eq(row.xreplace(r), 0))
