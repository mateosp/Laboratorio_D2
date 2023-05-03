import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = {}
    
    def add_edge(self, node, weight=0):
        self.edges[node] = weight
    
    def remove_edge(self, node):
        del self.edges[node]

class Graph:
    def __init__(self):
        self.nodes = []
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def remove_node(self, node):
        self.nodes.remove(node)
        for n in self.nodes:
            if node in n.edges:
                n.remove_edge(node)
    
    def draw(self, canvas):
        for node in self.nodes:
            for neighbor, weight in node.edges.items():
                canvas.create_line(node.x, node.y, neighbor.x, neighbor.y)
                canvas.create_text((node.x + neighbor.x) / 2, (node.y + neighbor.y) / 2, text=weight)
            canvas.create_oval(node.x-10, node.y-10, node.x+10, node.y+10, fill='white')
            canvas.create_text(node.x, node.y, text=str(self.nodes.index(node)))
            
class App:
    def __init__(self, master):
        self.master = master
        master.title('Graph Editor')
        
        self.graph = Graph()
        self.selected = None

        image = ImageTk.PhotoImage(Image.open('imagenes/mapa.png'))
        
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor='nw', image = image)

        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        
        add_button = tk.Button(master, text='Add Node', command=self.add_node)
        add_button.pack(side='left')
        remove_button = tk.Button(master, text='Remove', command=self.remove)
        remove_button.pack(side='left')
        
        self.weight_entry = tk.Entry(master)
        self.weight_entry.pack(side='left')
        
        self.draw()
        
    def draw(self):
        self.canvas.delete('all')
        self.graph.draw(self.canvas)
        
        if self.selected:
            self.canvas.create_oval(self.selected.x-13, self.selected.y-13, self.selected.x+13, self.selected.y+13, outline='red', width=2)
        
        self.master.after(100, self.draw)
    
    def on_click(self, event):
        for node in self.graph.nodes:
            if abs(node.x - event.x) < 10 and abs(node.y - event.y) < 10:
                if self.selected and node != self.selected:
                    self.selected.add_edge(node, int(self.weight_entry.get()))
                elif not self.selected:
                    self.selected = node
                else:
                    self.selected = None
                return
        if not self.selected:
            self.add_node(event)
    
    def on_drag(self, event):
        if self.selected:
            self.selected.x = event.x
            self.selected.y = event.y
    
    def add_node(self, event=None):
        node = Node(250, 250)
        self.graph.add_node(node)
    
    def remove(self):
        if self.selected:
            self.graph.remove_node(self.selected)
            self.selected = None
        
root = tk.Tk()
app = App(root)
root.mainloop()
