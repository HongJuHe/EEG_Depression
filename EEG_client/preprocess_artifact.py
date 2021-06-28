import json
import numpy as np
import pandas as pd
import scipy.io as sio
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from pymatreader import read_mat
from oct2py import octave

## mat 파일에 키값으로 setname 포함시키기
octave.addpath('C:/Users/DS/mat_code_test')
#octave.addpath('C:/Program Files/MATLAB/eeglab_current/eeglab2021.0/functions/popfunc')
#octave.addpath('C:/Program Files/MATLAB/eeglab_current/eeglab2021.0/plugins/firfilt')

## 이상치 제거
f = open("D:/ThinkGearData/data0.txt", "r")
con = f.readline()
f.close()
con = con.split() # 한 글자씩 저장된 것을 한 덩어리씩 저장하도록 함
ERR_MIN = 39 # 이상치 최소값
ERR_MAX = 43 # 이상치 최대값
ERR_LEN = 20 # 이상치 길이

cnt = 0
fst = -1
lst = -1
add = []
arr = []

for i in range(len(con)):
    num = float(con[i])
    arr.append(num)
    
    if(num >= ERR_MIN and num <= ERR_MAX):
        cnt += 1
        lst = i
        if(fst < 0):
            fst = i
    else:
        if(cnt > ERR_LEN):
            add.append(fst)
            add.append(lst)
        elif(cnt < 0):
            continue
        cnt = 0
        fst = -1
        lst = -1 

for i in range(len(add), 0, -1):
    if(i % 2 == 1): ##홀수일때
        for j in range(add[i], add[i-1], - 1):
            del(arr[j])

# del(arr[0]) # file length

f = open("D:/ThinkGearData/file0.txt", "w")
for i in arr:
    f.write(str(int(i)) + " ")
f.close()

## txt 형태로 측정된 raw data 가져오기
f = open("D:/ThinkGearData/file0.txt", "r")
con = f.readline()
f.close()

## mat 형태로 변환
con = con.split()
arr = [] #list
for i in range(len(con)):
    arr.append(int(con[i]))

## pnts는 전체 데이터 길이(숫자 단위가 아닌 문자 단위)
data = {"data" : arr, "label" : "experiment", "setname" : "CNT file", "filename" : "",
"icaact" : "", "icawinv" : "", "icaweights" : "", "icasphere" : "", "icachansind" : "",
"nbchan" : "1", "pnts" : 0, "trials" : 1, "srate" : 512, "xmin" : 0, "xmax" : 60.0,}
sio.savemat('D:/ThinkGearData/data0.mat', data)
## xmax - 측정 시간에 맞춰 변경

EEG = octave.pop_loadset('D:/ThinkGearData/data0.mat')

### 제거 전 출력
'''
EEG2 = EEG.data[0]
print(np.shape(EEG2))
plt.xlim([0, 30000])
plt.ylim([-4000, 4000])
plt.plot(EEG2)
plt.show()
'''

## 생성된 mat 파일에 FIR 필터링
EEG3 = octave.pop_eegfiltnew(EEG, 0.2, [], 8448, 0, [], 0) #8448
EEG3 = octave.pop_eegfiltnew(EEG3, [], 35, 86, 0, [], 0)  #86

### 제거 후 줄력
'''
plt.xlim([0, 30000])
plt.ylim([-4000, 4000])
plt.plot(EEG3.data[0][:])
plt.show()
'''

# for z-score
temp = []
temp_t = []
## 다시 txt 형태로 변환
con = EEG3.data[0]

f = open("D:/ThinkGearData/filted_data0.txt", 'w')
for i in con:
    f.write(str(round(i, 6)) + " ")
    temp_t.append(i) # for z-score
temp.append(temp_t) # for z-score
f.close() 

## z-score normalization 
transformer = StandardScaler()
dataset = pd.DataFrame(temp)
x = dataset.iloc[0:1, :].values
y = dataset.iloc[-1, :].values
 
sc_x = StandardScaler()
sc_y = StandardScaler()
x = sc_x.fit_transform(x)
y = np.squeeze(sc_y.fit_transform(y.reshape(-1, 1)))

np.savetxt("D:/ThinkGearData/parsed_data0.txt", y, delimiter = ',')

## 사용할 수 있는 실수 형태로 변환
f = open("D:/ThinkGearData/parsed_data0.txt", "r")
con = f.readlines()
f.close()

f = open("D:/ThinkGearData/result.txt", 'w')
for i in con:
    tmp = float(i.rstrip('\n'))
    f.write(str(round(tmp, 8)) + " ") # 소수점 아래 8자리
f.close() 

## argument? (data, Transition bandwith, )
## band width df as (dF/order) * fs

## to correctly filter 0.1-100Hz at 1kHz srate?
## (EEG, 0.2, [], 16500, 0, [], 0)
## (EEG, [], 89, 150, 0, [], 0)

## 0.1 as half amplitude cutoff - 30/40Hz
## shift the passband edge by half the transition band width
## (EEG, 0.2, [], 4224, 0, [], 1)
## (EEG, [], 35, 86, 0, [])

## 0.1Hz high-pass and 40Hz low-pass (0.2-0.2/2 and 35+10/2, respectively)
## 0.05Hz high-pass and 45Hz low-pass
