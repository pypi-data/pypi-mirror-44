#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

######################################################################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonFigureWrapper or "./gradlew :Generators:generatePythonFigureWrapper" to generate
######################################################################################################################


import sys
import logging
import jpy
import numpy
import pandas
import functools

from ..conversion_utils import _isJavaType, _isStr, makeJavaArray, _ensureBoxedArray


__plotting_convenience__ = None  # this module will be useless with no jvm
__figure_widget__ = None


def defineSymbols():
    """
    Defines appropriate java symbols, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global __plotting_convenience__, __figure_widget__
    if __plotting_convenience__ is None:
        # an exception will be raised if not in the jvm classpath
        __plotting_convenience__ = jpy.get_type("com.illumon.iris.db.plot.PlottingConvenience")
        __figure_widget__ = jpy.get_type('com.illumon.iris.db.plot.FigureWidget')


if sys.version_info[0] > 2:
    def __is_basic_type__(obj):
        return isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str)
else:
    def __is_basic_type__(obj):
        return isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, long) \
               or isinstance(obj, float) or isinstance(obj, basestring)


def __is_widget__(obj):
    if obj is None:
        return False
    return type(obj).__name__ == 'FigureWidget'


def __create_java_object__(obj):
    if obj is None:
        return None
    elif isinstance(obj, FigureWrapper) or __is_widget__(obj) or _isJavaType(obj):
        # nothing to be done
        return obj
    elif __is_basic_type__(obj):
        # jpy will (*should*) convert this properly
        return obj
    elif isinstance(obj, numpy.ndarray) or isinstance(obj, pandas.Series) or isinstance(obj, pandas.Categorical):
        return makeJavaArray(obj, 'unknown', False)
    elif isinstance(obj, dict):
        return obj  # what would we do?
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return __create_java_object__(numpy.array(obj))  # maybe it's better to pass it straight through?
    elif hasattr(obj, '__iter__'):
        # return __create_java_object__(numpy.array(list(obj))) # this is suspect
        return obj
    else:
        # I have no idea what it is - just pass it straight through
        return obj


def __convert_arguments__(args):
    return [__create_java_object__(el) for el in args]


def convertArguments(func):
    """
    For decoration of FigureWrapper class methods, to convert arguments as necessary

    :param func: the method to be decorated
    :return: the decorated version of the method
    """

    @functools.wraps(func)
    def wrapper(*args):
        return func(*__convert_arguments__(args))
    return wrapper


def convertCatPlotArguments(func):
    """
    For decoration of FigureWrapper catPlot, catErrorBar, piePlot method, to convert arguments

    :param func: the method to be decorated
    :return: the decorated version of the method
    """

    @functools.wraps(func)
    def wrapper(*args):
        cargs = __convert_arguments__(args)
        cargs[2] = _ensureBoxedArray(cargs[2])
        return func(*cargs)
    return wrapper


def convertCatPlot3dArguments(func):
    """
    For decoration of FigureWrapper catPlot3d method, to convert arguments as necessary

    :param func: the method to be decorated
    :return: the decorated version of the method
    """

    @functools.wraps(func)
    def wrapper(*args):
        cargs = __convert_arguments__(args)
        cargs[2] = _ensureBoxedArray(cargs[2])
        cargs[3] = _ensureBoxedArray(cargs[3])
        return func(*cargs)
    return wrapper


class FigureWrapper(object):
    """
    Class which assembles a variety of plotting convenience methods into a single usable package
    """

    def __init__(self, figure, *args):
        defineSymbols()
        if figure is None:
            self.figure_ = __plotting_convenience__.figure(*__convert_arguments__(args))
        else:
            self.figure_ = figure
        self.valid_groups = None

    def show(self):
        """
        Wraps the figure in a figure widget for display
        :return: FigureWrapper with figure attribute set to applicable widget
        """

        figure = __figure_widget__(self.figure_)
        return FigureWrapper(figure)

    def getWidget(self):
        """
        Get figure widget, if applicable. This should only return a value if .show() has been called.
        :return: None or the widget reference
        """

        if __is_widget__(self.figure_):
            return self.figure_
        return None

    def getValidGroups(self):
        """
        Get the list of valid users
        :return: java array of user id strings
        """
        return __create_java_object__(self.valid_groups)

    def setValidGroups(self, groups):
        """
        Set the list of user ids which should have access to this figure wrapper object
        :param groups: None, single user id string, or list of user id strings
        """

        if groups is None:
            self.valid_groups = None
        elif _isStr(groups):
            self.valid_groups = [groups, ]
        else:
            try:
                self.valid_groups = list(groups)  # any other iterable will become a list
            except Exception as e:
                logging.error("Failed to set valid groups using input {} with exception {}".format(groups, e))

    @convertArguments
    def axes(self, *args):
        return FigureWrapper(self.figure_.axes(*args))

    @convertArguments
    def axesRemoveSeries(self, *args):
        return FigureWrapper(self.figure_.axesRemoveSeries(*args))

    @convertArguments
    def axis(self, *args):
        return FigureWrapper(self.figure_.axis(*args))

    @convertArguments
    def axisColor(self, *args):
        return FigureWrapper(self.figure_.axisColor(*args))

    @convertArguments
    def axisFormat(self, *args):
        return FigureWrapper(self.figure_.axisFormat(*args))

    @convertArguments
    def axisFormatPattern(self, *args):
        return FigureWrapper(self.figure_.axisFormatPattern(*args))

    @convertArguments
    def axisLabel(self, *args):
        return FigureWrapper(self.figure_.axisLabel(*args))

    @convertArguments
    def axisLabelFont(self, *args):
        return FigureWrapper(self.figure_.axisLabelFont(*args))

    @convertArguments
    def businessTime(self, *args):
        return FigureWrapper(self.figure_.businessTime(*args))

    @convertCatPlotArguments
    def catErrorBar(self, *args):
        return FigureWrapper(self.figure_.catErrorBar(*args))

    @convertArguments
    def catErrorBarBy(self, *args):
        return FigureWrapper(self.figure_.catErrorBarBy(*args))

    @convertArguments
    def catHistPlot(self, *args):
        return FigureWrapper(self.figure_.catHistPlot(*args))

    @convertCatPlotArguments
    def catPlot(self, *args):
        return FigureWrapper(self.figure_.catPlot(*args))

    @convertCatPlot3dArguments
    def catPlot3d(self, *args):
        return FigureWrapper(self.figure_.catPlot3d(*args))

    @convertArguments
    def catPlot3dBy(self, *args):
        return FigureWrapper(self.figure_.catPlot3dBy(*args))

    @convertArguments
    def catPlotBy(self, *args):
        return FigureWrapper(self.figure_.catPlotBy(*args))

    @convertArguments
    def chart(self, *args):
        return FigureWrapper(self.figure_.chart(*args))

    @convertArguments
    def chartRemoveSeries(self, *args):
        return FigureWrapper(self.figure_.chartRemoveSeries(*args))

    @convertArguments
    def chartTitle(self, *args):
        return FigureWrapper(self.figure_.chartTitle(*args))

    @convertArguments
    def chartTitleColor(self, *args):
        return FigureWrapper(self.figure_.chartTitleColor(*args))

    @convertArguments
    def chartTitleFont(self, *args):
        return FigureWrapper(self.figure_.chartTitleFont(*args))

    @convertArguments
    def colSpan(self, *args):
        return FigureWrapper(self.figure_.colSpan(*args))

    @convertArguments
    def errorBarX(self, *args):
        return FigureWrapper(self.figure_.errorBarX(*args))

    @convertArguments
    def errorBarXBy(self, *args):
        return FigureWrapper(self.figure_.errorBarXBy(*args))

    @convertArguments
    def errorBarXY(self, *args):
        return FigureWrapper(self.figure_.errorBarXY(*args))

    @convertArguments
    def errorBarXYBy(self, *args):
        return FigureWrapper(self.figure_.errorBarXYBy(*args))

    @convertArguments
    def errorBarY(self, *args):
        return FigureWrapper(self.figure_.errorBarY(*args))

    @convertArguments
    def errorBarYBy(self, *args):
        return FigureWrapper(self.figure_.errorBarYBy(*args))

    @convertArguments
    def figureRemoveSeries(self, *args):
        return FigureWrapper(self.figure_.figureRemoveSeries(*args))

    @convertArguments
    def figureTitle(self, *args):
        return FigureWrapper(self.figure_.figureTitle(*args))

    @convertArguments
    def figureTitleColor(self, *args):
        return FigureWrapper(self.figure_.figureTitleColor(*args))

    @convertArguments
    def figureTitleFont(self, *args):
        return FigureWrapper(self.figure_.figureTitleFont(*args))

    @convertArguments
    def funcNPoints(self, *args):
        return FigureWrapper(self.figure_.funcNPoints(*args))

    @convertArguments
    def funcRange(self, *args):
        return FigureWrapper(self.figure_.funcRange(*args))

    @convertArguments
    def gradientVisible(self, *args):
        return FigureWrapper(self.figure_.gradientVisible(*args))

    @convertArguments
    def group(self, *args):
        return FigureWrapper(self.figure_.group(*args))

    @convertArguments
    def histPlot(self, *args):
        return FigureWrapper(self.figure_.histPlot(*args))

    @convertArguments
    def invert(self, *args):
        return FigureWrapper(self.figure_.invert(*args))

    @convertArguments
    def legendColor(self, *args):
        return FigureWrapper(self.figure_.legendColor(*args))

    @convertArguments
    def legendFont(self, *args):
        return FigureWrapper(self.figure_.legendFont(*args))

    @convertArguments
    def legendVisible(self, *args):
        return FigureWrapper(self.figure_.legendVisible(*args))

    @convertArguments
    def lineColor(self, *args):
        return FigureWrapper(self.figure_.lineColor(*args))

    @convertArguments
    def lineStyle(self, *args):
        return FigureWrapper(self.figure_.lineStyle(*args))

    @convertArguments
    def linesVisible(self, *args):
        return FigureWrapper(self.figure_.linesVisible(*args))

    @convertArguments
    def log(self, *args):
        return FigureWrapper(self.figure_.log(*args))

    @convertArguments
    def max(self, *args):
        return FigureWrapper(self.figure_.max(*args))

    @convertArguments
    def min(self, *args):
        return FigureWrapper(self.figure_.min(*args))

    @convertArguments
    def minorTicks(self, *args):
        return FigureWrapper(self.figure_.minorTicks(*args))

    @convertArguments
    def minorTicksVisible(self, *args):
        return FigureWrapper(self.figure_.minorTicksVisible(*args))

    @convertArguments
    def newAxes(self, *args):
        return FigureWrapper(self.figure_.newAxes(*args))

    @convertArguments
    def newChart(self, *args):
        return FigureWrapper(self.figure_.newChart(*args))

    @convertArguments
    def ohlcPlot(self, *args):
        return FigureWrapper(self.figure_.ohlcPlot(*args))

    @convertArguments
    def ohlcPlotBy(self, *args):
        return FigureWrapper(self.figure_.ohlcPlotBy(*args))

    @convertCatPlotArguments
    def piePlot(self, *args):
        return FigureWrapper(self.figure_.piePlot(*args))

    @convertArguments
    def plot(self, *args):
        return FigureWrapper(self.figure_.plot(*args))

    @convertArguments
    def plot3d(self, *args):
        return FigureWrapper(self.figure_.plot3d(*args))

    @convertArguments
    def plot3dBy(self, *args):
        return FigureWrapper(self.figure_.plot3dBy(*args))

    @convertArguments
    def plotBy(self, *args):
        return FigureWrapper(self.figure_.plotBy(*args))

    @convertArguments
    def plotOrientation(self, *args):
        return FigureWrapper(self.figure_.plotOrientation(*args))

    @convertArguments
    def plotStyle(self, *args):
        return FigureWrapper(self.figure_.plotStyle(*args))

    @convertArguments
    def pointColor(self, *args):
        return FigureWrapper(self.figure_.pointColor(*args))

    @convertArguments
    def pointColorByY(self, *args):
        return FigureWrapper(self.figure_.pointColorByY(*args))

    @convertArguments
    def pointColorInteger(self, *args):
        return FigureWrapper(self.figure_.pointColorInteger(*args))

    @convertArguments
    def pointLabel(self, *args):
        return FigureWrapper(self.figure_.pointLabel(*args))

    @convertArguments
    def pointLabelFormat(self, *args):
        return FigureWrapper(self.figure_.pointLabelFormat(*args))

    @convertArguments
    def pointShape(self, *args):
        return FigureWrapper(self.figure_.pointShape(*args))

    @convertArguments
    def pointSize(self, *args):
        return FigureWrapper(self.figure_.pointSize(*args))

    @convertArguments
    def pointsVisible(self, *args):
        return FigureWrapper(self.figure_.pointsVisible(*args))

    @convertArguments
    def range(self, *args):
        return FigureWrapper(self.figure_.range(*args))

    @convertArguments
    def removeChart(self, *args):
        return FigureWrapper(self.figure_.removeChart(*args))

    @convertArguments
    def rowSpan(self, *args):
        return FigureWrapper(self.figure_.rowSpan(*args))

    @convertArguments
    def save(self, *args):
        return FigureWrapper(self.figure_.save(*args))

    @convertArguments
    def series(self, *args):
        return FigureWrapper(self.figure_.series(*args))

    @convertArguments
    def seriesColor(self, *args):
        return FigureWrapper(self.figure_.seriesColor(*args))

    @convertArguments
    def seriesNamingFunction(self, *args):
        return FigureWrapper(self.figure_.seriesNamingFunction(*args))

    @convertArguments
    def span(self, *args):
        return FigureWrapper(self.figure_.span(*args))

    @convertArguments
    def theme(self, *args):
        return FigureWrapper(self.figure_.theme(*args))

    @convertArguments
    def tickLabelAngle(self, *args):
        return FigureWrapper(self.figure_.tickLabelAngle(*args))

    @convertArguments
    def ticks(self, *args):
        return FigureWrapper(self.figure_.ticks(*args))

    @convertArguments
    def ticksFont(self, *args):
        return FigureWrapper(self.figure_.ticksFont(*args))

    @convertArguments
    def ticksVisible(self, *args):
        return FigureWrapper(self.figure_.ticksVisible(*args))

    @convertArguments
    def toolTipPattern(self, *args):
        return FigureWrapper(self.figure_.toolTipPattern(*args))

    @convertArguments
    def transform(self, *args):
        return FigureWrapper(self.figure_.transform(*args))

    @convertArguments
    def twin(self, *args):
        return FigureWrapper(self.figure_.twin(*args))

    @convertArguments
    def twinX(self, *args):
        return FigureWrapper(self.figure_.twinX(*args))

    @convertArguments
    def twinY(self, *args):
        return FigureWrapper(self.figure_.twinY(*args))

    @convertArguments
    def twinZ(self, *args):
        return FigureWrapper(self.figure_.twinZ(*args))

    @convertArguments
    def updateInterval(self, *args):
        return FigureWrapper(self.figure_.updateInterval(*args))

    @convertArguments
    def xAxis(self, *args):
        return FigureWrapper(self.figure_.xAxis(*args))

    @convertArguments
    def xBusinessTime(self, *args):
        return FigureWrapper(self.figure_.xBusinessTime(*args))

    @convertArguments
    def xColor(self, *args):
        return FigureWrapper(self.figure_.xColor(*args))

    @convertArguments
    def xFormat(self, *args):
        return FigureWrapper(self.figure_.xFormat(*args))

    @convertArguments
    def xFormatPattern(self, *args):
        return FigureWrapper(self.figure_.xFormatPattern(*args))

    @convertArguments
    def xInvert(self, *args):
        return FigureWrapper(self.figure_.xInvert(*args))

    @convertArguments
    def xLabel(self, *args):
        return FigureWrapper(self.figure_.xLabel(*args))

    @convertArguments
    def xLabelFont(self, *args):
        return FigureWrapper(self.figure_.xLabelFont(*args))

    @convertArguments
    def xLog(self, *args):
        return FigureWrapper(self.figure_.xLog(*args))

    @convertArguments
    def xMax(self, *args):
        return FigureWrapper(self.figure_.xMax(*args))

    @convertArguments
    def xMin(self, *args):
        return FigureWrapper(self.figure_.xMin(*args))

    @convertArguments
    def xMinorTicks(self, *args):
        return FigureWrapper(self.figure_.xMinorTicks(*args))

    @convertArguments
    def xMinorTicksVisible(self, *args):
        return FigureWrapper(self.figure_.xMinorTicksVisible(*args))

    @convertArguments
    def xRange(self, *args):
        return FigureWrapper(self.figure_.xRange(*args))

    @convertArguments
    def xTickLabelAngle(self, *args):
        return FigureWrapper(self.figure_.xTickLabelAngle(*args))

    @convertArguments
    def xTicks(self, *args):
        return FigureWrapper(self.figure_.xTicks(*args))

    @convertArguments
    def xTicksFont(self, *args):
        return FigureWrapper(self.figure_.xTicksFont(*args))

    @convertArguments
    def xTicksVisible(self, *args):
        return FigureWrapper(self.figure_.xTicksVisible(*args))

    @convertArguments
    def xToolTipPattern(self, *args):
        return FigureWrapper(self.figure_.xToolTipPattern(*args))

    @convertArguments
    def xTransform(self, *args):
        return FigureWrapper(self.figure_.xTransform(*args))

    @convertArguments
    def yAxis(self, *args):
        return FigureWrapper(self.figure_.yAxis(*args))

    @convertArguments
    def yBusinessTime(self, *args):
        return FigureWrapper(self.figure_.yBusinessTime(*args))

    @convertArguments
    def yColor(self, *args):
        return FigureWrapper(self.figure_.yColor(*args))

    @convertArguments
    def yFormat(self, *args):
        return FigureWrapper(self.figure_.yFormat(*args))

    @convertArguments
    def yFormatPattern(self, *args):
        return FigureWrapper(self.figure_.yFormatPattern(*args))

    @convertArguments
    def yInvert(self, *args):
        return FigureWrapper(self.figure_.yInvert(*args))

    @convertArguments
    def yLabel(self, *args):
        return FigureWrapper(self.figure_.yLabel(*args))

    @convertArguments
    def yLabelFont(self, *args):
        return FigureWrapper(self.figure_.yLabelFont(*args))

    @convertArguments
    def yLog(self, *args):
        return FigureWrapper(self.figure_.yLog(*args))

    @convertArguments
    def yMax(self, *args):
        return FigureWrapper(self.figure_.yMax(*args))

    @convertArguments
    def yMin(self, *args):
        return FigureWrapper(self.figure_.yMin(*args))

    @convertArguments
    def yMinorTicks(self, *args):
        return FigureWrapper(self.figure_.yMinorTicks(*args))

    @convertArguments
    def yMinorTicksVisible(self, *args):
        return FigureWrapper(self.figure_.yMinorTicksVisible(*args))

    @convertArguments
    def yRange(self, *args):
        return FigureWrapper(self.figure_.yRange(*args))

    @convertArguments
    def yTickLabelAngle(self, *args):
        return FigureWrapper(self.figure_.yTickLabelAngle(*args))

    @convertArguments
    def yTicks(self, *args):
        return FigureWrapper(self.figure_.yTicks(*args))

    @convertArguments
    def yTicksFont(self, *args):
        return FigureWrapper(self.figure_.yTicksFont(*args))

    @convertArguments
    def yTicksVisible(self, *args):
        return FigureWrapper(self.figure_.yTicksVisible(*args))

    @convertArguments
    def yToolTipPattern(self, *args):
        return FigureWrapper(self.figure_.yToolTipPattern(*args))

    @convertArguments
    def yTransform(self, *args):
        return FigureWrapper(self.figure_.yTransform(*args))

    @convertArguments
    def zAxis(self, *args):
        return FigureWrapper(self.figure_.zAxis(*args))

    @convertArguments
    def zBusinessTime(self, *args):
        return FigureWrapper(self.figure_.zBusinessTime(*args))

    @convertArguments
    def zColor(self, *args):
        return FigureWrapper(self.figure_.zColor(*args))

    @convertArguments
    def zFormat(self, *args):
        return FigureWrapper(self.figure_.zFormat(*args))

    @convertArguments
    def zFormatPattern(self, *args):
        return FigureWrapper(self.figure_.zFormatPattern(*args))

    @convertArguments
    def zInvert(self, *args):
        return FigureWrapper(self.figure_.zInvert(*args))

    @convertArguments
    def zLabel(self, *args):
        return FigureWrapper(self.figure_.zLabel(*args))

    @convertArguments
    def zLabelFont(self, *args):
        return FigureWrapper(self.figure_.zLabelFont(*args))

    @convertArguments
    def zLog(self, *args):
        return FigureWrapper(self.figure_.zLog(*args))

    @convertArguments
    def zMax(self, *args):
        return FigureWrapper(self.figure_.zMax(*args))

    @convertArguments
    def zMin(self, *args):
        return FigureWrapper(self.figure_.zMin(*args))

    @convertArguments
    def zMinorTicks(self, *args):
        return FigureWrapper(self.figure_.zMinorTicks(*args))

    @convertArguments
    def zMinorTicksVisible(self, *args):
        return FigureWrapper(self.figure_.zMinorTicksVisible(*args))

    @convertArguments
    def zRange(self, *args):
        return FigureWrapper(self.figure_.zRange(*args))

    @convertArguments
    def zTickLabelAngle(self, *args):
        return FigureWrapper(self.figure_.zTickLabelAngle(*args))

    @convertArguments
    def zTicks(self, *args):
        return FigureWrapper(self.figure_.zTicks(*args))

    @convertArguments
    def zTicksFont(self, *args):
        return FigureWrapper(self.figure_.zTicksFont(*args))

    @convertArguments
    def zTicksVisible(self, *args):
        return FigureWrapper(self.figure_.zTicksVisible(*args))

    @convertArguments
    def zToolTipPattern(self, *args):
        return FigureWrapper(self.figure_.zToolTipPattern(*args))

    @convertArguments
    def zTransform(self, *args):
        return FigureWrapper(self.figure_.zTransform(*args))

