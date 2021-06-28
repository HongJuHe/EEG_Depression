from keras.models import load_model
import numpy as np

model = load_model('../server/eeg_deeplearning_conv1d_lstm.h5')

x = np.load("../server/savedfp1_x_z.npy")  #saved2_x.npy, saved3_x.npy
y = np.load("../server/saved_y.npy")  #saved2_y.npy, saved3_y.npy
x_list = np.array(x)
y_list = np.array(y)
X_test = np.reshape(x_list, (109, 500, 420))
Y_test = np.reshape(y_list, (109, 1))

score = model.evaluate(X_test, Y_test, verbose=0)
print("accuracy: ", score[1], "loss: ", score[0])