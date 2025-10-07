# Confluence-page-migration-fromMDfile
Confluence page update using markdown files

## System requirement:
* Python.
* Notepad.
* Any terminal application (cmd or git for windows).
* ```pip install requests markdown``` => run from CMD to install the dependency for md files. 

## How to upload:
* Folder structure:
	Main folder: script + Input folder(with .md files)
* Inside main folder, create a folder named "Input". Place all the .md file which need to be uploaded inside this "Input" folder.
* Create the script inside the main folder.
* Edit the script and change the hardcoded values as per requirement.
   	* Following values are hardcoded:
       * Confluence base url.
       * Space key.
       * username.
       * API Key.

6) *Space id* is the only variable.
4) Open command line in the main folder.
5) Run the script: python <filename>
6) Check the confluence.

