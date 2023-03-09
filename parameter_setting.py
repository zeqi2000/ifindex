import argparse

def generate_args(): # intialize paprameters
    parser = argparse.ArgumentParser()

    # int type
    parser.add_argument("--query_num", type=int, default=10, help= "the number of queries")


    # float type
    parser.add_argument("--epsilon", type=float, default=0.1, help= "the privacy budget")
    # 将α设置在[0.2, 0.6]的范围内会产生类似的准确性。我们设定α=0.5
    parser.add_argument("--alpha", type=float, default=0.5, help= "how to allocate the privacy budget")
    parser.add_argument("--c1", type=float, default=10, help= "该值与数据集有关，一般设为10")
    parser.add_argument("--c2", type=float, default=5, help= "")

    # str type
    parser.add_argument("--algorithm_name", type=str, default="", help="")

    args = parser.parse_args()
    return args

