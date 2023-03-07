from Graph import Graph

adjency_matrix_options = "Wybierz w jaki sposób chcesz przekazać macierz sąsiedztwa: \n\
    1) Poprzez ścieżkę do pliku .txt \n\
    2) Bezpośrednio z konsoli \n\
    3) Losowo wygenerować na podstawie liczby wierzchołków oraz gęstości:"
    
main_options = "Wybierz opcję, którą chcesz wykonać:\n\
    1) Pokoloruj graf algorytmem LargestFirst \n\
    2) Pokoloruj graf zmodyfikowanym algorytmem DSatur \n\
    3) Porównaj czas działania obu algorytmów"

if __name__ == "__main__":
    run = "1"
    while run == "1":
        print(main_options)
        choice = input("Wybierz opcję: ")
        if choice == "1":
            print(adjency_matrix_options)
            choice = input("Wybierz opcję: ")
            if choice == "1":
                path = input("Podaj ścieżkę:")
                G = Graph(path)
                G.draw_graph()
            elif choice == "2":
                print("Not implemented yet!")
            elif choice == "3":
                number_of_vertices = int(input("Podaj liczbę wierzchołków:"))
                density = float(input("Podaj gęstość grafu:"))
                G = Graph()
                G.adjency_matrix = G.generate_random_graph(number_of_vertices, density)
                G.draw_graph()
            else:
                print("Błędny wybór.")
                
        elif choice == "2":
            print("Not implemented yet!")
            
        elif choice == "3":
            print(adjency_matrix_options)
            choice = input("Wybierz opcję: ")
            if choice == "1":
                path = input("Podaj ścieżkę:")
                print("Not implemented yet!")
            elif choice == "2":
                print("Not implemented yet!")
            elif choice == "3":
                number_of_vertices = int(input("Podaj liczbę wierzchołków:"))
                density = float(input("Podaj gęstość grafu:"))
                print("Not implemented yet!")
            else:
                print("Błędny wybór.")
                
        else:
            print("Błędny wybór.")

        run = input("Czy chcesz kontynuować, jeśli tak, to wybierz 1: ")
        
