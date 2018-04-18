# Safe Option-Critic: Learning Safety in Option-Critic Architecture

This repo contains code accompanying the paper, [Safe Option-Critic: Learning Safety](https://github.com/kkhetarpal/safe_a2oc_delib) in the Option-Critic Architecture. 

For experiments in the grid-world and cartpole, see this [codebase](https://github.com/arushi12130/LearningSafeOptions).

## Dependencies

Here's a list of all dependencies:

- Numpy
- Theano
- Lasagne
- Argparse
- OpenAI Gym [Atari]
- matplotlib
- PIL (Image)

## Training

To train, run following command:
```
python train.py --sub-env Breakout --num-options 8 --num-threads 16 --folder-name Breakout_model
```
or, you might need to run:
```
THEANO_FLAGS=floatX=float32 python2.7 train.py --sub-env Breakout --num-options 8 --num-threads 16 --folder-name Breakout_model
```


To view a list of available parameters, run:
```
print train.py --help
```

During training, you can run utils/plot.py to view the training curve. Every argument given can be a path to a different run, which will put all runs on the same plot.
```
python utils/plot.py models/Breakout_model/ models/Breakout_model_v2/ models/Breakout_model_v3/
```
or, you might need to run:
```
THEANO_FLAGS=floatX=float32 python2.7 utils/plot.py models/Breakout_model_v1/ models/Montezuma_model/
```

For training with different hyperparameters than the default settings, Here is an example of setting controllability true with a parameter 4.0
```
THEANO_FLAGS=floatX=float32 python2.7 train.py --sub-env Seaquest --num-options 8 --num-threads 16 --folder-name  Seaquest_model_C0.5 --controllability True --beta 4.0
```

Here is an example of how to train with different delib cost, margin cost, etc:
```
THEANO_FLAGS=floatX=float32 python2.7 train.py --sub-env Seaquest --num-options 8 --delib-cost 0.020 --margin-cost 0.99 --num-threads 16 --folder-name  Seaquest_model_NC_D0.02_M0.99
```

## Testing

To watch model after training, run watch.py and give it the path the saved model files. e.g.:
```
python watch.py models/Breakout_model/
```
or you might need to run:
```
THEANO_FLAGS=floatX=float32 python2.7 watch.py models/Montezuma_model/
```

## Plot Learning curves

To plot multiple training curves during or after training, you could run:
```
python2.7 utils/plot.py pathto/models/MsPacman_DC0.02_MC0.99_C0.15_OPT4_EPS0.2 pathto/models/MsPacman_DC0.02_MC0.99_C0_OPT4_EPS0.2/ pathto/models/MsPacman_DC0.02_MC0.99_C0.5_OPT4_EPS0.2/ pathto/models/MsPacman_DC0.02_MC0.99_C2.0_OPT4_EPS0.2/
```

## 
