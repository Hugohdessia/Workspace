"""Padrão visual: fundo claro, título marrom, verdes -> marrom escuro/tan, amarelo -> vermelho. Uso: src.png saida.png"""
import sys
from PIL import Image
import numpy as np, matplotlib.colors as mc
a = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(float); H, W, _ = a.shape
BGC = np.array([240, 244, 238.]); BROWN = np.array([43, 26, 17.]); TAN = np.array([160, 120, 78.]); RED = np.array([214, 40, 40.]); WHITE = np.array([248, 247, 243.])
hsv = mc.rgb_to_hsv(a / 255); h = hsv[..., 0] * 360; s = hsv[..., 1]; v = hsv[..., 2]
out = a.copy()
panels = [(30, 971, 120, 803), (981, 1851, 120, 803)]
inner = np.zeros((H, W), bool); band = np.zeros((H, W), bool)
for x0, x1, y0, y1 in panels:
    inner[y0 + 10:y1 - 10, x0 + 10:x1 - 10] = True; band[y0:y1, x0:x1] = True
band &= ~inner
# título (texto branco sobre verde) -> marrom
w = np.clip((a.min(-1) - 70) / 150, 0, 1)[..., None]
title = (BGC * (1 - w) + BROWN * w)
outside = ~(inner | band)
out[outside] = title[outside]
cor = band & (s > 0.4) & (v < 0.4)          # cantos arredondados dos cartões
out[cor] = BGC
out[band & ~cor & (a.min(-1) > 200)] = a[band & ~cor & (a.min(-1) > 200)]
# recolor dentro dos cartões
t = np.clip(s / 0.75, 0, 1)[..., None]
green = inner & (h > 70) & (h < 130) & (s > 0.2) & (v < 0.6)
teal = inner & (h >= 130) & (h < 170) & (s > 0.2) & (v < 0.7)
yel = inner & (h > 30) & (h < 62) & (s > 0.2) & (v > 0.6)
base = (a * 0 + WHITE)
for m, c in ((green, BROWN), (teal, TAN), (yel, RED)):
    out[m] = (base * (1 - t) + c * t)[m]
Image.fromarray(out.clip(0, 255).astype(np.uint8)).resize((W * 2, H * 2), Image.LANCZOS).save(sys.argv[2])
