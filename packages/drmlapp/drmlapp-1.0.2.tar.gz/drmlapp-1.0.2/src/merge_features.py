import numpy as np

"""
features_input = np.load("imagedata_train002_250_750.npy")
print(features_input.ndim) #2
print(features_input.shape) #(500,25088)
"""
no_of_images = 2938
flatten_arr_dim = 25088
features_input = np.zeros(shape=(no_of_images,flatten_arr_dim),dtype = np.float32)

feature_file_index = [(0,1000),(1000,2000),(2000,2938)]
path = "C:\\Users\\SUMANTH C\\Desktop\\features\\"

feature_file_names = ['imagedata_test007_0_1000.npy','imagedata_test007_1000_2000.npy','imagedata_test007_2000_2938.npy']

for index in range(len(feature_file_index)):
    name = path + feature_file_names[index]
    length = feature_file_index[index]
    start = length[0]
    end = length[1]
    flatten_features = np.load(name)
    for i in range(0,end-start):
        features_input[start+i] = flatten_features[i]

print("Saving features")
print(features_input.shape)
print(features_input.ndim)
np.save("imagedata_test007_0_2938",features_input)





