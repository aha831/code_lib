# pytorch-lightning-tutorial
Pytorch lightning tutorial using MNIST

[Youtube stream](https://www.youtube.com/watch?v=O7dNXpgdWbo&ab_channel=AI%E8%91%B5)
(Maybe there will be another... still planning!)

[Pytorch lightning introduction](https://github.com/PyTorchLightning/pytorch-lightning)

[scheduler introduction (Japanese)](https://katsura-jp.hatenablog.com/entry/2019/01/30/183501)

# Installation

Python>=3.7, creation using anaconda is recommended. Install libraries by `pip install -r requirements.txt`.

# Train MNIST

Run (example)
```python3
python train.py --root_dir "./"
```

It will download the dataset to `root_dir` and start training. You can monitor the training process by launching tensorboard in another terminal:
```python3
tensorboard --logdir logs
```

And go to `localhost:6006` in your browser.



# pytorch-cppcuda-tutorial
tutorial for writing custom pytorch cpp+cuda kernel, applied on volume rendering (NeRF)

tutorial playlist: https://www.youtube.com/watch?v=l_Rpk6CRJYI&list=PLDV2CyUo4q-LKuiNltBqCKdO9GH4SS_ec&ab_channel=AI%E8%91%B5


CUDA explanation in video 2: https://nyu-cds.github.io/python-gpu/02-cuda/

C++ API in video 3: https://pytorch.org/cppdocs/

kernel launching: https://pytorch.org/tutorials/advanced/cpp_extension.html