#Python Implementation of Huffman Encoding

### Introduction:
This program is used to implement the Huffman encoding for compression and decompression of different text files.
The program allows user to input different files into the textfile.txt file for compression and decompression to be accomplished successfully.

### Requirements:
--> Python 3.8
--> Imports:
            
            --> pip install bitstring 

            --> from heapq import heappop, heappush
            
            --> import json
            
--> Terminal

### Making use of the program:
--> Navigate and run  main.py from the source files

--> When main.py runs a textfile.bin will appear and so will the textfile_decompressed.txt file will appear

--> These two files are the compressed and decompressed version of the textfile input at the start
                
If compiled and decompiled successfully, a confirmation message will appear. 
A compressed file and a decompressed file in the directory of the input file will be created.
 
 Link to screen recording of how program works:    
https://screenrec.com/share/GUBLkDKzZF           


### Data that user could input into textfile.txt:
Below are ebooks that are made available to input as data for the Huffman coding implementation.
If user wants to use a specific book; go to the following website and search for it:
https://www.gutenberg.org/: 
Other data sets that can also be used to test the program can be found in the following website:
http://pizzachili.dcc.uchile.cl/repcorpus.html, eg. rs.13.txt


| File name                                             |
|------------------------------------------------------|
| Pride and prejudice.txt      | Language: English      |
| Pride and prejudice.en.fr.txt| Language: French       | 
| Pride and prejudice.en.pt.txt| Language: Portuguese   |
| Frankenstein.txt             | Language: English      |
| Frankenstein.en.fr.txt       | Language: French       |                                            
| Frankenstein.en.pt.txt       | Language: Portuguese   |