# torch-parameter-groups [![Build Status](https://travis-ci.com/FebruaryBreeze/torch-parameter-groups.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/torch-parameter-groups) [![codecov](https://codecov.io/gh/FebruaryBreeze/torch-parameter-groups/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/torch-parameter-groups) [![PyPI version](https://badge.fury.io/py/torch-parameter-groups.svg)](https://pypi.org/project/torch-parameter-groups/)

Group PyTorch Parameters according to Rules.

## Installation

Need Python 3.6+.

```bash
pip install torch-parameter-groups
```

## Usage

```python
import torch
import torch_basic_models
import torch_parameter_groups


model = torch_basic_models.MobileNetV2.factory()
optimizer = torch_parameter_groups.OptimizerWrapper.factory(
    model=model,
    config={
        'type': 'SGD',
        'momentum': 0.9,
        'nesterov': True,
        'weight_decay': 0.0001,
        'rules': [
            {
                'param_name_list': ['weight'],
                'weight_decay': 0
            },
            {
            }
        ]
    },
)

criterion = torch.nn.CrossEntropyLoss()
output = model(torch.randn(1, 3, 224, 224))
loss = criterion(output, torch.Tensor([0]).long())
loss.backward()
optimizer.step()
```
