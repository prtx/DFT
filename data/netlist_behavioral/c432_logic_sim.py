import sys
from collections import OrderedDict
import re
import numpy as np
import pdb

def M1(E, A):
    Ab = np.invert(A)
    EAb = np.invert(np.bitwise_and(Ab, E))
    for i in range(len(EAb)):
        if i == 0:
            PA = EAb[i]
        else:
            PA &= EAb[i]
    PA = np.invert(PA)
    X1 = EAb ^ np.repeat(PA, 9)
    return PA, X1


def M2(E, X1, B):
    Eb = np.invert(E)
    EbB = np.invert(np.bitwise_or(Eb, B))
    XEB = np.invert(np.bitwise_and(X1, EbB))
    for i in range(len(XEB)):
        if i == 0:
            PB = XEB[i]
        else:
            PB &= XEB[i]
    PB = np.invert(PB)
    X2 = XEB ^ np.repeat(PB, 9)
    return PB, X2


def M3(E, X1, X2, C):
    Eb = np.invert(E)
    EbC = np.invert(np.bitwise_or(Eb, C))
    XEC =np.invert(np.bitwise_and(np.bitwise_and(X1, X2), EbC))
    for i in range(len(XEC)):
        if i == 0:
            PC = XEC[i]
        else:
            PC &= XEC[i]
    PC = ~PC
    return PC


def M4(E, A, B, C, PA, PB, PC):
    APA = np.invert(np.bitwise_and(A, np.repeat(PA, 9)))
    BPB = np.invert(np.bitwise_and(B, np.repeat(PB, 9)))
    CPC = np.invert(np.bitwise_and(C, np.repeat(PC, 9)))
    I = np.invert(np.bitwise_and(np.bitwise_and(E, APA), np.bitwise_and(BPB, CPC)))
    return I


def M5(I):
    I8b = ~I[8-8]
    for i in range(1, len(I)):
        if i == 1:
            Iand = I[i]
        else:
            Iand &= I[i]
    Chan_3 = np.invert(np.bitwise_or(I8b, Iand))

    I1b = ~I[8-1]
    I2b = ~I[8-2]
    I3b = ~I[8-3]
    I5b = ~I[8-5]

    I56 = ~(I5b & I[8-6])
    I245 = ~(I2b & I[8-4] & I[8-5])
    I3456 = ~(I3b & I[8-4] & I[8-5] & I[8-6])
    I1256 = ~(I1b & I[8-2] & I[8-5] & I[8-6])

    Chan_2 = ~(I[8-4] & I[8-6] & I[8-7] & I56)
    Chan_1 = ~(I[8-6] & I[8-7] & I245 & I3456)
    Chan_0 = ~(I[8-7] & I56 & I1256 & I3456)
    return [Chan_0, Chan_1, Chan_2, Chan_3]


def c432_sim(in_vec_dict):
    # Create the input and output variables (top level)
    E = np.array(
        [in_vec_dict['4'], in_vec_dict['17'], in_vec_dict['30'], in_vec_dict['43'], in_vec_dict['56'],
         in_vec_dict['69'], in_vec_dict['82'], in_vec_dict['95'], in_vec_dict['108']], dtype=bool)
    A = np.array(
        [in_vec_dict['1'], in_vec_dict['11'], in_vec_dict['24'], in_vec_dict['37'], in_vec_dict['50'],
         in_vec_dict['63'], in_vec_dict['76'], in_vec_dict['89'], in_vec_dict['102']], dtype=bool)
    B = np.array(
        [in_vec_dict['8'], in_vec_dict['21'], in_vec_dict['34'], in_vec_dict['47'], in_vec_dict['60'],
         in_vec_dict['73'], in_vec_dict['86'], in_vec_dict['99'], in_vec_dict['112']], dtype=bool)
    C = np.array(
        [in_vec_dict['14'], in_vec_dict['27'], in_vec_dict['40'], in_vec_dict['53'], in_vec_dict['66'],
         in_vec_dict['79'], in_vec_dict['92'], in_vec_dict['105'], in_vec_dict['115']], dtype=bool)

    # Call the modules in order
    PA, X1 = M1(E, A)
    PB, X2 = M2(E, X1, B)
    PC = M3(E, X1, X2, C)
    I = M4(E, A, B, C, PA, PB, PC)
    Chan = M5(I)

    # Get the output dictionary
    out_vec_dict = OrderedDict()
    out_vec_dict['223'] = PA.astype(int)
    out_vec_dict['329'] = PB.astype(int)
    out_vec_dict['370'] = PC.astype(int)
    out_vec_dict['421'] = Chan[3].astype(int)
    out_vec_dict['430'] = Chan[2].astype(int)
    out_vec_dict['431'] = Chan[1].astype(int)
    out_vec_dict['432'] = Chan[0].astype(int)

    return out_vec_dict


if __name__ == '__main__':
    if len(sys.argv) != 3:  # Check if the input arguments are enough
        print('Not enough arguments. ')
        exit(1)

    input_file = sys.argv[1]  # This is the path for the input file
    output_file = sys.argv[2]  # This is the path for the output file

    # Read the input vector and create the dictionary
    input_file = open(input_file, 'r')
    in_vec_dict = OrderedDict()
    for line in input_file:
        line = line.strip()
        vector_array = re.split(r',', line)
        in_vec_dict[vector_array[0]] = int(vector_array[1])

    # Simulate c432
    out_vec_dict = c432_sim(in_vec_dict)

    # Write output to file
    output_file = open(output_file, 'w')
    for dict_item in out_vec_dict:
        if out_vec_dict[dict_item].astype(int):
            output_file.write('%s,1\n' % dict_item)
        else:
            output_file.write('%s,0\n' % dict_item)
