import math
import numpy as np
from generate_query import RangeQuery
import argparse
import data_process


# 第一层索引
class gindex:
    def __init__(self, args: argparse):

        # 将α设置在[0.2, 0.6]的范围内会产生类似的准确性。我们设定α=0.5
        self.args = args
        self.alpha = args.alpha
        self.c1 = args.c1
        self.c2 = self.c1 / 2
        self.N = -1
        self.epsilon = args.epsilon
        self.m1 = -1
        self.m2 = -1
        self.sub_grid_set: list[sindex] = []  # list中元素指定类型为第二级索引 sindex

    def build_index(self, data):
        self.N = len(data)
        # 每个维度都划分成为m1个区间
        self.m1 = max(10, (math.ceil(self.N * self.epsilon / self.c1) ** 0.5) / 4)

        self.X = data['Longitude'].tolist()
        self.Y = data['Latitude'].tolist()

        self.min_x = min(self.X) - 1e-10
        self.max_x = max(self.X) + 1e-10
        self.min_y = min(self.Y) - 1e-10
        self.max_y = max(self.Y) + 1e-10
        self.cell_size_x = (self.max_x - self.min_x) / self.m1
        self.cell_size_y = (self.max_y - self.min_y) / self.m1
        self.cells = [[] for i in range(self.m1 * self.m1)]

        # 进行网格划分
        self.grid_x, self.grid_y = np.meshgrid(
            np.arange(self.min_x, self.max_x, self.cell_size_x),
            np.arange(self.min_y, self.max_y, self.cell_size_y)
        )
        self.grid_x = self.grid_x.flatten()
        self.grid_y = self.grid_y.flatten()

        # 遍历data，将点放入各cell
        for i in range(len(data)):
            self.add_point(self.X[i], self.Y[i])

        self.real_count = [len(self.cells[i]) for i in range(self.m1 * self.m1)]
        ##这里写扰动数据的逻辑
        # self.perturbed_count = self.real_count
        self.perturbed_count = laplace_noisy(self.real_count, 1, self.epsilon * self.alpha)
        self.perturbed_count = data_process.norm_sub(self.perturbed_count)

        self.construct_grid_set()

    # def build_second_index(self,data,n_):
    #     """
    #     @param data: 此二级索引内部的所有数据点
    #     @param n_: 二级索引接收到的被扰动的数据点个数
    #     @return:
    #     """
    #
    #     self.N = n_
    #     # 每个维度都划分成为m1个区间
    #     # self.m1 = max(10,(math.ceil(self.N*self.epsilon/self.c1)**0.5)/4 )
    #     self.m2 = math.ceil( (self.N*(1-self.alpha)*self.epsilon/self.c2)**0.5 )
    #
    #     # self.X = data['Longitude'].tolist()
    #     # self.Y = data['Latitude'].tolist()
    #     temp_o = list(zip(*data))
    #     self.X = temp_o[0]
    #     self.Y = temp_o[1]
    #
    #     self.min_x = min(self.X) - 1e-10
    #     self.max_x = max(self.X) + 1e-10
    #     self.min_y = min(self.Y) - 1e-10
    #     self.max_y = max(self.Y) + 1e-10
    #     self.cell_size_x = (self.max_x - self.min_x)/self.m2
    #     self.cell_size_y = (self.max_y - self.min_y)/self.m2
    #     self.cells = [[] for i in range(self.m2 * self.m2)]
    #
    #     # 遍历data，将点放入各cell
    #     for i in range(len(data)):
    #         self.add_point(self.X[i],self.Y[i])
    #
    #     self.real_count = [len(self.cells[i]) for i in range(self.m2 * self.m2)]
    #     self.perturbed_count = self.real_count ##这里写扰动数据的逻辑

    def construct_grid_set(self):
        for i in range(self.m1 ** 2):
            if (self.perturbed_count[i] > 0):
                tmp_gindex = sindex(self.args)
                tmp_gindex.build_second_index(self.grid_x[i], self.grid_x[i] + self.cell_size_x, self.grid_y[i],
                                              self.grid_y[i] + self.cell_size_y, self.cells[i], self.perturbed_count[i])
                self.sub_grid_set.append(tmp_gindex)
            else:
                self.sub_grid_set.append(None)

    def add_point(self, x, y):
        cell_x = int((x - self.min_x) / self.cell_size_x)
        cell_y = int((y - self.min_y) / self.cell_size_y)
        cell_index = cell_y * self.m1 + cell_x
        self.cells[cell_index].append((x, y))

    # 计算数据点(x,y)属于第几个cell
    def get_cell_index(self, x, y):
        cell_x = int((x - self.min_x) / self.cell_size_x)
        cell_y = int((y - self.min_y) / self.cell_size_y)
        cell_index = cell_y * self.m1 + cell_x
        return cell_index

    def answer_query(self, query: RangeQuery):
        # 进行网格划分
        # grid_x, grid_y = np.meshgrid(
        #     np.arange(self.min_x, self.max_x, self.cell_size_x),
        #     np.arange(self.min_y, self.max_y, self.cell_size_y)
        # )
        # grid_x = grid_x.flatten()
        # grid_y = grid_y.flatten()

        count_answer = 0.0
        for i in range(len(self.grid_x)):
            # 确定当前网格的范围
            cell_x_min = self.grid_x[i]
            cell_x_max = self.grid_x[i] + self.cell_size_x
            cell_y_min = self.grid_y[i]
            cell_y_max = self.grid_y[i] + self.cell_size_y

            vertexNum = get_vertexNum_of_cell_in_query(cell_x_min, cell_x_max, cell_y_min, cell_y_max, query)
            if (vertexNum == 4):
                count_answer += self.perturbed_count[i]
            elif (vertexNum == 2 or vertexNum == 1):
                # 若穿过该cell，也加上该cell全部数值
                # count_answer += self.perturbed_count[i]

                count_answer += self.get_part_of_count(i, query)

        return count_answer

    def get_part_of_count(self, index_of_cell, query: RangeQuery):
        tmp_sindex = self.sub_grid_set[index_of_cell]
        if tmp_sindex != None:
            return tmp_sindex.answer_query(query)
        else:
            return 0


