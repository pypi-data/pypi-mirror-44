#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

#############################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonIntegrationStaticMethods or
# "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
#############################################################################


import jpy
import functools


__java_type__ = None  # None until the first define_symbols() call
__DBTimeZone_defined__ = False


def defineDBTimeZone():
    """
    Defines appropriate enum mirroring the java enum, which requires that the jvm has been initialized through the jpy
    module, for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would
    lead to an exception if the jvm wasn't initialized BEFORE importing the module.
    """

    # To avoid (worse) confusion, we will not define
    #   DBTimeZone until it could be defined correctly
    global __DBTimeZone_defined__

    if __DBTimeZone_defined__:
        return
    elif not jpy.has_jvm():
        raise SystemError("The DBTimeZone class mirror functionality of the java enum "
                          "'com.illumon.iris.db.tables.utils.DBTimeZone'. No java functionality can be used until "
                          "the JVM has been initialized through the jpy module.")
    global DBTimeZone
    dbtz = jpy.get_type("com.illumon.iris.db.tables.utils.DBTimeZone")

    class DBTimeZone(object):
        TZ_NY = dbtz.TZ_NY
        TZ_ET = dbtz.TZ_ET
        TZ_MN = dbtz.TZ_MN
        TZ_CT = dbtz.TZ_CT
        TZ_MT = dbtz.TZ_MT
        TZ_PT = dbtz.TZ_PT
        TZ_HI = dbtz.TZ_HI
        TZ_BT = dbtz.TZ_BT
        TZ_KR = dbtz.TZ_KR
        TZ_HK = dbtz.TZ_HK
        TZ_JP = dbtz.TZ_JP
        TZ_AT = dbtz.TZ_AT
        TZ_NF = dbtz.TZ_NF
        TZ_AL = dbtz.TZ_AL
        TZ_IN = dbtz.TZ_IN
        TZ_CE = dbtz.TZ_CE
        TZ_UTC = dbtz.TZ_UTC

    __DBTimeZone_defined__ = True


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global __java_type__, __DBTimeZone_defined__
    if __java_type__ is not None:
        return
    # This will raise an exception if the desired object is not the classpath
    __java_type__ = jpy.get_type("com.illumon.iris.db.tables.utils.DBTimeUtils")

    if not __DBTimeZone_defined__:
        defineDBTimeZone()


# every module method should be decorated with @passThrough
def passThrough(func):
    """
    For decoration of module methods, to define necessary symbols at runtime

    :param func: the method to be decorated
    :return: the decorated version of the method
    """

    @functools.wraps(func)
    def wrapper(*args):
        defineSymbols()
        return func(*args)
    return wrapper


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


@passThrough
def autoEpochToTime(epoch):
    return __java_type__.autoEpochToTime(epoch)


@passThrough
def cappedTimeOffset(original, period, cap):
    return __java_type__.cappedTimeOffset(original, period, cap)


@passThrough
def convertDate(s):
    return __java_type__.convertDate(s)


@passThrough
def convertDateQuiet(*args):
    return __java_type__.convertDateQuiet(*args)


@passThrough
def convertDateTime(s):
    return __java_type__.convertDateTime(s)


@passThrough
def convertDateTimeQuiet(s):
    return __java_type__.convertDateTimeQuiet(s)


@passThrough
def convertExpression(formula):
    return __java_type__.convertExpression(formula)


@passThrough
def convertJimDateTimeQuiet(s):
    return __java_type__.convertJimDateTimeQuiet(s)


@passThrough
def convertJimMicrosDateTimeQuiet(s):
    return __java_type__.convertJimMicrosDateTimeQuiet(s)


@passThrough
def convertJimMicrosDateTimeQuietFast(s, timeZone):
    return __java_type__.convertJimMicrosDateTimeQuietFast(s, timeZone)


@passThrough
def convertJimMicrosDateTimeQuietFastTz(s):
    return __java_type__.convertJimMicrosDateTimeQuietFastTz(s)


@passThrough
def convertLocalTimeQuiet(s):
    return __java_type__.convertLocalTimeQuiet(s)


@passThrough
def convertPeriod(s):
    return __java_type__.convertPeriod(s)


@passThrough
def convertPeriodQuiet(s):
    return __java_type__.convertPeriodQuiet(s)


@passThrough
def convertTime(s):
    return __java_type__.convertTime(s)


@passThrough
def convertTimeQuiet(s):
    return __java_type__.convertTimeQuiet(s)


