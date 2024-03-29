import numpy as np
import torch
import matplotlib.pyplot as plt
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# 1.prepare dataset
xy = np.loadtxt("diabetes.csv", skiprows=1, delimiter=",", dtype=np.float32)
x_data = torch.from_numpy(xy[:, :-1])  # 第一个‘：’是指读取所有行，第二个‘：’是指从第一列开始，最后一列不要
y_data = torch.from_numpy(xy[:, [-1]])  # [-1] 最后得到的是个矩阵


# 2.design model using class
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(8, 6)  # 输入数据x的特征是8维，x有8个特征
        self.linear2 = torch.nn.Linear(6, 4)
        self.linear3 = torch.nn.Linear(4, 1)
        self.activate = torch.nn.ReLU()
        self.sigmoid = torch.nn.Sigmoid()  # 将其看作是网络的一层，而不是简单的函数使用

    def forward(self, x):
        x = self.activate(self.linear1(x))
        x = self.activate(self.linear2(x))
        x = self.sigmoid(self.linear3(x))  # y hat
        return x


device = torch.device("cuda:0")
model = Model().to(device)
x_data = x_data.to(device)
y_data = y_data.to(device)

# 3.construct loss and optimizer
criterion = torch.nn.BCELoss(reduction="mean")
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

epoch_list = []
loss_list = []
# 4.training cycle forward, backward, update
for epoch in range(100000):
    y_pred = model(x_data)
    loss = criterion(y_pred, y_data)
    if epoch % 1000 == 0:
        print(epoch, loss.item())
        epoch_list.append(epoch)
        loss_list.append(loss.item())

    optimizer.zero_grad()
    loss.backward()

    optimizer.step()

# 5.test
print("w = ", model.linear3.weight.data)
print("b = ", model.linear3.bias.data)
x_test = torch.Tensor(
    [
        0.176471,
        0.256281,
        0.147541,
        -0.474747,
        -0.728132,
        -0.0730253,
        -0.891546,
        -0.333333,
    ]
).to(device)
y_test = model(x_test)
print("y_pred = ", y_test.data)
x_test = torch.Tensor(
    [-0.0588235, -0.00502513, 0.377049, 0, 0, 0.0551417, -0.735269, -0.0333333]
).to(device)
y_test = model(x_test)
print("y_pred = ", y_test.data)

plt.plot(epoch_list, loss_list)
plt.ylabel("loss")
plt.xlabel("epoch")
plt.show()
