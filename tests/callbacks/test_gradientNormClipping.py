from unittest import TestCase
from unittest.mock import patch, Mock

from bink.callbacks import GradientNormClipping
import torch.nn as nn


class TestGradientNormClipping(TestCase):
    @patch('torch.nn.utils.clip_grad_norm_')
    def test_not_given_params(self, mock_clip):
        model = nn.Sequential(nn.Conv2d(3, 3, 3))
        model.parameters = Mock(return_value=-1)
        state = {'model': model}

        clipper = GradientNormClipping(5)

        clipper.on_start(state)
        clipper.on_backward(state)

        self.assertTrue(mock_clip.mock_calls[0][1][0] == -1)

    @patch('torch.nn.utils.clip_grad_norm_')
    def test_given_params(self, mock_clip):
        model = nn.Sequential(nn.Conv2d(3, 3, 3))
        model.parameters = Mock(return_value=-1)
        state = {'model': model}

        clipper = GradientNormClipping(5, params=model.parameters())

        clipper.on_start(state)
        clipper.on_backward(state)

        self.assertTrue(mock_clip.mock_calls[0][1][0] == -1)

    @patch('torch.nn.utils.clip_grad_norm_')
    def test_passed_norm(self, mock_clip):
        model = nn.Sequential(nn.Conv2d(3, 3, 3))
        model.parameters = Mock(return_value=-1)
        state = {'model': model}

        clipper = GradientNormClipping(5, 2, params=model.parameters())

        clipper.on_start(state)
        clipper.on_backward(state)

        self.assertTrue(mock_clip.mock_calls[0][1][1] == 5)
        self.assertTrue(mock_clip.mock_calls[0][2]['norm_type'] == 2)

    @patch('torch.nn.utils.clip_grad_norm_')
    def test_default_norm_type(self, mock_clip):
        model = nn.Sequential(nn.Conv2d(3, 3, 3))
        model.parameters = Mock(return_value=-1)
        state = {'model': model}

        clipper = GradientNormClipping(5, params=model.parameters())

        clipper.on_start(state)
        clipper.on_backward(state)

        self.assertTrue(mock_clip.mock_calls[0][1][1] == 5)
        self.assertTrue(mock_clip.mock_calls[0][2]['norm_type'] == 2)