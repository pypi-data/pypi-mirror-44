# mnist

[![Build Status](https://travis-ci.com/blester125/mnist.svg?branch=master)](https://travis-ci.com/blester125/mnist)

Download MNIST and Fashion MNIST datasets without needing to install tensorflow.

Install with `pip install get-mnist`

Download data with `from mnist import get_mnist; x, y, x_test, y_test = get_mnist('MNIST')` or use `get_fashion_mnist`. Data is downloaded and cached (in this case into the folder called `'MNIST'`).
