import torch
import torchvision
from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.utils import save_image
from torchvision.datasets import MNIST
import os
import datetime

# if not os.path.exists('./vae_img'):
#     os.mkdir('./vae_img')
if not os.path.exists('./vae_img_infe'):
    os.mkdir('./vae_img_infe')

def to_img(x):
    x = x.clamp(0, 1)
    x = x.view(x.size(0), 1, 28, 28)
    return x


num_epochs = 10
batch_size = 128
learning_rate = 1e-3

img_transform = transforms.Compose([
    transforms.ToTensor()
    # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

dataset = MNIST('./data', transform=img_transform, download=True)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

class VAE(nn.Module):
    def __init__(self):
        super(VAE, self).__init__()
        self.fc1 = nn.Linear(784, 400)
        self.fc21 = nn.Linear(400, 20)
        self.fc22 = nn.Linear(400, 20)
        self.fc3 = nn.Linear(20, 400)
        self.fc4 = nn.Linear(400, 784)

    def encode(self, x):
        h1 = F.relu(self.fc1(x))
        return self.fc21(h1), self.fc22(h1)

    def reparametrize(self, mu, logvar):
        # print("mu:",mu)
        # print("mu.size():", mu.size())
        # print("logvar:",logvar)
        # print("logvar.size():", logvar.size())
        std = logvar.mul(0.5).exp_()
        if torch.cuda.is_available():
            eps = torch.cuda.FloatTensor(std.size()).normal_()
        else:
            eps = torch.FloatTensor(std.size()).normal_()
        eps = Variable(eps)
        # print("eps:",eps)
        # print("eps.size():", eps.size())
        return eps.mul(std).add_(mu)

    def decode(self, z):
        h3 = F.relu(self.fc3(z))
        # return F.sigmoid(self.fc4(h3))
        return torch.sigmoid(self.fc4(h3))

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparametrize(mu, logvar)
        return self.decode(z), mu, logvar


strattime = datetime.datetime.now()
model = VAE()
if torch.cuda.is_available():
    # model.cuda()
    print('cuda is OK!')
    model = model.to('cuda')
else:
    print('cuda is NO!')

reconstruction_function = nn.MSELoss(size_average=False)
# reconstruction_function = nn.MSELoss(reduction=sum)


def loss_function(recon_x, x, mu, logvar):
    """
    recon_x: generating images
    x: origin images
    mu: latent mean
    logvar: latent log variance
    """
    BCE = reconstruction_function(recon_x, x)  # mse loss
    # loss = 0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    KLD_element = mu.pow(2).add_(logvar.exp()).mul_(-1).add_(1).add_(logvar)
    KLD = torch.sum(KLD_element).mul_(-0.5)
    # KL divergence
    return BCE + KLD


optimizer = optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(num_epochs):
    model.train()
    train_loss = 0
    for batch_idx, data in enumerate(dataloader):
        img, _ = data
        img = img.view(img.size(0), -1)
        img = Variable(img)
        img = (img.cuda() if torch.cuda.is_available() else img)
        optimizer.zero_grad()
        recon_batch, mu, logvar = model(img)
        # break
    # break
        loss = loss_function(recon_batch, img, mu, logvar)
        loss.backward()
        # train_loss += loss.data[0]
        train_loss += loss.item()
        optimizer.step()
        if batch_idx % 100 == 0:
            endtime = datetime.datetime.now()
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f} time:{:.2f}s'.format(
                epoch,
                batch_idx * len(img),
                len(dataloader.dataset), 
                100. * batch_idx / len(dataloader),
                loss.item() / len(img), 
                (endtime-strattime).seconds))
    print('====> Epoch: {} Average loss: {:.4f}'.format(
        epoch, train_loss / len(dataloader.dataset)))
    if epoch % 10 == 0:
        save = to_img(recon_batch.cpu().data)
        save_image(save, './vae_img/image_{}.png'.format(epoch))

torch.save(model.state_dict(), './vae.pth')









model = VAE()
checkpoint = torch.load('vae.pth')
model.load_state_dict(checkpoint)
print("load checkpoint from %s", 'vae.pth')
if torch.cuda.is_available():
    device = torch.cuda.current_device()
    model = model.to(device)

z = torch.cuda.FloatTensor(torch.Size([1, 20])).normal_()
recon_batch = model.decode(z)

save = to_img(recon_batch.cpu().data)
save_image(save, './vae_img_infe/image_{}.png'.format(1))