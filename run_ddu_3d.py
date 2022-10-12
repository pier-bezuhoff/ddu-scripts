
class Sphere:
    def __init__(self, x, y, z, r, color=0x000000, fill=False, visible=False, rule=[]):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        # in ddu: base10 BBGGRR / here: hex RRGGBB
        self.color = color
        self.fill = fill
        self.visible = visible
        self.rule = rule

    # invert *self* with respect to *sphere*
    def invert(self, sphere):
        dx, dy, dz = self.x - sphere.x, self.y - sphere.y, self.z - sphere.z
        d = sqrt(dx*dx + dy*dy + dz*dz)
        ratio = sphere.r * sphere.r / (d*d - self.r * self.r)
        self.x = sphere.x + ratio * dx
        self.y = sphere.y + ratio * dy
        self.z = sphere.z + ratio * dz
        self.r = abs(self.r * ratio)

    def show():
        pass # display in blender


def step(spheres, all_spheres=[]):
    new_spheres = [copy(shpere) for sphere in spheres]
    for new_sphere in new_spheres:
        for j in new_sphere.rule:
            new_sphere.invert(spheres[j])
        new_sphere.show()
    return (new_spheres, spheres + all_spheres)


winter_spheres = [
    Sphere(-920.753173828125, 1866.708740234375, 0, 1859.665708492877),
    Sphere(-901.8592529296875, 1878.81103515625, 0, 1854.104930797163),
    Sphere(468.9537048339844, 340.31658935546875, 0, 339.07684691208505, rule=[0,1]),
    Sphere(468.5248718261719, 345.0711669921875, 0, 335.5959384049609, rule=[0,1]),
    Sphere(1388.179443359375, -3772.58935546875, 0, 4538.483459205404, rule=[2,3,0,1]),
    Sphere(1767.4017333984375, -5054.71484375, 0, 5872.806895318434, rule=[2,3,0,1]),
    Sphere(677.2852783203125, 879.8759765625, 0, 63.33096624273902, color=0x200020, fill=True, visible=True, rule=[4,5,4,5,2,3,0,1]),
    Sphere(663.2559814453125, 889.6435546875, 0, 56.01607696333538, color=0x0000ff, fill=True, visible=True, rule=[4,5,4,5,2,3,0,1]),
    Sphere(369.8866882324219, 806.8751220703125, 0, 299.7592443917674, color=0x80ffff, visible=True, rule=[4,5,4,5,2,3,0,1])
]

