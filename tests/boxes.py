import ctypes
import os

from pyglet.gl import *
from pywavefront import visualization, Wavefront

window = pyglet.window.Window(width=1280, height=720, resizable=True)

root_path = os.path.dirname(__file__)

box1 = Wavefront(os.path.join(root_path, "data/box/box-V3F.obj"))
box2 = Wavefront(os.path.join(root_path, "data/box/box-C3F_V3F.obj"))
box3 = Wavefront(os.path.join(root_path, "data/box/box-N3F_V3F.obj"))
box4 = Wavefront(os.path.join(root_path, "data/box/box-T2F_V3F.obj"))
box5 = Wavefront(os.path.join(root_path, "data/box/box-T2F_C3F_V3F.obj"))
box6 = Wavefront(os.path.join(root_path, "data/box/box-T2F_N3F_V3F.obj"))

rotation = 0.0
lightfv = ctypes.c_float * 4


@window.event
def on_resize(width, height):
    viewport_width, viewport_height = window.get_framebuffer_size()
    glViewport(0, 0, viewport_width, viewport_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_draw():
    window.clear()
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))

    draw_box(box1, -4.0, 2.0)
    draw_box(box2, 0.0, 2.0)
    draw_box(box3, 4.0, 2.0)

    draw_box(box4, -4.0, -2.0)
    draw_box(box5, 0.0, -2.0)
    draw_box(box6, 4.0, -2.0)


def draw_box(box, x, y):
    glLoadIdentity()
    glTranslated(x, y, -10.0)
    glRotatef(rotation, 0.0, 1.0, 0.0)
    glRotatef(-25.0, 1.0, 0.0, 0.0)
    glRotatef(45.0, 0.0, 0.0, 1.0)

    visualization.draw(box)


def update(dt):
    global rotation
    rotation += 90.0 * dt

    if rotation > 720.0:
        rotation = 0.0


pyglet.clock.schedule(update)
pyglet.app.run()
