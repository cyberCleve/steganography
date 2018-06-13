#!/usr/bin/env python3

def chunks(ls, ch):
    for m in range(0, len(ls), ch):
        yield ls[m:m+ch]

def encode_pgm(msg,coverfilename,outputfilename):
    '''Encodes a message in a PGM file
    Args:
        msg (str): the message to encode
        coverfilename (str): the name of the PGM file on disk to use as the cover
        outputfilename (str): the name of the new PGM file to write
    Returns:
        None
    '''

    imageHandler = open(str(coverfilename))
    image = imageHandler.readlines()
    imageHeader = image[0:4]
    imageHeader = ''.join(imageHeader)
    image = image[4:]
    imageHandler.close()

    # setup message
    messagebin = []
    message = str(msg)
    for letter in message:
        letter = format(ord(letter),'0>8b')
        letter = list(letter)
        for bit in letter:
            messagebin.append(int(bit))

    # entire message represented in bin
    #print(messagebin)

    # setup image
    imagebin = []

    i = 0
    broke = True
    for line in image:
        line = format(int(line),'0>8b')
        if i < len(messagebin):
            imagebin.append(str(line[0:7]) + str(messagebin[i]))
            i += 1
        else:
            if broke == True:
                imagebin.append(str(100010010))
                broke = False
            imagebin.append(str(line))

    #print(imagebin)

    # open file for writing
    fileHandler = open(str(outputfilename),'w')
    fileHandler.write(imageHeader)

    # build image back into ints
    for pixel in range(len(imagebin)):
        fileHandler.write(str(int(imagebin[pixel], 2)))
        fileHandler.write('\n')
        #print(str(int(imagebin[pixel],2)))

    fileHandler.close()
    pass

def decode_pgm(filename):
    '''Decodes a message hidden in a PGM file
    Args:
        filename (str): the name of the PGM file that contains a hidden message
    Returns:
        str: the message that was encoded in the PGM file
    '''
    fileHandler = open(filename)
    image = fileHandler.readlines()
    fileHandler.close()
    image = image[4::]
    message = []

    for pixel in image:
        if int(pixel) != 274:
            pixel = format(int(pixel),'0>8b')
            message.append(pixel[-1])
        else:
            break

    # message is now a list of lists 8 bits each
    message = chunks(message,8)
    decodedmsg = []

    for letter in message:
        decodedmsg.append(chr(int(''.join(letter),2)))

    return str(''.join(decodedmsg))

if __name__ == '__main__':
    encode_pgm('This message is hidden within an image','plain.pgm','out.pgm')
    print(decode_pgm('out.pgm'))
    pass
