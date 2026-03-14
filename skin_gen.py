import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import random
# Usiamo la nuova libreria che non richiede compilatori C++
from perlin_noise import PerlinNoise 

# --- LOGICA DI GENERAZIONE ---
def genera_skin_completa(base_color_rgb, eye_color_rgb, include_mouth):
    """Genera una skin Minecraft 64x64 mappata su ogni lato dei cubi."""
    canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Inizializziamo il rumore di Perlin (octaves=4 per un effetto roccioso)
    noise = PerlinNoise(octaves=4, seed=random.randint(1, 99999))
    
    # MAPPA COORDINATE UFFICIALE (Layout 64x64 Moderno)
    mappa = {
        "testa": [(8, 0, 16, 8), (16, 0, 24, 8), (8, 8, 16, 16), (24, 8, 32, 16), (0, 8, 8, 16), (16, 8, 24, 16)],
        "corpo": [(20, 16, 28, 20), (28, 16, 36, 20), (20, 20, 28, 32), (32, 20, 40, 32), (16, 20, 20, 32), (28, 20, 32, 32)],
        "braccio_dx": [(44, 16, 48, 20), (48, 16, 52, 20), (44, 20, 48, 32), (52, 20, 56, 32), (40, 20, 44, 32), (48, 20, 52, 32)],
        "gamba_dx": [(4, 16, 8, 20), (8, 16, 12, 20), (4, 20, 8, 32), (12, 20, 16, 32), (0, 20, 4, 32), (8, 20, 12, 32)],
        # Braccio e Gamba sinistra (nuovo layout)
        "braccio_sx": [(36, 48, 40, 52), (40, 48, 44, 52), (36, 52, 40, 64), (44, 52, 48, 64), (32, 52, 36, 64), (40, 52, 44, 64)],
        "gamba_sx": [(20, 48, 24, 52), (24, 48, 28, 52), (20, 52, 24, 64), (28, 52, 32, 64), (16, 52, 20, 64), (24, 52, 28, 64)]
    }
    
    # 1. GENERAZIONE TEXTURE
    for parte, lista_coords in mappa.items():
        for coords in lista_coords:
            x1, y1, x2, y2 = coords
            for x in range(x1, x2):
                for y in range(y1, y2):
                    # Calcolo del rumore
                    n_val = noise([x/10, y/10])
                    # Variazione colore
                    r = max(0, min(255, int(base_color_rgb[0] + n_val * 45)))
                    g = max(0, min(255, int(base_color_rgb[1] + n_val * 25)))
                    b = max(0, min(255, int(base_color_rgb[2] + n_val * 25)))
                    canvas.putpixel((x, y), (r, g, b, 255))
    
    # 2. DETTAGLI VISO (Fronte della testa)
    # Occhi
    canvas.putpixel((10, 12), eye_color_rgb + (255,))
    canvas.putpixel((13, 12), eye_color_rgb + (255,))
    
    # Bocca
    if include_mouth:
        dark_red = (int(base_color_rgb[0]*0.3), 0, 0, 255)
        draw.rectangle([11, 14, 12, 14], fill=dark_red)
        
    return canvas

# --- INTERFACCIA ---
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Skin Gen")
        self.root.geometry("400x600")
        self.root.configure(bg="#1a1a1a")

        self.color_body = (150, 0, 0)
        self.color_eyes = (0, 255, 255)
        self.skin = None

        tk.Label(root, text="NETHER SKIN FACTORY", fg="red", bg="#1a1a1a", font=("Impact", 20)).pack(pady=20)
        
        tk.Button(root, text="Scegli Colore Corpo", command=self.set_body).pack(pady=5)
        tk.Button(root, text="Scegli Colore Occhi", command=self.set_eyes).pack(pady=5)
        
        self.chk_bocca = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Mostra Bocca", variable=self.chk_bocca, bg="#1a1a1a", fg="white").pack()

        tk.Button(root, text="⚡ GENERA ⚡", command=self.run, bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        
        self.l_prev = tk.Label(root, bg="#333")
        self.l_prev.pack(pady=10)
        
        tk.Button(root, text="💾 Salva Skin", command=self.save, bg="green", fg="white").pack(pady=10)

    def set_body(self):
        c = colorchooser.askcolor()[0]
        if c: self.color_body = tuple(map(int, c))

    def set_eyes(self):
        c = colorchooser.askcolor()[0]
        if c: self.color_eyes = tuple(map(int, c))

    def run(self):
        self.skin = genera_skin_completa(self.color_body, self.color_eyes, self.chk_bocca.get())
        img = self.skin.resize((160, 160), Image.NEAREST)
        self.tk_img = ImageTk.PhotoImage(img)
        self.l_prev.config(image=self.tk_img)

    def save(self):
        if self.skin:
            f = filedialog.asksaveasfilename(defaultextension=".png")
            if f: self.skin.save(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()