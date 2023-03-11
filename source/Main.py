from tkinter import *
import tkinter.ttk as ttk
from Graph import Graph
from PIL import ImageTk, Image

class GraphApp:
    def __init__(self, master):
        self.master = master
        master.title("Graf")
        self.adjency_matrix_options = "Wybierz w jaki sposób chcesz przekazać macierz sąsiedztwa: \n\
1) Poprzez ścieżkę do pliku .txt \n\
2) Bezpośrednio z konsoli \n\
3) Losowo wygenerować na podstawie liczby wierzchołków oraz gęstości:"
        self.main_options = "Wybierz opcję, którą chcesz wykonać:\n\
1) Pokoloruj graf algorytmem LargestFirst \n\
2) Pokoloruj graf zmodyfikowanym algorytmem DSatur \n\
3) Porównaj oba algorytmy"
        self.run = "1"
        
        self.menu_label = Label(master, text=self.main_options, width=1500, height=125, fg="white", font=("Arial", 16), image=button_image, compound="center", justify="left")
        self.menu_label.pack()

        self.menu_choice = Entry(master, width=34)
        self.menu_choice.place(relx=0.42, rely=0.21)
        
        self.menu_choice_2 = Entry(master, width=34)
        self.menu_choice_2.place_forget()

        self.submit_button = Button(master, text="Zatwierdź", command=self.select_menu_option, width=12, height=3, font=("Arial", 13), bg='#5cac2d')
        self.submit_button.place(relx=0.36, rely=0.32)

        self.run_again_button = Button(master, text="Wróc", command=self.select_run_option, width=12, height=3, font=("Arial", 13), bg='#6370b6')
        self.run_again_button.place(relx=0.55, rely=0.32)
        
        
        button_quit = Button(root, text="ZAKOŃCZ", command=self.quit_program, width=10, height=2, font=("Arial", 12), bg='#ff1133')
        button_quit.pack(side=BOTTOM, anchor=SE)

    def select_menu_option(self):
        choice = self.menu_choice.get()
        self.menu_choice.delete(0, END)
        self.menu_choice_2.delete(0, END)
        if choice == "1":
            self.menu_label.config(text=self.adjency_matrix_options)
            self.submit_button.config(command=self.select_adjacency_matrix_option)
        else:
            self.menu_label.config(text="Błędny wybór.")

    def select_adjacency_matrix_option(self):
        choice = self.menu_choice.get()
        self.menu_choice.delete(0, END)
        self.menu_choice_2.delete(0, END)
        if choice == "1":
            self.menu_label.config(text="Podaj ścieżkę:")
            self.submit_button.config(command=self.load_graph_from_file)
            
        elif choice == "2":
            self.menu_label.config(text="Podaj macierz sąsiedztwa:")
            self.submit_button.config(command=self.load_graph_from_adjency_matrix)
            
        elif choice == "3":
            self.menu_label.config(text="W pierwszym okienku podaj liczbę wierzchołków, a w drugim gęstość grafu:")
            self.menu_choice_2.place(relx=0.42, rely=0.26)
            self.submit_button.config(command=self.generate_random_graph_with_density)
        else:
            self.menu_label.config(text="Błędny wybór.")

    def load_graph_from_file(self):
        path = self.menu_choice.get()
        G = Graph(path)
        G.draw_graph()

    def load_graph_from_adjency_matrix(self):
        G = Graph()
        # TODO

    def generate_random_graph_with_density(self):
        number_of_vertices = int(self.menu_choice.get())
        density = float(self.menu_choice_2.get())
        G = Graph()
        G.adjency_matrix = G.generate_random_graph(number_of_vertices, density)
        G.draw_graph()

    def select_run_option(self):
        self.menu_label.config(text=self.main_options)
        self.submit_button.config(command=self.select_menu_option)
        self.menu_choice.delete(0, END)
        self.menu_choice_2.delete(0, END)
        self.menu_choice_2.place_forget()
    
    def quit_program(self):
        root.quit()

root = Tk()
image = Image.open("images/background.jpg")
photo = ImageTk.PhotoImage(image)
button_image = PhotoImage(file="images/button.png")    
background_label = Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
root.attributes('-fullscreen', True)
graph_app = GraphApp(root)
root.mainloop()
