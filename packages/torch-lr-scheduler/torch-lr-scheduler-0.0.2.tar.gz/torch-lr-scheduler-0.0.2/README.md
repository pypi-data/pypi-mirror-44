# torch-lr-scheduler [![Build Status](https://travis-ci.com/FebruaryBreeze/torch-lr-scheduler.svg?branch=master)](https://travis-ci.com/FebruaryBreeze/torch-lr-scheduler) [![codecov](https://codecov.io/gh/FebruaryBreeze/torch-lr-scheduler/branch/master/graph/badge.svg)](https://codecov.io/gh/FebruaryBreeze/torch-lr-scheduler) [![PyPI version](https://badge.fury.io/py/torch-lr-scheduler.svg)](https://pypi.org/project/torch-lr-scheduler/)

PyTorch Optimizer Lr Scheduler.

## Installation

Need Python 3.6+.

```bash
pip install torch-lr-scheduler
```

## Usage

```python
import torch_lr_scheduler


lr_scheduler = torch_lr_scheduler.LrScheduler.factory(config={
    'total_steps': 100,
    'initial_lr': 0.2,
    'scheduler_list': [{
        # warm up to 0.8
        'lr_mode': 'linear',
        'milestone': 0.01,
        'target_lr': 0.8
    }, {
        # cos to 0.0
        'lr_mode': 'cos',
        'milestone': 1.0,
        'target_lr': 0.0
    }]
})

print(lr_scheduler)
#> LrScheduler (
#>     0.0%, fixed to 0.2,
#>     1.0%, linear to 0.8,
#>   100.0%, cos to 0.0,
#> )
```
