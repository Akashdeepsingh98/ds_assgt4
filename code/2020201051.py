from os.path import join
import sys
import os
import glob
import time

TUPLE_PER_BLOCK = 100


def fun_openSM(Rfn, Sfn, M):
    Rfile = open(Rfn, 'r')
    intermed_fnum = 0  # number of intermediate file
    canread = True
    while canread:
        lines = []
        for i in range(TUPLE_PER_BLOCK):
            t = Rfile.readline()
            if not t:
                canread = False
                break
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
        if count >= TUPLE_PER_BLOCK:
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
        for i in range(TUPLE_PER_BLOCK):
            t = Sfile.readline()
            if not t:
                canread = False
                break
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
        if count >= TUPLE_PER_BLOCK:
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
                    return count, curb, blockptr, startline
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

    joinfile = open(os.path.basename(Rfn)+'_' +
                    os.path.basename(Sfn)+'_join.txt', 'w')
    lines = []
    curbR, curbS = 0, 0
    countR, curbR, blockR, startR = fun_getNextS('R', BR, curbR, blockR, 0)
    countS, curbS, blockS, startS = fun_getNextS('S', BS, curbS, blockS, 0)
    while countR > 0 and countS > 0:
        # input()
        Rset = open('Rset.txt', 'r')
        Sset = open('Sset.txt', 'r')
        tR = Rset.readline()
        tS = Sset.readline()
        Rset.close()
        Sset.close()

        if tR.strip().split(' ')[1] == tS.strip().split(' ')[0]:
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
    joinfile.close()
    blockR.close()
    blockS.close()
    if os.path.exists('Rset.txt'):
        os.remove('Rset.txt')
    if os.path.exists('Sset.txt'):
        os.remove('Sset.txt')
    for i in range(BR):
        os.remove('blockR'+str(i)+'.txt')
    for i in range(BS):
        os.remove('blockS'+str(i)+'.txt')


def fun_rollHash(s, N):
    result = 0
    for i in range(len(s)):
        t = ord(s[i])-ord('a')
        t *= (31**i)
        result += t
    return result % N


def fun_openHJ(Rfn, Sfn, M):
    # blk size will give number of tuples in each block and num blks is the number of buckets
    BLK_SIZE = NUM_BLKS = M//2
    MXTB = (BLK_SIZE)*TUPLE_PER_BLOCK  # max tuples per bucket

    Rfiledata = []  # each element will store number of files - 1 and current nuber of lines
    Rfptrs = []
    for i in range(NUM_BLKS):
        Rfiledata.append([0, 0])
        Rfptrs.append(open('sublistR'+str(i)+'_0.txt', 'w'))

    Rfptr = open(Rfn, 'r')
    while True:
        line = Rfptr.readline()
        if not line:
            break
        rowlist = line.strip().split(' ')
        bucketno = fun_rollHash(rowlist[1], NUM_BLKS)
        Rfptrs[bucketno].write(line)
        Rfiledata[bucketno][1] += 1
        if Rfiledata[bucketno][1] == MXTB:
            Rfiledata[bucketno][1] = 0
            Rfiledata[bucketno][0] += 1
            Rfptrs[bucketno].close()
            Rfptrs[bucketno] = open(
                'sublistR'+str(bucketno)+'_'+str(Rfiledata[bucketno][0])+'.txt', 'w')
    Rfptr.close()
    for i in range(NUM_BLKS):
        Rfptrs[i].close()

    Sfiledata = []  # each element will store number of files - 1 and current nuber of lines
    Sfptrs = []
    for i in range(NUM_BLKS):
        Sfiledata.append([0, 0])
        Sfptrs.append(open('sublistS'+str(i)+'_0.txt', 'w'))

    Sfptr = open(Sfn, 'r')
    while True:
        line = Sfptr.readline()
        if not line:
            break
        rowlist = line.strip().split(' ')
        bucketno = fun_rollHash(rowlist[0], NUM_BLKS)
        Sfptrs[bucketno].write(line)
        Sfiledata[bucketno][1] += 1
        if Sfiledata[bucketno][1] == MXTB:
            Sfiledata[bucketno][1] = 0
            Sfiledata[bucketno][0] += 1
            Sfptrs[bucketno].close()
            Sfptrs[bucketno] = open(
                'sublistS'+str(bucketno)+'_'+str(Sfiledata[bucketno][0])+'.txt', 'w')
    Sfptr.close()
    for i in range(NUM_BLKS):
        Sfptrs[i].close()

    return Rfiledata, Sfiledata


