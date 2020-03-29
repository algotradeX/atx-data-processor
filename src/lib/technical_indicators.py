"""
    Indicators as shown by Peter Bakker at:
    https://www.quantopian.com/posts/technical-analysis-indicators-without-talib-code
"""

# Import Built-Ins
import logging

# Import Third-Party
import pandas as pd
import numpy as np

# Init Logging Facilities
log = logging.getLogger(__name__)


def moving_average(df, p, n):
    """Calculate the moving average for the given data.

    :param df: pandas.DataFrame
    :param p: String
    :param n: Integer
    :return: pandas.DataFrame
    """
    MA = pd.Series(df[p].rolling(n, min_periods=n).mean(), name="MA_" + str(n))
    df = df.join(MA)
    return df


def exponential_moving_average(df, p, n):
    """

    :param df: pandas.DataFrame
    :param p: String
    :param n: Integer
    :return: pandas.DataFrame
    """
    EMA = pd.Series(df[p].ewm(span=n, min_periods=n).mean(), name="EMA_" + str(n))
    df = df.join(EMA)
    return df


def momentum(df, p, n):
    """

    :param df: pandas.DataFrame
    :param p: String
    :param n: Integer
    :return: pandas.DataFrame
    """
    M = pd.Series(df[p].diff(n), name="Momentum_" + str(n))
    df = df.join(M)
    return df
