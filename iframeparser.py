import glob
import os

version_nr = "1.0"
print("Camtasia mAuthor server parser\nVersion %s\nDeveloped by Eivind Rostad for Cyberbook AS" %version_nr)
print("This is a script that changes the local references for the Camtasia HTML video player so that it can be imported from the mAuthor servers via an iframe")
serverdir = "/file/serve/"
address_player_js = serverdir + "5241833092415488"
address_player_css = serverdir + "5519734387900416"


directory = input("File directory for the rendered project: ")
def getprojectname(directory):
    #Use the name of the .mp4 file to determine the name of the project
    os.chdir(directory)
    mp4 = glob.glob("*.mp4")
    if len(mp4) == 0: #Exception handler for no .mp4 file
        print("no .mp4 files in this directory.")
        return 0
    elif len(mp4) > 1: #Exception handler for multiple .mp4s
        print("Found multiple video files in directory")
        for (i, item) in enumerate(mp4, start=1):
            print(i, item)
        correctidx = int(input("Which one is the right file? number: "))
        return mp4[correctidx - 1].rstrip('.mp4')

    else:
        return mp4[0].rstrip('.mp4')

def findandreplace(filetochange, wordmap):
    # Read in the file
    with open(filetochange, 'r') as file:
        filedata = file.read()

    # Replace the target string
    for k, v in wordmap:
        filedata = filedata.replace(k, v)

    # Write the file out again
    with open(filetochange, 'w') as file:
        file.write(filedata)

projectname = getprojectname(directory)

if projectname == 0: #avoid using recursion for reprompting
    projectname = getprojectname(directory)

namenospace = projectname.replace(" ", "_")

#generate filenames
file_config_xml = "%s_config.xml" %projectname
file_player_html = "%s_player.html" %projectname
file_mp4 = "%s.mp4" %projectname
file_firstframe = "%s_First_Frame.png" %namenospace
file_thumbnails = "%s_Thumbnails.png" %namenospace
file_player_css = "skins/remix/techsmith-smart-player.min.css"
file_config_xml_js = "scripts/config_xml.js"
file_player_js = "scripts/techsmith-smart-player.min.js"

print("\nCreate an iframe in mAuthor, and upload the .mp4 and the two .png files to the File list")
address_mp4 = input("Input the server reference for the .mp4 file: /file/serve/")
address_firstframe = serverdir + input("Input the server reference for the first_frame.png file: /file/serve/")
address_thumbnails = serverdir + input("Input the server reference for the thumbnails.png file: /file/serve/")

###todo: separate into assignment lists
replacemap_partial = [(file_mp4, address_mp4), (file_firstframe, address_firstframe), (file_thumbnails, address_thumbnails)]
findandreplace(file_config_xml, replacemap_partial)

os.chdir(directory + "\scripts")
findandreplace("config_xml.js", replacemap_partial)
####todo: parse this file with correct formatting
#mapping_test = ['        <div class="pip-wrapper">\n', ""] <- formatting is a problem here
#findandreplace("techsmith-smart-player.min.js", mapping_test)
os.chdir(directory)
print("Now, upload ~config.xml and \scripts\config_xml.js to the file list")
address_config_xml = serverdir + input("Input the server reference for the config.xml file: /file/serve/")
address_config_xml_js = serverdir + input("Input the server reference for the \scripts\config_xml.js file: /file/serve/")

replacemap_full = replacemap_partial + [(file_player_css, address_player_css), (file_config_xml_js, address_config_xml_js), (file_config_xml, address_config_xml), (file_player_js, address_player_js)]
findandreplace(file_player_html, replacemap_full)
print("Now upload <%s> as the <index file>, and you are done.\n" %file_player_html)
input("Press Enter to continue...")

