import numpy as np
import sys
from math import sqrt
import random
#import matplotlib.pyplot as plt



def DataFromCsv(file):
    f = open(file, 'r')
    data = {}
    # delkeylist = []
    lines = f.readlines()
    head = lines.pop(0).strip('\n')
    lablelist = head.split(',')
    totalfeature = len(lablelist)
    for line in lines:
        cols = line.strip('\n').split(',')
        if len(cols) < totalfeature:
            continue
        for i in range(len(cols)):
            try:
                data.setdefault(lablelist[i], []).append((cols[i]))
            except:
                data.setdefault(lablelist[i], []).append(0)

    return data


def Fit(Y_Exp, X, ScaleFactors, NumSwarm, StopTriger, MaxIteration):
    S = []
    V = []
    GBest = []
    Fx = []
    P_MAE = []
    P_RMSE = []
    P_R2 = []
    G_MAE = 9e99
    G_RMSE = 9e99
    G_R2 = -9e99
    NumSample = len(Y_Exp)
    ParamDim = len(ScaleFactors)
    Vector = Transpose(X)
    for i in range(NumSwarm):
        Si = []
        Vi = []
        Y_Pred = []
        for j in range(ParamDim):
            Si.append(ScaleFactors[j] * random.uniform(-1, 1))
            Vi.append(0.0)
        for k in range(NumSample):
            Y_Pred.append(Function(Si, Vector[k]))
        MAE, RMSE, R2 = CalcAccuracy(Y_Exp, Y_Pred)
        if R2 > G_R2:
            G_R2 = R2
            G_MAE = MAE
            G_RMSE = RMSE
            GBest = Si
            Fx = Y_Pred
        P_MAE.append(MAE)
        P_RMSE.append(RMSE)
        P_R2.append(R2)
        S.append(Si)
        V.append(Vi)
    PBest = S
    Iteration = 0
    KeepBest = 0
    while (Iteration < MaxIteration and KeepBest < StopTriger):
        UpdateTime = 0
        for i in range(NumSwarm):
            for j in range(ParamDim):
                V[i][j]=0.0*V[i][j]+2*random.uniform(0,1)*(GBest[j]-S[i][j])+2*random.uniform(0,1)*(PBest[i][j]-S[i][j])
                S[i][j] = S[i][j] + V[i][j]
            Y_Pred = []
            for k in range(NumSample):
                Y_Pred.append(Function(S[i], Vector[k]))
            MAE, RMSE, R2 = CalcAccuracy(Y_Exp, Y_Pred)
#            if (RMSE - P_RMSE[i]) < -0.0001:
            if R2 > (P_R2[i] + 0.0001):
                P_MAE[i] = MAE
                P_RMSE[i]= RMSE
                P_R2[i]=R2
                PBest[i] = S[i]
#                if (RMSE - G_RMSE) < -0.0001:
                if R2 > (G_R2 + 0.0001):
                    G_R2 = R2
                    G_MAE = MAE
                    G_RMSE = RMSE
                    GBest = S[i]
                    Fx = Y_Pred
                    UpdateTime += 1
        print('Iteration', Iteration, end=': ')
        print('R2=%.4f,MAE=%.1f,RMSE=%.1f' % (G_R2, G_MAE, G_RMSE), end='/')
        print(GBest)
        Iteration += 1
        if UpdateTime > 0:
            KeepBest = 0
        else:
            KeepBest += 1
    if KeepBest >= StopTriger:
        Signal = 'Converged'
    else:
        Signal = 'Not Converged'

    return Signal, Fx


def Transpose(matrix):
    new_matrix = []
    for i in range(len(matrix[0])):
        matrix1 = []
        for j in range(len(matrix)):
            matrix1.append(matrix[j][i])
        new_matrix.append(matrix1)
    return new_matrix


def Test(Parameters, X):
    Fx = []
    TransX = Transpose(X)
    for I in TransX:
        Fx.append(Function(Parameters, I))

    return Fx


def CalcAccuracy(Y_Exp, Y_Pred):
    NumSample = len(Y_Exp)
    Y_Ave = sum([i for i in Y_Exp]) / NumSample
    MAE = sum([abs(Y_Exp[i] - Y_Pred[i]) for i in range(NumSample)]) / NumSample
    RMSE = sqrt(sum([(Y_Exp[i] - Y_Pred[i]) ** 2 for i in range(NumSample)]) / NumSample)
    R2 = 1 - sum([(Y_Pred[i] - Y_Exp[i]) ** 2 for i in range(NumSample)]) / sum([(Y_Exp[i] - Y_Ave) ** 2 for i in range(NumSample)])

    return MAE, RMSE, R2


def Function(A, strX):
    X = []
    for i in strX:
        X.append(float(i))
    # Fx = A[0] * X[0] + A[1] * (X[1])**2 + A[2] * X[2] + A[3]*X[6] + A[4] * X[7]  + A[5] * X[8] + A[6]
    Fx = A[0] * X[0] + A[1]*X[1] + A[2] * X[2]**1.5 + A[3] * X[3] + A[4]
    return Fx


if __name__ == '__main__':
    data = DataFromCsv(sys.argv[1])
    Y_Exp = []
    for i in data['EXP']:
        Y_Exp.append(float(i))
    X = [data['Polar'], data['TPSA'], data['NO2Count'], data['Spher']]
    ID = data['ID']
    NumSwarm = 500
    ScaleFactors = [1.0, 1.0, 1.0, 1.0, 1.0]  # Training
    # FinalParameters = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0] #Testing
    StopTriger = 5
    MaxIteration = 1000
    Signal, Y_Pred = Fit(Y_Exp, X, ScaleFactors, NumSwarm, StopTriger, MaxIteration)  # Training
    # Y_Pred = Test(FinalParameters, X) #Testing
    print('_'*50)
    # print('ID,', 'Y_Exp,', 'Y_Pred,', 'Error,')
    # for i in range(len(Y_Exp)):
    #     print('%s,%.1f,%.1f' % (ID[i], Y_Exp[i],Y_Pred[i]), round((Y_Pred[i]-Y_Exp[i]),2))