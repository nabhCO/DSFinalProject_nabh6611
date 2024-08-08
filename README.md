## Felzenszwalb-Huttenlocher Segmentation- from Scratch!

### Walkthrough

I used a virtual environment in order to access the OpenCV and Numpy libraries on VSCode. Running this might be tedious, so I have uploaded a video of my code walkthrough on Google Drive below (visible to anyone with this link):
https://drive.google.com/file/d/1_hB837R2jJHMxjJoM5nvGeN0Vn6MnPZL/view?usp=drive_link

If you would like to run the code yourself, the instructions for creating a local virtual environment in VSCode are below:

1. Create a new terminal.
2. Switch from powershell to command line interface (cmd) using the downward facing arrow at the top right of the terminal (to the right of the + symbol)
3. Enter `python -m venv nameofenvironment` in the command line. Note: "nameofenvironment" should just be whatever you want to name your virtual environment
4. A new folder for your virtual environment should appear in the directory. VSCode will ask if you want to select this new environment for your workspace folder- select "Yes"
5. Now, you must activate the environment. To do this, enter `nameofenvironment\Scripts\activate` in the command line

You should now see the name of the virtual environment preceding the path in the command line. 

6. Now install OpenCV with the command `pip install opencv-python`. This will also install Numpy.
7. To run your the code, enter `python filename.py` in the command line. Make sure you are using the command line and not the powershell whenever you run the code.

The sample images for running the code are "apple.jpg" and "objects.png", but you can use others too. Examples of results are in the "result examples" folder.

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
