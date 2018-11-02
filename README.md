# visdom_logger
A thin wrapper to use visdom as logger when training ML models

# Usage

Start a visdom server:

```bash
python -m visdom.server -port 8097 
```

In your training code, use the visdom_logger to monitor the training progress:

```python
import numpy as np
from visdom_logger.logger import VisdomLogger

# Initialize the logger with the same port visdom is running
logger = VisdomLogger(port=8097)
    
for i in range(100): # Training iterations
    loss = 100 - i   # This is the loss we want to monitor
    
    # Log the current loss:
    logger.scalar('loss', i, loss) # This will update the visdom plot immediately
   
    acc = i 
    
    # You can plot two scalars in the same plot:
    logger.scalars(['loss', 'acc'], i, [loss, acc])
    
# Also display images
imgs = np.random.random((10, 3, 25, 25)) # 10 images of size 25x25x3
logger.images('images', imgs)

# Lastly, you can also save all plots to a file
logger.save('my_plots.pth')
```

The code above will create the following plots in visdom:

![example](https://i.imgur.com/m1WP3qg.png)

You can re-load saved plots as follows:

```
python -m visdom_logger.load my_plots.pth -port 8097 
```
