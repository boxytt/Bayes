from numpy import *

class NaiveBayesClassifier(object):

    # 全局变量

    allList = []   # 全部数据
    maleList = []   # 男性数据
    femaleList = [] # 女性数据
    # 存储均值
    average_male_height = 0
    average_male_weight = 0
    average_male_foot = 0
    average_female_height = 0
    average_female_weight = 0
    average_female_foot = 0
    # 存储方差
    variance_male_height = 0
    variance_male_weight = 0
    variance_male_foot = 0
    variance_female_height = 0
    variance_female_weight = 0
    variance_female_foot = 0


    # 工具方法

    '''
    将全部数据allList分类成男maleList和女femaleList
    '''
    def sexClassify(self):
        for i in range(len(self.allList)):
            if self.allList[i][0] == '1':
                self.maleList.append(self.allList[i])
            else:
                self.femaleList.append(self.allList[i])

    '''
    返回list的propertyNum字段的平均值
    '''
    def average(self, list, propertyNum):
        count = len(list)  # 数据个数
        thisPropertyList = []
        for i in range(count):
           thisPropertyList.append(float(list[i][propertyNum]))

        return mean(thisPropertyList)

    '''
    返回list的propertyNum字段的方差
    '''
    def variance(self, list, propertyNum):
        count = len(list)  # 数据个数
        thisPropertyList = []
        for i in range(count):
            thisPropertyList.append(float(list[i][propertyNum]))

        return var(thisPropertyList)

    '''
    返回list的propertyNum字段的密度函数值
    '''
    def density(self, ave, var, value):
        return 1 / sqrt(2 * pi * var) * exp(-square(value - ave) / (2 * var))




    # 主要方法

    '''
    从文件中读取训练数据，并存储到列表dataList中
    列属性按次序分别为：性别 身高 体重 脚掌；
    '''
    def loadData(self, filename):
        f = open(filename, 'r') # 打开文件
        next(f)     # 跳过第一行
        lines = f.readlines()    # 按行读出文件内容
        f.close()
        for line in lines:
            temp1 = line.strip('\n')    # 去掉每行最后的换行符'\n'
            temp2 = temp1.split('     ')   # 以制表符'     '为标志，将每行分割成列表
            self.allList.append(temp2)
        self.sexClassify()


    '''
    用dataList中的数据训练，得到密度函数
    假设男性和女性的身高、体重、脚掌都是正态分布，通过样本计算出均值和方差，也就是得到正态分布的密度函数。
    有了密度函数，就可以把值代入，算出某一点的密度函数的值。
    '''
    def trainData(self):
        # 属性：1-身高 2-体重 3-脚掌

        # 求均值
        self.average_male_height = self.average(self.maleList, 1)
        self.average_male_weight = self.average(self.maleList, 2)
        self.average_male_foot = self.average(self.maleList, 3)
        self.average_female_height = self.average(self.femaleList, 1)
        self.average_female_weight = self.average(self.femaleList, 2)
        self.average_female_foot = self.average(self.femaleList, 3)

        # 求方差
        self.variance_male_height = self.variance(self.maleList, 1)
        self.variance_male_weight = self.variance(self.maleList, 2)
        self.variance_male_foot = self.variance(self.maleList, 3)
        self.variance_female_height = self.variance(self.femaleList, 1)
        self.variance_female_weight = self.variance(self.femaleList, 2)
        self.variance_female_foot = self.variance(self.femaleList, 3)

    '''
    计算 P(身高|性别) x P(体重|性别) x P(脚掌|性别) x P(性别) 的值
    P通过正态分布的密度函数计算
    比较得出的男性和女性的比例
    '''
    def calculateClassify(self, height, weight, foot):
        p_male_height = self.density(self.average_male_height, self.variance_male_height, float(height))
        p_male_weight = self.density(self.average_male_weight, self.variance_male_weight, float(weight))
        p_male_foot = self.density(self.average_male_foot, self.variance_male_foot, float(foot))
        p_male = p_male_height * p_male_weight * p_male_foot * 0.5
        print("男性概率：%e" %(p_male))

        p_male_height = self.density(self.average_female_height, self.variance_female_height, float(height))
        p_male_weight = self.density(self.average_female_weight, self.variance_female_weight, float(weight))
        p_male_foot = self.density(self.average_female_foot, self.variance_female_foot, float(foot))
        p_female = p_male_height * p_male_weight * p_male_foot * 0.5
        print("女性概率：%e"%(p_female))

        if p_male > p_female:
            print("该人是男性!")
        elif p_male < p_female:
            print("该人是女性!")
        else:
            print("该人是中性(男女都有可能)")





if __name__ == '__main__':
    NB = NaiveBayesClassifier()
    NB.loadData('data')
    NB.trainData()
    height = input("输入身高(英尺):")
    weight = input("输入体重(磅):")
    foot = input("输入脚掌(英寸):")
    print("")
    NB.calculateClassify(height, weight, foot)




