from sympy import *
from sympy.matrices import *

from math import hypot

a = symbols("a", real=True)
phi, th = symbols("phi theta", real=True)

# M * [x y z w].T = [x' y' z' w'].T
M = Matrix([
    [a*a + 1, 0,       0,       -2*a    ],
    [0,       1 - a*a, 0,       0       ],
    [0,       0,       1 - a*a, 0       ],
    [2*a,     0,       0,       -a*a - 1]
])

# th = -atan2(z, x)
Ry = Matrix([
    [cos(th), 0, -sin(th), 0],
    [0,       1, 0,        0],
    [sin(th), 0, cos(th),  0],
    [0,       0, 0,        1]
])

# phi = -atan2(y, hypot(x, z)=x')
Rz = Matrix([
    [cos(phi), -sin(phi), 0, 0],
    [sin(phi), cos(phi),  0, 0],
    [0,        0,         1, 0],
    [0,        0,         0, 1]
])

# P --> Ry->Rz->M->Rz.inv->Ry.inv = P'
MI = simplify(Ry.inv()*Rz.inv()*M*Rz*Ry)

## stereogrpahic + pole (tested):
# let any T be on the circle omega, e.g. C+R*[1 0 0]
# S = A(T) = [2tx 2ty |t|2-1] / (1+|t|2)
# P = [tx ty 1-t], t = (s^2-sz)/(x*sx+y*sy-sz)

# sphere 0,0,0, R=1
# from the north pole 0,0,1
# onto plane z=0
def stereo2plane(x, y, z):
    "stereographic projection from a unit sphere onto a plane, also the point CAN be not on the sphere"
    return (x/(1-z), y/(1-z))

def circle2pole(x, y, r):
    # T = any point on the circle
    tx = x + r
    ty = y
    t2 = tx*tx+ty*ty
    denom = 1 + t2
    (sx, sy, sz) = (2*tx/denom, 2*ty/denom, (t2 - 1)/denom) # = stereographic(T)
    s2 = sx*sx+sy*sy+sz*sz
    t = (s2 - sz)/(x * sx + y * sy - sz)
    P = (t*x, t*y, 1-t)
    return P

def pole2circle(x, y, z, w=1):
    x, y, z = x/w, y/w, z/w
    # st proj: pole->center
    cx, cy = x/(1-z), y/(1-z) # correct formulae even if the pole is not on the sphere
    # T = a point on the polar circle
    d = hypot(x, y)
    p2 = x*x + y*y + z*z
    tz = z/p2 + d * sqrt(p2 - 1)/p2
    if d == 0:
        tx = sqrt(1 - tz*tz)
        ty = 0
    else:
        tx = - x * (z*tz - 1)/(d*d)
        ty = y * tx/x
    sx, sy = tx/(1-tz), ty/(1-tz) # S = st proj T
    r = hypot(cx-sx, cy-sy)
    return (cx, cy, r)

def pole2matrix(x, y, z):
    a0 = sqrt(x*x + y*y + z*z)
    th0 = -atan2(z, x)
    phi0 = -atan2(y, hypot(x, z))
    matrix = MI.xreplace({a:a0, th:th0, phi:phi0})
    return matrix2numpy(matrix)
