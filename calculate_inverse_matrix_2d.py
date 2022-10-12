from __future__ import division
from sympy import *
from sympy.matrices import *
from sympy.physics.quantum import TensorProduct

init_printing()

k = symbols("k:4", real=True)
(xa,ya) = symbols("x_a y_a", real=True)
(x,y) = symbols("x y", real=True)
M = Matrix(MatrixSymbol("M", 3, 3))

def vec(x,y,w=1):
    return Matrix([[x],[y],[w]])

def act(v0, v):
    return TensorProduct(Matrix.hstack(-eye(2), v[:-1,:]), v0.T)

def fix(v0):
    return act(v0, v0)

O = vec(0,0) # center of the R=1 sphere
A = vec(xa,ya)
X = vec(x,y)

d = sqrt(xa*xa + ya*ya)
# I = A/d/d = p_A intersect AO
(xa0, ya0) = (xa/d/d, ya/d/d)
P_left = vec(xa0 - ya, ya0 + xa)
P_right = vec(xa0 + ya, ya0 - xa)

trans = Matrix.vstack(
    act(vec(xa/d, ya/d), vec(-xa/d, -ya/d)),
    fix(A),
    fix(P_left),
    fix(P_right),
)
trans1 = Matrix.vstack(trans, ones(1, 9)/9)
M_v = Matrix(list(M))
eq = Eq(trans1 * M_v, Matrix.vstack(zeros(8, 1), eye(1)))

# NOTE: works, incredibly slow
#r = solve(eq, list(M))
#M_result = M.xreplace(r)
