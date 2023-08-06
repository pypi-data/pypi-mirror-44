<h1 align="center">DLCreator</h1>
<p align="center">One-line command to generate a deep learning folder structure and code template！</p>

<p align="center">
  <a href="https://github.com/nghuyong/DLCreator/stargazers">
    <img src="https://img.shields.io/github/stars/nghuyong/DLCreator.svg?colorA=orange&colorB=orange&logo=github"
         alt="GitHub stars">
  </a>
  <a href="https://github.com/nghuyong/DLCreator/issues">
        <img src="https://img.shields.io/github/issues/nghuyong/DLCreator.svg"
             alt="GitHub issues">
  </a>
  <a href="https://github.com/nghuyong/DLCreator/">
        <img src="https://img.shields.io/github/last-commit/nghuyong/DLCreator.svg">
  </a>
  <a href="https://github.com/nghuyong/DLCreator/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/nghuyong/DLCreator.svg"
             alt="GitHub license">
  </a>
</p>


<h2 align="center">What is it</h2>
When you start a new deep learning project, are you still worrying about how to organize a project structure and writing many duplicate codes every time ?

**DLCreator** is made ! It is a one-line command tool, which will automatically generate the entire folder structure and code template including data loading; model training; configuration; logs; visualization; etc.
**So, All YOU NEED TO DO is just design your model and write some code snippet**.

<h2 align="center">Install</h2>

Install it via `pip`.

```bash
pip install DLCreator
```

:point_up: The command can be running on both Python 2 and 3.


<h2 align="center">Getting Started</h2>
Start a new deep learning project, just from this:

```bash
DLCreator <tensorflow|pytorch|keras> <project-name>
```
Take `DLCreator pytorch test` as an example, The same directory will generate a `test` directory, the structure is as follows:
```
  test/
  │
  ├── train.py - main script to start training
  ├── test.py - evaluation of trained model
  ├── config.json - config file
  │
  ├── base/ - abstract base classes
  │   ├── base_data_loader.py - abstract base class for data loaders
  │   ├── base_model.py - abstract base class for models
  │   └── base_trainer.py - abstract base class for trainers
  │
  ├── data_loader/ - anything about data loading goes here
  │   └── data_loaders.py
  │
  ├── data/ - default directory for storing input data
  │
  ├── model/ - models, losses, and metrics
  │   ├── loss.py
  │   ├── metric.py
  │   └── model.py
  │
  ├── saved/ - default checkpoints folder
  │   └── runs/ - default logdir for tensorboardX
  │
  ├── trainer/ - trainers
  │   └── trainer.py
  │
  └── utils/
      ├── util.py
      ├── logger.py - class for train logging
      ├── visualization.py - class for tensorboardX visualization support
      └── ...
  ```


<h2 align="center">TODOs</h2>

- [ ] Support tensorflow
- [ ] Support pytorch
- [ ] Support keras
- [ ] Release a version to pypi


<h2 align="center">Acknowledgments</h2>
This project is inspired these projects:

- [Tensorflow-Project-Template](https://github.com/MrGemy95/Tensorflow-Project-Template)
- [pytorch-template](https://github.com/victoresque/pytorch-template)
- [Keras-Project-Template](https://github.com/Ahmkel/Keras-Project-Template)


