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
        intermedfiles.append(open('intermedR'+str(i)+'.txt', 'r'))
        t = intermedfiles[-1].readline()
        rowlist = t.strip().split(' ')
        fileheap.append([i, rowlist])
    fileheap.sort(key=lambda x: x[1][1])

    BR = 0  # block sublist number, also the number of blocks
    count = 0  # count number of tuples written in a block file
    blockfile = open('blockR'+str(BR)+'.txt', 'w')
    intermeds_done = 0
    while intermeds_done < intermed_fnum:
        top = fileheap[0]

        # write line in block file
        # if count of lines written gets bigger than M*TUPLE_PER_BLOCK
        # then open a new block file for writing
        line = top[1][0]+' '+top[1][1]+'\n'
        blockfile.write(line)
        count += 1
        if count >= M*TUPLE_PER_BLOCK:
            blockfile.close()
            BR += 1
            blockfile = open('blockR'+str(BR)+'.txt', 'w')
            count = 0

        # get a newline from the file from which we just wrote in block file.
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
    blockfile.close()

    # get rid of intermediate files
    for i in range(intermed_fnum):
        os.remove('intermedR'+str(i)+'.txt')

    # if last block file is empty delete it.
    # if there is some content then incrmement BR by 1
    lastblockfile = open('blockR'+str(BR)+'.txt', 'r')
    if not lastblockfile.readline():
        lastblockfile.close()
        os.remove('blockR'+str(BR)+'.txt')
    else:
        lastblockfile.close()
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
            lines.sort(key=lambda x: x[0])
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
        intermedfiles.append(open('intermedS'+str(i)+'.txt', 'r'))
        t = intermedfiles[-1].readline()
        rowlist = t.strip().split(' ')
        fileheap.append([i, rowlist])
    fileheap.sort(key=lambda x: x[1][0])

    BS = 0  # block sublist number, also the number of blocks
    count = 0  # count number of tuples written in a block file
    blockfile = open('blockS'+str(BS)+'.txt', 'w')
    intermeds_done = 0
    while intermeds_done < intermed_fnum:
        top = fileheap[0]
        line = top[1][0]+' '+top[1][1]+'\n'
        blockfile.write(line)
        count += 1
        if count >= M*TUPLE_PER_BLOCK:
            blockfile.close()
            BS += 1
            blockfile = open('blockS'+str(BS)+'.txt', 'w')
            count = 0
        newline = intermedfiles[top[0]].readline()
        if newline:
            rowlist = newline.strip().split()
            fileheap[0] = [top[0], rowlist]
        else:
            intermeds_done += 1
            fileheap = fileheap[1:]
            intermedfiles[top[0]].close()
        fileheap.sort(key=lambda x: x[1][0])
    blockfile.close()

    for i in range(intermed_fnum):
        os.remove('intermedS'+str(i)+'.txt')

    lastblockfile = open('blockS'+str(BS)+'.txt', 'r')
    if not lastblockfile.readline():
        lastblockfile.close()
        os.remove('blockS'+str(BS)+'.txt')
    else:
        lastblockfile.close()
        BS += 1

    return BR, BS, open('blockR0.txt', 'r'), open('blockS0.txt', 'r')
#
#
# def fun_getNextSM(blockR, blockS, M, tR, tS, curbR, curbS, BR, BS):
#
#    # if no tuples read yet then read them
#    # if tR == None and tS == None:
#    #    tR = blockR.readline().strip().split(' ')
#    #    tS = blockS.readline().strip().split(' ')
#    #    while tR[1]<tS[0]:
#    #        tR
#
#    # get next tuple from S.
#    # if no lines left, then open next block and read line
#    # if no blocks left then we are done joining and return.
#    tS = blockS.readline()
#    if not tS:
#        curbS += 1
#        if curbS >= BS:
#            return tR, None, blockR, blockS, curbR, curbS
#        else:
#            blockS.close()
#            blockS = open('blockS'+str(curbS)+'.txt', 'r')
#            tS = blockS.readline().strip().split(' ')
#    else:
#        tS = tS.strip().split(' ')
#
#    while True:
#        # if we already have same y then simply return data.
#        if tR==None:
#            tR = blockR.readline()
#            if not tR:
#                curbR += 1
#                if curbR >= BR:
#                    return None, tS, blockR, blockS, curbR, curbS
#                else:
#                    blockR.close()
#                    blockR = open('blockR'+str(curbR)+'.txt', 'r')
#                    tR = blockR.readline().strip().split()
#            else:
#                tR = tR.strip().split()
#
#        if tS[0] == tR[1]:
#
#            return tR, tS, blockR, blockS, curbR, curbS
#
#        # otherwise go through R
#        elif tS[0]>tR[1]:
#            tR = blockR.readline()
#            if not tR:
#                curbR += 1
#                if curbR >= BR:
#                    return None, tS, blockR, blockS, curbR, curbS
#                else:
#                    blockR.close()
#                    blockR = open('blockR'+str(curbR)+'.txt', 'r')
#                    tR = blockR.readline().strip().split()
#            else:
#                tR = tR.strip().split()
#
#        # in this case get new S tuples until possible.
#        elif tS[0] < tR[1]:
#            tS = blockS.readline()
#            if not tS:
#                curbS += 1
#                if curbS >= BS:
#                    return tR, None, blockR, blockS, curbR, curbS
#                else:
#                    blockS.close()
#                    blockS = open('blockS'+str(curbS)+'.txt', 'r')
#                    tS = blockS.readline().strip().split(' ')
#            else:
#                tS = tS.strip().split(' ')
#
#    return tR, tS, blockR, blockS, curbR, curbS


