# -*- coding: utf-8 -*-
import clr
import xml.etree.ElementTree as ET


from pyrevit import forms, script

from Autodesk.Revit.DB import*
from Autodesk.Revit.UI.Selection import*


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def tunning(newRoot):
    print("****"*10)
    for rt in newRoot:
        user = rt.get("name")
        print("<{}>".format(user))
        admin = rt.find("admin").text
        print("\t admin-{}".format(admin))
        workset = rt.find("workset").text
        print("\t workset-{}".format(workset))


output = script.get_output()

#Public config and local config
public_config = "\\\\10.1.37.5\\国住共享文件夹\\国住设计区\\设计共享区\\BIM项目\\pyRevitExtension\\GUOZHU_Beta.extension\\GUOZHU_Beta_config.xml"
text_XML = "C:\\Users\\6321011\\Desktop\\textXML.xml"


# The main code check for admin
try:
    value = forms.ask_for_string(
        
        prompt='INPUT ADMIN CODE:',
        title='Admin Check'
    )

    print(value)
    if value == "1q2w3e4r":
        print("correct")
    else:
        forms.alert("错误，请联系管理员")
        output.close()
        script.exit()
except:
    script.exit()


# parse the public config(original) from the utf-8 xml
tree = ET.parse(public_config)
root = tree.getroot()
# Create new root
newRoot = ET.Element("data")


for rt in root:

    user = rt.get("name").decode("utf-8")
    admin = rt.find("admin").text
    workset = rt.find("workset").text

    #Create new root
    newElem = ET.Element("user", name = user)

    subE1 = ET.SubElement(newElem, "admin")
    subE1.text = admin
    subE2 = ET.SubElement(newElem, "workset")
    subE2.text = workset

    # root.append(newElem)
    newRoot.append(newElem)

newTree = ET.ElementTree(newRoot)

# running cmd command
exit_condition = False
while exit_condition == False:
    #user input command
    
    while True:
        tunning(newRoot)
        users = [i.get("name") for i in newRoot.findall("user")]
        cmd = raw_input()

        if cmd.lower() == "rf":
            exit_condition = True
            break

        #cmd for individual user
        if len(cmd.split("_"))==2:

            for user in newRoot.findall("user"):
                input_name = cmd.split("_")[0]
                input_cmd1 = cmd.split("_")[1]
                
                if user.get("name") == input_name:
                    if input_cmd1.lower() == "workset.true" :
                        user.find("workset").text = "True"

                    elif input_cmd1.lower() == "workset.false":
                        user.find("workset").text = "False"

                    elif input_cmd1.lower() == "admin.true":
                        user.find("admin").text = "True"

                    elif input_cmd1.lower() == "admin.false":
                        user.find("admin").text = "False"

            exit_condition = False
            break

        if cmd.lower() == "admin.alltrue":
            # set all user's admin to ture
            for i in newRoot.iter("admin"):
                i.text = "True"
            exit_condition = False
            break

        if cmd.lower() == "admin.allfalse":
            # set all user's admin to False
            for i in newRoot.iter("admin"):
                i.text = "False"
            exit_condition = False
            break

        if cmd.lower() == "workset.alltrue":
            # set all user's workset to ture
            for i in newRoot.iter("workset"):
                i.text = "True"
            exit_condition = False
            break

        if cmd.lower() == "workset.allfalse":
            # set all user's workset to false
            for i in newRoot.iter("workset"):
                i.text = "False"
            exit_condition = False
            break

        if cmd.lower() == "exit":
            # exit with nothing changed
            exit_condition = True
            output.close()
            break

        if cmd.lower() == "write":
            # writ to xml and exit
            newTree.write(public_config, encoding="UTF-8",xml_declaration=True)
            exit_condition = True
            break

        else:
            # also refrshed
            print("NO SUCH COMMAND")