# Preamble
This project contains some simple modules to manipulate a jpeg.file. To present our knowledge
about the dataflow of a jpeg we decided to manipulate the raw data of the EXIF- and DQT-Segments and also to update the coeficients of the entropie-coded Data with the help of jpegio.

# Important to know
The jpegs used are all copyright free to use. All of them are big endian based (4D 4D), contain a exif_header and use a 4:1:1 sampling for YCbCr so our examples are working with them, but are by no means exception safe for different data.

# Guide
- First step is to activate the included virtual enviroment we created to ensure portability if an error happens the command
"pip3 install -r requirements.txt can probably fix it"
- Our script.py is for running all manipulations for a single file or all files in the /jpegs folder. To use a specific file just add it with a parameter (examples following) and make sure the file is in the jpegs/ folder.
- If you want to call script.py with E.g. frog1.jpeg make sure it is in the following folder /jpegs and run this command:
"python3 script.py -a frog1.jpeg"
- If you want to call script.py on every file in the folder just run it like this:
"python3 script.py"

# Note
- After testing this project we realized the requiered wheel for jpegio can't be build on windows 11 and therefore or project shouldn't work on it.

# References
- bird1.jpeg: https://pxhere.com/en/photo/810613
- bird2.jpeg: https://pxhere.com/en/photo/553565
- bird3.jpeg: https://pxhere.com/en/photo/1065658
- frog1.jpeg: https://pxhere.com/en/photo/1325016