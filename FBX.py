import FbxCommon
import fbx
import math
import sys
import webbrowser
import glob, os
from xml.etree import ElementTree as et


PATH = os.getcwd()
FBX_FOLDER = "Fbx Files"
FBX_FOLDER_PATH = os.path.join(PATH, FBX_FOLDER)
FBX_EXT = ".fbx"
FBX_PATTERN = "*.fbx"
OUTPUT_FOLDER = "Images"
IMG_FOLDER_PATH = os.path.join(PATH, OUTPUT_FOLDER)


def fbx_files():
    print("[fbx_file_list] path:", PATH)

    pattern = os.path.join(FBX_FOLDER_PATH, FBX_PATTERN)
    print("[fbx_file_list] files:", pattern)

    files = [fbx_path for fbx_path in glob.glob(pattern)]
    return sorted(files)

def fbx_name(fbxpath):
    return os.path.basename(fbxpath).split(FBX_EXT)[0]

def fbx_view_name(fbxname):
    return '%s_view.svg' % fbxname

def fbx_full_path(fbxviewname):
    filename = '%s%s' % (fbxviewname, FBX_EXT)
    return os.path.join(FBX_FOLDER_PATH, filename)

def process_fbx_files():
    files = fbx_files()
    for fbx_path in files:
        print("[process_fbx_files] processing:", fbx_path)
        view_name = fbx_view_name(fbx_name(fbx_path))
        out_path = os.path.join(IMG_FOLDER_PATH, view_name)
        process_model(fbx_path, out_path)

def process_model(fbx_path, out_path, change_camera=False):
    # global variables
    polygoncount = 0
    vertexcount = 0

    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    converter = fbx.FbxGeometryConverter(sdk_manager)

    doc = et.Element('svg', width='4800', height='4800', version='1.1', xmlns='http://www.w3.org/2000/svg')
    if not FbxCommon.LoadScene(sdk_manager, scene, fbx_path):
        print("Not found")

    node = scene.GetRootNode()

    # change point of view
    if change_camera:
        root = node
        cam = root.GetCamera()
        if cam == None:
            # print "[cam] not in root node"
            # cam_node = scene.FindNodeByName(scene.GetGlobalSettings().GetDefaultCamera())
            # print "[cam] cam_node found", cam_node

            cam_node = FbxCommon.FbxNode.Create(scene, 'myCameraNode')
            cam = FbxCommon.FbxCamera.Create(scene, 'myCamera')
            cam_node.SetNodeAttribute(cam)
            root.ConnectSrcObject(cam_node)

            pos = cam.Position.Get()
            print '[cam]', pos[0], pos[1], pos[2]
            newpos = FbxCommon.FbxDouble3(300.0, 1000.0, 1500.0)
            cam.Position.Set(newpos)

        # cam = root.GetCamera()
        # print cam
        # camera = FbxCommon.GetCurrentCamera
        # camera_name = scene.GetGlobalSettings().GetDefaultCamera()
        # print '[camera found!]', camera
        # scene.GlobalCameraSettings().

    


    f = open(out_path, 'w')
    f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
    f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
    f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
    f.write(et.tostring(doc))
    f.close()


# for fbx test purpose
if __name__ == "__main__":
    tfile = os.path.join(FBX_FOLDER_PATH, 'teapot0.fbx')
    print("[changing camera]:", tfile)
    view_name = fbx_view_name(fbx_name(tfile))
    out_path = os.path.join(IMG_FOLDER_PATH, view_name)
    process_model(tfile, out_path, change_camera=True)
