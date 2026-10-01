"""Troca os amarelos das imagens de Endividamento Privado (uso: src.png saida.png) por vermelhos e remove os logos da Nomad."""
import sys
from PIL import Image
import numpy as np, matplotlib.colors as mc
a = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(float); H, W, _ = a.shape
BG = np.array([246, 249, 246.]); RED = np.array([214, 40, 40.]); PAST = np.array([240, 150, 140.])
hsv = mc.rgb_to_hsv(a / 255); h = hsv[..., 0] * 360; s = hsv[..., 1]; v = hsv[..., 2]
yel = (h > 36) & (h < 62) & (v > 0.85)
out = a.copy()
line = yel & (s >= 0.5); k = np.clip((s - 0.3) / 0.3, 0, 1)[..., None]
pale = yel & (s >= 0.12) & (s < 0.5); kp = np.clip(s / 0.45, 0, 1)[..., None]
out[line] = (BG * (1 - k) + RED * k)[line]
out[pale] = (BG * (1 - kp) + PAST * kp)[pale]
out[:int(H*0.125), int(W*0.88):int(W*0.97)] = BG      # logo do topo (círculo amarelo)
out[int(H*0.93):, int(W*0.87):] = BG     # logo de baixo
Image.fromarray(out.clip(0, 255).astype(np.uint8)).resize((W * 2, H * 2), Image.LANCZOS).save(sys.argv[2])
