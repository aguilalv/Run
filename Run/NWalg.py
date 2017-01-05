# #### Log of next steps:
#       - TODO Split the alignment algorithm from main()
#       - TODO Logging
#       - TODO Eliminate main() and test in a separate module


import coordinates
import numpy

import TCX

def nw_global_alignment(first_seq, second_seq):
    #Create scores matrix
    scores_dim = (len(second_seq)+1,len(first_seq)+1)
    scores = numpy.zeros(scores_dim)

    # Initialize first row and column of scores matrix
    for j in range(1,scores_dim[1]):
        scores[0][j] = GAP*j
    for i in range(1,scores_dim[0]):
        scores[i][0]= GAP*i

    # Calculate scores matrix
    for i in range(1,scores_dim[0]):
        for j in range(1,scores_dim[1]):
            # Score calc
            diag_score = scores[i-1][j-1] - (second_seq[i-1]-first_seq[j-1])
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
            second_ret.insert(0,'(---------,--------)')
            j = j-1
        elif j == 0:
            first_ret.insert(0,'(---------,--------)')
            second_ret.insert(0,second_seq[i-1])
            i = i-1
        elif scores[i][j] == scores[i-1][j-1] + (second_seq[i-1]-first_seq[j-1]):
            first_ret.insert(0,first_seq[j-1])
            second_ret.insert(0,second_seq[i-1])
            i = i-1
            j = j-1
        elif scores[i][j] == scores[i-1][j] + GAP:
            first_ret.insert(0,'(---------,--------)')
            second_ret.insert(0,second_seq[i-1])
            i = i-1
        else:
            first_ret.insert(0,first_seq[j-1])
            second_ret.insert(0,'(---------,--------)')
            j = j-1



def main():

    GAP = -1

    first_seq = []
    smpl_lst = TCX.parse("../activities/STRun2.tcx")
    for smpl in smpl_lst:
        coord_to_append = coordinates.coord(float(smpl[2]),float(smpl[3]))
        first_seq.append(coord_to_append)
    print(len(first_seq))
    first_seq = first_seq[:10]
    print(len(first_seq))

    second_seq = []
    smpl_lst = TCX.parse("../activities/STRun3.tcx")
    for smpl in smpl_lst:
        coord_to_append = coordinates.coord(float(smpl[2]),float(smpl[3]))
        second_seq.append(coord_to_append)
    print(len(second_seq))
    second_seq = second_seq[:10]
    print(len(second_seq))

    for elm in first_seq:
        print (elm,end='')
    print()
    for elm in second_seq:
        print (elm,end='')
    print()

    nw_global_alignment(first_seq,second_seq)

    for elm in first_ret:
        print (elm,end='')
    print()
    for elm in second_ret:
        print (elm,end='')
    print()

if __name__ == '__main__':
    main()