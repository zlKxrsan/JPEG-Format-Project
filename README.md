# Preamble
This project contains some simple modules to manipulate a jpeg.file. To present our knowledge
about the dataflow of a jpeg we decided to manipulate the raw data of the EXIF- and DQT-Segments and also to update the coeficients of the entropie-coded Data with the help of jpegio.

# Important to know
The jpegs used are all copyright free to use. All of them are big endian based (4D 4D), contain a exif_header and use a 4:1:1 sampling for YCbCr so our examples are working with them, but are by no means exception safe for different data.

# Guide
Our main.py is for running all manipulations for a single file. To use a specific file just rename the input variable to the file name and make sure the file is in the jpegs/ folder. 

# References
- bird1.jpeg: https://pxhere.com/en/photo/810613
- bird2.jpeg: https://pxhere.com/en/photo/553565
- bird3.jpeg: https://pxhere.com/en/photo/1065658
- frog1.jpeg: https://pxhere.com/en/photo/1325016