from abc import ABC, abstractmethod

import torch
import torch.nn as nn
import torch.optim as optim

class Task(ABC):
  def __init__(self):
    super(Task).__init__()

  # Hooks
  @abstractmethod
  def model(self, config_dict: dict) -> nn.Module:
    pass

  @abstractmethod
  def optim(self, config_dict: dict, model: nn.Module) -> optim.Optimizer:
    pass

  @abstractmethod
  def sample(self, config_dict: dict, training: bool):
    pass

  @abstractmethod
  def train_batch(self, model: nn.Module, batch, labels):
    pass

  @abstractmethod
  def test_batch(self, model: nn.Module, batch, labels):
    pass

  # Summary tools
  def summary(self, **kwargs):
    serialized = {}
    for k in kwargs:
      v = kwargs[k]
      if not torch.is_tensor(v):
        serialized[k] = v
      else:
        if len(v.shape) == 1 and v.shape[0] == 1:
          serialized[k] = v.item()
        else:
          serialized[k] = v.tolist()
    self.summary_cache.update(serialized)

  def summary_field(self, field, **kwargs):
    prefixed = {
      ('%s:%s' % (field, key)) : kwargs[key]
      for key in kwargs
    }
    self.summary_cache.update(prefixed)

  summary_reduction = {}
