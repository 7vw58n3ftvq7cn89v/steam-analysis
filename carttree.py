import numpy as np

def loadDataSet(fileName):
    """导入数据"""
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        # 使用python3会报错1，因为python3中map的返回类型是‘map’类，不能进行计算，需要将map转换为list
        fltLine = list(map(float, curLine))
        dataMat.append(fltLine)
    return dataMat


def binSplitDataSet(dataSet, feature, value):
    """
    通过数组过滤切分数据集
    :param dataSet: 数据集合
    :param feature: 待切分的特征
    :param value: 该特征的某个值
    :return:
    """
    # 使用python3会报错2，需要将书中脚本修改为以下内容
    mat0 = dataSet[np.nonzero(dataSet[:, feature] > value)[0], :]
    mat1 = dataSet[np.nonzero(dataSet[:, feature] <= value)[0], :]
    return mat0, mat1


def regLeaf(dataSet):
    """生成叶子节点，即目标变量的均值"""
    return np.mean(dataSet[:, -1])


def regErr(dataSet):
    """计算数据集中目标变量的误差平方和
    误差平方和 = 目标变量的均方差 * 数据集的样本个数
    """
    return np.var(dataSet[:, -1]) * dataSet.shape[0]


def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    """
    遍历所有的特征及其可能的取值来找到使误差平方和最小化的切分特征及其切分点
    :param dataSet: 数据集合
    :param leafType: 建立叶节点的函数，该参数也决定了要建立的是模型树还是回归树
    :param errType: 代表误差计算函数,即误差平方和计算函数
    :param ops: 用于控制函数的停止时机，第一个是容许的误差下降值，第二个是切分的最少样本数
    :return:最佳切分特征及其切分点
    """
    tolS = ops[0]
    tolN = ops[1]
    # 如果所有值都相等，则停止切分，直接生成叶结点
    if len(set(dataSet[:-1].T.tolist()[0])) == 1:
        return None, leafType(dataSet)
    m, n = dataSet.shape
    S = errType(dataSet)
    bestS = np.inf
    bestIndex = 0
    bestValue = 0
    # 数据集中最后一列是标签，不是特征，所以这里是n-1
    for featIndex in range(n - 1):
        # set(dataSet[:,featIndex]) 使用python3会报错3，因为matrix类型不能被hash，需要修改为下面这句
        for splitVal in set(dataSet[:, featIndex].T.tolist()[0]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            # 如果切分出的数据集小于切分最小样本数，则继续下一个
            if mat0.shape[0] < tolN or mat1.shape[0] < tolN:
                continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestS = newS
                bestIndex = featIndex
                bestValue = splitVal
    # 如果误差减少不大，则停止切分，直接生成叶结点
    if (S - bestS) < tolS:
        return None, leafType(dataSet)

    # 《机器学习实战》中，感觉下面这三句话多余(可以删了)，因为在上面已经判断过了切分出的数据集很小的情况 #
    # mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)  # 用最佳切分特征和切分点进行切分
    # if mat0.shape[0] < tolN or mat1.shape[0] < tolN: # 如果切分出的数据集很小，则停止切分，直接生成叶结点
    #     return None, leafType(dataSet)

    return bestIndex, bestValue  # 返回最佳切分特征编号和切分点


def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    """
    构建CART回归树
    :param dataSet: 数据集，默认NumPy Mat
    :param leafType: 建立叶节点的函数，该参数也决定了要建立的是模型树还是回归树
    :param errType: 代表误差计算函数,即误差平方和计算函数
    :param ops: 用于控制函数的停止时机，第一个是容许的误差下降值，第二个是切分的最少样本数
    :return:
    """
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
    # 如果feat为None, 则返回叶结点对应的预测值
    if feat == None:
        return val
    retTree = {}
    retTree['spInd'] = feat  # 最佳切分特征
    retTree['spVal'] = val  # 切分点
    # 切分后的左右子树
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet, leafType, errType, ops)
    return retTree


dataMat = loadDataSet('./data/ex00.txt')
dataMat = np.mat(dataMat)
regTree = createTree(dataMat)
print(regTree)