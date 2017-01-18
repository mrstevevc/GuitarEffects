
from pyo import *

class Flanger(PyoObject):
    """
    Flanging effect.

    A flanging is an audio effect produced by mixing two identical signals together,
    with one signal delayed by a small and gradually changing period, usually smaller
    than 20 milliseconds. This produces a swept comb filter effect: peaks and notches
    are produced in the resultant frequency spectrum, related to each other in a linear
    harmonic series. Varying the time delay causes these to sweep up and down the
    frequency spectrum.


    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        depth : float or PyoObject, optional
            Amplitude of the delay line modulation, between 0 and 1.
            Defaults to 0.75.
        lfofreq : float or PyoObject, optional
            Frequency of the delay line modulation, in Hertz.
            Defaults to 0.2.
        feedback : float or PyoObject, optional
            Amount of output signal reinjected into the delay line.
            Defaults to 0.25.

    >>> s = Server().boot()
    >>> s.start()
    >>> inp = SfPlayer(SNDS_PATH + "/transparent.aif", loop=True)
    >>> lf = Sine(0.005, mul=0.25, add=0.5)
    >>> flg = Flanger(input=inp, depth=0.9, lfofreq=0.1, feedback=lf).out()

    """
    def __init__(self, input, depth=0.75, lfofreq=0.2, feedback=0.5, mul=1, add=0):
        PyoObject.__init__(self)
        self._input = input
        self._depth = depth
        self._lfofreq = lfofreq
        self._feedback = feedback
        self._in_fader = InputFader(input)
        in_fader, depth, lfofreq, feedback, mul, add, lmax = convertArgsToLists(
                                self._in_fader, depth, lfofreq, feedback, mul, add)

        self._modamp = Sig(depth, mul=0.005)
        self._mod = Sine(freq=lfofreq, mul=self._modamp, add=0.005)
        self._dls = Delay(in_fader, delay=self._mod, feedback=feedback)
        self._flange = Interp(in_fader, self._dls, mul=mul, add=add)

        self._base_objs = self._flange.getBaseObjects()

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.

        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setDepth(self, x):
        """
        Replace the `depth` attribute.

        :Args:

            x : float or PyoObject
                New `depth` attribute.

        """
        self._depth = x
        self._modamp.value = x

    def setLfoFreq(self, x):
        """
        Replace the `lfofreq` attribute.

        :Args:

            x : float or PyoObject
                New `lfofreq` attribute.

        """
        self._lfofreq = x
        self._mod.freq = x

    def setFeedback(self, x):
        """
        Replace the `feedback` attribute.

        :Args:

            x : float or PyoObject
                New `feedback` attribute.

        """
        self._feedback = x
        self._dls.feedback = x

    def play(self, dur=0, delay=0):
        self._modamp.play(dur, delay)
        self._mod.play(dur, delay)
        self._dls.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self):
        self._modamp.stop()
        self._mod.stop()
        self._dls.stop()
        return PyoObject.stop(self)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self._modamp.play(dur, delay)
        self._mod.play(dur, delay)
        self._dls.play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0., 1., "lin", "depth", self._depth),
                          SLMap(0.001, 20., "log", "lfofreq", self._lfofreq),
                          SLMap(0., 1., "lin", "feedback", self._feedback),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to process."""
        return self._input
    @input.setter
    def input(self, x):
        self.setInput(x)

    @property
    def depth(self):
        """float or PyoObject. Amplitude of the delay line modulation."""
        return self._depth
    @depth.setter
    def depth(self, x):
        self.setDepth(x)

    @property
    def lfofreq(self):
        """float or PyoObject. Frequency of the delay line modulation."""
        return self._lfofreq
    @lfofreq.setter
    def lfofreq(self, x):
        self.setLfoFreq(x)

    @property
    def feedback(self):
        """float or PyoObject. Amount of out sig sent back in delay line."""
        return self._feedback
    @feedback.setter
    def feedback(self, x):
        self.setFeedback(x)

# Run the script to test the Flanger object.
if __name__ == "__main__":
    s = Server().boot()
    src = BrownNoise([.2,.2]).out()
    fl = Flanger(src, depth=.9, lfofreq=.1, feedback=.5, mul=.5).out()
    s.gui(locals())
