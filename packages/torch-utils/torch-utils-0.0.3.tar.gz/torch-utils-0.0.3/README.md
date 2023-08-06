# torch-utils [![Build Status](https://travis-ci.com/FebruaryBreeze/torch-utils.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/torch-utils) [![codecov](https://codecov.io/gh/FebruaryBreeze/torch-utils/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/torch-utils) [![PyPI version](https://badge.fury.io/py/torch-utils.svg)](https://pypi.org/project/torch-utils/)

Group PyTorch Parameters according to Rules.

## Installation

Need Python 3.6+.

```bash
pip install torch-utils
```

## Usage

1. Accuracy

```python
import torch_utils

# ...

top_1, top_5 = torch_utils.accuracy(output=..., target=..., top_k=(1, 5))
```

2. Meter

```python
import torch_utils

loss_meter = torch_utils.AverageMeter(length=10)
loss_meter.update(val=...)

print(loss_meter.avg, loss_meter.val)
```
