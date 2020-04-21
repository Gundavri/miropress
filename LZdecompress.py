from sys import argv
import time


def is2sPower(num):
    while num > 1:
        num /= 2
    return num == 1


def makeLexLonger(lex, currLen):
    first = lex.copy()
    for key in first:
        if len(key) == currLen:
            lex['0'+key] = lex[key]
            del lex[key]


def readAndWriteFile(fr, num):
    res = ''
    for i in range(num):
        single_byte = fr.read(1)
        if not single_byte:
            break
        res += writeInBits(ord(single_byte))
    return res


def writeInBits(single_byte):
    result = ''
    for i in range(0, 8):
        single_bit = single_byte << i
        single_bit = single_bit & 128
        if single_bit > 0:
            result += '1'
        else:
            result += '0'
    return result


def bufferEliasCode(fr):
    global codeToDecompress
    counter = 0
    while True:
        codeToDecompress += readAndWriteFile(fr, 1)
        counter += 1
        if int(codeToDecompress) > 0:
            break
    for i in range(counter):
        codeToDecompress += readAndWriteFile(fr, 1)


def findFileSize(fr):
    global codeToDecompress
    global fileToWriteSize
    counter = 0
    for i in codeToDecompress:
        if i == '0':
            counter += 1
        else:
            break

    binaryString = codeToDecompress[counter:2*counter+1]
    codeToDecompress = codeToDecompress[2*counter+1:]
    fileToWriteSize = int(binaryString, 2)
    codeToDecompress += readAndWriteFile(fr, 1)


def writeInFile(code, fileToWrite):
    while len(code) > 0:
        temp = code[0:8]
        code = code[8:]
        temp = int(temp, 2)
        fileToWrite.write(temp.to_bytes(1, "little"))


def main(fileToRead, fileToWrite):
    global codeToDecompress

    start_time = time.time()

    fileToRead = open(fileToRead, 'rb')
    fileToWrite = open(fileToWrite, 'wb')

    codeToDecompress = ''
    codeToWrite = ''
    fileToWriteSize = 0
    keySize = 1

    lexicon = {
        '0': '0',
        '1': '1'
    }

    bufferEliasCode(fileToRead)
    findFileSize(fileToRead)

    while len(codeToDecompress) > 0:
        if keySize+1 > len(codeToDecompress):
            codeToDecompress += readAndWriteFile(fileToRead, keySize//8 + 1)
        key = codeToDecompress[0:keySize]
        codeToDecompress = codeToDecompress[keySize:]
        val = ''
        try:
            val = lexicon[key]
        except:
            break
        codeToWrite += val
        codeToCutSize = len(codeToWrite)//8*8
        writeInFile(codeToWrite[0:codeToCutSize], fileToWrite)
        codeToWrite = codeToWrite[codeToCutSize:]
        lexicon[key] = val + '0'
        lexicon[bin(len(lexicon))[2:]] = val + '1'
        if is2sPower(len(lexicon)-1) and len(lexicon) != 2:
            makeLexLonger(lexicon, keySize)
            keySize += 1

    fileToRead.close()
    fileToWrite.close()

    print(str(time.time()-start_time) + ' --- Decompress Time')


def init():
    main(argv[1], argv[2])


if __name__ == '__main__':
    init()
