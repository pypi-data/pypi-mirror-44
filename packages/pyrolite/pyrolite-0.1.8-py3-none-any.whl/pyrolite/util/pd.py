import pandas as pd
import hashlib
from functools import partial
from pathlib import Path
import numpy as np
import logging
import inspect

from .general import pathify

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger()


def column_ordered_append(df1, df2, **kwargs):
    """
    Appends one dataframe to another, preserving the column order of the
    first and adding new columns on the right. Also accepts and passes on
    standard keyword arguments for pd.DataFrame.append.

    Parameters
    ------------
    df1 : :class:`pandas.DataFrame`
        The dataframe for which columns order is preserved in the output.
    df2 : :class:`pandas.DataFrame`
        The dataframe for which new columns are appended to the output.

    Returns
    --------
    :class:`pandas.DataFrame`
    """
    outcols = list(df1.columns) + [i for i in df2.columns if not i in df1.columns]
    return df1.append(df2, **kwargs).reindex(columns=outcols)


def accumulate(dfs, ignore_index=False, trace_source=False, names=[]):
    """
    Accumulate an iterable containing multiple :class:`pandas.DataFrame` to a single frame.
    """
    acc = None
    for ix, df in enumerate(dfs):
        if trace_source:
            if names:
                df["src_idx"] = names[ix]
            else:
                df["src_idx"] = ix
        if acc is None:
            acc = df
        else:
            acc = column_ordered_append(acc, df, ignore_index=ignore_index)
    return acc


def to_frame(df):
    """
    Simple utility for converting to :class:`pandas.DataFrame`.
    """

    if type(df) == pd.Series:  # using series instead of dataframe
        df = df.to_frame().T
    elif type(df) == pd.DataFrame:  # 1 column slice
        if df.columns.size == 1:
            df = df.T
    else:
        msg = "Conversion from {} to dataframe not yet implemented".format(type(df))
        raise NotImplementedError(msg)

    return df


def to_ser(df):
    """
    Simple utility for converting single column :class:`pandas.DataFrame`
    to :class:`pandas.Series`.
    """
    if isinstance(df, pd.Series):  # passed series instead of dataframe
        ser = df
    elif isinstance(df, pd.DataFrame):
        assert (df.columns.size == 1) or (
            df.index.size == 1
        ), """Can't convert DataFrame to Series:
              either columns or index need to have size 1."""
        if df.columns.size == 1:
            ser = df.iloc[:, 0]
        else:
            ser = df.iloc[0, :]
    else:
        msg = "Conversion from {} to series not yet implemented".format(type(df))
        raise NotImplementedError(msg)

    return ser


def to_numeric(df, errors: str = "coerce"):
    """
    Takes all non-metadata columns and converts to numeric type where possible.

    Notes
    -----
    Avoid using .loc or .iloc on the LHS to make sure that data dtypes
    are propagated.
    """
    return df.apply(pd.to_numeric, errors=errors)


def outliers(
    df,
    cols=[],
    detect=lambda x, quantile, qntls: (
        (x > quantile.loc[qntls[0], x.name]) & (x < quantile.loc[qntls[1], x.name])
    ),
    quantile_select=(0.02, 0.98),
    logquantile=False,
    exclude=False,
):
    """
    """
    if not cols:
        cols = df.columns
    colfltr = (df.dtypes == np.float) & ([i in cols for i in df.columns])
    low, high = np.min(quantile_select), np.max(quantile_select)
    if not logquantile:
        quantile = df.loc[:, colfltr].quantile([low, high])
    else:
        quantile = df.loc[:, colfltr].apply(np.log).quantile([low, high])
    whereout = (
        df.loc[:, colfltr]
        .apply(detect, args=(quantile, quantile_select), axis=0)
        .sum(axis=1)
        > 0
    )
    if not exclude:
        whereout = np.logical_not(whereout)
    return df.loc[whereout, colfltr]


def concat_columns(df, columns=None, astype=str, **kwargs):
    """
    Concatenate strings across columns.

    Parameters
    -----------
    df : :class:`pandas.DataFrame`
        Dataframe to concatenate.
    columns : :class:`list`
        List of columns to concatenate.
    astype : :class:`type`
        Type to convert final concatenation to.

    Returns
    -------
    :class:`pandas.Series`
    """
    if columns is None:
        columns = df.columns
    out = pd.Series(index=df.index, **kwargs)
    for ix, c in enumerate(columns):
        if ix == 0:
            out = df.loc[:, c].astype(astype)
        else:
            out += df.loc[:, c].astype(astype)
    return out


def uniques_from_concat(df, columns=None, hashit=True):
    """
    Creates ideally unique keys from multiple columns.
    Optionally hashes string to standardise length of identifier.

    Parameters
    ------------
    df : :class:`pandas.DataFrame`
        DataFrame to create indexes for.
    columns : :class:`list`
        Columns to use in the string concatenatation.
    hashit : :class:`bool`, :code:`True`
        Whether to use a hashing algorithm to create the key from a typically
        longer string.

    Returns
    ---------
    :class:`pandas.Series`
    """
    if columns is None:
        columns = df.columns

    if hashit:

        def fmt(ser):
            ser = ser.str.encode("UTF-8")
            ser = ser.apply(lambda x: hashlib.md5(x).hexdigest())
            return ser

    else:
        fmt = lambda x: x.str.encode("UTF-8")

    return fmt(concat_columns(df, columns, dtype="category"))


def df_from_csvs(csvs, dropna=True, ignore_index=False, **kwargs):
    """
    Takes a list of .csv filenames and converts to a single DataFrame.
    Combines columns across dataframes, preserving order of the first entered.

    E.g.
    SiO2, Al2O3, MgO, MnO, CaO
    SiO2, MgO, FeO, CaO
    SiO2, Na2O, Al2O3, FeO, CaO
    =>
    SiO2, Na2O, Al2O3, MgO, FeO, MnO, CaO
    - Existing neighbours take priority (i.e. FeO won't be inserted bf Al2O3)
    - Earlier inputs take priority (where ordering is ambiguous, place the earlier first)

    Todo
    -----
        Attempt to preserve column ordering across column sets, assuming
        they are generally in the same order but preserving only some of the
        information.
    """
    cols = []
    dfs = []
    for ix, t in enumerate(csvs):
        dfs.append(pd.read_csv(t, **kwargs))
        cols = cols + [i for i in dfs[-1].columns if i not in cols]

    df = accumulate(dfs, ignore_index=ignore_index)
    return df


def pickle_from_csvs(targets, out_filename, sep="\t", suffix=".pkl"):
    df = df_from_csvs(targets, sep=sep, low_memory=False)
    sparse_pickle_df(df, out_filename, suffix=suffix)


def sparse_pickle_df(df: pd.DataFrame, filename, suffix=".pkl"):
    """
    Converts dataframe to sparse dataframe before pickling to disk.
    """
    df.to_sparse().to_pickle(pathify(filename).with_suffix(suffix))


def load_sparse_pickle_df(filename, suffix=".pkl", keep_sparse=False):
    """
    Loads sparse dataframe from disk, with optional densification.
    """
    if keep_sparse:
        return pd.read_pickle(pathify(filename).with_suffix(suffix))
    else:
        return pd.read_pickle(pathify(filename).with_suffix(suffix)).to_dense()
