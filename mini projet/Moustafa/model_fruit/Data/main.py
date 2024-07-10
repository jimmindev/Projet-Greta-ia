import os
import xml.etree.ElementTree as ET
 
def replace_text_in_xml(directory, old_text, new_text):
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            filepath = os.path.join(directory, filename)
            tree = ET.parse(filepath)
            root = tree.getroot()
 
            for elem in root.iter():
                if old_text in elem.text:
                    elem.text = elem.text.replace(old_text, new_text)
 
            tree.write(filepath)
 
# Replace 'your_directory' with the path to your directory
replace_text_in_xml('D:\\Github\\Projet Greta ia\\mini projet\\Moustafa\\model_fruit\\Data', 'C:\\Users\\illye\\Documents\\labelimg_v1.8.1\\Exemple', 'D:\\Github\\Projet Greta ia\\mini projet\\Moustafa\\model_fruit')