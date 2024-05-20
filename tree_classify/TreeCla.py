from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import matplotlib.pyplot as plt
from pylab import mpl
# 设置显示中文字体
all_tags = set()
all_tags_dev = set()
clf = DecisionTreeClassifier(random_state=0, max_depth=30)

def decision_tree(x_train, y_train):
    """最基础的决策树"""
    X_tr, X_te, y_tr, y_te = train_test_split(x_train, y_train, test_size=0.1, random_state=42)
    # print(data)
    clf.fit(X_tr, y_tr)
    predict(X_te, y_te)
    
def predict(X_te, y_te):
    y_pred = clf.predict(X_te)
    
    accuracy = accuracy_score(y_te, y_pred)
    print(f'Accuracy: {accuracy:.2f}')
    plt.figure(figsize=(15,9))

    comm = ['好评如潮','特别好评','好评','多半好评','褒贬不一','多半差评','特别差评','差评如潮']
    plot_tree(clf,filled=True,feature_names=list(all_tags)+list(all_tags_dev), class_names=comm)


    plt.show()

def ans(tags,dev):
    global all_tags
    global all_tags_dev
    tags = tags.split()

    # print(all_tags)
    x_te = pd.DataFrame(0, index=[0], columns=all_tags)
    for tag in tags:
        x_te.loc[0, tag] = 1
    x_te = x_te.to_numpy()

    # print(all_tags_dev)
    developer = pd.DataFrame(0, index=[0], columns=all_tags_dev)
        # 对于每个列表，设置对应的标签为1
    developer.loc[0, dev] = 1
    developer = developer.to_numpy()

    for i in range(developer.shape[1]):
        x_te = np.column_stack((x_te, developer[:,i]))
    comm = ['好评如潮','特别好评','好评','多半好评','褒贬不一','多半差评','特别差评','差评如潮']
    ans = clf.predict(x_te)[0]
    return comm[ans]

def gbdt(x_train, y_train):

    """GBDT决策树，疑似能用来预测价格"""
    params = {'n_estimators': 500, # 弱分类器的个数
          'max_depth': 3,       # 弱分类器（CART回归树）的最大深度
          'min_samples_split': 5, # 分裂内部节点所需的最小样本数
          'learning_rate': 0.05,  # 学习率
          'loss': 'ls'}           # 损失函数：均方误差损失函数
    GBDTreg = GradientBoostingRegressor(**params)
    X_tr, X_te, y_tr, y_te = train_test_split(x_train, y_train, test_size=0.1, random_state=42)
    GBDTreg.fit(X_tr, y_tr)
    y_predict = GBDTreg.predict(X_te)
    mse = mean_squared_error(y_te, y_predict)
    print("The mean squared error (MSE) on test set: {:.4f}".format(mse))

# if __name__ == 'main':
def training():
    global all_tags
    global all_tags_dev
    mpl.rcParams["font.sans-serif"] = ["SimHei"]
    data = pd.read_csv(r'G:\\code\\data_mining\\groupwork\\game_info.csv',sep=',',header='infer')

    tags = []
    for i in data['tag']:
        temp = i.split('\n')
        tags.append(temp)

    all_tags = set(tag for tags_list in tags for tag in tags_list)
    # 创建一个空的DataFrame，标签作为列
    x_train = pd.DataFrame(0, index=range(len(tags)), columns=all_tags)
    # 对于每个列表，设置对应的标签为1
    for i, tags_list in enumerate(tags):
        for tag in tags_list:
            x_train.loc[i, tag] = 1
    x_train = x_train.to_numpy()

    # 加入发行商
    dev_data = data['developer'].values
    # encoder=OneHotEncoder(sparse=False) # One-Hot编码
    # developer=encoder.fit_transform(developer.reshape((-1,1)))
    all_tags_dev = set(i for i in dev_data)
    developer = pd.DataFrame(0, index=range(len(dev_data)), columns=all_tags_dev)
        # 对于每个列表，设置对应的标签为1
    for i, tags in enumerate(dev_data):
        developer.loc[i, tag] = 1
    developer = developer.to_numpy()

    #合起来
    for i in range(developer.shape[1]):
        x_train = np.column_stack((x_train, developer[:,i]))

    # print("One-hot 编码结果（numpy 数组格式）:")
    # print(x_train)

    comm = ['好评如潮','特别好评','好评','多半好评','褒贬不一','多半差评','特别差评','差评如潮']

    percen = np.array(data['Overall_Percentage'])

    od = data['Overall_Description']
    y_train = []
    for i in od:
        y_train.append(comm.index(i))
    y_train = np.array(y_train)
    # print(y_train)

    x_train_comm = np.column_stack((x_train, y_train))

    # y_price = np.array(data['price'])
    # # one_hot_y_train = y_train.to_numpy()

    # print("One-hot 编码结果（numpy 数组格式）:")
    # print(y_train)

    # decision_tree(one_hot_x_train,comm)

    decision_tree(x_train, y_train)


    # y_pred = clf.predict(X_test)
    # accuracy = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {accuracy:.2f}')

# training()