def laplace_noisy(data, sensitivity, epsilon):
    """
    :param data: 数据
    :param sensitivity: 敏感度
    :param epsilon: 隐私预算
    :return: 添加拉普拉斯噪声后的数据
    """
    beta = sensitivity / epsilon  # 计算噪声参数
    noise = np.random.laplace(0, beta, len(data))  # 生成拉普拉斯噪声
    return data + noise  # 返回添加噪声后的数据


# cell的四个顶点在有几个query范围内
def get_vertexNum_of_cell_in_query(cell_x_min, cell_x_max, cell_y_min, cell_y_max, query: RangeQuery):
    tmp_count = 0
    tmp_count += is_point_in_query(cell_x_min, cell_y_min, query)
    tmp_count += is_point_in_query(cell_x_max, cell_y_min, query)
    tmp_count += is_point_in_query(cell_x_min, cell_y_max, query)
    tmp_count += is_point_in_query(cell_x_max, cell_y_max, query)
    return tmp_count


def is_point_in_query(point_x, point_y, query: RangeQuery):
    if (point_x >= query.query_x_min and point_x <= query.query_x_max
            and point_y >= query.query_y_min and point_y <= query.query_y_max):
        return True
    else:
        return False


# 第二层索引
class sindex:
    def __init__(self, args: argparse):
        self.alpha = args.alpha

        self.c1 = args.c1
        self.c2 = self.c1 / 2
        self.N = -1
        self.epsilon = args.epsilon
        # self.m1 = -1
        self.m2 = -1

    def build_second_index(self, index_x_min, index_x_max, index_y_min, index_y_max, data, n_):
        """
        @param data: 此二级索引内部的所有数据点，格式为[(x1,y1),...,(xn,yn)]
        @param n_: 二级索引接收到的被扰动的数据点个数
        @return:
        """

        self.N = n_
        # 每个维度都划分成为m个区间
        # self.m1 = max(10,(math.ceil(self.N*self.epsilon/self.c1)**0.5)/4 )

        # m2 = (self.N*(1-self.alpha)*self.epsilon/self.c2)**0.5) 时，可能为0，此时取1
        # self.m2 = math.ceil((self.N*(1-self.alpha)*self.epsilon/self.c2)**0.5)
        tmp_m = math.ceil((self.N * (1 - self.alpha) * self.epsilon / self.c2) ** 0.5)
        self.m2 = max(tmp_m, 1)

        # self.X = data['Longitude'].tolist()
        # self.Y = data['Latitude'].tolist()
        temp_o = list(zip(*data))
        if len(temp_o) > 0:
            self.X = temp_o[0]
            self.Y = temp_o[1]
        else:
            self.X = []
            self.Y = []

        self.min_x = index_x_min
        self.max_x = index_x_max
        self.min_y = index_y_min
        self.max_y = index_y_max
        self.cell_size_x = (self.max_x - self.min_x) / self.m2
        self.cell_size_y = (self.max_y - self.min_y) / self.m2
        self.cells = [[] for i in range(self.m2 * self.m2)]

        # 遍历data，将点放入各cell
        for i in range(len(data)):
            self.add_point(self.X[i], self.Y[i])

        self.real_count = [len(self.cells[i]) for i in range(self.m2 * self.m2)]
        ##这里写扰动数据的逻辑
        # self.perturbed_count = self.real_count
        self.perturbed_count = laplace_noisy(self.real_count, 1, (1 - self.alpha) * self.epsilon)

    def add_point(self, x, y):
        cell_x = int((x - self.min_x) / self.cell_size_x)
        cell_y = int((y - self.min_y) / self.cell_size_y)
        cell_index = cell_y * self.m2 + cell_x
        self.cells[cell_index].append((x, y))

    def answer_query(self, query: RangeQuery):
        # 进行网格划分

        # aa=np.arange(self.min_x, self.max_x, self.cell_size_x)
        aa = [self.min_x + i * self.cell_size_x for i in range(self.m2)]
        # bb=np.arange(self.min_y, self.max_y, self.cell_size_y)
        bb = [self.min_y + i * self.cell_size_y for i in range(self.m2)]
        grid_x, grid_y = np.meshgrid(
            aa,
            bb
        )
        grid_x = grid_x.flatten()
        grid_y = grid_y.flatten()

        count_answer = 0.0
        for i in range(len(grid_x)):
            # 确定当前网格的范围
            cell_x_min = grid_x[i]
            cell_x_max = grid_x[i] + self.cell_size_x
            cell_y_min = grid_y[i]
            cell_y_max = grid_y[i] + self.cell_size_y

            count_answer += self.perturbed_count[i] * area_ratio(cell_x_min, cell_x_max, cell_y_min, cell_y_max, query)

            # vertexNum = get_vertexNum_of_cell_in_query(cell_x_min, cell_x_max, cell_y_min, cell_y_max, query)
            # if(vertexNum == 4):
            #     count_answer += self.perturbed_count[i]
            # elif(vertexNum == 2 or vertexNum == 1):
            #     # count_answer += self.perturbed_count[i]
            #
            #     count_answer += self.perturbed_count[i] * area_ratio(cell_x_min,cell_x_max, cell_y_min, cell_y_max,query)

        return count_answer


# 返回某cell在query中的面积 与 此整个cell 的面积占比
def area_ratio(cell_x_min, cell_x_max, cell_y_min, cell_y_max, query: RangeQuery):
    # (x1,y1),(x2,y2)是两个矩形的相交部分
    x1 = max(cell_x_min, query.query_x_min)
    y1 = max(cell_y_min, query.query_y_min)
    x2 = min(cell_x_max, query.query_x_max)
    y2 = min(cell_y_max, query.query_y_max)
    if (x2 > x1 and y2 > y1):
        return (x2 - x1) * (y2 - y1) / ((cell_x_max - cell_x_min) * (cell_y_max - cell_y_min))
    else:
        return 0
