import numpy as np
from numpy.lib.npyio import save
from sklearn.preprocessing import StandardScaler
import pandas as pd
from keras.models import load_model
import json


## 받은 텍스트 파일 열기 (숫자 사이에 띄어쓰기만 있는 상태)
con = ""
file = "../server/sample.txt"
with open(file, 'rb') as fopen:
    q = fopen.read()
    #print(q.decode('latin-1'))
    con = q.decode('latin-1') 

## 파일에서 이상한 문자 지우기 (0~9, - .부호 제외)
f = open("../server/sample1.txt", 'w')
for i in range(len(con)):
    if(con[i] >= '0' and con[i] <= '9'):
        f.write(con[i])
    elif(con[i] == '-' or con[i] == ' ' or con[i] == '\n' or con[i] == '.'):
        f.write(con[i])
f.close()

## 39~43 집중된 곳 없애기
f = open("../server/sample1.txt", "r")
con = f.readline()
f.close()
con = con.split() # 한 글자씩 저장된 것을 한 덩어리씩 저장하도록 함

ERR_MIN = 39
ERR_MAX = 43
ERR_LEN = 20

cnt = 0
fst = -1
lst = -1
add = []
arr = []

check = False
for i in range(len(con)):
    num = 0

    if con[i] == '-' or con[i] == '- ':
        #print("1")
        check = True
    else:
        if check:
            #print("2")
            num = float(con[i]) * -1
            check = False
        else:
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

del(arr[0])
temp = []
temp_t = []
f = open("../server/sample2.txt", "w")
for i in arr:
    f.write(str(i) + "\n")
    temp_t.append(i)
temp.append(temp_t)
f.close()

#print(temp)
transformer = StandardScaler()
dataset = pd.DataFrame(temp)
x = dataset.iloc[0:1, :].values
y = dataset.iloc[-1, :].values

sc_x = StandardScaler()
sc_y = StandardScaler()
x = sc_x.fit_transform(x)
y = np.squeeze(sc_y.fit_transform(y.reshape(-1, 1)))
y_temp = np.array([])

for i in range(0, 3):
    y = np.append(y, y)

print(np.shape(y))
y_temp = y[0:210000]

#y 길이를 210000으로 자르기
model = load_model('../server/eeg_deeplearning_conv1d_lstm.h5')
x = np.load("../server/savedfp1_x_z.npy")
y = np.load("../server/saved_y.npy")
x_list = np.array(x)
y_list = np.array(y)
X_test = np.reshape(x_list, (109, 500, 420))
Y_test = np.reshape(y_list, (109, 1))
X_sample = np.reshape(y_temp, (1, 500, 420))

score = model.evaluate(X_test, Y_test, verbose=0)
predict = model.predict(X_sample)
classes = np.argmax(predict, axis = 1)
result = np.ndarray.tolist(classes)

print(result)
data = {}
data['accuracy'] = score[1]
data['loss'] = score[0]
data['predict'] = result[0]

with open("../server/result.json", 'w') as r:
    json.dump(data, r)

text_string = json.dumps(data)
f = open("../server/result.txt", "w")
f.write(text_string)
f.close
print("accuracy: ", score[1], "loss: ", score[0])
