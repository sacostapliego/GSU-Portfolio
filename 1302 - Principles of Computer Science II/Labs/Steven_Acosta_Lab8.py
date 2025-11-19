#total numbers of words
def numWords(filename):
    infile = open(filename)
    content = infile.read()
    infile.close
    wordList = content.split()

    return len(wordList)

#total numbers of lines
def numLines (filename):
    infile = open(filename)
    lines = infile.readlines()
    infile.close

    return len(lines)

#number of words in each line of the file
def numWordsAndLines (filename):
    wordsInLines = []
    with open(filename,'r') as f:
        for line in f:
            words = line.split()
            wordsInLines.append(len(words))
    return wordsInLines


with open('output.txt','r+') as f:
    #Writes both of the vaules of the functions
    f.write(f"Total number of lines: {str(numLines('example.txt'))}\n")
    f.write(f"Total number of words: {str(numWords('example.txt'))}\n")
    numsWordsLines = numWordsAndLines('example.txt')
    #Prints out each line and number from the function above
    for i in range(len(numsWordsLines)):
        f.write(f"Line{i + 1} >> {numsWordsLines[i]} words\n")
