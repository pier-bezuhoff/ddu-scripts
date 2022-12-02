from math import hypot
from sympy import symbols, atan2, sqrt, sin, cos, Matrix, simplify
from sympy.matrices import matrix2numpy

a, k = symbols("a k", real=True)
phi, th = symbols("phi theta", real=True)

# M * [x y z w].T = [x' y' z' w'].T
# k = scaling/sphere radius
M = Matrix([
    [a*a + 1, 0,       0,       -2*a*k  ],
    [0,       1 - a*a, 0,       0       ],
    [0,       0,       1 - a*a, 0       ],
    [2*a/k,   0,       0,       -a*a - 1]
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

# R here and onwards is the sphere radius
def circle2pole(x, y, r, R=1):
    x /= R
    y /= R
    r /= R
    # T = any point on the circle
    tx = x + r
    ty = y
    d = 1 + tx*tx + ty*ty
    (sx, sy, sz) = (2*tx/d, 2*ty/d, (d - 2)/d) # = stereographic(T)
    k = (1 - sz)/(x * sx + y * sy - sz)
    P = (k*x *R, k*y *R, (1-k) *R)
    return P

def pole2circle(x, y, z, w=1, R=1):
    w *= R
    x, y, z = x/w, y/w, z/w
    nz = 1 - z
    # st proj: pole->center
    cx, cy = x/nz, y/nz # correct formulae even if the pole is not on the sphere
    op2 = x*x + y*y + z*z
    r: float = sqrt(op2 - 1)/abs(nz)
    return (cx *R, cy *R, r *R)

def pole2matrix(x, y, z, R=1):
    a0 = sqrt(x*x + y*y + z*z)
    th0 = -atan2(z, x)
    phi0 = -atan2(y, hypot(x, z))
    matrix = MI.xreplace({a:a0, k:R, th:th0, phi:phi0})
    return matrix2numpy(matrix)

def pole2xyz(pole):
    (x,), (y,), (z,), (w,) = pole
    return (x/w, y/w, z/w)
