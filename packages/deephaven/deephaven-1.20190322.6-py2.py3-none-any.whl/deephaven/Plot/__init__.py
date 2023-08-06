#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

####################################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonFigureWrapper or
# "./gradlew :Generators:generatePythonFigureWrapper" to generate
####################################################################################


import jpy
import functools
from .figure_wrapper import FigureWrapper, __convert_arguments__


__plotting_convenience__ = None  # this module will be useless with no jvm


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global __plotting_convenience__
    if __plotting_convenience__ is None:
        # an exception will be raised if not in the jvm classpath
        __plotting_convenience__ = jpy.get_type("com.illumon.iris.db.plot.PlottingConvenience")


def convertArguments(func):
    """
    For decoration of module methods, to define necessary symbols and convert arguments, as necessary

    :param func: the method to be decorated
    :return: the decorated version of the method
    """

    @functools.wraps(func)
    def wrapper(*args):
        defineSymbols()
        return func(*__convert_arguments__(args))
    return wrapper


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


def figure(*args):
    return FigureWrapper(None, *args)


def catErrorBar(*args):
    return FigureWrapper(None).catErrorBar(*args)


def catErrorBarBy(*args):
    return FigureWrapper(None).catErrorBarBy(*args)


def catHistPlot(*args):
    return FigureWrapper(None).catHistPlot(*args)


def catPlot(*args):
    return FigureWrapper(None).catPlot(*args)


def catPlot3d(*args):
    return FigureWrapper(None).catPlot3d(*args)


def catPlot3dBy(*args):
    return FigureWrapper(None).catPlot3dBy(*args)


def catPlotBy(*args):
    return FigureWrapper(None).catPlotBy(*args)


@convertArguments
def color(*args):
    return __plotting_convenience__.color(*args)


@convertArguments
def colorHSL(*args):
    return __plotting_convenience__.colorHSL(*args)


def colorNames(*args):
    return list(__plotting_convenience__.colorNames(*args))


@convertArguments
def colorRGB(*args):
    return __plotting_convenience__.colorRGB(*args)


def errorBarX(*args):
    return FigureWrapper(None).errorBarX(*args)


def errorBarXBy(*args):
    return FigureWrapper(None).errorBarXBy(*args)


def errorBarXY(*args):
    return FigureWrapper(None).errorBarXY(*args)


def errorBarXYBy(*args):
    return FigureWrapper(None).errorBarXYBy(*args)


def errorBarY(*args):
    return FigureWrapper(None).errorBarY(*args)


def errorBarYBy(*args):
    return FigureWrapper(None).errorBarYBy(*args)


@convertArguments
def font(*args):
    return __plotting_convenience__.font(*args)


def fontFamilyNames(*args):
    return list(__plotting_convenience__.fontFamilyNames(*args))


@convertArguments
def fontStyle(*args):
    return __plotting_convenience__.fontStyle(*args)


def fontStyleNames(*args):
    return list(__plotting_convenience__.fontStyleNames(*args))


def histPlot(*args):
    return FigureWrapper(None).histPlot(*args)


@convertArguments
def lineEndStyle(*args):
    return __plotting_convenience__.lineEndStyle(*args)


def lineEndStyleNames(*args):
    return list(__plotting_convenience__.lineEndStyleNames(*args))


@convertArguments
def lineJoinStyle(*args):
    return __plotting_convenience__.lineJoinStyle(*args)


def lineJoinStyleNames(*args):
    return list(__plotting_convenience__.lineJoinStyleNames(*args))


@convertArguments
def lineStyle(*args):
    return __plotting_convenience__.lineStyle(*args)


def newAxes(*args):
    return FigureWrapper(None).newAxes(*args)


def newChart(*args):
    return FigureWrapper(None).newChart(*args)


@convertArguments
def notify(*args):
    return __plotting_convenience__.notify(*args)


def ohlcPlot(*args):
    return FigureWrapper(None).ohlcPlot(*args)


def ohlcPlotBy(*args):
    return FigureWrapper(None).ohlcPlotBy(*args)


@convertArguments
def oneClick(*args):
    return __plotting_convenience__.oneClick(*args)


def piePlot(*args):
    return FigureWrapper(None).piePlot(*args)


def plot(*args):
    return FigureWrapper(None).plot(*args)


def plot3d(*args):
    return FigureWrapper(None).plot3d(*args)


def plot3dBy(*args):
    return FigureWrapper(None).plot3dBy(*args)


def plotBy(*args):
    return FigureWrapper(None).plotBy(*args)


def plotStyleNames(*args):
    return list(__plotting_convenience__.plotStyleNames(*args))


def scatterPlotMatrix(*args):
    return FigureWrapper(None).scatterPlotMatrix(*args)


def themeNames(*args):
    return list(__plotting_convenience__.themeNames(*args))