@passThrough
def createFormatter(timeZoneName):
    return __java_type__.createFormatter(timeZoneName)


@passThrough
def currentDate(timeZone):
    return __java_type__.currentDate(timeZone)


@passThrough
def currentDateNy():
    return __java_type__.currentDateNy()


@passThrough
def currentTime():
    return __java_type__.currentTime()


@passThrough
def dateAtMidnight(dateTime, timeZone):
    return __java_type__.dateAtMidnight(dateTime, timeZone)


@passThrough
def dayDiff(start, end):
    return __java_type__.dayDiff(start, end)


@passThrough
def dayOfMonth(dateTime, timeZone):
    return __java_type__.dayOfMonth(dateTime, timeZone)


@passThrough
def dayOfMonthNy(dateTime):
    return __java_type__.dayOfMonthNy(dateTime)


@passThrough
def dayOfWeek(dateTime, timeZone):
    return __java_type__.dayOfWeek(dateTime, timeZone)


@passThrough
def dayOfWeekNy(dateTime):
    return __java_type__.dayOfWeekNy(dateTime)


@passThrough
def dayOfYear(dateTime, timeZone):
    return __java_type__.dayOfYear(dateTime, timeZone)


@passThrough
def dayOfYearNy(dateTime):
    return __java_type__.dayOfYearNy(dateTime)


@passThrough
def diff(d1, d2):
    return __java_type__.diff(d1, d2)


@passThrough
def diffDay(start, end):
    return __java_type__.diffDay(start, end)


@passThrough
def diffNanos(d1, d2):
    return __java_type__.diffNanos(d1, d2)


@passThrough
def diffYear(start, end):
    return __java_type__.diffYear(start, end)


@passThrough
def expressionToNanos(formula):
    return __java_type__.expressionToNanos(formula)


@passThrough
def format(*args):
    return __java_type__.format(*args)


@passThrough
def formatDate(dateTime, timeZone):
    return __java_type__.formatDate(dateTime, timeZone)


@passThrough
def formatDateNy(dateTime):
    return __java_type__.formatDateNy(dateTime)


@passThrough
def formatNy(dateTime):
    return __java_type__.formatNy(dateTime)


@passThrough
def getExcelDateTime(*args):
    return __java_type__.getExcelDateTime(*args)


@passThrough
def getFinestDefinedUnit(timeDef):
    return __java_type__.getFinestDefinedUnit(timeDef)


@passThrough
def getPartitionFromTimestampMicros(dateTimeFormatter, timestampMicros):
    return __java_type__.getPartitionFromTimestampMicros(dateTimeFormatter, timestampMicros)


@passThrough
def getPartitionFromTimestampMillis(dateTimeFormatter, timestampMillis):
    return __java_type__.getPartitionFromTimestampMillis(dateTimeFormatter, timestampMillis)


@passThrough
def getPartitionFromTimestampNanos(dateTimeFormatter, timestampNanos):
    return __java_type__.getPartitionFromTimestampNanos(dateTimeFormatter, timestampNanos)


@passThrough
def getPartitionFromTimestampSeconds(dateTimeFormatter, timestampSeconds):
    return __java_type__.getPartitionFromTimestampSeconds(dateTimeFormatter, timestampSeconds)


@passThrough
def getZonedDateTime(*args):
    return __java_type__.getZonedDateTime(*args)


@passThrough
def hourOfDay(dateTime, timeZone):
    return __java_type__.hourOfDay(dateTime, timeZone)


@passThrough
def hourOfDayNy(dateTime):
    return __java_type__.hourOfDayNy(dateTime)


@passThrough
def isAfter(d1, d2):
    return __java_type__.isAfter(d1, d2)


@passThrough
def isBefore(d1, d2):
    return __java_type__.isBefore(d1, d2)


@passThrough
def lastBusinessDateNy(*args):
    return __java_type__.lastBusinessDateNy(*args)


@passThrough
def lowerBin(dateTime, intervalNanos):
    return __java_type__.lowerBin(dateTime, intervalNanos)


@passThrough
def microsOfMilli(dateTime, timeZone):
    return __java_type__.microsOfMilli(dateTime, timeZone)


@passThrough
def microsOfMilliNy(dateTime):
    return __java_type__.microsOfMilliNy(dateTime)


@passThrough
def microsToNanos(micros):
    return __java_type__.microsToNanos(micros)


@passThrough
def microsToTime(micros):
    return __java_type__.microsToTime(micros)


