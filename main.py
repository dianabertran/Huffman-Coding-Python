import json
from heapq import heappop, heappush
from bitstring import BitArray
import os

# opens and loads the file from config.json file
config = open('./config.json')
config_json = json.load(config)

# returns a list containing each line in the file as a list item
# uses encoding parameter to open file and read it in any possible language
file = open(config_json["filepath_text"], encoding="utf8").readlines()
# print(file)


def count_frequencies(file) -> dict:

    """
    This function opens a text file as an argument and then returns the
    frequencies each character occurs in the text file. The characters
    are then sorted out by order starting from the lowest frequency to
    the highest. Values sorted by ascending order.
    """

    dictionary = {}
    # loops through every line in the text file in config.json
    for line in file:
        # loops through every character in the text file in config.json
        for char in line:
            # checks if character has already been added to the dictionary
            if char not in dictionary:
                dictionary[char] = 1
            else:
                # if not added, then it proceeds to add that character into dictionary
                dictionary[char] = dictionary[char] + 1
    # dictionary is returned
    return dictionary


# store dictionary of frequencies in a variable called "d" for later usage
d = count_frequencies(file)
# print(d)


def creation_of_huffmantree(d) -> list:

    """
    This function gets the dictionary returned by the count_frequencies function
    and returns a list of lists that represent the huffman tree of the characters
    in the text file. It is formatted in the following way:
    [[character_frequency,[character,code]]
    At the start the code will be an empty string but it will have content later on.
    """
    # assign variable to lists of lists for huffman tree representation
    # uses items() method to return a view object
    # view object contains the key-value pairs of the dictionary, as tuples in a list.
    huffman_tree = [[frequency, [char, ""]] for char, frequency in d.items()]
    # uses while statements to create huffman tree
    # while the huffman tree length of list is longer than 1
    while len(huffman_tree) > 1:
        # use heappop to remove and return smallest item that stays at index 0 from the right branch
        right = heappop(huffman_tree)
        # print("right = ", right)
        # use heappop to remove and return smallest item that stays at index 0 from the left branch
        left = heappop(huffman_tree)
        # print("left= ", left)

        # loops through the right branch of the tree
        for pair in right[1:]:
            # adds zero to all the right branch
            pair[1] = '0' + pair[1]
        # print("right add zero = ", right)

        # loops through the left branch of the tree
        for pair in left[1:]:
            # adds one to all the left node
            pair[1] = '1' + pair[1]
        # print("left add one = ", left)
        # print(" ")
        # use heappush to add an element/values into the huffman tree
        heappush(huffman_tree, [right[0] + left[0]] + right[1:] + left[1:])
        # returns a list with the completed tree
        huffman_list = right[1:] + left[1:]

    return huffman_list


# print(creation_of_huffmantree(d))


def encoded_texts(huffman_list: list, new_list: list) -> str:

    """
    This function gets the list returned from the creation_of_huffmantree function
    and a new list as a parameter too. This function is used to obtain the encoded
    text, it replaces the characters with the context of the original text file with
    expected codes and therefore returns an encoded text.
    """
    # dictionary used to store data values in key
    dictionary = {}
    # joins all items in a dictionary into a string
    string = "".join(huffman_list)
    # loops through the list
    for i in new_list:
        dictionary[i[0]] = i[1]
    # print(dictionary)

    # uses maketrans method to create a mapping table
    convert = string.maketrans(dictionary)
    # uses translate method to return a string where some specified characters are replaced
    # characters are replaced with characters described above using mapping table
    encoded_text = string.translate(convert)
    # print(encoded_text)
    return dictionary, encoded_text


def padding_text(encoded_text: str):

    """
    This function gets the encoded_text string from the encoded_text function above
    and returns the padded version of the encoded text. Adds characters to format
    encoded text as it should be displayed. adds bits to encoded string so length
    is a multiple of 8 so can be encoded effectively.
    """
    # gets the extra padding of encoding text
    padded_text = 8 - (len(encoded_text) % 8)
    # print(padded_text)
    # loops through the padded text
    for i in range(padded_text):
        encoded_text += "0"
    # merges the details of extra padding in strings of bits with encoded text
    # this helps when shortening it later on
    # uses format method to format the specified values and insert them into string
    padded_data = "{0:08b}".format(padded_text)
    # joins the padded and the encoded text to get the final encoded text version
    encoded_text = padded_data + encoded_text
    return encoded_text


