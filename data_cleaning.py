import ffmpeg_class
import Labeling_data
import cv2
import os
import pickle
import numpy as np


# image_path example Label/label1 takes all of them and turns it into numpy arrays in a pickle
# it also lowers dementions
def save_images_as_array(image_path, pickle_name, save=False):
    image_array = []
    image_list = os.listdir(image_path)

    for image in image_list:
        image_path_ = f"{image_path}/{image}"
        data_read = cv2.imread(image_path_)
        resized = cv2.resize(data_read, (128, 72))
        # print(resized.shape)
        image_array.append(resized)

    image_array = np.array(image_array)
    if save:
        pickle.dump(image_array, open(pickle_name, "wb"))
    return image_array


# take the entire data and randomize it if it's an array
def randomize_numpyarray(pickle_file, save=False):
    all_data = pickle.load(open(pickle_file, "rb"))
    np.random.shuffle(all_data)
    if save:
        pickle.dump(all_data, open("r_array.p", "wb"))
    return all_data


# declare a percent of data split between test and train data
def split_data(labels, random_array, percent_test, save = False):
    r_array = pickle.load(open(random_array, "rb"))
    labels = pickle.load(open(labels, "rb"))

    percent_train = 100 - percent_test

    index_train = int((percent_train / 100) * labels.shape[0])
    print(index_train)
    train_data = r_array[:index_train]
    train_label = labels[:index_train]

    test_data = r_array[index_train:]
    test_label = labels[index_train:]

    if save:
        pickle.dump(train_data, open("data_clean/train_data", "wb"))
        pickle.dump(train_label, open("data_clean/train_label", "wb"))
        pickle.dump(test_data, open("data_clean/test_data", "wb"))
        pickle.dump(test_label, open("data_clean/test_label", "wb"))

    return train_data, train_label, test_data, test_label


# create array from dictionary of all of the labels
def create_label_array(random_array, dict_val, save=False):
    r_array = pickle.load(open(random_array, "rb"))
    label_dict = pickle.load(open(dict_val, "rb"))
    labels = [label_dict[str(i)] for i in r_array]
    labels = np.array(labels)
    if save:
        pickle.dump(labels, open("Labels.p", "wb"))
    return labels


# creates equal amounts of Label1 and label2 data from the max
def create_even_split(pickle_name1, pickle_name2, name_1="cut_1.p", name_2="cut_2.p", save=False):
    pickle_raw1 = pickle.load(open(pickle_name1, "rb"))
    pickle_raw2 = pickle.load(open(pickle_name2, "rb"))

    minimum = (min([pickle_raw1.shape[0], pickle_raw2.shape[0]]))

    array_1 = pickle_raw1[:minimum]
    array_2 = pickle_raw2[:minimum]
    if save:
        pickle.dump(array_1, open(name_1, "wb"))
        pickle.dump(array_2, open(name_2, "wb"))
    return array_1, array_2


# create dictionary of both labels #Only works with 2
def create_dictionary(pickle_file1, pickle_file2, save=False):
    image_array1 = pickle.load(open(pickle_file1, "rb"))
    image_array2 = pickle.load(open(pickle_file2, "rb"))

    value_dict1 = {}
    value_dict2 = {}

    for i in image_array1:
        value_dict1[str(i)] = 1

    for i in image_array2:
        value_dict2[str(i)] = 2

    value_dict1.update(value_dict2)
    new_dict = value_dict1
    if save:
        pickle.dump(new_dict, open("label_dict.p", 'wb'))
    return new_dict


def combine_pickle(pickle_file1, pickle_file2, save=False):
    a = pickle.load(open("cut_1.p", "rb"))
    b = pickle.load(open("cut_2.p", "rb"))
    combine_array = np.concatenate((a, b), axis=0)
    if save:
        pickle.dump(combine_array, open("combined_labels.p", "wb"))
    return combine_array


def main():
    # resize
    # cut to min size
    # create dictionary
    # combine cut data
    # randomize
    # labeled data
    # split into train and test data

    # create_label_array("r_array.p","label_dict.p",save=True)
    #split_data("Labels.p", "r_array.p", 10, save= True)



if __name__ == "__main__":
    main()
