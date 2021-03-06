import numpy as np

from simple_autodiff.ops.tensor_op import TensorOp


class Add(TensorOp):
    """Element-wise addition of two tensors: t1 + t2"""
    def _forward(self, tensor_data_1, tensor_data_2):
        assert tensor_data_1.shape == tensor_data_2.shape
        return tensor_data_1 + tensor_data_2, ()

    def _backward(self, upstream_grad, _):
        return (upstream_grad, upstream_grad)


class Subtract(TensorOp):
    """Element-wise subtraction of two tensors: t1 - t2"""
    def _forward(self, tensor_data_1, tensor_data_2):
        assert tensor_data_1.shape == tensor_data_2.shape
        return tensor_data_1 - tensor_data_2, ()

    def _backward(self, upstream_grad, _):
        return (upstream_grad, -upstream_grad)


class Power(TensorOp):
    """Tensor element-wise to the power of scalar: t ** exponent"""
    def _forward(self, tensor_data, scalar_exponent=2):
        output = tensor_data ** scalar_exponent
        return output, tensor_data

    def _backward(self, upstream_grad, tensor_data, scalar_exponent=2):
        grad = scalar_exponent * tensor_data ** (scalar_exponent - 1)
        return (grad * upstream_grad,)


class Exp(TensorOp):
    """e to power of tensor, element-wise: e ** t"""
    def _forward(self, tensor_data):
        output = np.exp(tensor_data)
        return output, output

    def _backward(self, upstream_grad, output):
        return (output * upstream_grad,)


class MatMul(TensorOp):
    """Matrix multiplication of two tensors: t1 * t2"""
    def _forward(self, tensor_data_1, tensor_data_2):
        assert tensor_data_1.shape[-1] == tensor_data_2.shape[0]
        output = np.matmul(tensor_data_1, tensor_data_2)
        cache = (tensor_data_1, tensor_data_2)
        return output, cache

    def _backward(self, upstream_grad, cache):
        tensor_data_1, tensor_data_2 = cache
        tensor_1_grads = np.matmul(upstream_grad, tensor_data_2.T)
        tensor_2_grads = np.matmul(tensor_data_1.T, upstream_grad)
        return (tensor_1_grads, tensor_2_grads)


class Sum(TensorOp):
    """Sum together all elements in a tensor: sum(t)"""
    def _forward(self, tensor_data):
        return np.sum(tensor_data), tensor_data.shape

    def _backward(self, upstream_grad, tensor_shape):
        grad = np.full(tensor_shape, upstream_grad)
        return (grad,)


class Mean(TensorOp):
    """Mean over all elements in a tensor: mean(t)"""
    def _forward(self, tensor_data):
        assert tensor_data.size > 0
        tensor_shape = tensor_data.shape
        factor = 1. / float(tensor_data.size)
        output = np.sum(tensor_data) * factor
        cache = (tensor_shape, factor)
        return output, cache

    def _backward(self, upstream_grad, cache):
        tensor_shape, factor = cache
        grad = np.full(tensor_shape, upstream_grad) * factor
        return (grad,)