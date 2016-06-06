# pythonFBX
6uu6


Tools and middleware 2

The program reads a directory of FBX files and outputs to webpage in SVG.
Using python bindings I can extract information about the polygons in each mesh for each FBX file.


def build_polys(node):
    mesh = node.GetMesh()
    if mesh:
        indices = []

        for i in range(mesh.GetPolygonCount()):
            nrVrtx = mesh.GetPolygonSize(i)

We basically extract the mesh then the polygon and then the vertices. We look at the number of vertices for each polygon, if it is 3 we have a triangle structure and if it is 4 we have a quad structure.  After this we do not need to rely on the python bindings. We then have to translate them to be isometric, so that we have to change the camera perspective. So for this we need rotation matrices, we rotate 45 degrees on the 2 axis and try to scale it up or down.  Here we are going through the row of the rotation matrix and columns of the camera matrix, to reposition the views. 

def rotate_x(angle):
    rx = [[1, 0, 0],
          [0, math.cos(angle), -math.sin(angle)],
          [0, math.sin(angle), math.cos(angle)]]

    result = [[0 for x in range(3)] for x in range(3)]

    for i in range(3):
        for j in range(3):
            result[i][j] = camera[i][0] * rx[0][j] + camera[i][1] * rx[1][j] + camera[i][2] * rx[2][j]

    for i in range(3):
        for j in range(3):
            camera[i][j] = result[i][j]

def rotate_y(angle):
    ry = [[math.cos(angle), 0, math.sin(angle)],
          [0, 1, 0],
          [-math.sin(angle), 0, math.cos(angle)]]

    result = [[0 for x in range(3)] for x in range(3)]

    for i in range(3):
        for j in range(3):
            result[i][j] = camera[i][0] * ry[0][j] + camera[i][1] * ry[1][j] + camera[i][2] * ry[2][j]

    for i in range(3):
        for j in range(3):
            camera[i][j] = result[i][j]


We check the depth, which is the z-axis, the aim is to get polygons that are nearer to the camera to appear at the front. We go through each polygon centre and check which has the smallest distance, the ones with the smallest distance will be placed at the front.

  for i in range(0, len(polygons)-1):
        for j in range(i, len(polygons)):
            if (centers[j] < centers[i]):
                temp = centers[i]
                centers[i] = centers[j]
                centers[j] = temp
                temp = polygons[i]
                polygons[i] = polygons[j]
                polygons[j] = temp

Using flask, I rendered a template on the screen, using server EC2 screen. 






















![fbxmodels_webpage](https://cloud.githubusercontent.com/assets/15308778/15824102/80fba098-2bf5-11e6-971b-41f2856c033b.png)
