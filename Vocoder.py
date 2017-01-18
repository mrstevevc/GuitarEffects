from pyo import *
from random import random

s = Server().boot()

# First sound - dynamic spectrum.
spktrm = SfPlayer("../snds/baseballmajeur_m.aif", speed=[1,1.001], loop=True)

# Second sound - rich and stable spectrum.
excite = Noise(0.2)

# LFOs to modulated every parameters of the Vocoder object.
lf1 = Sine(freq=0.1, phase=random()).range(60, 100)
lf2 = Sine(freq=0.11, phase=random()).range(1.05, 1.5)
lf3 = Sine(freq=0.07, phase=random()).range(1, 20)
lf4 = Sine(freq=0.06, phase=random()).range(0.01, 0.99)

voc = Vocoder(spktrm, excite, freq=lf1, spread=lf2, q=lf3, slope=lf4, stages=32).out()

s.gui(locals())

