import cv2
import numpy as np

#Felzenszwalb-Huttenlocher algorithm, from scratch!

''' Disjoint_Set class allows for grouping of visually similar pixels into  "flattened tree" sets. 
    Parent array keeps track of which set a pixel is in. Max array stores the maximum edge weight connecting two pixels in the set. 
    Size array keeps track of the number of pixels currently in that set. Both max and size arrays store these values at the
    set root pixel's index. '''
class Disjoint_Set:     

    def __init__(self, n):

        self.parent = list(range(n))
        self.max = [0] * n
        self.size = [1] * n

    def find(self, node_sub):   #finds parent of set that the pixel is in

        if node_sub != self.parent[node_sub]:

            self.parent[node_sub] = self.find(self.parent[node_sub])

        return self.parent[node_sub]
    
    def find_max(self, node_sub):

        parent_node = self.find(node_sub)

        return self.max[parent_node]
    
    
    def find_size(self, node_sub):

        parent_node = self.find(node_sub)

        return self.size[parent_node]

    def union(self, node1, node2, edge_weight): #merges two sets (if representative nodes are in different sets)
                                                #updates size and max of merged set
        par_one = self.find(node1)
        par_two = self.find(node2)

        if par_one == par_two:

            return
        
        elif self.size[par_one] < self.size[par_two]:

            self.parent[par_one] = par_two
            self.size[par_two] += self.size[par_one]
            
            if self.max[par_two] < edge_weight:
                self.max[par_two] = edge_weight

        else:

            self.parent[par_two] = par_one
            self.size[par_one] += self.size[par_two]

            if self.max[par_one] < edge_weight:
                self.max[par_one] = edge_weight

class Edge:

    def __init__(self, start, end, weight):

        self.start = start
        self.end = end
        self.weight = weight

class Pixel_Node:

    def __init__(self, color, subscript, boundary):
        
        self.color = color
        self.subscript = subscript
        self.boundary = boundary

##### HELPER FUNCTIONS FOR SEGMENTATION ####

''' preprocesses input image based on steps in paper by Felzenszwalb and Huttenlocher- resizing if necessary,
    Gaussian blur applied with sigma 0.8 to remove artifacts '''
def preprocess_img(input_image):

    pixel_nodes = cv2.imread(input_image, 1)

    if pixel_nodes.shape[0] > 250 or pixel_nodes.shape[1] > 250:

        if pixel_nodes.shape[0] > pixel_nodes.shape[1]:
            pixel_nodes = cv2.resize(pixel_nodes, (200, 250))

        elif pixel_nodes.shape[0] < pixel_nodes.shape[1]:
            pixel_nodes = cv2.resize(pixel_nodes, (250, 200))

        else:
            pixel_nodes = cv2.resize(pixel_nodes, (250, 250))

    pixel_nodes = cv2.GaussianBlur(pixel_nodes, (5, 5), 0.8, 0.8)

    return pixel_nodes

''' function that creates a specific subscript for a Pixel_Node object, useful for accessing said object 
    in Disjoint_Set structure'''
def subscript_func(i, j, width):

    return ((i * width) + j)

''' gets row location of pixel using subscript '''
def get_i(node_sub, width):

    return node_sub // width
    
''' gets column location of pixel using subscript '''
def get_j(node_sub, width):

    return  node_sub % width

''' converts pixels in original numpy array to Pixel_Node objects, with color ([B, G, R]) and 
    subscript for identification '''
def create_nodearray(height, width, pixel_nodes):

    node_array = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):

            color = pixel_nodes[i, j]
            subscript  = subscript_func(i, j, width)
            node_array[i][j] = Pixel_Node(color, subscript, False)

    return node_array


''' creates list of edges connected to each node- each node will have eight edges containing start, end, and weight based
    on color similarity (for up, down, left, right, and four diagonal pixels) '''
