import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageTk

# --- Data Models ---
class Trait:
    def __init__(self, name, shape, color, size, position):
        self.name = name
        self.shape = shape  # 'oval', 'rectangle', 'triangle', etc.
        self.color = color
        self.size = size  # (width, height)
        self.position = position  # (x, y)

class Animal:
    def __init__(self):
        self.traits = []

    def add_trait(self, trait):
        self.traits.append(trait)

    def remove_trait(self, trait_name):
        self.traits = [t for t in self.traits if t.name != trait_name]

    def get_trait(self, trait_name):
        for t in self.traits:
            if t.name == trait_name:
                return t
        return None

# --- GUI ---
class AnimalGeneLabApp:
    CANVAS_SIZE = 400
    def __init__(self, root):
        self.root = root
        self.root.title("Animal Gene Lab (Prototype)")
        self.animal = Animal()
        self.setup_default_traits()
        self.create_widgets()
        self.draw_animal()

    def setup_default_traits(self):
        # Start with a basic body
        body = Trait('Body', 'oval', '#deb887', (180, 120), (110, 140))
        self.animal.add_trait(body)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=self.CANVAS_SIZE, height=self.CANVAS_SIZE, bg='white')
        self.canvas.grid(row=0, column=0, rowspan=8)

        # Trait controls
        tk.Label(self.root, text="Add Trait:").grid(row=0, column=1, sticky='w')
        self.trait_var = tk.StringVar(value='Wings')
        trait_options = ['Wings', 'Tail', 'Ears']
        self.trait_menu = tk.OptionMenu(self.root, self.trait_var, *trait_options)
        self.trait_menu.grid(row=1, column=1, sticky='w')
        tk.Button(self.root, text="Add", command=self.add_trait).grid(row=2, column=1, sticky='w')

        tk.Label(self.root, text="Remove Trait:").grid(row=3, column=1, sticky='w')
        self.remove_var = tk.StringVar(value='Wings')
        self.remove_menu = tk.OptionMenu(self.root, self.remove_var, *trait_options)
        self.remove_menu.grid(row=4, column=1, sticky='w')
        tk.Button(self.root, text="Remove", command=self.remove_trait).grid(row=5, column=1, sticky='w')

        tk.Label(self.root, text="Manipulate Trait:").grid(row=6, column=1, sticky='w')
        tk.Button(self.root, text="Change Color", command=self.change_trait_color).grid(row=7, column=1, sticky='w')

    def add_trait(self):
        name = self.trait_var.get()
        if self.animal.get_trait(name):
            return  # Already exists
        if name == 'Wings':
            trait = Trait('Wings', 'rectangle', '#b0c4de', (120, 40), (70, 100))
        elif name == 'Tail':
            trait = Trait('Tail', 'rectangle', '#8b4513', (20, 80), (250, 220))
        elif name == 'Ears':
            trait = Trait('Ears', 'triangle', '#deb887', (40, 40), (120, 100))
        else:
            return
        self.animal.add_trait(trait)
        self.draw_animal()

    def remove_trait(self):
        name = self.remove_var.get()
        self.animal.remove_trait(name)
        self.draw_animal()

    def change_trait_color(self):
        name = self.trait_var.get()
        trait = self.animal.get_trait(name)
        if not trait:
            return
        color = colorchooser.askcolor(title=f"Choose color for {name}")[1]
        if color:
            trait.color = color
            self.draw_animal()

    def draw_animal(self):
        # Draw on PIL image, then display on Tkinter canvas
        img = Image.new('RGBA', (self.CANVAS_SIZE, self.CANVAS_SIZE), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        for trait in self.animal.traits:
            self.draw_trait(draw, trait)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)

    def draw_trait(self, draw, trait):
        x, y = trait.position
        w, h = trait.size
        if trait.shape == 'oval':
            draw.ellipse([x, y, x + w, y + h], fill=trait.color, outline='black')
        elif trait.shape == 'rectangle':
            draw.rectangle([x, y, x + w, y + h], fill=trait.color, outline='black')
        elif trait.shape == 'triangle':
            # Draw an upward triangle
            points = [(x + w // 2, y), (x, y + h), (x + w, y + h)]
            draw.polygon(points, fill=trait.color, outline='black')

if __name__ == '__main__':
    root = tk.Tk()
    app = AnimalGeneLabApp(root)
    root.mainloop()