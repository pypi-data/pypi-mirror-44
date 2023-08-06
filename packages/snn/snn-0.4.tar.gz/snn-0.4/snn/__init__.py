#!/usr/bin/env python
# coding: utf-8
import numpy as np

# tasks
REGRESSION = 0
CLASSIFICATION = 1


# activation functions
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def identity(x):
    return x


class Layer:
    def train(self, prev_z, task, target=np.array([]), loss=None, next_w=np.array([]), next_dL_da=np.array([]), lr=0.2):
        if next_dL_da.size == 0:  # last layer
            # dL_dz = (self.z - target) / loss  # for 'distance based' (pythagoras) loss
            dL_dz = self.z - target
            if task == REGRESSION:
                dz_da = 1
            else:  # task == CLASSIFICATION
                dz_da = self.z * (1 - self.z)
        else:
            dL_dz = next_dL_da @ next_w
            dz_da = self.z * (1 - self.z)

        # dz_da = self.z * (1 - self.z)
        self.dL_da = dL_dz * dz_da
        self.dL_dw = (np.tile(prev_z, (len(self.dL_da), 1)).T * self.dL_da).T
        self.dL_db = self.dL_da

        self.delta_w = self.dL_dw * (-lr)
        self.delta_b = self.dL_db * (-lr)

    def apply_training(self):
        self.w += self.delta_w
        self.b += self.delta_b

    def eval(self, input_list, act_f):
        a = self.w @ input_list + self.b
        self.z = act_f(a)

    def __init__(self, n_neurons, n_input) -> None:
        super().__init__()
        self.w = np.random.rand(n_neurons, n_input) * 2 - 1
        self.b = np.random.rand(n_neurons) * 2 - 1


class SNN:
    def train(self, input_list, target, lr=0.2):
        self.eval(input_list)
        # self.loss = np.sqrt(np.sum((self.layers[-1].z - target) ** 2))
        self.loss = np.sum((self.layers[-1].z - target) ** 2)

        # train each layer
        # train(self, prev_a, target?, loss?, next_w?, next_dL_dz?)
        for i in range(len(self.layers) - 1, -1, -1):
            if i == 0:
                prev_z = input_list
            else:
                prev_z = self.layers[i - 1].z

            if i == len(self.layers) - 1:
                self.layers[i].train(prev_z, self.task, target, self.loss, lr=lr)
            else:
                self.layers[i].train(prev_z, self.task, next_w=self.layers[i + 1].w,
                                     next_dL_da=self.layers[i + 1].dL_da, lr=lr)

    def apply_training(self):
        for layer in self.layers:
            layer.apply_training()

    def eval(self, input_list):
        for i, layer in enumerate(self.layers):
            if self.task == REGRESSION and i == len(self.layers) - 1:  # last layer in regression task
                act_f = identity  # sigmoid function
            else:
                act_f = sigmoid  # identity function

            if i == 0:
                layer.eval(input_list, act_f)
            else:
                layer.eval(self.layers[i - 1].z, act_f)
        return self.layers[-1].z

    def __init__(self, topology, n_input, task=REGRESSION) -> None:
        super().__init__()
        self.task = task
        self.layers = []
        self.dL_da = []
        self.dL_dw = []
        self.dL_db = []
        self.delta_w = []
        self.delta_b = []

        for i, n in enumerate(topology):
            if i == 0:
                self.layers.append(Layer(n, n_input))
            else:
                self.layers.append(Layer(n, topology[i - 1]))