def create_edgelist(node_array, height, width):

    edge_list = []

    for i in range(1, height - 1):
        for j in range(1, width - 1):

            current = node_array[i][j]

            node_neighbours = [[i-1, j], [i-1, j+1], [i, j+1], [i+1, j+1],[i+1, j], [i+1, j-1], [i, j-1], [i-1, j-1]]

            for k in range(0, 8):

                neighbour_i = node_neighbours[k][0]
                neighbour_j = node_neighbours[k][1]

                neighbour = node_array[neighbour_i][neighbour_j]

                edge = Edge(current, neighbour, color_similarity(current.color, neighbour.color))

                edge_list.append(edge)

    return edge_list


''' function that calculates color similarity between two pixels, accounting for human perception '''
def color_similarity(color_one, color_two):

    blue1, green1, red1 = np.array(color_one, dtype=np.float64)
    blue2, green2, red2 = np.array(color_two, dtype=np.float64)
    color_diff = (0.3 * ((red1 - red2)**2)) + (0.59 * ((green1 - green2)**2)) + (0.11 * (blue1 - blue2)**2)

    return color_diff

''' threshold function for calculating dissimilarity between pixels- if difference between pixels less than 
    minimum internal difference (between disjoint sets), merge sets (algorithm by Felzenszwalb and Huttenlocher, 2004) '''
def threshold_formula(disjoint_set, node1, node2, edge, k_val):

    int_diff_one = disjoint_set.find_max(node1.subscript)
    int_diff_two = disjoint_set.find_max(node2.subscript)

    min_edge = edge.weight

    size_one = disjoint_set.find_size(node1.subscript)
    size_two = disjoint_set.find_size(node2.subscript)

    k = k_val
    m_int_one = int_diff_one + (k // size_one)
    m_int_two = int_diff_two + (k // size_two)

    boundary = min_edge < min(m_int_one, m_int_two)

    return boundary



'''' function that uses Kruskal's minimum spanning tree algorithm to create disjoint sets based on color similarity -
    if sets are similar they are merged with the Disjoint_Set union function, 
    and will have the same "parent pixel" in the disjoint set '''
def Kruskal_MST(disjoint_set, edge_list, k_val):

    while len(edge_list) > 0:

        next_edge = edge_list[0]
        edge_list.pop(0)

        vertex_one = next_edge.start
        vertex_two = next_edge.end

        threshold_result = threshold_formula(disjoint_set, vertex_one, vertex_two, next_edge, k_val)

        if threshold_result == True:

            disjoint_set.union(vertex_one.subscript, vertex_two.subscript, next_edge.weight)


''' function for visual segmentation of the input image- a new numpy array for the segmented image 
    is created with same dimensions as original. pixel parent for each pixel is found using Disjoint_Set find function, 
    and corresponding pixel location is set to inverted color values of parent pixel. new image is then written up 
    (name and extension specified by user) '''
def segment_image(disjoint_set, pixel_nodes, node_array, height, width):

    segmented_img = np.zeros_like(pixel_nodes, dtype=np.uint8)


    for i in range(height):
        for j in range(width):

            parent = disjoint_set.find(node_array[i][j].subscript)
            parent_color = node_array[get_i(parent, width)][get_j(parent, width)].color
            segmented_img[i, j] = [255 - parent_color[0], 255 - parent_color[1], 255 - parent_color[2]]

    segmented_img_name = input("Enter a new name for the segmented image file, along with the extension: ")
    cv2.imwrite(segmented_img_name, segmented_img)


##############################################################################################################

input_image = input("Please enter the exact filename of your image (e.g. apple.jpg): ")
print("Choose a k value. The standard is 300 - 500, but you can use smaller values for smaller segments, and larger values for larger segments")
input_k = int(input())

pixel_nodes = preprocess_img(input_image)

height = pixel_nodes.shape[0]
width = pixel_nodes.shape[1]

node_array = create_nodearray(height, width, pixel_nodes)

edge_list = create_edgelist(node_array, height, width)
edge_list.sort(key= lambda edge: edge.weight)

disjoint_set = Disjoint_Set(height * width)

Kruskal_MST(disjoint_set, edge_list, input_k)

segment_image(disjoint_set, pixel_nodes, node_array, height, width)

            






        








    



 











