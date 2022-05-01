from entropy import find_most_informative_feature

def generate_sub_tree(feature_name, train_data, label, class_list):
    # feature_name: string, the name of the feature that we want to add to tree and shrink dataset (Ex. Outlook)
    # train_data: a pandas dataframe/dataset
    # label: string, name of the label of the dataframe (=Play Tennis)
    # class_list: list, unique classes of the label (=[Yes, No]).
    # returns: (dictionary, dataframe), the tree node with it’s branches and the updated dataset
    feature_value_count_dict = train_data[feature_name].value_counts(
        sort=False)  # dictionary of the count of unqiue feature value
    tree = {}  # sub tree or node

    for feature_value, count in feature_value_count_dict.iteritems():
        # dataset with only feature_name = feature_value
        feature_value_data = train_data[train_data[feature_name]
                                        == feature_value]

        assigned_to_node = False  # flag for tracking feature_value is pure class or not
        for c in class_list:  # for each class
            # count of class c
            class_count = feature_value_data[feature_value_data[label] == c].shape[0]

            # count of feature_value = count of class (pure class)
            if class_count == count:
                tree[feature_value] = c  # adding node to the tree
                # removing rows with feature_value
                train_data = train_data[train_data[feature_name]
                                        != feature_value]
                assigned_to_node = True
        if not assigned_to_node:  # not pure class
            # should extend the node, so the branch is marked with ?
            tree[feature_value] = "?"

    return tree, train_data


def make_tree(root, prev_feature_value, train_data, label, class_list):
    # root: dictionary, the current pointed node/feature of the tree. It is contineously being updated.
    # prev_feature_value: Any datatype (Int or Float or String etc.) depending on the datatype of the previous feature, the previous value of the pointed node/feature
    # train_data: a pandas dataframe/dataset
    # label: string, name of the label of the dataframe (=Play Tennis)
    # class_list: list, unique classes of the label (=[Yes, No]).
    # returns: None
    if train_data.shape[0] != 0:  # if dataset becomes enpty after updating
        max_info_feature = find_most_informative_feature(train_data, label, class_list)  # most informative feature
        # getting tree node and updated dataset
        tree, train_data = generate_sub_tree(max_info_feature, train_data, label, class_list)
        next_root = None

        if prev_feature_value != None:  # add to intermediate node of the tree
            root[prev_feature_value] = dict()
            root[prev_feature_value][max_info_feature] = tree
            next_root = root[prev_feature_value][max_info_feature]
        else:  # add to root of the tree
            root[max_info_feature] = tree
            next_root = root[max_info_feature]

        for node, branch in list(next_root.items()):  # iterating the tree node
            if branch == "?":  # if it is expandable
                # using the updated dataset
                feature_value_data = train_data[train_data[max_info_feature] == node]
                make_tree(next_root, node, feature_value_data, label,
                          class_list)  # recursive call with updated dataset


def id3(train_data_m, label):
    # train_data_m: a pandas dataframe/dataset
    # label: string, name of the label of the dataframe (=Play Tennis)
    # returns: (nested) dictionary, the decision tree
    train_data = train_data_m.copy() #getting a copy of the dataset
    tree = {} #tree which will be updated
    class_list = train_data[label].unique() #getting unqiue classes of the label
    print(class_list)
    make_tree(tree, None, train_data_m, label, class_list) #start calling recursion
    return tree
