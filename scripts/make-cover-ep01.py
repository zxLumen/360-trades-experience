#!/usr/bin/env python3
"""生成 EP01 封面 1080x1440（纯 ctypes + cairo/pango，无第三方依赖）。

用法：python3 scripts/make-cover-ep01.py
输出：assets/covers/EP01-家政保洁-1080x1440.png
"""

import ctypes
import math
import os

CAIRO_FORMAT_ARGB32 = 0
PANGO_SCALE = 1024
PANGO_ALIGN_LEFT = 0
PANGO_ALIGN_CENTER = 1

cairo = ctypes.CDLL("libcairo.so.2")
pango = ctypes.CDLL("libpango-1.0.so.0")
pangocairo = ctypes.CDLL("libpangocairo-1.0.so.0")

# cairo
cairo.cairo_image_surface_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
cairo.cairo_image_surface_create.restype = ctypes.c_void_p
cairo.cairo_create.argtypes = [ctypes.c_void_p]
cairo.cairo_create.restype = ctypes.c_void_p
cairo.cairo_set_source_rgb.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]
cairo.cairo_set_source_rgba.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
cairo.cairo_paint.argtypes = [ctypes.c_void_p]
cairo.cairo_rectangle.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
cairo.cairo_fill.argtypes = [ctypes.c_void_p]
cairo.cairo_arc.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
cairo.cairo_move_to.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
cairo.cairo_line_to.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
cairo.cairo_set_line_width.argtypes = [ctypes.c_void_p, ctypes.c_double]
cairo.cairo_stroke.argtypes = [ctypes.c_void_p]
cairo.cairo_surface_write_to_png.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
cairo.cairo_surface_write_to_png.restype = ctypes.c_int
cairo.cairo_destroy.argtypes = [ctypes.c_void_p]
cairo.cairo_surface_destroy.argtypes = [ctypes.c_void_p]

# pango
pango.pango_font_description_from_string.argtypes = [ctypes.c_char_p]
pango.pango_font_description_from_string.restype = ctypes.c_void_p
pango.pango_font_description_set_absolute_size.argtypes = [ctypes.c_void_p, ctypes.c_double]
pango.pango_font_description_free.argtypes = [ctypes.c_void_p]
pango.pango_layout_set_font_description.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
pango.pango_layout_set_text.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
pango.pango_layout_set_width.argtypes = [ctypes.c_void_p, ctypes.c_int]
pango.pango_layout_set_alignment.argtypes = [ctypes.c_void_p, ctypes.c_int]
pango.pango_layout_get_pixel_size.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
pangocairo.pango_cairo_create_layout.argtypes = [ctypes.c_void_p]
pangocairo.pango_cairo_create_layout.restype = ctypes.c_void_p
pangocairo.pango_cairo_show_layout.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

FONT = b"WenQuanYi Zen Hei"

BG = (0.035, 0.043, 0.059)
YELLOW = (1.0, 0.878, 0.4)      # #FFE066
WHITE = (0.95, 0.96, 0.98)
GRAY = (0.62, 0.66, 0.72)
DARK = (0.04, 0.05, 0.07)


def set_color(cr, rgb, alpha=1.0):
    cairo.cairo_set_source_rgba(cr, rgb[0], rgb[1], rgb[2], alpha)


def draw_text(cr, text, x, y, size, color, alpha=1.0, align="left", width=None):
    layout = pangocairo.pango_cairo_create_layout(cr)
    desc = pango.pango_font_description_from_string(FONT)
    pango.pango_font_description_set_absolute_size(desc, float(size * PANGO_SCALE))
    pango.pango_layout_set_font_description(layout, desc)
    pango.pango_layout_set_text(layout, text.encode("utf-8"), -1)
    if width is not None:
        pango.pango_layout_set_width(layout, int(width * PANGO_SCALE))
        pango.pango_layout_set_alignment(
            layout, PANGO_ALIGN_CENTER if align == "center" else PANGO_ALIGN_LEFT
        )
    set_color(cr, color, alpha)
    cairo.cairo_move_to(cr, x, y)
    pangocairo.pango_cairo_show_layout(cr, layout)
    w = ctypes.c_int()
    h = ctypes.c_int()
    pango.pango_layout_get_pixel_size(layout, ctypes.byref(w), ctypes.byref(h))
    pango.pango_font_description_free(desc)
    return w.value, h.value


def main():
    w, h = 1080, 1440
    surface = cairo.cairo_image_surface_create(CAIRO_FORMAT_ARGB32, w, h)
    cr = cairo.cairo_create(surface)

    # 深色底
    set_color(cr, BG)
    cairo.cairo_paint(cr)

    # 右上角荧光黄斜块
    set_color(cr, YELLOW, 0.10)
    cairo.cairo_move_to(cr, 700, 0)
    cairo.cairo_line_to(cr, 1080, 0)
    cairo.cairo_line_to(cr, 1080, 520)
    cairo.cairo_line_to(cr, 560, 0)
    cairo.cairo_fill(cr)

    # 背景气泡（洗车/清洁的水泡感）
    bubbles = [
        (120, 980, 160, 0.05), (940, 760, 220, 0.04), (820, 1120, 120, 0.05),
        (210, 1220, 90, 0.04), (980, 360, 70, 0.05), (80, 420, 110, 0.03),
    ]
    for x, y, r, a in bubbles:
        set_color(cr, WHITE, a)
        cairo.cairo_arc(cr, x, y, r, 0, 2 * math.pi)
        cairo.cairo_fill(cr)

    # 顶部系列标识
    set_color(cr, YELLOW)
    cairo.cairo_rectangle(cr, 72, 78, 10, 52)
    cairo.cairo_fill(cr)
    draw_text(cr, "360 行体验", 102, 72, 34, WHITE)
    draw_text(cr, "EP01 · 家政保洁", 102, 120, 28, GRAY)

    # 主数字 15
    draw_text(cr, "15", 60, 300, 430, YELLOW, align="center", width=960)
    draw_text(cr, "元", 850, 560, 76, YELLOW)

    # 主标题
    draw_text(cr, "擦一个卫生间，30 分钟", 90, 790, 62, WHITE, align="center", width=900)
    draw_text(cr, "这就是阿姨到手的工钱", 90, 872, 40, GRAY, align="center", width=900)

    # 对比数据
    draw_text(cr, "你付 90/小时 · 阿姨拿 30/小时", 90, 980, 36, WHITE, align="center", width=900)

    # 底部荧光条
    set_color(cr, YELLOW)
    cairo.cairo_rectangle(cr, 72, 1130, 936, 150)
    cairo.cairo_fill(cr)
    draw_text(cr, "这钱，到底谁在赚？", 90, 1160, 52, DARK, align="center", width=900)

    # 底部系列名
    draw_text(cr, "我去干了一个月 · 真人实测", 90, 1330, 26, GRAY, align="center", width=900)

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "covers")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "EP01-家政保洁-1080x1440.png")
    rc = cairo.cairo_surface_write_to_png(surface, out.encode("utf-8"))
    cairo.cairo_destroy(cr)
    cairo.cairo_surface_destroy(surface)
    if rc != 0:
        raise SystemExit(f"write png failed: {rc}")
    print(out)


if __name__ == "__main__":
    main()
