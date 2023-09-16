from logging import raiseExceptions
import os
import xml.etree.ElementTree as ET

"""

read xml
width, height, class name, xmin, ymin, xmax, ymax

made by : Jeong ho Lee

"""


## PASCAL VOC
PASCAL_Class_index = {"public": 0, "attacker": 1, "victim": 2}

XML_DIRECTORY = "/Users/jack/Documents/GitHub/AIRCCTV/traindata/labels_xml/"
TXT_DIRECTORY = "/Users/jack/Documents/GitHub/AIRCCTV/traindata/labels"


def Write_TXT(file_name, width, height, result):
    file_name = file_name[:-3] + "txt"
    file_path = os.path.join(TXT_DIRECTORY, file_name)
    f = open(file_path, "w")
    for i, data in enumerate(result):
        data = f"{data}\n"
        data = data.replace(",", "").replace("[", "").replace("]", "")
        f.write(data)
    f.close()


def Read_XML(file_path, file_name):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ## size inform
    size = root.find("size")
    width = float(size.find("width").text)
    height = float(size.find("height").text)

    ## box inform
    result = list()
    for object in root.findall("object"):
        name = object.find("name").text
        class_index = PASCAL_Class_index[name]
        bndbox = object.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)
        bnd_width = round((xmax - xmin) / width, 6)
        bnd_height = round((ymax - ymin) / height, 6)
        x_center = round((xmax + xmin) / 2 / width, 6)
        y_center = round((ymax + ymin) / 2 / height, 6)
        result.append([class_index, x_center, y_center, bnd_width, bnd_height])
    Write_TXT(file_name=file_name, width=width, height=height, result=result)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


def main():
    if not os.path.isdir(XML_DIRECTORY):
        raise Exception("no XML DIr")
    createFolder(TXT_DIRECTORY)
    for root, directories, files in os.walk(XML_DIRECTORY):
        for file in files:
            if ".xml" in file:
                file_path = os.path.join(root, file)
                Read_XML(file_path, file)


if __name__ == "__main__":
    main()
