import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

class Graph:
    """ Implementation  for undirected and unweighted graphs
    """
    
    def __init__(self, path = '', adjacency_matrix = []):
        """ Initiating constructor

        Args:
            path (string): path to .txt file with adjacency matrix 
            adjacency_matrix (list[list[int]]): adjacency matrix
        """
        if len(adjacency_matrix) > 0 and self.is_adjacency_matrix_symmetric(adjacency_matrix):
            self.adjacency_matrix = adjacency_matrix
        elif len(path) > 0:
            self.adjacency_matrix = self.load_adjacency_matrix(path) 
        else:
            self.adjacency_matrix = []
    
    def load_adjacency_matrix(self, path):
        """ Load adjacency matrix from the .txt file

        Args:
            path (string): path to .txt file with adjacency matrix 

        Returns:
            list[list[int]]: adjacency matrix
        """
        temp = []
        adjacency_matrix = []
        with open(path) as file:
            lines = file.readlines()
            
        for line in lines:
            temp.append(list(map(int, line.split(' '))))
            
        for i in range(len(temp)):
            adjacency_matrix.append([])
            for j in range(len(temp[i])):
                adjacency_matrix[i].append(temp[i][j])
                
        return(np.array(adjacency_matrix))
    
    def save_adjacency_matrix(self, name):
        """ Save adjacency matrix to .txt file

        Args:
            name (string): name of the new .txt file
        """
        file = open(name, 'a')
        for row in self.adjacency_matrix:
            file.write(" ".join(map(str, row)) + "\n")

        file.close()
        
    def is_adjacency_matrix_symmetric(self, adjacency_matrix):
        """ Check whether a given adjacency matrix is symmetric or not

        Args:
            adjacency_matrix (list[list[int]]): adjacency matrix

        Returns:
            bool: True if given adjacency_matrix is symmetric, False otherwise
        """
        transposition = np.transpose(adjacency_matrix)   
        return np.array_equal(adjacency_matrix, transposition)
    
    def generate_random_graph(self, number_of_vertices, density):
        """ Generate a graph with a given  number of vertices and density

        Args:
            number_of_vertices (int): number of vertices
            density (float): density of the graph

        Raises:
            Exception: If density is not between 0 and 1

        Returns:
            list[list[int]]: adjacency matrix
        """
        if not 0 <= density <= 1:
            raise Exception('Density must be between 0 and 1.') 
        adjacency_matrix = np.eye(number_of_vertices, dtype=int)
        temp_adjacency_matrix = adjacency_matrix.flatten()
        number_of_edges = int(density * number_of_vertices * (number_of_vertices - 1) / 2)
        
        for i in range(number_of_edges):
            j = random.randint(0, number_of_vertices * (number_of_vertices - 1) - 2*i - 1)
            temp = list(np.where(temp_adjacency_matrix == 0)[0])
            col_no = temp[j] % number_of_vertices
            row_no = int(temp[j]/number_of_vertices)
            temp_adjacency_matrix[row_no * number_of_vertices + col_no] = 1
            temp_adjacency_matrix[col_no * number_of_vertices + row_no] = 1
            
        adjacency_matrix = temp_adjacency_matrix.reshape(number_of_vertices, number_of_vertices) - np.eye(number_of_vertices)
        return adjacency_matrix

    def vertex_degree(self, vertex):
        """ Get degree of the vertex

        Args:
            vertex (int): vertex

        Returns:
            int: degree
        """
        return(sum(self.adjacency_matrix[vertex]))
    
    def graph_degree(self):
        """ Get degree of the graph

        Returns:
            maximum (int): vertex of the graph
            vertex (int): vertex with maximum degree
        """
        degree = np.sum(self.adjacency_matrix, axis=0)
        vertex = np.argmax(degree)
        return(degree[vertex], vertex)
    
    def delete_edges_connected_to_vertex(self, vertex):
        """ Delete all vertices connected to given vertex

        Args:
            vertex (int): vertex
            
        Returns:
            list[list[int]]: adjacency matrix where given vertex has zero degree
        """
        for i in range(len(self.adjacency_matrix)):
            self.adjacency_matrix[vertex][i] = 0
            self.adjacency_matrix[i][vertex] = 0
    
    def sort_vertices_descending_by_degrees(self):
        """ Sort the vertices in descending order by their degrees

        Returns:
            list[int]: sorted vertices
        """
        sorted_vertices = [0]
        for i in range(1, len(self.adjacency_matrix)):
            degree = self.vertex_degree(i)
            temp_list = []
            vertex_inserted = False
            for j in sorted_vertices:
                if degree >= self.vertex_degree(j) and not vertex_inserted:
                    temp_list.append(i)
                    vertex_inserted = True
                    temp_list.append(j)
                else:
                    temp_list.append(j) 
                    
            if not vertex_inserted:
                temp_list.append(i)      
                  
            sorted_vertices = temp_list
        return(sorted_vertices)
    
    def is_neighbor(self, vertex, V):
        """ Check whether a vertex is adjacent to any of the vertices in the set V.

        Args:
            vertex (int): vertex
            V (list[int]): set of vertices
            
        Returns:
            bool: True if given vertex is neighbor to a vertex from set V, False otherwise
        """
        for i in range(len(self.adjacency_matrix[vertex])):
            if (i in V) and (self.adjacency_matrix[vertex][i] > 0):
                return(True)
        return(False)

    def largest_first(self):
        """ Largest First algorithm for graph coloring 
        """
        if self.adjacency_matrix == []:
            raise Exception('There is no adjacency matrix.') 
            
        V = self.sort_vertices_descending_by_degrees()
        graph_colored = []
        S = []
        while sum(V) > -1 * len(V):
            for i in range(len(V)):
                if (not self.is_neighbor(V[i], S)) and (V[i] >= 0):
                    S.append(V[i])
                    V[i] = -1
                    
            graph_colored.append(S)
            S = []
        return(graph_colored)
                    
    def distance_between_vertex(self, first_vertex, second_vertex):
        n = len(self.adjacency_matrix)
        visited = [False] * n
        distance = [float('inf')] * n

        distance[first_vertex] = 0

        while True:
            min_distance = float('inf')
            current_vertex = None

            # Wybierz wierzchołek o najmniejszej odległości spośród nieodwiedzonych
            for v in range(n):
                if not visited[v] and distance[v] < min_distance:
                    min_distance = distance[v]
                    current_vertex = v

            if current_vertex is None:
                # Wierzchołek końcowy jest nieosiągalny
                return float('inf')

            if current_vertex == second_vertex:
                # Osiągnięto wierzchołek końcowy
                return distance[current_vertex]

            visited[current_vertex] = True

            # Zaktualizuj odległości do sąsiadów
            for v in range(n):
                if self.adjacency_matrix[current_vertex][v] == 1:
                    new_distance = distance[current_vertex] + 1
                    if new_distance < distance[v]:
                        distance[v] = new_distance

    def vertices_with_max_saturation(self, colouring_of_the_graph):
        n = len(colouring_of_the_graph)
        temp_list = []
        for v in range(n):
            v_set = {0}
            for u in range(n):
                if self.adjacency_matrix[v][u] == 1 and colouring_of_the_graph[u] != 0:
                    v_set.add(colouring_of_the_graph[u])
            v_set.remove(0)
            temp_list.append(len(v_set))
        list_coloured_vertex = [i for i, element in enumerate(colouring_of_the_graph) if element > 0]
        for i in sorted(set(temp_list), reverse=True):
            vertex = [j for j, element in enumerate(temp_list) if element == i]
            if len(list(set(vertex) - set(list_coloured_vertex))) > 0:
                return list(set(vertex) - set(list_coloured_vertex))



    def d_satur(self, k):
        k = max(k, 2)
        n = len(self.adjacency_matrix)
        colouring_of_the_graph = [0]*n
        for _ in range(n):
            V = self.vertices_with_max_saturation(colouring_of_the_graph)
            choice = V[0]
            if len(V) > 1:
                for v in V:
                    if self.vertex_degree(v) > self.vertex_degree(choice):
                        choice = v

            if colouring_of_the_graph == [0]*n:
                colouring_of_the_graph[choice] = 1
            else:
                colours_min = []
                colours_max = []
                for v in range(n):
                    if colouring_of_the_graph[v] != 0:
                        colours_max.append(self.distance_between_vertex(choice, v) - k + colouring_of_the_graph[v])
                        colours_min.append(k - self.distance_between_vertex(choice, v) + colouring_of_the_graph[v])
                mini = max(colours_min)
                maks = min(colours_max)
                color_not_selected = True
                while color_not_selected:
                    for color in range(1, (k-1)*(n-1) + 2):
                        color_correct = True
                        for limit in range(len(colours_max)):
                            if (color > colours_max[limit] and color < colours_min[limit]):
                                color_correct = False
                                break
                        if color_correct:
                            color_not_selected = False
                            colouring_of_the_graph[choice] = color
                            break
        vertex = []
        for colors in set(colouring_of_the_graph):
            vertex.append([i for i, elem in enumerate(colouring_of_the_graph) if elem == colors])
        return vertex
    
    def create_node_colors(self,colouring_of_the_graph):
        rand_colors = []
        for _ in range(len(colouring_of_the_graph)):
            rand_colors.append("#"+''.join([random.choice('ABCDEF0123456789') for _ in range(6)]))
        
        graph = nx.from_numpy_matrix(self.adjacency_matrix)
        graph_colors = [0 for _ in range(len(self.adjacency_matrix))]
        for i in range(len(colouring_of_the_graph)):
            for j in colouring_of_the_graph[i]:
                graph_colors[j] = rand_colors[i]
                
        return(graph, graph_colors)
        
    def draw_graph(self, use_largest_first = False, use_d_satur = False, k = 0):
        """ Draw colored graph using Largest First or modified DSatur algorithm
        """
        if (not use_largest_first and not use_d_satur):
            raise Exception('You have to choose at least one algorithm.') 
        
        graph_colors_lf = None
        graph_colors_ds = None
        graph_lf = None
        graph_ds = None
        colouring_of_the_graph_lf = []
        colouring_of_the_graph_ds = []
        if use_largest_first:
            colouring_of_the_graph_lf = self.largest_first()
            graph_lf, graph_colors_lf = self.create_node_colors(colouring_of_the_graph_lf)
            
        if use_d_satur:
            colouring_of_the_graph_ds = self.d_satur(k)
            graph_ds, graph_colors_ds = self.create_node_colors(colouring_of_the_graph_ds)

        if use_largest_first and use_d_satur:
            _, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
            ax1.set_title('Number of used colors in LargestFirst: ' + str(len(colouring_of_the_graph_lf)))
            nx.draw(graph_lf, node_color=graph_colors_lf, ax=ax1)
            ax2.set_title('Number of used colors in DSatur: ' + str(len(colouring_of_the_graph_ds)))
            nx.draw(graph_ds, node_color=graph_colors_ds, ax=ax2)
            plt.show()
            
        elif use_largest_first:
            plt.figure()
            ax = plt.gca()
            ax.set_title('Number of used colors: ' + str(len(colouring_of_the_graph_lf)))
            nx.draw(graph_lf, node_color = graph_colors_lf, ax=ax)
            plt.show()
            
        else: 
            plt.figure()
            ax = plt.gca()
            ax.set_title('Number of used colors: ' + str(len(colouring_of_the_graph_ds)))
            nx.draw(graph_ds, node_color = graph_colors_ds, ax=ax)
            plt.show()

