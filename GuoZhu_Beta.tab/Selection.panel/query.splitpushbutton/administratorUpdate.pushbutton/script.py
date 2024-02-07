# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

from Autodesk.Revit.DB import*

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


#Public config and local config
public_config = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\GUOZHU_Beta.extension\\GUOZHU_Beta_config.xml"


# function for doc's unique user names
user_names = []
all_3d_view = FilteredElementCollector(doc).OfClass(View3D).WhereElementIsNotElementType().ToElementIds()
for i in all_3d_view:
    user = WorksharingUtils.GetWorksharingTooltipInfo(doc,i).Creator
    user_names.append(user)

user_names = list(set(user_names))


# Check if local_config's user name exist
difference = []

tree = ET.parse(public_config)
root = tree.getroot()


xml_user_name = []
for i in root:
    value = i.attrib['name'] 
    # Input context with utf-8 must decode with utf-8
    xml_user_name.append(value.decode("utf-8"))


difference_set = [x for x in user_names if x not in xml_user_name]
# print(difference_set)

if len(difference_set) ==0:
    pass

else:

    difference = (list(set(user_names).union(set(xml_user_name))))

    newroot = ET.Element("data")

    #Set the default XML tree structure
    for i in difference:
        # Create new element for user name
        newElem = ET.Element("user", name = i)

        subE1 = ET.SubElement(newElem, "admin")
        subE1.text = "False"
        subE2 = ET.SubElement(newElem, "workset")
        subE2.text = "False"

        # root.append(newElem)
        newroot.append(newElem)

    # Write in UTF-8 for nature language reading
    new_tree = ET.ElementTree(newroot)
    new_tree.write(public_config,encoding="UTF-8",xml_declaration=True)
    print("Added:",difference_set)