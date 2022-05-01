import numpy as np

def calc_total_entropy(train_data, label, class_list):
    # train_data: a pandas dataframe/dataset
    # label: string, name of the label of the dataframe (=Play Tennis)
    # class_list: list, unique classes of the label (=[Yes, No]).
    # returns: float, calculated entropy of the whole dataframe (=0.94)
    total_row = train_data.shape[0] #the total size of the dataset
    total_entr = 0
    
    for c in class_list: #for each class in the label
        total_class_count = train_data[train_data[label] == c].shape[0] #number of the class
        total_class_entr = - (total_class_count/total_row)*np.log2(total_class_count/total_row) #entropy of the class
        total_entr += total_class_entr #adding the class entropy to the total entropy of the dataset
    
    return total_entr

def calc_entropy(feature_value_data, label, class_list):
    # feature_value_data: a pandas dataframe/dataset, which contains rows that has a specific value of a feature (Ex. Rows with only Outlook = Sunny)
    # label: string, name of the label of the dataframe (=Play Tennis)
    # class_list: list, unique classes of the label (=[Yes, No]).
    # returns: float, calculated entropy of the feature value dataframe (Ex. for Outlook = Sunny, returns 0.971)
    class_count = feature_value_data.shape[0]
    entropy = 0
    
    for c in class_list:
        label_class_count = feature_value_data[feature_value_data[label] == c].shape[0] #row count of class c 
        entropy_class = 0
        if label_class_count != 0:
            probability_class = label_class_count/class_count #probability of the class
            entropy_class = - probability_class * np.log2(probability_class)  #entropy
        entropy += entropy_class
    return entropy

def calc_info_gain(feature_name, train_data, label, class_list):
    # feature_name: string, the name of the feature that we want to find it’s information gain (Ex. Outlook)
    # train_data: a pandas dataframe/dataset
    # label: string, name of the label of the dataframe (=Play Tennis)
    # class_list: list, unique classes of the label (=[Yes, No]).
    # returns: calculated information gain of the feature (Ex. for Outlook, returns 0.247)
    feature_value_list = train_data[feature_name].unique() #unqiue values of the feature
    total_row = train_data.shape[0]
    feature_info = 0.0
    
    for feature_value in feature_value_list:
        feature_value_data = train_data[train_data[feature_name] == feature_value] #filtering rows with that feature_value
        feature_value_count = feature_value_data.shape[0]
        feature_value_entropy = calc_entropy(feature_value_data, label, class_list) #calculcating entropy for the feature value
        feature_value_probability = feature_value_count/total_row
        feature_info += feature_value_probability * feature_value_entropy #calculating information of the feature value
        
    return calc_total_entropy(train_data, label, class_list) - feature_info #calculating information gain by subtracting

def find_most_informative_feature(train_data, label, class_list):
#   train_data: a pandas dataframe/dataset
#   label: string, name of the label of the dataframe (=Play Tennis)
#   class_list: list, unique classes of the label (=[Yes, No]).
#   returns: string, the feature name
    feature_list = train_data.columns.drop(label) #finding the feature names in the dataset
                                            #N.B. label is not a feature, so dropping it
    max_info_gain = -1
    max_info_feature = None
    
    for feature in feature_list:  #for each feature in the dataset
        feature_info_gain = calc_info_gain(feature, train_data, label, class_list)
        if max_info_gain < feature_info_gain: #selecting feature name with highest information gain
            max_info_gain = feature_info_gain
            max_info_feature = feature
            
    return max_info_feature