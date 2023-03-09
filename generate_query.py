import random


class RangeQuery:
    def __init__(self, query_x_min, query_x_max, query_y_min, query_y_max):
        self.query_x_min = query_x_min
        self.query_x_max = query_x_max
        self.query_y_min = query_y_min
        self.query_y_max = query_y_max

    # def __str__(self):
    #     return "("+self.query_x_min+","+self.query_x_max+","+self.query_y_min+","+self.query_y_max+")"


class RangeQueryList:
    def __init__(self, query_num, args=None):
        self.args = args
        self.query_num = query_num

        self.range_query_list = []
        self.real_answer_list = []
        self.index_answer_list = []


    def generate_range_query_list(self, min_x, max_x, min_y, max_y):
        print("generating range queries...")
        for i in range(self.query_num):
            x1 = random.uniform(min_x, max_x)
            x2 = random.uniform(min_x, max_x)
            y1 = random.uniform(min_y, max_y)
            y2 = random.uniform(min_y, max_y)
            if (x1 > x2):
                x1, x2 = x2, x1
            if (y1 > y2):
                y1, y2 = y2, y1
            tmp_range_query = RangeQuery(x1, x2, y1, y2)
            self.range_query_list.append(tmp_range_query)