def fun_getNextHJR(Rfiledata, Sfiledata, i, joinfile):
    Rbucket = Rfiledata[i]  # data about ith bucket of R
    Sbucket = Sfiledata[i]
    # go over each R bucket file one by one.
    # for each file get all lines and prepare a dictionary Rd to store a list for each Y value.
    for j in range(Rbucket[0]+1):
        Rfile = open('sublistR'+str(i)+'_'+str(j)+'.txt')
        allRlines = Rfile.readlines()
        Rfile.close()
        Rd = {}
        for w in range(len(allRlines)):
            rowlist = allRlines[w].strip().split(' ')
            if rowlist[1] in Rd.keys():
                Rd[rowlist[1]].append(rowlist[0])
            else:
                Rd[rowlist[1]] = [rowlist[0]]

        for k in range(Sbucket[0]+1):
            Sfile = open('sublistS'+str(i)+'_'+str(k)+'.txt')
            allSlines = Sfile.readlines()
            Sfile.close()
            for w in range(len(allSlines)):
                rowlist = allSlines[w].strip().split(' ')
                if rowlist[0] in Rd.keys():
                    t = []
                    for z in range(len(Rd[rowlist[0]])):
                        t.append(Rd[rowlist[0]][z]+' ' +
                                 rowlist[0]+' '+rowlist[1]+'\n')
                    joinfile.writelines(t)


def fun_getNextHJS(Sfiledata, Rfiledata, i, joinfile):
    Sbucket = Sfiledata[i]  # data about ith bucket of R
    Rbucket = Rfiledata[i]
    # go over each R bucket file one by one.
    # for each file get all lines and prepare a dictionary Rd to store a list for each Y value.
    for j in range(Sbucket[0]+1):
        Sfile = open('sublistS'+str(i)+'_'+str(j)+'.txt')
        allSlines = Sfile.readlines()
        Sfile.close()
        Sd = {}
        for w in range(len(allSlines)):
            rowlist = allSlines[w].strip().split(' ')
            if rowlist[0] in Sd.keys():
                Sd[rowlist[0]].append(rowlist[1])
            else:
                Sd[rowlist[0]] = [rowlist[1]]

        for k in range(Rbucket[0]+1):
            Rfile = open('sublistR'+str(i)+'_'+str(k)+'.txt')
            allRlines = Rfile.readlines()
            Rfile.close()
            for w in range(len(allRlines)):
                rowlist = allRlines[w].strip().split(' ')
                if rowlist[1] in Sd.keys():
                    t = []
                    for z in range(len(Sd[rowlist[1]])):
                        t.append(rowlist[0]+' '+rowlist[1] +
                                 ' '+Sd[rowlist[1]][z]+'\n')
                    joinfile.writelines(t)


def fun_HashJoin(Rfn, Sfn, M):
    Rfiledata, Sfiledata = fun_openHJ(Rfn, Sfn, M)
    NUM_BUCKETS = M//2

    joinfile = open(os.path.basename(Rfn)+'_' +
                    os.path.basename(Sfn)+'_join.txt', 'w')

    Rsize = os.path.getsize(Rfn)
    Ssize = os.path.getsize(Sfn)

    if Rsize < Ssize:
        for i in range(NUM_BUCKETS):
            fun_getNextHJR(Rfiledata, Sfiledata, i, joinfile)
    else:
        for i in range(NUM_BUCKETS):
            fun_getNextHJS(Sfiledata, Rfiledata, i, joinfile)

    joinfile.close()
    for filename in glob.glob('sublist*'):
        os.remove(filename)


def test():
    R = open('..\inputR', 'r')
    outputfile = open('mytest.txt', 'w')
    r = R.readline()
    while r:
        S = open('..\inputS', 'r')
        s = S.readline()
        while s:
            if r.strip().split(' ')[1] == s.strip().split(' ')[0]:
                outputfile.write(r.strip()+' '+s)
            s = S.readline()
        r = R.readline()
        S.close()


def main():
    
    Rfn = sys.argv[1]  # filename of R
    Sfn = sys.argv[2]  # filename of S
    join_type = sys.argv[3]
    M = int(sys.argv[4])
    #test()
    start = time.time()
    if join_type == 'sort':
        fun_SortMerge(Rfn, Sfn, M)
    else:
        fun_HashJoin(Rfn, Sfn, M)
    end = time.time()
    tf = open('timing.txt', 'a')
    tf.write(str(M) + ' ' + str(end-start)+'\n')
    tf.close()


if __name__ == '__main__':
    main()
