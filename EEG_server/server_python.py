import socket
from keras.models import load_model
import numpy as np
import json

HOST = '172.31.29.204'
PORT = 8080
SOCKET_SIZE = 1024

temp_list_f = []
flag = True

# 소켓 객체 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

# 클라이언트 접속 허용
server_socket.listen()

# accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓 리턴
client_socket, addr = server_socket.accept()

# 접속한 클라이언트 주소
print('Connect by', addr)

while True:
    # 클라이언트가 보낸 메시지를 수신하기 위해 대기
    data = ""

    if flag:
        data = client_socket.recv(SOCKET_SIZE)

    # 빈 문자열을 수신하면 루프 중지
    if not data:
        break

    # 수신 받은 데이터 출력 & 저장
    print('Received from', addr)
    #print(data.decode())
    data_decode = data.decode()
    temp_list = data_decode.split()
    check = False
    
    for i in temp_list:
        if i == '-':
            check = True

        elif i == 'end':
            flag = False
        else:
            if check:
                check = False
                temp_list_f.append(float(i)*-1)
            else:
                temp_list_f.append(float(i))
    
    #temp_list_f.extend(list(map(float, temp_list)))

#print(temp_list_f)

for i in range(0, 3):
    temp_list_f.extend(temp_list_f)

arr_np = np.array(temp_list_f[:210000])
print(np.shape(arr_np))

# 모델 호출
model = load_model('../server/eeg_deeplearning_conv1d_lstm.h5')
x = np.load("../server/savedfp1_x_z.npy")
y = np.load("../server/saved_y.npy")
x_list = np.array(x)
y_list = np.array(y)
X_test = np.reshape(x_list, (109, 500, 420))
Y_test = np.reshape(y_list, (109, 1))
X_sample = np.reshape(arr_np, (1, 500, 420))

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

data_str = "accuracy:" + str(score[1]) + " loss:" + str(score[0]) + " predict:" + str(result[0])
print(data_str)

client_socket.sendall(data_str.encode())

client_socket.close()
server_socket.close()