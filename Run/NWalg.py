# #### Log of next steps:
#      - Split the alignment algorithm from main()


import coordinates
import numpy

import TCX

def main():

    smpl_lst = TCX.parse("../activities/STRun2.tcx")

    GAP = -1

    a = coordinates.coord(1,15)
    n = coordinates.coord(23,2)
    d = coordinates.coord(32,31)

    s = coordinates.coord(10,10)
    e = coordinates.coord(20,5)

    first_seq = [s,a,e,n,d]
    second_seq = [a,n,d]

    for elm in first_seq:
        print (elm,end='')
    print()
    for elm in second_seq:
        print (elm,end='')
    print()

    #Create scores matrix
    scores_dim = (len(second_seq)+1,len(first_seq)+1)
    scores = numpy.zeros(scores_dim)
    print()
    print (scores)
    print()

    # Initialize first row and column of scores matrix
    for j in range(1,scores_dim[1]):
        scores[0][j] = GAP*j
    for i in range(1,scores_dim[0]):
        scores[i][0]= GAP*i

    # Calculate scores matrix
    for i in range(1,scores_dim[0]):
        for j in range(1,scores_dim[1]):
            # Score calc
            diag_score = scores[i-1][j-1] + (second_seq[i-1]-first_seq[j-1])
            up_score   = scores[i-1][j]   + GAP
            left_score = scores[i][j-1]   + GAP
            scores[i][j]= max(diag_score,up_score,left_score)
    print (scores)
    print()

    # Trace back optimal alignment
    i = scores_dim[0]-1
    j = scores_dim[1]-1
    first_ret=[]
    second_ret=[]
    while i>0 or j>0:
        if i == 0:
            first_ret.insert(0,first_seq[j-1])
            second_ret.insert(0,'(-,-)')
            j = j-1
        elif j == 0:
            first_ret.insert(0,'(-,-)')
            second_ret.insert(0,second_seq[i-1])
            i = i-1
        elif scores[i][j] == scores[i-1][j-1] + (second_seq[i-1]-first_seq[j-1]):
            first_ret.insert(0,first_seq[j-1])
            second_ret.insert(0,second_seq[i-1])
            i = i-1
            j = j-1
        elif scores[i][j] == scores[i-1][j] + GAP:
            first_ret.insert(0,'(-,-)')
            second_ret.insert(0,second_seq[i-1])
            i = i-1
        else:
            first_ret.insert(0,first_seq[j-1])
            second_ret.insert(0,'(-,-)')
            j = j-1


    for elm in first_ret:
        print (elm,end='')
    print()
    for elm in second_ret:
        print (elm,end='')
    print()

if __name__ == '__main__':
    main()