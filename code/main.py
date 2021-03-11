import sys
import os

TUPLE_PER_BLOCK = 100


def fun_openSM(Rfn, Sfn, M):
    Rfile = open(Rfn, 'r')
    intermed_fnum = 0  # number of intermediate file
    canread = True
    while canread:
        lines = []
        for i in range(M*TUPLE_PER_BLOCK):
            t = Rfile.readline()
            if not t:
                canread = False
                break
#           if t[-1]=='\n':
#               t = t[:-1]
            rowlist = t.strip().split(' ')
            lines.append(rowlist)

        if len(lines) > 0:
            lines.sort(key=lambda x: x[1])
            intermedfile = open('intermedR'+str(intermed_fnum)+'.txt', 'w')
            intermed_fnum += 1
            for i in range(len(lines)):
                lines[i] = lines[i][0]+' '+lines[i][1]+'\n'
            intermedfile.writelines(lines)
            intermedfile.close()

    Rfile.close()

    fileheap = []
    intermedfiles = []
    for i in range(intermed_fnum):
        #intermedfile = open('intermedR'+str(i)+'.txt', 'r')
        #t = intermedfile.readline()
        # intermedfiles.append(intermedfile)
        intermedfiles.append(open('intermedR'+str(i)+'.txt', 'r'))
        t = intermedfiles[-1].readline()
        rowlist = t.strip().split(' ')
        fileheap.append([i, rowlist])
        # intermedfile.close()
    fileheap.sort(key=lambda x: x[1][1])

    BR = 0  # final sublist number, also the number of blocks
    count = 0  # count number of tuples written in a final file
    finalfile = open('finalR'+str(BR)+'.txt', 'w')
    intermeds_done = 0
    while intermeds_done < intermed_fnum:
        top = fileheap[0]

        # write line in final file
        # if count of lines written gets bigger than M*TUPLE_PER_BLOCK
        # then open a new final file for writing
        line = top[1][0]+' '+top[1][1]+'\n'
        finalfile.write(line)
        count += 1
        if count >= M*TUPLE_PER_BLOCK:
            finalfile.close()
            BR += 1
            finalfile = open('finalR'+str(BR)+'.txt', 'w')
            count = 0

        # get a newline from the file from which we just wrote in final file.
        # if file is exhausted close it, and increment intermeds_done.
        # also get rid of first element in fileheap
        # otherwise split the line into a list and replace
        newline = intermedfiles[top[0]].readline()
        if newline:
            rowlist = newline.strip().split()
            fileheap[0] = [top[0], rowlist]
        else:
            intermeds_done += 1
            fileheap = fileheap[1:]
            intermedfiles[top[0]].close()
        fileheap.sort(key=lambda x: x[1][1])
    finalfile.close()

    # get rid of intermediate files
    for i in range(intermed_fnum):
        os.remove('intermedR'+str(i)+'.txt')

    # if last final file is empty delete it.
    # if there is some content then incrmement BR by 1
    lastfinalfile = open('finalR'+str(BR)+'.txt', 'r')
    if not lastfinalfile.readline():
        lastfinalfile.close()
        os.remove('finalR'+str(BR)+'.txt')
    else:
        lastfinalfile.close()
        BR += 1

    # Work on Relation S here.

    Sfile = open(Sfn, 'r')
    intermed_fnum = 0  # number of intermediate files
    canread = True
    while canread:
        lines = []
        for i in range(M*TUPLE_PER_BLOCK):
            t = Sfile.readline()
            if not t:
                canread = False
                break
#           if t[-1]=='\n':
#               t = t[:-1]
            rowlist = t.strip().split(' ')
            lines.append(rowlist)

        if len(lines) > 0:
            lines.sort(key=lambda x: x[1])
            intermedfile = open('intermedS'+str(intermed_fnum)+'.txt', 'w')
            intermed_fnum += 1
            for i in range(len(lines)):
                lines[i] = lines[i][0]+' '+lines[i][1]+'\n'
            intermedfile.writelines(lines)
            intermedfile.close()

    Sfile.close()

    fileheap = []
    intermedfiles = []
    for i in range(intermed_fnum):
        #intermedfile = open('intermedR'+str(i)+'.txt', 'r')
        #t = intermedfile.readline()
        # intermedfiles.append(intermedfile)
        intermedfiles.append(open('intermedS'+str(i)+'.txt', 'r'))
        t = intermedfiles[-1].readline()
        rowlist = t.strip().split(' ')
        fileheap.append([i, rowlist])
        # intermedfile.close()
    fileheap.sort(key=lambda x: x[1][1])

    BS = 0  # final sublist number, also the number of blocks
    count = 0  # count number of tuples written in a final file
    finalfile = open('finalS'+str(BS)+'.txt', 'w')
    intermeds_done = 0
    while intermeds_done < intermed_fnum:
        top = fileheap[0]

        # write line in final file
        # if count of lines written gets bigger than M*TUPLE_PER_BLOCK
        # then open a new final file for writing
        line = top[1][0]+' '+top[1][1]+'\n'
        finalfile.write(line)
        count += 1
        if count >= M*TUPLE_PER_BLOCK:
            finalfile.close()
            BS += 1
            finalfile = open('finalS'+str(BS)+'.txt', 'w')
            count = 0

        # get a newline from the file from which we just wrote in final file.
        # if file is exhausted close it, and increment intermeds_done.
        # also get rid of first element in fileheap
        # otherwise split the line into a list and replace
        newline = intermedfiles[top[0]].readline()
        if newline:
            rowlist = newline.strip().split()
            fileheap[0] = [top[0], rowlist]
        else:
            intermeds_done += 1
            fileheap = fileheap[1:]
            intermedfiles[top[0]].close()
        fileheap.sort(key=lambda x: x[1][1])
    finalfile.close()

    # get rid of intermediate files
    for i in range(intermed_fnum):
        os.remove('intermedS'+str(i)+'.txt')

    # if last final file is empty delete it.
    # if there is some content then incrmement BR by 1
    lastfinalfile = open('finalS'+str(BS)+'.txt', 'r')
    if not lastfinalfile.readline():
        lastfinalfile.close()
        os.remove('finalS'+str(BS)+'.txt')
    else:
        lastfinalfile.close()
        BS += 1

    return BR, BS


def fun_SortMerge(Rfn, Sfn, M):
    # first deal with R, then with S
    BR, BS = fun_openSM(Rfn, Sfn, M)
    print(BR, BS)


def main():
    Rfn = sys.argv[1]  # filename of R
    Sfn = sys.argv[2]  # filename of S
    join_type = sys.argv[3]
    M = int(sys.argv[4])

    if join_type == 'sort':
        fun_SortMerge(Rfn, Sfn, M)
        pass
    else:
        pass


if __name__ == '__main__':
    main()
