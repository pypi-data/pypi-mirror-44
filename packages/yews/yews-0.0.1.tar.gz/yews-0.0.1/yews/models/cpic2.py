import torch
import torch.nn as nn
import torch.nn.functional as F

__all__ = [
    'Cpic2',
]

class Cpic2(nn.Module):

    def __init__(self, num_classes=3):
        super(Cpic2, self).__init__()

        # use inception v3 stem
        # use two 3x3 to replace 5x5
        self.Conv1d_1a_3x3 = BasicConv1d(3, 4, kernel_size=3, stride=2)
        self.Conv1d_2a_3x3 = BasicConv1d(4, 4, kernel_size=3)
        self.Conv1d_2b_3x3 = BasicConv1d(4, 8, kernel_size=3, padding=1)
        self.Conv1d_3b_1x1 = BasicConv1d(8, 10, kernel_size=1)
        self.Conv1d_4a_3x3 = BasicConv1d(10, 28, kernel_size=3)
        self.Mixed5a = InceptionA(28, pool_features=4)
        self.Mixed5b = InceptionA(32, pool_features=8)
        self.Mixed5c = InceptionA(36, pool_features=8)
        self.Mixed6a = InceptionB(36)
        self.fc = nn.Linear(96, num_classes)

    def forward(self, x):
        # N x 3 x 2000
        x = self.Conv1d_1a_3x3(x)
        # N x 4 x 999
        x = self.Conv1d_2a_3x3(x)
        # N x 4 x 997
        x = self.Conv1d_2b_3x3(x)
        # N x 8 x 997
        x = F.max_pool1d(x, kernel_size=3, stride=2)
        # N x 8 x 498
        x = self.Conv1d_3b_1x1(x)
        # N x 10 x 498
        x = self.Conv1d_4a_3x3(x)
        # N x 28 x 496
        x = F.max_pool1d(x, kernel_size=3, stride=2)
        # N x 28 x 247
        x = self.Mixed5a(x)
        # N x 32 x 247
        x = self.Mixed5b(x)
        # N x 36 x 247
        x = self.Mixed5c(x)
        # N x 36 x 247
        x = self.Mixed6a(x)
        # N x 96 x 123
        x = F.adaptive_avg_pool1d(x, 1)
        # N x 96 x 1
        x = F.dropout(x, training=self.training)
        # N x 96 x 1
        x = x.view(x.size(0), -1)
        # N x 96
        x = self.fc(x)
        # N x 3 (num_classes)
        return x

class BasicConv1d(nn.Module):

    def __init__(self, in_channels, out_channels, **kwargs):
        super(BasicConv1d, self).__init__()
        self.conv = nn.Conv1d(in_channels, out_channels, bias=False, **kwargs)
        self.bn = nn.BatchNorm1d(out_channels)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)

        return F.relu(x, inplace=True)

class InceptionA(nn.Module):

    def __init__(self, in_channels, pool_features):
        super(InceptionA, self).__init__()
        self.branch1x1 = BasicConv1d(in_channels, 8, kernel_size=1)

        self.branch3x3_1 = BasicConv1d(in_channels, 6, kernel_size=1)
        self.branch3x3_2 = BasicConv1d(6, 8, kernel_size=3, padding=1)

        self.branch3x3dbl_1 = BasicConv1d(in_channels, 8, kernel_size=1)
        self.branch3x3dbl_2 = BasicConv1d(8, 12, kernel_size=3, padding=1)
        self.branch3x3dbl_3 = BasicConv1d(12, 12, kernel_size=3, padding=1)

        self.branch_pool = BasicConv1d(in_channels, pool_features, kernel_size=1)


    def forward(self, x):
        branch1x1 = self.branch1x1(x)

        branch3x3 = self.branch3x3_1(x)
        branch3x3 = self.branch3x3_2(branch3x3)

        branch3x3dbl = self.branch3x3dbl_1(x)
        branch3x3dbl = self.branch3x3dbl_2(branch3x3dbl)
        branch3x3dbl = self.branch3x3dbl_3(branch3x3dbl)

        branch_pool = F.avg_pool1d(x, kernel_size=3, stride=1, padding=1)
        branch_pool = self.branch_pool(branch_pool)

        outputs = [branch1x1, branch3x3, branch3x3dbl, branch_pool]
        return torch.cat(outputs, 1)

class InceptionB(nn.Module):

    def __init__(self, in_channels):
        super(InceptionB, self).__init__()
        self.branch3x3 = BasicConv1d(in_channels, 48, kernel_size=3, stride=2)

        self.branch3x3dbl_1 = BasicConv1d(in_channels, 8, kernel_size=1)
        self.branch3x3dbl_2 = BasicConv1d(8, 12, kernel_size=3, padding=1)
        self.branch3x3dbl_3 = BasicConv1d(12, 12, kernel_size=3, stride=2)

    def forward(self, x):
        branch3x3 = self.branch3x3(x)

        branch3x3dbl = self.branch3x3dbl_1(x)
        branch3x3dbl = self.branch3x3dbl_2(branch3x3dbl)
        branch3x3dbl = self.branch3x3dbl_3(branch3x3dbl)

        branch_pool = F.max_pool1d(x, kernel_size=3, stride=2)

        outputs = [branch3x3, branch3x3dbl, branch_pool]
        return torch.cat(outputs, 1)

