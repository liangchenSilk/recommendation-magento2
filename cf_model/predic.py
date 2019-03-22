# -*- coding: utf-8 -*-
import numpy as np
import math
from data import Data

with open('prodX.txt', 'r') as file:
    lines = file.readlines()
    
    n_row = (int)(lines[0].split()[1])
    n_col = (int)(lines[1].split()[1])
    print(n_row)
    print(n_col)
    print(len(lines))
    
    #p2p = np.zeros(n_row, n_col)
    #row = 0
    
    p2p = np.zeros([n_row, n_col])
    line_no = 0
    
    for line in lines[2:]:
        if len(line.strip()) == 0:
            continue
        else:
            p2p[line_no, :] = np.fromstring(line, dtype = float, sep = ' ')
            #print(pMatrix[line_no][0])
            line_no += 1
    
    pMatrix = [[0 for i in range(n_row)] for j in range(n_row)]
    
    count = 0
    for i in range(n_row):
        for j in range(i + 1, n_row):
            distance = math.sqrt(np.sum(np.square(p2p[i] - p2p[j])))
            pMatrix[i][j] = distance
            pMatrix[j][i] = distance
            #count += 1
            #print(str(distance) + "|" + str(count))

    dbData = Data()
    dbData.storeProd2ProdDist(pMatrix)
