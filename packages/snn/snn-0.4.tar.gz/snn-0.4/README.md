# simple-neural-network

Simple neural network for solving problems of classification and regression.

## Installation

The module can be installed via the [pip](https://pip.pypa.io/en/stable/) package manager.


```bash
$ pip install snn
```

## Usage

```python
from snn import SNN


# CREATE A NEURAL NETWORK INSTANCE
# topology: List of integers representing the number of neurons in each layer.
#           The last element is for the output layer.
# n_input : The number of the input variables.
# task    : 0 for regression, 1 for classification
nn = SNN(topology=[3, 4, 5, 6, 4], n_input = 2, task=0)


# TRAIN THE NEURAL NETWORK
for i in range(1000):
    # input_list: list of floating point numbers representing each input variable.
    #             The number of elements must be the same as the n_input parameter used to create the network.
    # target    : The training target for the current input_list taken from the set of data.
    #             The number of elements must be the same as the number of elements in the last layer
    #             (i.e. the last element of the topology parameter used to create the network).
    # lr        : The learning rate. The factor that multiplies the derivative of the loss value with respect
    #             to each coefficient (w) of the network to get the deltas of the w coefficients.
    nn.train(input_list=[2.45, 4.67], target=[1.345, 3.45, -5.34, 8.54], lr=0.3)
    
    # The deltas are not applied (added) until this function is called. Call this after each call to SNN.train().
    nn.apply_training()


# EVAL SOME INPUT
# input_list: list of input variables to be evaluated by the network. The number of elements must be the same
#             as the the n_input param used to create the network.
output = nn.eval(input_list=[3.55, 2.73])
print(output)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[BSD 2-Clause](https://raw.githubusercontent.com/hpc0/simple-neural-network/master/LICENSE)