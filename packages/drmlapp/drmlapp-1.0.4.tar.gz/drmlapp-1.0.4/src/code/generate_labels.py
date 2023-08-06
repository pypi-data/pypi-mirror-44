import glob
import csv 

def generate_labels_from_file(file_pattern, parent_file_path, all_labels_file_path, output_file_path):
	"""

	:param file_pattern: specify file extension
	:param parent_file_path: Image file path for which labels have to be generated
	:param all_labels_file_path: CSV file containing the labels for all the images
	:param output_file_path: CSV file containing image names and labels for the specified image file
	:return: None

	"""
	train_image=[]
	dict_labels_all = {}
	dict_labels_req_file = {}
	imgs = glob.glob(file_pattern) 


	print (len(train_image))
	print (train_image[0])

	with open(all_labels_file_path,"r") as csvfile:
		reader = csv.reader(csvfile, delimiter = ",")
		for row in reader:
			dict_labels_all[row[0]] = row[1]

	for filename in train_image:
		dict_labels_req_file[filename] = dict_labels_all[filename]

	with open(output_file_path,"w") as csvfile:
		for name,label in dict_labels_req_file.items():
			csvfile.write(name + "," + label + "\n")
	

#if __name__ == "__main__":
	#generate_labels_from_file('E:\\DR\\test\\*.jpeg','E:\\DR\\test\\','E:\\DR\\test_labels.csv','E:\\DR\\test007.csv')

	

