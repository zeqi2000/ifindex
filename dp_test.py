import numpy as np

# 定义数据集
data = np.random.rand(1000, 2)

# 定义网格大小
grid_size = 0.1

# 进行网格划分
grid_x, grid_y = np.meshgrid(
    np.arange(0, 1, grid_size),
    np.arange(0, 1, grid_size)
)

grid_x = grid_x.flatten()
grid_y = grid_y.flatten()

# 计算每个网格中的数据点数量
counts = np.zeros_like(grid_x)
for i in range(len(grid_x)):
    # 确定当前网格的范围
    x_min = grid_x[i]
    x_max = grid_x[i] + grid_size
    y_min = grid_y[i]
    y_max = grid_y[i] + grid_size

    # 进行网格过滤，只保留符合条件的网格
    mask = np.logical_and(
        np.logical_and(data[:, 0] >= x_min, data[:, 0] < x_max),
        np.logical_and(data[:, 1] >= y_min, data[:, 1] < y_max)
    )

    # 统计当前网格中符合条件的数据点数量
    counts[i] = np.sum(mask)

# 输出结果
print(counts)