def compression():

    """
    This function is formatted to be used when compressing
    the text file. It makes use of the returned values in the following
    functions to get a correctly compressed file:
    --> count_frequencies function
    --> creation_of_huffmantree function
    --> encoded_text function
    --> padding_text function
    All of the above
    """

    path = config_json["filepath_text"]
    # the splitext method is used to split the path name into a pair root and ext.
    # ext being the extension(of the filepath) and root being everything except extension part
    filename, file_extension = os.path.splitext(path)
    # command to create filepath for the binary file
    output_path = filename+".bin"

    # opens and reads the file
    # uses encoding parameter to open file and read it in any possible language
    with open(path, "r", encoding="utf8") as file, open(output_path, "wb") as output:
        # uses read method that returns the specified number of bytes from the file
        # default is -1 (the whole file)
        text = file.read()
        # uses the rstrip method removes any trailing characters at the end of a string
        text = text.rstrip()
        # dictionary used to store data values in key
        d = {}
        frequency = count_frequencies(text)
        g = creation_of_huffmantree(frequency)

        # loops through each frequency element from dictionary
        for el in g:
            d[el[0]] = el[1]

        # uses maketrans method to create a mapping table
        table = text.maketrans(d)
        # uses translate method to return a string where some specified characters are replaced
        # characters are replaced with characters described above using mapping table
        encoded_text = text.translate(table)
        padded_encoded_text = padding_text(encoded_text)
        # saves bytes to a binary file
        b = BitArray(bin=padded_encoded_text)
        b.tofile(output)

    # returns compressed file
    return output_path


print("Successfully compressed the text file")


def remove_padding(bit_string):

    """
    This function is used in the decompress function to decompress the text
    file. Its functionality is to remove the padding added at the padding
    text function to get a correct decompression of the text.
    It returns the encoded text without the padding.
    """

    padded_data = bit_string[:8]
    extra_padding = int(padded_data, 2)

    bit_string = bit_string[8:]
    encoded_text = bit_string[:-1*extra_padding]

    return encoded_text


def decompress(input_path):

    """
    This functions functionality is to decompress the already compressed
    text file from before. It makes use of the returned values in the following
    functions to get a correctly compressed file:
    --> creation_of_huffmantree function
    --> encoded_text function
    --> remove_padding function
    All of the above
    """

    # the splitext method is used to split the path name into a pair root and ext.
    # ext being the extension(of the filepath) and root being everything except extension part
    filename, file_extension = os.path.splitext(input_path)
    output_path = filename+"_decompressed" + ".txt"

    # opens and reads the file
    # uses encoding parameter to open file and read it in any possible language
    with open(input_path, "rb") as file, open(output_path, "w", encoding="utf8") as output:
        bit_string = ""
        # returns the specified number of bytes from the file
        # default is -1 which means the whole file
        byte = file.read(1)
        # loops through the bytes until no bytes remaining to loop through therefore length will be null
        while len(byte) > 0:
            # using ord to return the number that represents the unicode code of each specified character
            byte = ord(byte)
            # using bin returns the binary string of each  and removes leading zeros
            # padding the number from the index to the end with 0's to the left to make a byte
            # adds this to the string
            bits = bin(byte)[2:].rjust(8, "0")
            bit_string += bits
            byte = file.read(1)

        encoded_text = remove_padding(bit_string)
        # print(encoded_text)
        decoded_text = decode_text(encoded_text, encoded_texts(file, creation_of_huffmantree(d))[0])
        # overwrite any existing content to decoded text
        output.write(decoded_text)

    print("Successfully decompressed the text file")
    return output_path


def decode_text(encoded_text: str, reverse_mapping: dict):

    """
    This function returns the decoded text from the text file.
    Uses for loops and if statement to obtain the decoded text.
    """

    decoded_text = ""
    current_code = ""

    # iterates over dictionaries using for loops
    reverse_mapping = dict((y, x) for x, y in reverse_mapping.items())
    # print(reverse_mapping)

    # loops through each bit in the encoded compressed text
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_mapping:
            char = reverse_mapping[current_code]
            decoded_text += char
            current_code = ""

    print("Text file was decoded successfully, the following displays the decoded text: ", decoded_text)

    return decoded_text


#print(count_frequencies(file))
#print(creation_of_huffmantree(d))
#print(encoded_texts(file, creation_of_huffmantree(d))[1])
#print(padding_text(encoded_texts(file, creation_of_huffmantree(d))[1]))
print(compression())
print(decompress(compression()))