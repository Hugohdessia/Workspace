"""Recolore a imagem 'Endividamento Privado - Ibovespa': barras em vermelho, realce em vermelho pastel nos setores
mais pressionados (barra pelo menos 0,10 acima da mediana de 6 anos, valores lidos da imagem) e remove o círculo amarelo."""
import sys
from PIL import Image, ImageFilter
import numpy as np, matplotlib.colors as mc
src = sys.argv[1]
im = Image.open(src).convert("RGB"); a = np.asarray(im).astype(float); H, W, _ = a.shape
BG = np.array([246, 249, 246.]); TAN = np.array([186, 172, 152.]); RED = np.array([214, 40, 40.]); PASTEL = np.array([250, 214, 210.])
n = lambda x: np.linalg.norm(x, axis=-1)
nomes = ["Serviços de Comunicação", "Materiais Básicos", "Petróleo e Gás", "Construção Civil", "Varejo", "Tecnologia", "Saúde", "Imobiliário",
         "Consumo Discricionário", "Educação", "Indústria", "Bens de Consumo", "Energia Elétrica e Saneamento"]
cx = [119, 185, 251, 317, 383, 449, 515, 580, 646, 712, 778, 844, 909]
topo = [357, 326, 350, 203, 266, 333, 265, 281, 311, 213, 296, 248, 271]
marc = [345.5, 360, 395.5, 320.5, 279.5, 370.5, 278.5, 309.5, 299.5, 209.5, 291.5, 296.5, 338]
v = lambda y: (459 - y) / 352.5          # eixo: 0 em y=459 e 0,8 em y=177
folga = [v(t) - v(m) for t, m in zip(topo, marc)]
press = [i for i, f in enumerate(folga) if f >= 0.095]
print("pressionados:", [(nomes[i], round(folga[i], 2)) for i in press])
hsv = mc.rgb_to_hsv(a / 255); h = hsv[..., 0] * 360; s = hsv[..., 1]; vv = hsv[..., 2]
tan = (h > 25) & (h < 50) & (s > 0.10) & (s < 0.55) & (vv > 0.58) & (vv < 0.92)
reg = np.zeros((H, W), bool); reg[168:470, :] = True; reg[180:200, 340:370] = True
mask = tan & reg
alpha = np.clip(n(a - BG) / n(TAN - BG), 0, 1)[..., None]
out = a.copy(); out[mask] = (BG * (1 - alpha) + RED * alpha)[mask]
w = np.clip(1 - n(out - BG) / 45, 0, 1)[..., None]
for i in press:
    band = np.zeros((H, W), bool); band[198:507, cx[i] - 33:cx[i] + 34] = True
    out[band] = (out * (1 - w) + PASTEL * w)[band]
yl = (h > 28) & (h < 68) & (s > 0.20) & (vv > 0.75); yl[70:, :] = False; yl[:, :int(W * 0.8)] = False
ym = np.asarray(Image.fromarray((yl * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(11))) > 0; ym[70:, :] = False; ym[:, :int(W * 0.8)] = False
out[ym] = BG
Image.fromarray(out.clip(0, 255).astype(np.uint8)).resize((W * 2, H * 2), Image.LANCZOS).save("endividamento_privado_ibovespa_vermelho.png")
