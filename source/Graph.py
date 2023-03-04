import numpy as np
import random

class Graph:
    """ Implementation  for undirected and unweighted graphs
    """
    
    def __init__(self, path):
        """ Initiating constructor

        Args:
            path (string): path to .txt file with adjency matrix 
        """
        self.adjency_matrix = self.load_adjency_matrix(path) 
    
    def load_adjency_matrix(self, path):
        """ Load adjency matrix from the .txt file

        Args:
            path (string): path to .txt file with adjency matrix 

        Returns:
            list[list[int]]: adjency matrix
        """
        temp = []
        adjency_matrix = []
        with open(path) as file:
            lines = file.readlines()
        for line in lines:
            temp.append(list(map(int, line.split(' '))))
        for i in range(len(temp)):
            adjency_matrix.append([])
            for j in range(len(temp[i])):
                adjency_matrix[i].append(temp[i][j])
        return adjency_matrix
    
    def generate_random_graph(self, number_of_vertices, density):
        """ Generate a graph with a given  number of vertices and density

        Args:
            number_of_vertices (int): number of vertices
            density (float): density of the graph

        Raises:
            Exception: If density is not between 0 and 1

        Returns:
            list[list[int]]: adjency matrix
        """
        if (density > 1) or (density < 0):
            raise Exception('Density must be between 0 and 1.') 
        adjency_matrix = np.eye(number_of_vertices, dtype=int)
        temp_adjency_matrix = adjency_matrix.flatten()
        number_of_edges = int(density * number_of_vertices * (number_of_vertices - 1) / 2)
        for i in range(number_of_edges):
            j = random.randint(0, number_of_vertices * (number_of_vertices - 1) - 2*i - 1)
            temp = list(np.where(temp_adjency_matrix == 0)[0])
            col_no = temp[j] % number_of_vertices
            row_no = int(temp[j]/number_of_vertices)
            temp_adjency_matrix[row_no * number_of_vertices + col_no] = 1
            temp_adjency_matrix[col_no * number_of_vertices + row_no] = 1
        adjency_matrix = temp_adjency_matrix.reshape(number_of_vertices, number_of_vertices) - np.eye(number_of_vertices)
        return adjency_matrix

    def vertex_degree(self, vertex):
        """ Get degree of the vertex

        Args:
            vertex (int): vertex

        Returns:
            int: degree
        """
        degree = 0
        for i in range(len(self.adjency_matrix[vertex])):
            if self.adjency_matrix[vertex][i] == 1:
                degree += 1
        return degree
    
    def graph_degree(self):
        """ Get degree of the graph

        Returns:
            maximum (int): vertex of the graph
            vertex (int): vertex with maximum degree
        """
        maximum = 0
        vertex = 0
        for i in range(len(self.adjency_matrix)):
            temp = self.vertex_degree(i) 
            if temp > maximum:
                maximum = temp
                vertex = i
        return(maximum, vertex) 
    
    def delete_edges_connected_to_vertex(self, vertex):
        """ Delete all vertices connected to given vertex

        Args:
            vertex (int): vertex
            
        Returns:
            list[list[int]]: adjency matrix where given vertex has zero degree
        """
        for i in range(len(self.adjency_matrix)):
            self.adjency_matrix[vertex][i] = 0
            self.adjency_matrix[i][vertex] = 0
    
    def sort_vertices_descending_by_degrees(self):
        """ Sort the vertices in descending order by their degrees

        Returns:
            list[int]: sorted vertices
        """
        sorted_vertices = [0]
        for i in range(1, len(self.adjency_matrix)):
            degree = self.vertex_degree(i)
            temp_list = []
            vartex_inserted = False
            for j in sorted_vertices:
                if degree >= self.vertex_degree(j) and not vartex_inserted:
                    temp_list.append(i)
                    vartex_inserted = True
                    temp_list.append(j)
                else:
                    temp_list.append(j) 
            if not vartex_inserted:
                temp_list.append(i)        
            sorted_vertices = temp_list
        return (sorted_vertices)
    
    def is_neighbor(self, vertex, V):
        """ Check whether a vertex is adjacent to any of the vertices in the set V.

        Args:
            vertex (int): vertex
            V (list[int]): set of vertices
            
        Returns:
            bool: True if given vertex is neighbor to a vertex from set V, False otherwise
        """
        for i in range(len(self.adjency_matrix[vertex])):
            if (i in V) and (self.adjency_matrix[vertex][i] > 0):
                return(True)
        return(False)

