import json
from pathlib import Path

import jsonschema
import torch
import torch.nn as nn
import torch.nn.functional as functional
import torch_model_loader

from .configs import CrossEntropyLossConfig
from .configs import L2LossConfig
from .configs import LabelSmoothingLossConfig


@torch_model_loader.register
class CrossEntropyLoss(nn.CrossEntropyLoss):
    with open(str(Path(__file__).parent / 'schema' / 'cross_entropy_loss_config.json')) as f:
        schema = json.load(f)

    def __init__(self, config: CrossEntropyLossConfig = None):
        super().__init__()

    @classmethod
    def factory(cls, config: dict = None):
        jsonschema.validate(config or {}, cls.schema)
        return cls(config=CrossEntropyLossConfig(config))


@torch_model_loader.register
class LabelSmoothingLoss(nn.Module):
    with open(str(Path(__file__).parent / 'schema' / 'label_smoothing_loss_config.json')) as f:
        schema = json.load(f)

    def __init__(self, config: LabelSmoothingLossConfig):
        super().__init__()
        self.smooth_ratio = config.smooth_ratio

    def forward(self, predict: torch.Tensor, target: torch.Tensor):
        num_classes = predict.size(1)
        positive = 1.0 - self.smooth_ratio
        negative = self.smooth_ratio / (num_classes - 1)

        one_hot = torch.zeros_like(predict).scatter(1, target.long().view((-1, 1)), 1)
        soft_target = one_hot * positive + (1.0 - one_hot) * negative
        return (functional.log_softmax(predict, dim=1) * soft_target).sum(dim=1).mean(dim=0).neg()

    @classmethod
    def factory(cls, config: dict = None):
        jsonschema.validate(config or {}, cls.schema)
        return cls(config=LabelSmoothingLossConfig(values=config))


@torch_model_loader.register
class L2Loss(nn.Module):
    with open(str(Path(__file__).parent / 'schema' / 'l2_loss_config.json')) as f:
        schema = json.load(f)

    def __init__(self, config: L2LossConfig = None):
        super().__init__()

    def forward(self, predict: torch.Tensor, target: torch.Tensor):
        return predict.sub(target).pow(2).sum(1).mean(0).div(2)

    @classmethod
    def factory(cls, config: dict = None):
        jsonschema.validate(config or {}, cls.schema)
        return cls(config=L2LossConfig(config))
