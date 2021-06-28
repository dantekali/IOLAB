import os,sys
import re 

# ioLab.py v1.901
# 
# DANTE AVIÑÓ - 106390
# 
 
# STEP 1: Read the following instructions carefully.
 
# You will provide your solution to the IO Lab by
# editing the collection of functions in this source file.

# For input/output, you only can use os.read() and os.write() functions. 
# However, you can use print()  in the showXXX functions  and for debugging purposes.

# This is an example!
# Argument filename is a path to the fastq file to read
# This function opens filename and reads the first sequence of bases and prints it on screen (stdout)
def showSequence(filename):
    fd  = os.open(filename, os.O_RDONLY)
    headerline = readLine(fd)      
    seqline    = readLine(fd)
    writeLine(seqline)
    os.close(fd)
    return 0


# str is a vector of ASCII bytes representing digits from 0 - 9
# function atoi converts str to integer.  The behavior is must be the same as 
# int(b''.join(str))
# example: if str = [b'3',b'0',b'9'] then  atoi(str) =  309
def atoi(str):
    out = 0
    for a in str:
        out = (int(a) + out) * 10   
    return (out//10)


# line is a byte string ended by '\n'
# that contains "length=<nnn>", where <nnn> are ascii digits
# readLenght(line) must return an integer
def readLength(line):    
    regex = r'length=(\d+)'
    matches = re.findall(regex,str(line))    
    return atoi(matches)


# Argument fd is a file descriptor of an already open file
# This functions returns a list of bytes read from the file 
# until a new line is reached (b'\n')
def readLine(fd):    
    out = []
    while True:       
        input = os.read(fd,1)
        if (not input):
            break
        elif (input == b'\n'):
            break
        else:
            out.append(input)
    return (b"".join(out))


# Argument line is a Fastq line in a bytestring. 
# like the return of readLine(fd).
# This function writes all the line to standard output
def writeLine(line):    
    os.write(1,line)  
    return 0

def writeLine2(fd,line):    
    os.write(fd,line)  
    return 0

# Argument filename is a path to the fastq file to  read
# This function opens filename and reads its first line, printing on screen
# the name of the sequence and the number of bases
def showHeader(filename):
    fd  = os.open(filename, os.O_RDONLY)
    line = readLine(fd)
    regex = r'(\@.*) length=(\d+)'
    matches = re.findall(regex,str(line))   
    print("Name: %s, Number of Bases: %s" % (matches[0][0],matches[0][1]))
    os.close(fd)
    return 0


# Argument filename is a path to the fastq file to read
# This function opens filename and reads bases on its fisrt sequence. For each base, 
# prints a pair base --> quality
def showSeqQlty(filename):
    fd = os.open(filename, os.O_RDONLY)
    #while True:      # loop for all seq in fastq
    headerline = readLine(fd)
    if headerline:
        seqline   = readLine(fd)
        readLine(fd)  # Breakline
        qltyline  = readLine(fd)
        seqlength = readLength(headerline)
        for i in range(seqlength):
            print ("%c --> %d" % (seqline[i], qltyline[i]-33 ))
    #    else:
    #        break    
    os.close(fd)
    return 0


# Arguments are bytestrings sequence of bases and its correspondence qualities
# The function returns de worst pair, ie, the base with the lowest quality
# Returns a list [base, quality] of the worst pair base -> quality
def worstQlty(seqLine, qltyLine): 
    worstqlty = qltyLine[0] - 33 
    base      = seqLine[0]
    seqlength = len( seqLine )

    for i in range(seqlength):
        quality =  qltyLine[i] - 33 
        if ( quality < worstqlty ):
            worstqlty = quality
            base = seqLine[i]
    return [base,worstqlty]


# Argument filename is a path to the fastq file to read
# This function opens filename and reads its bases. 
# It shows the worst pair. 
# Prints a pair base --> quality
def showWorstQlty(filename):
    fd  = os.open(filename, os.O_RDONLY)
    # Read first sequence and initiate allworst
    headerline = readLine(fd)
    if headerline:                
        seqline   = readLine(fd)
        readLine(fd)  # Breakline
        qltyline  = readLine(fd)
        allworst  = worstQlty(seqline,qltyline)

    """ If refering to the worst of all sequences in file:
    # Read the remaining sequences and update allworst accordingly
    while True:
        headerline = readLine(fd)       
        if headerline:            
            seqline   = readLine(fd)
            readLine(fd)  # Breakline
            qltyline  = readLine(fd)
            worst = worstQlty(seqline,qltyline)
        if (worst[1] < allworst[1]):
            allworst = worst        
        else:
            break
    """
    
    print("The worst: %c -> %d" % (allworst[0],allworst[1]))
    os.close(fd)    
    return 0


### TEST ioLab.py
filename  = 'SRR000049.fastq'
scriptdir = os.path.dirname(__file__)
filepath  = os.path.join(scriptdir,filename)

print(f"\nTesting showSequence of {filepath}...\n")
showSequence(filepath)
print(f"\nTesting showHeader of {filepath}...\n")
showHeader(filepath)
print(f"\nTesting showSeqQlty of {filepath}...\n")
showSeqQlty(filepath)
print(f"\nTesting showWorstQlty of {filepath}...\n")
showWorstQlty(filepath)
