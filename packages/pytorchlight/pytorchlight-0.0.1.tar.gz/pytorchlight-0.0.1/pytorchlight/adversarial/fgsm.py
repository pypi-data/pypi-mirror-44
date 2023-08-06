import pytorchlight.utils.log as L
import torch

fgsm_logger = L.Log('fgsm')


class FGSM(object):
    """Fast Gradient Sign Method for adversarial examples.

    This simple and fast method of generating adversarial examples comes from 
    a view of neural networks' vulnerability to adversarial perturbation is 
    their linear nature. The view is identified by Goodfellow et. al. in 
    [Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572).
    """

    def __init__(self, **params):
        """Define FGSM.

        Generating a FGSM attacker.

        Args:
            **params (dict): a series of pairs of FGSM's parameters

        Example::

            >>> fgsm = FGSM(epsilon=0.1)

        """
        self.epsilon = params.get('epsilon', 0.0)

    def __call__(self, **input):
        """Generate adversarial examples based on `x` through FGSM.

        input -> perturbated input: $perturbed\_x = x + \epsilon*sign(x\_grad)$

        Args:
            **input (dict of tensor): A FGSM input indicates an attack object 
            which can be features of various forms such as image(s), voice(s), 
            and one-verctor number(s), and object gradient which is 
            corresponding to the object. Note that the pair of x and gradient 
            should be same shape.

        Example::

            >>> import torch
            >>> fgsm = FGSM(epsilon=0.1)
            >>> perturbed_x = fgsm(x=torch.tensor([[1, 2, 3]]),
                                   grad=torch.tensor([0.1, 0.2, 0.3]))

        Returns:
            (tensor): perturbed x. If x is image, x should be then clipped by using torch.clamp(x, min=0, max=1)
        """
        x = input.get('x', None)
        if not isinstance(x, torch.Tensor):
            fgsm_logger.error(
                'TypeError - Invalid Type of x: {}'.format(
                    type(x).__name__))
            raise TypeError(
                'TypeError - Invalid Type of x: {}'.format(
                    type(x).__name__))
        if x is None:
            fgsm_logger.error(
                'ValueError - Excepted x: {}'.format(None))
            raise ValueError(
                'ValueError - Excepted x: {}'.format(None))
        grad = input.get('grad', None)
        if not isinstance(grad, torch.Tensor):
            fgsm_logger.error(
                'TypeError - Invalid Type of grad: {}'.format(
                    type(grad).__name__))
            raise TypeError(
                'TypeError - Invalid Type of grad: {}'.format(
                    type(grad).__name__))
        if grad is None:
            fgsm_logger.error(
                'ValueError - Excepted grad: {}'.format(None))
            raise ValueError(
                'ValueError - Excepted grad: {}'.format(None))
        # Create the perturbed image by adjusting each pixel of the input image
        perturbed_x = x + self.epsilon * grad.sign()
        return perturbed_x

    def set_params(self, **params):
        """Reset parameters of Fast Gradient Sign Method (FGSM).

        Update epsilon.

        Args:
            **params (dict): FGSM's parameters, such as epsilon.

        Example::

            >>> fgsm = FGSM(epsilon=0.1)
            >>> fgsm.set_params(epsilon=0.25)

        """
        self.epsilon = params.get('epsilon', self.epsilon)

    def get_params(self):
        """Print parameters of Fast Fradient Sign Method (FGSM).

        Returns:
                (dict): {'epsilon': epsilon}
        """
        return {'epsilon': self.epsilon}


def experiment(dataloader, **params):
    """Experiment for FSGM.

    Given data and FSGM's parameters are conducted to quantify performance.

    Args:
            dataloader (DataLoader): data loader of test set
            **params (dict): FSGM's parameters

    Example::

            >>>

    """
    pass