@passThrough
def millis(dateTime):
    return __java_type__.millis(dateTime)


@passThrough
def millisOfDay(dateTime, timeZone):
    return __java_type__.millisOfDay(dateTime, timeZone)


@passThrough
def millisOfDayNy(dateTime):
    return __java_type__.millisOfDayNy(dateTime)


@passThrough
def millisOfSecond(dateTime, timeZone):
    return __java_type__.millisOfSecond(dateTime, timeZone)


@passThrough
def millisOfSecondNy(dateTime):
    return __java_type__.millisOfSecondNy(dateTime)


@passThrough
def millisToDateAtMidnight(millis, timeZone):
    return __java_type__.millisToDateAtMidnight(millis, timeZone)


@passThrough
def millisToDateAtMidnightNy(millis):
    return __java_type__.millisToDateAtMidnightNy(millis)


@passThrough
def millisToNanos(millis):
    return __java_type__.millisToNanos(millis)


@passThrough
def millisToTime(millis):
    return __java_type__.millisToTime(millis)


@passThrough
def minus(*args):
    return __java_type__.minus(*args)


@passThrough
def minuteOfDay(dateTime, timeZone):
    return __java_type__.minuteOfDay(dateTime, timeZone)


@passThrough
def minuteOfDayNy(dateTime):
    return __java_type__.minuteOfDayNy(dateTime)


@passThrough
def minuteOfHour(dateTime, timeZone):
    return __java_type__.minuteOfHour(dateTime, timeZone)


@passThrough
def minuteOfHourNy(dateTime):
    return __java_type__.minuteOfHourNy(dateTime)


@passThrough
def monthOfYear(dateTime, timeZone):
    return __java_type__.monthOfYear(dateTime, timeZone)


@passThrough
def monthOfYearNy(dateTime):
    return __java_type__.monthOfYearNy(dateTime)


@passThrough
def nanos(dateTime):
    return __java_type__.nanos(dateTime)


@passThrough
def nanosOfDay(dateTime, timeZone):
    return __java_type__.nanosOfDay(dateTime, timeZone)


@passThrough
def nanosOfDayNy(dateTime):
    return __java_type__.nanosOfDayNy(dateTime)


@passThrough
def nanosOfSecond(dateTime, timeZone):
    return __java_type__.nanosOfSecond(dateTime, timeZone)


@passThrough
def nanosOfSecondNy(dateTime):
    return __java_type__.nanosOfSecondNy(dateTime)


@passThrough
def nanosToMicros(nanos):
    return __java_type__.nanosToMicros(nanos)


@passThrough
def nanosToMillis(nanos):
    return __java_type__.nanosToMillis(nanos)


@passThrough
def nanosToTime(nanos):
    return __java_type__.nanosToTime(nanos)


@passThrough
def overrideLastBusinessDateNyFromCurrentDateNy():
    return __java_type__.overrideLastBusinessDateNyFromCurrentDateNy()


@passThrough
def plus(*args):
    return __java_type__.plus(*args)


@passThrough
def secondOfDay(dateTime, timeZone):
    return __java_type__.secondOfDay(dateTime, timeZone)


@passThrough
def secondOfDayNy(dateTime):
    return __java_type__.secondOfDayNy(dateTime)


@passThrough
def secondOfMinute(dateTime, timeZone):
    return __java_type__.secondOfMinute(dateTime, timeZone)


@passThrough
def secondOfMinuteNy(dateTime):
    return __java_type__.secondOfMinuteNy(dateTime)


@passThrough
def secondsToNanos(seconds):
    return __java_type__.secondsToNanos(seconds)


@passThrough
def secondsToTime(seconds):
    return __java_type__.secondsToTime(seconds)


@passThrough
def toDateTime(zonedDateTime):
    return __java_type__.toDateTime(zonedDateTime)


@passThrough
def upperBin(*args):
    return __java_type__.upperBin(*args)


@passThrough
def year(dateTime, timeZone):
    return __java_type__.year(dateTime, timeZone)


@passThrough
def yearDiff(start, end):
    return __java_type__.yearDiff(start, end)


@passThrough
def yearNy(dateTime):
    return __java_type__.yearNy(dateTime)


@passThrough
def yearOfCentury(dateTime, timeZone):
    return __java_type__.yearOfCentury(dateTime, timeZone)


@passThrough
def yearOfCenturyNy(dateTime):
    return __java_type__.yearOfCenturyNy(dateTime)
