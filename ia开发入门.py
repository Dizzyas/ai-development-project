# 导入必要的库
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_scorei

# 生成模拟数据
np.random.seed(42)  # 设置随机种子，确保结果可重复
X = 2 * np.random.rand(100, 1)  # 生成100个0-2之间的随机数作为特征
y = 4 + 3 * X + np.random.randn(100, 1)  # 生成对应的目标值，添加一些噪声

# 数据可视化
plt.scatter(X, y)
plt.xlabel('特征 (X)')
plt.ylabel('目标值 (y)')
plt.title('模拟数据集')
plt.show()

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建并训练线性回归模型
model = LinearRegression()
model.fit(X_train, y_train)

# 查看模型参数
print("模型系数 (θ1):", model.coef_[0][0])
print("截距 (θ0):", model.intercept_[0])

# 在测试集上进行预测
y_pred = model.predict(X_test)

# 模型评估
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("均方误差 (MSE):", mse)
print("R² 评分:", r2)

# 可视化模型预测结果
plt.scatter(X_test, y_test, color='blue', label='真实值')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='预测值')
plt.xlabel('特征 (X)')
plt.ylabel('目标值 (y)')
plt.title('线性回归模型预测结果')
plt.legend()
plt.show()