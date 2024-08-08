## Felzenszwalb-Huttenlocher Segmentation- from Scratch!

### Walkthrough

I used a virtual environment in order to access the OpenCV and Numpy libraries on VSCode. Running this might be tedious, so I have uploaded a video of my code walkthrough on Google Drive below (visible to anyone with this link):

### Project Description

Main data structure used: Graph

My project is an attempt at implementing Felzenszwalb-Huttenlocher image segmentation from scratch, using the OpenCV and Numpy libraries. This segmentation method is graph-based, meaning that an image’s pixels will become our “nodes”. We create “edges” to connect these nodes to their neighbours (each node will have eight- two vertical, two horizontal, and the four diagonal neighbours). Each of these edges has a weight, calculated based on the weighted Euclidean distance between the start and end node colors. The weights are used to segment the graph based on color similarity between pixels, using Kruskal's MST algorithm. A disjoint set data structure has also been implemented in order to keep track of the segments.

### Resources

[Paper by Felzenszwalb and Huttenlocher (2004)](https://cs.brown.edu/people/pfelzens/papers/seg-ijcv.pdf)

[Paper by Narang and Rathinavel (Year Unknown)](https://www.cs.unc.edu/~sahil/data/Segmentation-Report.pdf)

[Weighted Euclidean Distance formula (and others)](https://www.baeldung.com/cs/compute-similarity-of-colours)

[Virtual Environment Tutorial](https://www.youtube.com/watch?v=fclTFQQvQFQ&t=78s)

[Apple] https://commons.wikimedia.org/wiki/File:Red_Apple.jpg

[Objects] https://www.acin.tuwien.ac.at/en/vision-for-robotics/software-tools/rgb-d-segmentation/

[OpenCV Documentation](https://docs.opencv.org/4.x/index.html)

[OpenCV Tutorial](https://www.geeksforgeeks.org/introduction-to-opencv/)

[Numpy Documentation](https://numpy.org/doc/)

[Disjoint Set Resource](https://takeuforward.org/data-structure/disjoint-set-union-by-rank-union-by-size-path-compression-g-46/)

[Data Type Error Handling ](https://stackoverflow.com/questions/7559595/python-runtimewarning-overflow-encountered-in-long-scalars)

Kruskal’s MST Algorithm: 
Zybooks Computer Science 2: Data Structures (Chapter 16.12, Minimum Spanning Tree)
