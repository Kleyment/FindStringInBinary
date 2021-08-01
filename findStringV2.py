from argparse import ArgumentParser
import multiprocessing as mp

# This code is a overhaul of this of the code http://www.arcade-cabinets.com/patreon/rom_hacks/tools/findString.py
# described in the youtube channel arcade-cabinets.com in this video https://www.youtube.com/watch?v=4JFO_MEPHsE
# It is now coded in python 3 and support multiprocessing

def main():
    parser = ArgumentParser()
    parser.add_argument("query", help="the search expression that will be transformed into a difference between one byte and another")
    parser.add_argument("files", nargs="+", help="the file(s) where we try to find the searched expression")
    parser.add_argument("-s", "--step", type=int, dest="step", default=1, help="Assume there is <step>-1 useless byte(s) between each letter in the file, by default jump from one byte to the next one (1)")
    args = parser.parse_args()

    # Get the search string and the difference array of the search string
    searchString=args.query
    searchDiff=getDifferences(bytes(searchString,"UTF-8"),1)

    for filename in args.files:
        file=open(filename,"rb").read()
        print("Looking for "+searchString+" in "+filename)

        pool = mp.Pool(mp.cpu_count())
        
        # Execute the function searchInFile asynchronously
        for i in range (1,mp.cpu_count()+1):
            if i == 1:
                pool.apply_async(searchInFile,args=(file,filename,searchDiff,0,int(len(file)/(mp.cpu_count())),args.step))
            elif i < mp.cpu_count():
                pool.apply_async(searchInFile,args=(file,filename,searchDiff,int(len(file)/(mp.cpu_count())*(i-1)-len(searchString)),int(len(file)/(mp.cpu_count())*i),args.step))
            else:
                pool.apply_async(searchInFile,args=(file,filename,searchDiff,int(len(file)/(mp.cpu_count())*(i-1)-len(searchString)),int(len(file)/(mp.cpu_count())*i-len(searchString)),args.step))

        pool.close()
        pool.join()

# Build an array which describes how far away each byte is from the next
# searchBytes: bytes with classic encoding (where ABCDEFGHIKLMNOPQRSTUVWXYZ are following each other)
# step: in some case there is some useless bytes between two character so the step could be 2 and more (exemple Wario Land 4 search: executive)
def getDifferences(searchBytes: bytes, step: int=1) -> list: # (list) array of bytes
    diffArray=[]
    for i in range(0,len(searchBytes)-step,step):
        diffArray.append(searchBytes[i+step] - searchBytes[i])
    return diffArray


# Loop through the file checking if each character is the begging of a pattern
# That matches the difference values and print them
# file: bytes value of the file
# filename : string of the file to display where the match has been found
# searchDiff: bytes of the difference to compare with each fileDiff to see if it match
# beginning: int of beginning of the search offset
# end: int of end of the search offset
# step: in some case there is some useless bytes between two character so the step could be 2 and more (exemple Wario Land 4 search: executive)
def searchInFile(file: bytes, filename: str, searchDiff: bytes, beginning: int, end: int, step: int=1):
    for i in range(beginning,end):
        fileDiff=getDifferences(file[i:i+len(searchDiff)*step+1],step)
        if fileDiff == searchDiff:
            print("Match in "+filename+" at offset "+str(hex(i)))

main()