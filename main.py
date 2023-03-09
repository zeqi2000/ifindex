import AG
import data_process
import parameter_setting as para
from generate_query import *
import objprint

def setup_args(args=None):
    args.epsilon = 0.2
    args.query_num = 20


args = para.generate_args()

print(args)

data = data_process.load_dataset("data/simple_acci_point.csv")

gindex = AG.gindex(args)

gindex.build_index(data)

queryList = RangeQueryList(10)
queryList.generate_range_query_list(gindex.min_x, gindex.max_x, gindex.min_y, gindex.max_y)

for query in queryList.range_query_list:
    x = gindex.answer_query(query)
    queryList.index_answer_list.append(x)


objprint.objprint(queryList)

# query = RangeQuery(0,1,50,52)
# print(gindex.answer_query(query))

# 待完成：
# 一二级索引拆分
# args 模块建立