def fun_getNextS(rel, B, curb, blockptr, startline):
    if rel == 'R':
        Rset = open('Rset.txt', 'w')
        tR = None
        blockptr.seek(0)
        for _ in range(startline):
            blockptr.readline()
        tR = blockptr.readline()
        if not tR:
            return 0, curb, blockptr, 0
        yval = tR.strip().split(' ')[1]
        Rset.write(tR)
        count = 1
        startline += 1
        while True:
            tR = blockptr.readline()
            if not tR:
                curb += 1
                if curb >= B:
                    return count, curb, blockptr, startline
                else:
                    blockptr.close()
                    blockptr = open('blockR'+str(curb)+'.txt', 'r')
                    startline = 0
                    tR = blockptr.readline()
            if tR.strip().split(' ')[1] == yval:
                Rset.write(tR)
                count += 1
                startline += 1
            else:
                Rset.close()
                return count, curb, blockptr, startline
    else:
        Sset = open('Sset.txt', 'w')
        tS = None
        blockptr.seek(0)
        for _ in range(startline):
            blockptr.readline()
        tS = blockptr.readline()
        if not tS:
            return 0, curb, blockptr, 0
        yval = tS.strip().split(' ')[0]
        Sset.write(tS)
        count = 1
        startline += 1
        while True:
            tS = blockptr.readline()
            if not tS:
                curb += 1
                if curb >= B:
                    return count, curb, blockptr, 0
                else:
                    blockptr.close()
                    blockptr = open('blockS'+str(curb)+'.txt', 'r')
                    startline = 0
                    tS = blockptr.readline()
            if tS.strip().split(' ')[0] == yval:
                Sset.write(tS)
                count += 1
                startline += 1
            else:
                Sset.close()
                return count, curb, blockptr, startline


def fun_cartesian(joinptr):
    Rset = open('Rset.txt', 'r')
    tR = Rset.readline()
    while tR:
        Sset = open('Sset.txt', 'r')
        tS = Sset.readline()
        while tS:
            joinptr.write(tR.strip()+' '+tS.strip().split(' ')[1]+'\n')
            tS = Sset.readline()
        tR = Rset.readline()
        Sset.close()
    Rset.close()
    os.remove('Rset.txt')
    os.remove('Sset.txt')


def fun_SortMerge(Rfn, Sfn, M):
    # first deal with R, then with S
    BR, BS, blockR, blockS = fun_openSM(Rfn, Sfn, M)
    if BR+BS > M**2:
        print("Too many blocks")
        return

    joinfile = open('joinfile.txt', 'w')
    lines = []
    curbR, curbS = 0, 0
    countR, curbR, blockR, startR = fun_getNextS('R', BR, curbR, blockR, 0)
    countS, curbS, blockS, startS = fun_getNextS('S', BS, curbS, blockS, 0)
    #print(countR, startR)
    # return
    while countR > 0 and countS > 0:
        #input()
        Rset = open('Rset.txt', 'r')
        Sset = open('Sset.txt', 'r')
        tR = Rset.readline()
        tS = Sset.readline()
        Rset.close()
        Sset.close()

        if tR.strip().split(' ')[1] == tS.strip().split(' ')[0]:
            #print(tR.strip(), end=' ')
            # print(tS)
            fun_cartesian(joinfile)
            countR, curbR, blockR, startR = fun_getNextS(
                'R', BR, curbR, blockR, startR)
            countS, curbS, blockS, startS = fun_getNextS(
                'S', BS, curbS, blockS, startS)
        elif tR.strip().split(' ')[1] < tS.strip().split(' ')[0]:
            countR, curbR, blockR, startR = fun_getNextS(
                'R', BR, curbR, blockR, startR)
        else:
            countS, curbS, blockS, startS = fun_getNextS(
                'S', BS, curbS, blockS, startS)
    #bufferSwrite = open('bufferS.txt','w')
    #bufferSread = open('bufferS.txt', 'r')
    # tR, tS, blockR, blockS, curbR, curbS = fun_getNextSM(
    #    blockR, blockS, M, None, None, curbR, curbS, BR, BS)
    # while True:
    #    tR, tS, blockR, blockS, curbR, curbS = fun_getNextSM(
    #        blockR, blockS, M, tR, tS, curbR, curbS, BR, BS)
    #    if tR == None or tS == None:
    #        joinfile.writelines(lines)
    #        break
    #    line = tR[0]+' '+tR[1]+' '+tS[1]+'\n'
    #    lines.append(line)
    #    if len(lines) >= M*TUPLE_PER_BLOCK:
    #        joinfile.writelines(lines)
    #        lines = []

    joinfile.close()


def test():
    R = open('..\inputR', 'r')
    outputfile = open('mytest.txt', 'w')
    r = R.readline()
    while r:
        S = open('..\inputS', 'r')
        s = S.readline()
        while s:
            if r.strip().split(' ')[1] == s.strip().split(' ')[0]:
                #print(r.strip(), end=' ')
                # print(s)
                outputfile.write(r.strip()+' '+s)
            s = S.readline()
        r = R.readline()
        S.close()


def main():
    Rfn = sys.argv[1]  # filename of R
    Sfn = sys.argv[2]  # filename of S
    join_type = sys.argv[3]
    M = int(sys.argv[4])
    test()
    # return
    if join_type == 'sort':
        fun_SortMerge(Rfn, Sfn, M)
        pass
    else:
        pass


if __name__ == '__main__':
    main()
