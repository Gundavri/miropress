from sys import argv
import os, time

def writeEliasCode(size):
    binarySize = bin(size)[2:]
    eliasPrefixSize = len(binarySize) - 1
    for i in range(eliasPrefixSize):
        binarySize = '0' + binarySize
    return binarySize

def readAndWriteFile(fr, num):
    res = ''
    for i in range(num):
        single_byte = fr.read(1)
        if  not single_byte:
            break
        res += writeInBits(ord(single_byte))
    return res

def writeInBits(single_byte):
    result = ''
    for i in range(0, 8):
        single_bit = single_byte << i
        single_bit = single_bit & 128
        if  single_bit > 0:
            result += '1'
        else:
            result += '0'
    return result

def findBiggestPref(lex):
    global longestKeySize
    for i in range(longestKeySize, 0, -1):
        pref = codeToCompress[0:i]
        if pref in lex:
            return pref
    return codeToCompress

def is2sPower(num):
    while num > 1 :
        num /= 2
    return num == 1

def makeLexLonger(lex, currLen):
    for key in lex:
        if len(lex[key]) == currLen:
            lex[key] = '0' + lex[key]

def changeLexicon(biggestPref, lex):
    global longestKeySize
    currLen = len(lex[biggestPref])
    lex[biggestPref+'0'] = lex[biggestPref]
    del lex[biggestPref]
    newVal = bin(len(lex))[2:]
    lex[biggestPref+'1'] = newVal

    newKeyLen = len(biggestPref) + 1
    if longestKeySize < newKeyLen:
        longestKeySize = newKeyLen

    if is2sPower(len(lex)-1):
        makeLexLonger(lex, currLen)
    
def writeInFile(code, fileToWrite):
    while len(code) > 0:
        temp = code[0:8]
        code = code[8:]
        temp = int(temp, 2)
        fileToWrite.write(temp.to_bytes(1, "little"))
		
def main(fileToRead, fileToWrite):
	global longestKeySize
	global codeToCompress
	
	start_time = time.time()
	
	size = os.path.getsize(fileToRead)
	
	fileToRead = open(fileToRead, 'rb')
	fileToWrite = open(fileToWrite, 'wb')
	
	codeToCompress = ''
	longestKeySize = 1
	codeToWrite = writeEliasCode(size)

	lexicon = {
		'0': '0',
		'1': '1'
	}

	codeToCompress = readAndWriteFile(fileToRead, 1)

	while len(codeToCompress) > 0:
		if longestKeySize+1 > len(codeToCompress): 
			codeToCompress += readAndWriteFile(fileToRead, (longestKeySize//8)+1)
		biggestPref = findBiggestPref(lexicon)
		while biggestPref not in lexicon:
			biggestPref += '0'
		codeToWrite += lexicon[biggestPref]
		codeToCutSize = len(codeToWrite)//8*8
		writeInFile(codeToWrite[0:codeToCutSize], fileToWrite)
		codeToWrite = codeToWrite[codeToCutSize:]
		changeLexicon(biggestPref, lexicon)
		codeToCompress = codeToCompress[len(biggestPref):]

	codeToWrite += '1'
	while len(codeToWrite)%8 != 0:
		codeToWrite += '0'

	writeInFile(codeToWrite, fileToWrite)
	fileToRead.close()
	fileToWrite.close()

	print(str(time.time()-start_time) + ' --- Compress Time')
	
def init():
	main(argv[1], argv[2])
	
if __name__ == '__main__':
	init()