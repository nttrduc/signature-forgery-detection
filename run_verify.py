import torch
import os
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from torchvision import models, transforms
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.backbone = models.resnet18(pretrained=False)
        self.backbone.fc = nn.Identity()  # Remove the last fully connected layer

        self.fc1 = nn.Linear(512, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)

    def forward_once(self, x):
        x = self.backbone(x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x

    def forward(self, input1, input2):
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return output1, output2

# Kiểm tra GPU có sẵn và chọn thiết bị
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# Tạo mô hình và chuyển sang GPU nếu có
model = SiameseNetwork().to(device)
model.load_state_dict(torch.load("siamese_network.pth"))
model.eval()  

# Định nghĩa các phép biến đổi ảnh
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Đọc và biến đổi ảnh
img1 = Image.open("results\\latest_net_G\\test_latest\\images\\image1_fake.png")
img2 = Image.open("results\\latest_net_G\\test_latest\\images\\image0_fake.png")
img1 = transform(img1).unsqueeze(0).to(device)  
img2 = transform(img2).unsqueeze(0).to(device)
output1, output2 = model(img1, img2)
euclidean_distance = F.pairwise_distance(output1, output2).detach().cpu().numpy()

folder_path = 'web'
file_name = 'final_predict.txt'
file_path = os.path.join(folder_path, file_name)
os.makedirs(folder_path, exist_ok=True)
if euclidean_distance[0] > 0.4:
    new_content = 'FAKE'
else:
    new_content = 'REAL'
with open(file_path, 'w') as file:
    file.write(new_content + '\n')