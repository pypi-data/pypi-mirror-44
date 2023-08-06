import warnings

import numpy as np
import pandas as pd
import numba

import scipy.ndimage
import skimage
import skimage.exposure

from matplotlib.pyplot import get_cmap as mpl_get_cmap

import bokeh.models
import bokeh.palettes
import bokeh.plotting

from . import utils

def fill_between(x1=None, y1=None, x2=None, y2=None,
                 x_axis_label=None, y_axis_label=None,
                 x_axis_type='linear', y_axis_type='linear',
                 title=None, plot_height=300, plot_width=450,
                 fill_color='#1f77b4', line_color='#1f77b4', show_line=True,
                 line_width=1, fill_alpha=1, line_alpha=1, p=None,  **kwargs):
    """
    Create a filled region between two curves.

    Parameters
    ----------
    x1 : array_like
        Array of x-values for first curve
    y1 : array_like
        Array of y-values for first curve
    x2 : array_like
        Array of x-values for second curve
    y2 : array_like
        Array of y-values for second curve
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default None
        Label for the y-axis. Ignored if `p` is not None.
    x_axis_type : str, default 'linear'
        Either 'linear' or 'log'.
    y_axis_type : str, default 'linear'
        Either 'linear' or 'log'.    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    fill_color : str, default '#1f77b4'
        Color of fill as a hex string.
    line_color : str, default '#1f77b4'
        Color of the line as a hex string.
    show_line : bool, default True
        If True, show the lines on the edges of the fill.
    line_width : int, default 1
        Line width of lines on the edgs of the fill.
    fill_alpha : float, default 1.0
        Opacity of the fill.
    line_alpha : float, default 1.0
        Opacity of the lines.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with fill-between.

    Notes
    -----
    .. Any remaining kwargs are passed to bokeh.models.patch().
    """

    if p is None:
        p = bokeh.plotting.figure(
            plot_height=plot_height, plot_width=plot_width,
            x_axis_type=x_axis_type, y_axis_type=y_axis_type,
            x_axis_label=x_axis_label, y_axis_label=y_axis_label, title=title)


    p.patch(x=np.concatenate((x1, x2[::-1])),
            y=np.concatenate((y1, y2[::-1])),
            alpha=fill_alpha,
            fill_color=fill_color,
            line_width=0,
            line_alpha=0,
            **kwargs)

    if show_line:
        p.line(x1,
               y1,
               line_width=line_width,
               alpha=line_alpha,
               color=line_color)
        p.line(x2,
               y2,
               line_width=line_width,
               alpha=line_alpha,
               color=line_color)

    return p


def ecdf(data=None, conf_int=False, ptiles=[2.5, 97.5], n_bs_reps=1000,
         fill_color='lightgray', fill_alpha=1, p=None, x_axis_label=None,
         y_axis_label='ECDF', title=None, plot_height=300, plot_width=450,
         formal=False, complementary=False, x_axis_type='linear',
         y_axis_type='linear', **kwargs):
    """
    Create a plot of an ECDF.

    Parameters
    ----------
    data : array_like
        One-dimensional array of data. Nan's are ignored.
    conf_int : bool, default False
        If True, display a confidence interval on the ECDF.
    ptiles : list, default [2.5, 97.5]
        The percentiles to use for the confidence interval. Ignored it
        `conf_int` is False.
    n_bs_reps : int, default 1000
        Number of bootstrap replicates to do to compute confidence
        interval. Ignored if `conf_int` is False.
    fill_color : str, default 'lightgray'
        Color of the confidence interbal. Ignored if `conf_int` is
        False.
    fill_alpha : float, default 1
        Opacity of confidence interval. Ignored if `conf_int` is False.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    formal : bool, default False
        If True, make a plot of a formal ECDF (staircase). If False,
        plot the ECDF as dots.
    complementary : bool, default False
        If True, plot the empirical complementary cumulative
        distribution functon.
    x_axis_type : str, default 'linear'
        Either 'linear' or 'log'.
    y_axis_type : str, default 'linear'
        Either 'linear' or 'log'.
    kwargs
        Any kwargs to be passed to either p.circle or p.line, for
        `formal` being False or True, respectively.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with ECDF.
    """
    # Check data to make sure legit
    data = utils._convert_data(data)

    # Data points on ECDF
    x, y = _ecdf_vals(data, formal, complementary)

    # Instantiate Bokeh plot if not already passed in
    if p is None:
        p = bokeh.plotting.figure(
            plot_height=plot_height, plot_width=plot_width,
            x_axis_label=x_axis_label, y_axis_label=y_axis_label,
            x_axis_type=x_axis_type, y_axis_type=y_axis_type, title=title)

    # Do bootstrap replicates
    if conf_int:
        x_plot = np.sort(np.unique(x))
        bs_reps = np.array([_ecdf_arbitrary_points(
                            np.random.choice(data, size=len(data)), x_plot)
                                for _ in range(n_bs_reps)])

        # Compute the confidence intervals
        ecdf_low, ecdf_high = np.percentile(np.array(bs_reps), ptiles, axis=0)

        # Make them formal
        _, ecdf_low = _to_formal(x=x_plot, y=ecdf_low)
        x_plot, ecdf_high = _to_formal(x=x_plot, y=ecdf_high)

        p = fill_between(x1=x_plot, y1=ecdf_low, x2=x_plot, y2=ecdf_high,
                         fill_color=fill_color, show_line=False, p=p)

    if formal:
        # Line of steps
        p.line(x, y, **kwargs)

        # Rays for ends
        if complementary:
            p.ray(x[0], 1, None, np.pi, **kwargs)
            p.ray(x[-1], 0, None, 0, **kwargs)
        else:
            p.ray(x[0], 0, None, np.pi, **kwargs)
            p.ray(x[-1], 1, None, 0, **kwargs)
    else:
        p.circle(x, y, **kwargs)

    return p


def im_hist(im, p=None, title=None, y_axis_type='linear', **kwargs):
    """
    Make plot of image histogram.

    Parameters
    ----------
    im : 2D Numpy array
        Image for which the histogram will be plotted.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    title : str, default None
        Title for the plot.
    y_axis_type : one of ['linear', 'log'], default 'linear'
        Speicifcation of y-axis being on a linear or logarithmic scale.
    kwargs : kwargs specification
        Keyword arguments sent to Bokeh's line glyph.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        A Bokeh figure containing the plot of the histogram.
    """
    # Get the histogram data
    hist, bins = skimage.exposure.histogram(im)

    if p is None:
        p = bokeh.plotting.figure(plot_height=300,
                                  plot_width=400,
                                  y_axis_type=y_axis_type,
                                  x_axis_label='intensity',
                                  y_axis_label='count',
                                  title=title)

    p.line(bins, hist, line_width=2, line_join='bevel', **kwargs)

    return p


def histogram(data=None, bins=10, p=None, x_axis_label=None,
              y_axis_label=None, title=None, plot_height=300, plot_width=450,
              density=False, kind='step', **kwargs):
    """
    Make a plot of a histogram of a data set.

    Parameters
    ----------
    data : array_like
        1D array of data to make a histogram out of
    bins : int, array_like, or one of 'exact' or 'integer' default 10
        Setting for `bins` kwarg to be passed to `np.histogram()`. If
        `'exact'`, then each unique value in the data gets its own bin.
        If `integer`, then integer data is assumed and each integer gets
        its own bin.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default None
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    density : bool, default False
        If True, normalized the histogram. Otherwise, base the histogram
        on counts.
    kind : str, default 'step'
        The kind of histogram to display. Allowed values are 'step' and
        'step_filled'.

    Returns
    -------
    output : Bokeh figure
        Figure populated with histogram.
    """
    if data is None:
        raise RuntimeError('Input `data` must be specified.')

    # Instantiate Bokeh plot if not already passed in
    if p is None:
        if y_axis_label is None:
            if density:
                y_axis_label = 'density'
            else:
                y_axis_label = 'count'

        p = bokeh.plotting.figure(
            plot_height=plot_height, plot_width=plot_width,
            x_axis_label=x_axis_label, y_axis_label=y_axis_label,
            title=title, y_range = bokeh.models.DataRange1d(start=0))

    if bins == 'exact':
        a = np.unique(data)
        if len(a) == 1:
            bins = np.array([a[0] - 0.5, a[0] + 0.5])
        else:
            bins = np.concatenate(((a[0] - (a[1] - a[0])/2,),
                                    (a[1:] + a[:-1]) / 2,
                                    (a[-1] + (a[-1]-a[-2]) / 2,)))
    elif bins == 'integer':
        if np.any(data != np.round(data)):
            raise RuntimeError(
                        "'integer' bins chosen, but data are not integer.")
        bins = np.arange(data.min()-1, data.max()+1) + 0.5

    # Compute histogram
    f, e = np.histogram(data, bins=bins, density=density)
    e0 = np.empty(2*len(e))
    f0 = np.empty(2*len(e))
    e0[::2] = e
    e0[1::2] = e
    f0[0] = 0
    f0[-1] = 0
    f0[1:-1:2] = f
    f0[2:-1:2] = f

    if kind == 'step':
        p.line(e0, f0, **kwargs)

    if kind == 'step_filled':
        x2 = [e0.min(), e0.max()]
        y2 = [0, 0]
        p = fill_between(e0, f0, x2, y2, show_line=True, p=p, **kwargs)

    return p


def jitter(data=None, cats=None, val=None, p=None, horizontal=False,
           x_axis_label=None, y_axis_label=None, title=None, plot_height=300,
           plot_width=400,
           palette=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f',
                    '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac'],
           width=0.4, order=None, val_axis_type='linear', show_legend=False,
           color_column=None, tooltips=None, **kwargs):
    """
    Make a jitter plot from a tidy DataFrame.

    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hastables
        Name of column(s) to use as categorical variable.
    val : hashable
        Name of column to use as value variable.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    horizontal : bool, default False
        If true, the categorical axis is the vertical axis.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    width : float, default 0.4
        Maximum allowable width of jittered points. A value of 1 means
        that the points take the entire space allotted.
    order : list or None
        If not None, must be a list of unique entries in `df[val]`. The
        order of the list specifies the order of the boxes. If None,
        the boxes appear in the order in which they appeared in the
        inputted DataFrame.
    val_axis_type : str, default 'linear'
        Type of scaling for the quantitative axis, wither 'linear' or
        'log'.
    show_legend : bool, default False
        If True, display legend.
    color_column : str, default None
        Column of `data` to use in determining color of glyphs. If None,
        then `cats` is used.
    tooltips : list of Bokeh tooltips
        Tooltips to add to the plot.
    kwargs
        Any kwargs to be passed to p.circle when making the jitter plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with jitter plot.
    """

    cols = _check_cat_input(data, cats, val, color_column, tooltips,
                            palette, kwargs)

    grouped = data.groupby(cats)

    if p is None:
        p, factors, color_factors = _cat_figure(data,
                                                grouped,
                                                plot_height,
                                                plot_width,
                                                x_axis_label,
                                                y_axis_label,
                                                title,
                                                order,
                                                color_column,
                                                tooltips,
                                                horizontal,
                                                val_axis_type)
    else:
        _, factors, color_factors = _get_cat_range(data,
                                                   grouped,
                                                   order,
                                                   color_column,
                                                   horizontal)
        if tooltips is not None:
            p.add_tools(bokeh.models.HoverTool(tooltips=tooltips))

    if 'color' not in kwargs:
        if color_column is None:
            color_column = 'cat'
        kwargs['color'] = bokeh.transform.factor_cmap(color_column,
                                                      palette=palette,
                                                      factors=color_factors)

    source = _cat_source(data, cats, cols, color_column)

    if show_legend:
        kwargs['legend'] = '__label'

    if horizontal:
        p.circle(source=source,
                 x=val,
                 y=bokeh.transform.jitter('cat',
                                          width=width,
                                          range=p.y_range),
                 **kwargs)
        p.ygrid.grid_line_color = None
    else:
        p.circle(source=source,
                 y=val,
                 x=bokeh.transform.jitter('cat',
                                          width=width,
                                          range=p.x_range),
                 **kwargs)
        p.xgrid.grid_line_color = None

    return p


def box(data=None, cats=None, val=None, p=None, horizontal=False,
        x_axis_label=None, y_axis_label=None, title=None, plot_height=300,
        plot_width=400,
        palette=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f',
                 '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac'],
        width=0.4, order=None, tooltips=None, val_axis_type='linear',
        display_outliers=True, box_kwargs=None, whisker_kwargs=None,
        outlier_kwargs=None):
    """
    Make a box-and-whisker plot from a tidy DataFrame.

    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hastables
        Name of column(s) to use as categorical variable.
    val : hashable
        Name of column to use as value variable.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all boxes are colored with that color. Default is
        the default color cycle employed by Altair.
    width : float, default 0.4
        Maximum allowable width of the boxes. A value of 1 means that
        the boxes take the entire space allotted.
    val_axis_type : str, default 'linear'
        Type of scaling for the quantitative axis, wither 'linear' or
        'log'.
    show_legend : bool, default False
        If True, display legend.
    tooltips : list of Bokeh tooltips
        Tooltips to add to the plot.
    order : list or None
        If not None, must be a list of unique entries in `df[val]`. The
        order of the list specifies the order of the boxes. If None,
        the boxes appear in the order in which they appeared in the
        inputted DataFrame.
    display_outliers : bool, default True
        If True, display outliers, otherwise suppress them. This should
        only be False when making an overlay with a jitter plot.
    box_kwargs : dict, default None
        A dictionary of kwargs to be passed into `p.hbar()` or
        `p.vbar()` when constructing the boxes for the box plot.
    whisker_kwargs : dict, default None
        A dictionary of kwargs to be passed into `p.segment()`
        when constructing the whiskers for the box plot.
    outlier_kwargs : dict, default None
        A dictionary of kwargs to be passed into `p.circle()`
        when constructing the outliers for the box plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with box-and-whisker plot.

    Notes
    -----
    .. Uses the Tukey convention for box plots. The top and bottom of
       the box are respectively the 75th and 25th percentiles of the
       data. The line in the middle of the box is the median. The
       top whisker extends to the lesser of the largest data point and
       the top of the box plus 1.5 times the interquartile region (the
       height of the box). The bottom whisker extends to the greater of
       the smallest data point and the bottom of the box minus 1.5 times
       the interquartile region. Data points not between the ends of the
       whiskers are considered outliers and are plotted as individual
       points.
    """
    cols = _check_cat_input(data, cats, val, None, tooltips, palette,
                            box_kwargs)

    if whisker_kwargs is None:
        whisker_kwargs = {'line_color': 'black'}
    elif type(whisker_kwargs) != dict:
        raise RuntimeError('`whisker_kwargs` must be a dict.')

    if outlier_kwargs is None:
        outlier_kwargs = dict()
    elif type(outlier_kwargs) != dict:
        raise RuntimeError('`outlier_kwargs` must be a dict.')

    if box_kwargs is None:
        box_kwargs = {'line_color': 'black'}
    elif type(box_kwargs) != dict:
        raise RuntimeError('`box_kwargs` must be a dict.')

    grouped = data.groupby(cats)

    if p is None:
        p, factors, color_factors = _cat_figure(data,
                                                grouped,
                                                plot_height,
                                                plot_width,
                                                x_axis_label,
                                                y_axis_label,
                                                title,
                                                order,
                                                None,
                                                tooltips,
                                                horizontal,
                                                val_axis_type)
    else:
        if tooltips is not None:
            p.add_tools(bokeh.models.HoverTool(tooltips=tooltips))

        _, factors, color_factors = _get_cat_range(data,
                                                   grouped,
                                                   order,
                                                   None,
                                                   horizontal)

    source_box, source_outliers = _box_source(data, cats, val, cols)

    if 'fill_color' not in box_kwargs:
        box_kwargs['fill_color'] = bokeh.transform.factor_cmap('cat', palette=palette, factors=factors)
    if 'line_color' not in box_kwargs:
        box_kwargs['line_color'] = 'black'

    if 'color' in outlier_kwargs:
        if 'line_color' in outlier_kwargs or 'fill_color' in outlier_kwargs:
            raise RuntimeError('If `color` is in `outlier_kwargs`, `line_color` and `fill_color` cannot be.')
    else:
        if 'fill_color' not in outlier_kwargs:
            outlier_kwargs['fill_color'] = bokeh.transform.factor_cmap(
                                    'cat', palette=palette, factors=factors)
        if 'line_color' not in outlier_kwargs:
            outlier_kwargs['line_color'] = bokeh.transform.factor_cmap(
                                    'cat', palette=palette, factors=factors)

    if horizontal:
        p.segment(source=source_box,
                  y0='cat',
                  y1='cat',
                  x0='top',
                  x1='top_whisker',
                  **whisker_kwargs)
        p.segment(source=source_box,
                  y0='cat',
                  y1='cat',
                  x0='bottom',
                  x1='bottom_whisker',
                  **whisker_kwargs)
        p.hbar(source=source_box,
               y='cat',
               left='top_whisker',
               right='top_whisker',
               height=width/4,
               **whisker_kwargs)
        p.hbar(source=source_box,
               y='cat',
               left='bottom_whisker',
               right='bottom_whisker',
               height=width/4,
               **whisker_kwargs)
        p.hbar(source=source_box,
               y='cat',
               left='bottom',
               right='top',
               height=width,
               **box_kwargs)
        p.hbar(source=source_box,
               y='cat',
               left='middle',
               right='middle',
               height=width,
               **box_kwargs)
        if display_outliers:
            p.circle(source=source_outliers,
                     y='cat',
                     x=val,
                     **outlier_kwargs)
        p.ygrid.grid_line_color = None
    else:
        p.segment(source=source_box,
                  x0='cat',
                  x1='cat',
                  y0='top',
                  y1='top_whisker',
                  **whisker_kwargs)
        p.segment(source=source_box,
                  x0='cat',
                  x1='cat',
                  y0='bottom',
                  y1='bottom_whisker',
                  **whisker_kwargs)
        p.vbar(source=source_box,
               x='cat',
               bottom='top_whisker',
               top='top_whisker',
               width=width/4,
               **whisker_kwargs)
        p.vbar(source=source_box,
               x='cat',
               bottom='bottom_whisker',
               top='bottom_whisker',
               width=width/4,
               **whisker_kwargs)
        p.vbar(source=source_box,
               x='cat',
               bottom='bottom',
               top='top',
               width=width,
               **box_kwargs)
        p.vbar(source=source_box,
               x='cat',
               bottom='middle',
               top='middle',
               width=width,
               **box_kwargs)
        if display_outliers:
            p.circle(source=source_outliers,
                     x='cat',
                     y=val,
                     **outlier_kwargs)
        p.xgrid.grid_line_color = None

    return p


def ecdf_collection(data=None, cats=None, val=None, p=None,
                    complementary=False, formal=False,
                    x_axis_label=None, y_axis_label=None, title=None,
                    plot_height=300, plot_width=400,
                    palette=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2',
                             '#59a14f', '#edc948', '#b07aa1', '#ff9da7',
                             '#9c755f', '#bab0ac'],
                    order=None, show_legend=True, tooltips=None,
                    val_axis_type='linear', ecdf_axis_type='linear',
                    **kwargs):
    """
    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hastables
        Name of column(s) to use as categorical variable (x-axis).
    val : hashable
        Name of column to use as value variable.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    complementary : bool, default False
        If True, plot the empirical complementary cumulative
        distribution functon.
    formal : bool, default False
        If True, make a plot of a formal ECDF (staircase). If False,
        plot the ECDF as dots.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    show_legend : bool, default False
        If True, show legend.
    order : list or None
        If not None, must be a list of unique entries in `df[val]`. The
        order of the list specifies the order of the boxes. If None,
        the boxes appear in the order in which they appeared in the
        inputted DataFrame.
    tooltips : list of 2-tuples
        Specification for tooltips. Ignored if `formal` is True.
    show_legend : bool, default False
        If True, show a legend.
    val_axis_type : 'linear' or 'log'
        Type of x-axis.
    ecdf_axis_type : 'linear' or 'log'
        Type of y-axis.
    kwargs
        Any kwargs to be passed to `p.circle()` or `p.line()` when
        making the plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with jitter plot or box plot.
    if formal and tooltips is not None:
        raise RuntimeError('tooltips not possible for formal ECDFs.')
    """
    cols = _check_cat_input(data, cats, val, None, tooltips, palette, kwargs)

    if complementary:
        y = '__ECCDF'
        if y_axis_label is None:
            y_axis_label = 'ECCDF'
    else:
        y = '__ECDF'
        if y_axis_label is None:
            y_axis_label = 'ECDF'

    if x_axis_label is None:
        x_axis_label = val


    if p is None:
        p = bokeh.plotting.figure(plot_height=plot_height,
                                  plot_width=plot_width,
                                  x_axis_label=x_axis_label,
                                  y_axis_label=y_axis_label,
                                  x_axis_type=val_axis_type,
                                  y_axis_type=ecdf_axis_type,
                                  title=title)

    if formal:
        p = _ecdf_collection_formal(data,
                                    val,
                                    cats,
                                    complementary,
                                    order,
                                    palette,
                                    show_legend,
                                    p,
                                    **kwargs)
    else:
        p = _ecdf_collection_dots(data,
                                  val,
                                  cats,
                                  cols,
                                  complementary,
                                  order,
                                  palette,
                                  show_legend,
                                  y,
                                  p,
                                  **kwargs)

    if not formal and tooltips is not None:
        p.add_tools(bokeh.models.HoverTool(tooltips=tooltips))

    if show_legend:
        if complementary:
            p.legend.location = 'top_right'
        else:
            p.legend.location = 'bottom_right'

    return p


def colored_ecdf(data=None, cats=None, val=None, p=None, complementary=False,
                 x_axis_label=None, y_axis_label=None, title=None,
                 plot_height=300, plot_width=400,
                 palette=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2',
                          '#59a14f', '#edc948', '#b07aa1', '#ff9da7',
                          '#9c755f', '#bab0ac'],
                 order=None, show_legend=True, tooltips=None,
                 val_axis_type='linear', ecdf_axis_type='linear', **kwargs):
    """
    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hashables
        Name of column(s) to use as categorical variable (x-axis).
    val : hashable
        Name of column to use as value variable.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    complementary : bool, default False
        If True, plot the empirical complementary cumulative
        distribution functon.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    show_legend : bool, default False
        If True, show legend.
    order : list or None
        If not None, must be a list of unique entries in `df[cat]`. The
        order of the list specifies the order of the colors. If None,
        the colors appear in the order in which they appeared in the
        inputted DataFrame.
    tooltips : list of 2-tuples
        Specification for tooltips.
    show_legend : bool, default False
        If True, show a legend.
    val_axis_type : 'linear' or 'log'
        Type of x-axis.
    ecdf_axis_type : 'linear' or 'log'
        Type of y-axis.
    kwargs
        Any kwargs to be passed to `p.circle()` when making the plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with jitter plot or box plot.
    if formal and tooltips is not None:
        raise RuntimeError('tooltips not possible for formal ECDFs.')
    """
    cols = _check_cat_input(data, cats, val, None, tooltips, palette, kwargs)

    if complementary:
        y = '__ECCDF'
        if y_axis_label is None:
            y_axis_label = 'ECCDF'
    else:
        y = '__ECDF'
        if y_axis_label is None:
            y_axis_label = 'ECDF'

    df = data.copy()
    df[y] = df[val].transform(_ecdf_y, complementary=complementary)
    cols += [y]
    source = _cat_source(df, cats, cols, None)
    _, _, color_factors = _get_cat_range(df,
                                         df.groupby(cats),
                                         order,
                                         None,
                                         False)

    if 'color' not in kwargs:
        kwargs['color'] = bokeh.transform.factor_cmap('cat',
                                                    palette=palette,
                                                    factors=color_factors)

    if show_legend:
        kwargs['legend'] = '__label'

    if p is None:
        p = bokeh.plotting.figure(plot_height=plot_height,
                                  plot_width=plot_width,
                                  x_axis_label=x_axis_label,
                                  y_axis_label=y_axis_label,
                                  x_axis_type=val_axis_type,
                                  y_axis_type=ecdf_axis_type,
                                  title=title,
                                  tooltips=tooltips)

    p.circle(source=source,
             x=val,
             y=y,
             **kwargs)

    if show_legend:
        if complementary:
            p.legend.location = 'top_right'
        else:
            p.legend.location = 'bottom_right'

    return p


def colored_scatter(data=None, cats=None, x=None, y=None, p=None,
                 x_axis_label=None, y_axis_label=None, title=None,
                 plot_height=300, plot_width=400,
                 palette=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2',
                          '#59a14f', '#edc948', '#b07aa1', '#ff9da7',
                          '#9c755f', '#bab0ac'],
                 order=None, show_legend=True, tooltips=None,
                 x_axis_type='linear', y_axis_type='linear', **kwargs):
    """
    Parameters
    ----------
    data : Pandas DataFrame
        DataFrame containing tidy data for plotting.
    cats : hashable or list of hashables
        Name of column(s) to use as categorical variable (x-axis).
    x : hashable
        Name of column to use as x-axis.
    y : hashable
        Name of column to use as y-axis.
    p : bokeh.plotting.Figure instance, or None (default)
        If None, create a new figure. Otherwise, populate the existing
        figure `p`.
    x_axis_label : str, default None
        Label for the x-axis. Ignored if `p` is not None.
    y_axis_label : str, default 'ECDF'
        Label for the y-axis. Ignored if `p` is not None.
    title : str, default None
        Title of the plot. Ignored if `p` is not None.
    plot_height : int, default 300
        Height of plot, in pixels. Ignored if `p` is not None.
    plot_width : int, default 450
        Width of plot, in pixels. Ignored if `p` is not None.
    palette : list of strings of hex colors, or single hex string
        If a list, color palette to use. If a single string representing
        a hex color, all glyphs are colored with that color. Default is
        the default color cycle employed by Altair.
    show_legend : bool, default False
        If True, show legend.
    order : list or None
        If not None, must be a list of unique entries in `df[cat]`. The
        order of the list specifies the order of the colors. If None,
        the colors appear in the order in which they appeared in the
        inputted DataFrame.
    tooltips : list of 2-tuples
        Specification for tooltips.
    show_legend : bool, default False
        If True, show a legend.
    x_axis_type : 'linear' or 'log'
        Type of x-axis.
    y_axis_type : 'linear' or 'log'
        Type of y-axis.
    kwargs
        Any kwargs to be passed to `p.circle()` when making the plot.

    Returns
    -------
    output : bokeh.plotting.Figure instance
        Plot populated with jitter plot or box plot.
    if formal and tooltips is not None:
        raise RuntimeError('tooltips not possible for formal ECDFs.')
    """
    cols = _check_cat_input(data, cats, x, None, tooltips, palette, kwargs)
    if y in data:
        cols += [y]
    else:
        raise RuntimeError(f'Column {y} not in inputted dataframe.')

    df = data.copy()
    source = _cat_source(df, cats, cols, None)
    _, _, color_factors = _get_cat_range(df,
                                         df.groupby(cats),
                                         order,
                                         None,
                                         False)

    if 'color' not in kwargs:
        kwargs['color'] = bokeh.transform.factor_cmap('cat',
                                                    palette=palette,
                                                    factors=color_factors)

    if show_legend:
        kwargs['legend'] = '__label'

    if p is None:
        p = bokeh.plotting.figure(plot_height=plot_height,
                                  plot_width=plot_width,
                                  x_axis_label=x_axis_label,
                                  y_axis_label=y_axis_label,
                                  x_axis_type=x_axis_type,
                                  y_axis_type=y_axis_type,
                                  title=title,
                                  tooltips=tooltips)

    p.circle(source=source,
             x=x,
             y=y,
             **kwargs)

    return p


def imshow(im, color_mapper=None, plot_height=400, plot_width=None,
           length_units='pixels', interpixel_distance=1.0,
           x_range=None, y_range=None, colorbar=False,
           no_ticks=False, x_axis_label=None, y_axis_label=None,
           title=None, flip=True, return_im=False,
           saturate_channels=True, min_intensity=None,
           max_intensity=None, display_clicks=False, record_clicks=False):
    """
    Display an image in a Bokeh figure.

    Parameters
    ----------
    im : Numpy array
        If 2D, intensity image to be displayed. If 3D, first two
        dimensions are pixel values. Last dimension can be of length
        1, 2, or 3, which specify colors.
    color_mapper : str or bokeh.models.LinearColorMapper, default None
        If `im` is an intensity image, `color_mapper` is a mapping of
        intensity to color. If None, default is 256-level Viridis.
        If `im` is a color image, then `color_mapper` can either be
        'rgb' or 'cmy' (default), for RGB or CMY merge of channels.
    plot_height : int
        Height of the plot in pixels. The width is scaled so that the
        x and y distance between pixels is the same.
    plot_width : int or None (default)
        If None, the width is scaled so that the x and y distance
        between pixels is approximately the same. Otherwise, the width
        of the plot in pixels.
    length_units : str, default 'pixels'
        The units of length in the image.
    interpixel_distance : float, default 1.0
        Interpixel distance in units of `length_units`.
    x_range : bokeh.models.Range1d instance, default None
        Range of x-axis. If None, determined automatically.
    y_range : bokeh.models.Range1d instance, default None
        Range of y-axis. If None, determined automatically.
    colorbar : bool, default False
        If True, include a colorbar.
    no_ticks : bool, default False
        If True, no ticks are displayed. See note below.
    x_axis_label : str, default None
        Label for the x-axis. If None, labeled with `length_units`.
    y_axis_label : str, default None
        Label for the y-axis. If None, labeled with `length_units`.
    title : str, default None
        The title of the plot.
    flip : bool, default True
        If True, flip image so it displays right-side up. This is
        necessary because traditionally images have their 0,0 pixel
        index in the top left corner, and not the bottom left corner.
    return_im : bool, default False
        If True, return the GlyphRenderer instance of the image being
        displayed.
    saturate_channels : bool, default True
        If True, each of the channels have their displayed pixel values
        extended to range from 0 to 255 to show the full dynamic range.
    min_intensity : int or float, default None
        Minimum possible intensity of a pixel in the image. If None,
        the image is scaled based on the dynamic range in the image.
    max_intensity : int or float, default None
        Maximum possible intensity of a pixel in the image. If None,
        the image is scaled based on the dynamic range in the image.
    display_clicks : bool, default False
        If True, display clicks to the right of the plot using
        JavaScript. The clicks are not recorded nor stored, just
        printed. If you want to store the clicks, use the
        `record_clicks()` or `draw_rois()` functions.
    record_clicks : bool, default False
        Deprecated. Use `display_clicks`.

    Returns
    -------
    p : bokeh.plotting.figure instance
        Bokeh plot with image displayed.
    im : bokeh.models.renderers.GlyphRenderer instance (optional)
        The GlyphRenderer instance of the image being displayed. This is
        only returned if `return_im` is True.

    Notes
    -----
    .. The plot area is set to closely approximate square pixels, but
       this is not always possible since Bokeh sets the plotting area
       based on the entire plot, inclusive of ticks and titles. However,
       if you choose `no_ticks` to be True, no tick or axes labels are
       present, and the pixels are displayed as square.
    """
    if record_clicks:
        warnings.warn(
            '`record_clicks` is deprecated. Use the `bi1x.viz.record_clicks()` function to store clicks. Otherwise use the `display_clicks` kwarg to print the clicks to the right of the displayed image.',
            DeprecationWarning)

    # If a single channel in 3D image, flatten and check shape
    if im.ndim == 3:
        if im.shape[2] == 1:
            im = im[:,:,0]
        elif im.shape[2] not in [2, 3]:
            raise RuntimeError('Can only display 1, 2, or 3 channels.')

    # If binary image, make sure it's int
    if im.dtype == bool:
        im = im.astype(np.uint8)

    # Get color mapper
    if im.ndim == 2:
        if color_mapper is None:
            color_mapper = bokeh.models.LinearColorMapper(
                                        bokeh.palettes.viridis(256))
        elif (type(color_mapper) == str
                and color_mapper.lower() in ['rgb', 'cmy']):
            raise RuntimeError(
                    'Cannot use rgb or cmy colormap for intensity image.')
        if min_intensity is None:
            color_mapper.low = im.min()
        else:
            color_mapper.low = min_intensity
        if max_intensity is None:
            color_mapper.high = im.max()
        else:
            color_mapper.high = max_intensity
    elif im.ndim == 3:
        if color_mapper is None or color_mapper.lower() == 'cmy':
            im = im_merge(*np.rollaxis(im, 2),
                          cmy=True,
                          im_0_min=min_intensity,
                          im_1_min=min_intensity,
                          im_2_min=min_intensity,
                          im_0_max=max_intensity,
                          im_1_max=max_intensity,
                          im_2_max=max_intensity)
        elif color_mapper.lower() == 'rgb':
            im = im_merge(*np.rollaxis(im, 2),
                          cmy=False,
                          im_0_min=min_intensity,
                          im_1_min=min_intensity,
                          im_2_min=min_intensity,
                          im_0_max=max_intensity,
                          im_1_max=max_intensity,
                          im_2_max=max_intensity)
        else:
            raise RuntimeError('Invalid color mapper for color image.')
    else:
        raise RuntimeError(
                    'Input image array must have either 2 or 3 dimensions.')

    # Get shape, dimensions
    n, m = im.shape[:2]
    if x_range is not None and y_range is not None:
        dw = x_range[1] - x_range[0]
        dh = y_range[1] - y_range[0]
    else:
        dw = m * interpixel_distance
        dh = n * interpixel_distance
        x_range = [0, dw]
        y_range = [0, dh]

    # Set up figure with appropriate dimensions
    if plot_width is None:
        plot_width = int(m/n * plot_height)
    if colorbar:
        plot_width += 40
        toolbar_location = 'above'
    else:
        toolbar_location = 'right'
    p = bokeh.plotting.figure(plot_height=plot_height,
                              plot_width=plot_width,
                              x_range=x_range,
                              y_range=y_range,
                              title=title,
                              toolbar_location=toolbar_location,
                              tools='pan,box_zoom,wheel_zoom,save,reset')
    if no_ticks:
        p.xaxis.major_label_text_font_size = '0pt'
        p.yaxis.major_label_text_font_size = '0pt'
        p.xaxis.major_tick_line_color = None
        p.xaxis.minor_tick_line_color = None
        p.yaxis.major_tick_line_color = None
        p.yaxis.minor_tick_line_color = None
    else:
        if x_axis_label is None:
            p.xaxis.axis_label = length_units
        else:
            p.xaxis.axis_label = x_axis_label
        if y_axis_label is None:
            p.yaxis.axis_label = length_units
        else:
            p.yaxis.axis_label = y_axis_label

    # Display the image
    if im.ndim == 2:
        if flip:
            im = im[::-1,:]
        im_bokeh = p.image(image=[im],
                           x=x_range[0],
                           y=y_range[0],
                           dw=dw,
                           dh=dh,
                           color_mapper=color_mapper)
    else:
        im_bokeh = p.image_rgba(image=[rgb_to_rgba32(im, flip=flip)],
                                x=x_range[0],
                                y=y_range[0],
                                dw=dw,
                                dh=dh)

    # Make a colorbar
    if colorbar:
        if im.ndim == 3:
            warnings.warn('No colorbar display for RGB images.')
        else:
            color_bar = bokeh.models.ColorBar(color_mapper=color_mapper,
                                              label_standoff=12,
                                              border_line_color=None,
                                              location=(0,0))
            p.add_layout(color_bar, 'right')

    if record_clicks or display_clicks:
        div = bokeh.models.Div(width=200)
        layout = bokeh.layouts.row(p, div)
        p.js_on_event(bokeh.events.Tap,
                      _display_clicks(div, attributes=['x', 'y']))
        if return_im:
            return layout, im_bokeh
        else:
            return layout

    if return_im:
        return p, im_bokeh
    return p


def record_clicks(im, notebook_url='localhost:8888', point_size=3,
            table_height=200, crosshair_alpha=0.5,
            point_color='white', color_mapper=None, plot_height=400,
            plot_width=None, length_units='pixels', interpixel_distance=1.0,
            x_range=None, y_range=None, colorbar=False, no_ticks=False,
            x_axis_label=None, y_axis_label=None, title=None, flip=False,
            saturate_channels=True, min_intensity=None, max_intensity=None):
    """Display and record mouse clicks on a Bokeh plot of an image.

    Parameters
    ----------
    im : 2D Numpy array
        Image to display while clicking.
    notebook_url : str, default 'localhost:8888'
        URL of notebook for display.
    point_size : int, default 3
        Size of points to display when clicking.
    table_height : int, default 200
        Height, in pixels, of table displaying mouse click locations.
    crosshair_alpha : float, default 0.5
        Opacity value for crosshairs when using the crosshair tool.
    point_color : str, default 'white'
        Color of the points displaying clicks.
    color_mapper : str or bokeh.models.LinearColorMapper, default None
        If `im` is an intensity image, `color_mapper` is a mapping of
        intensity to color. If None, default is 256-level Viridis.
        If `im` is a color image, then `color_mapper` can either be
        'rgb' or 'cmy' (default), for RGB or CMY merge of channels.
    plot_height : int
        Height of the plot in pixels. The width is scaled so that the
        x and y distance between pixels is the same.
    plot_width : int or None (default)
        If None, the width is scaled so that the x and y distance
        between pixels is approximately the same. Otherwise, the width
        of the plot in pixels.
    length_units : str, default 'pixels'
        The units of length in the image.
    interpixel_distance : float, default 1.0
        Interpixel distance in units of `length_units`.
    x_range : bokeh.models.Range1d instance, default None
        Range of x-axis. If None, determined automatically.
    y_range : bokeh.models.Range1d instance, default None
        Range of y-axis. If None, determined automatically.
    colorbar : bool, default False
        If True, include a colorbar.
    no_ticks : bool, default False
        If True, no ticks are displayed. See note below.
    x_axis_label : str, default None
        Label for the x-axis. If None, labeled with `length_units`.
    y_axis_label : str, default None
        Label for the y-axis. If None, labeled with `length_units`.
    title : str, default None
        The title of the plot.
    flip : bool, default False
        If True, flip image so it displays right-side up. This is
        necessary because traditionally images have their 0,0 pixel
        index in the top left corner, and not the bottom left corner.
        If you are going to use the clicks you record in further image
        processing applicaitons, you should have `flip` set to False.
    saturate_channels : bool, default True
        If True, each of the channels have their displayed pixel values
        extended to range from 0 to 255 to show the full dynamic range.
    min_intensity : int or float, default None
        Minimum possible intensity of a pixel in the image. If None,
        the image is scaled based on the dynamic range in the image.
    max_intensity : int or float, default None
        Maximum possible intensity of a pixel in the image. If None,
        the image is scaled based on the dynamic range in the image.

    Returns
    -------
    output : Bokeh ColumnDataSource
        A Bokeh ColumnDataSource instance. This can be immediately
        converted to a Pandas DataFrame using the `to_df()` method. For
        example, `output.to_df()`.
    """
    points_source = bokeh.models.ColumnDataSource({'x': [], 'y': []})

    def modify_doc(doc):
        p = imshow(im,
                   color_mapper=color_mapper,
                   plot_height=plot_height,
                   plot_width=plot_width,
                   length_units=length_units,
                   interpixel_distance=interpixel_distance,
                   x_range=x_range,
                   y_range=y_range,
                   colorbar=colorbar,
                   no_ticks=no_ticks,
                   x_axis_label=x_axis_label,
                   y_axis_label=y_axis_label,
                   title=title,
                   flip=flip,
                   return_im=False,
                   saturate_channels=saturate_channels,
                   min_intensity=min_intensity,
                   max_intensity=max_intensity)

        view = bokeh.models.CDSView(source=points_source)

        renderer = p.scatter(x='x', y='y', source=points_source, view=view,
                             color=point_color, size=point_size)

        columns = [bokeh.models.TableColumn(field='x', title='x'),
                   bokeh.models.TableColumn(field='y', title='y')]

        table = bokeh.models.DataTable(source=points_source,
                                       columns=columns,
                                       editable=True,
                                       height=table_height)

        draw_tool = bokeh.models.PointDrawTool(renderers=[renderer])
        p.add_tools(draw_tool)
        p.add_tools(bokeh.models.CrosshairTool(line_alpha=crosshair_alpha))
        p.toolbar.active_tap = draw_tool

        doc.add_root(bokeh.layouts.column(p, table))

    bokeh.io.show(modify_doc, notebook_url=notebook_url)

    return points_source


def draw_rois(im, notebook_url='localhost:8888', table_height=100,
            crosshair_tool_alpha=0.5,
            color='white', fill_alpha=0.1, vertex_color='red',
            vertex_size=10, color_mapper=None, plot_height=400,
            plot_width=None, length_units='pixels', interpixel_distance=1.0,
            x_range=None, y_range=None, colorbar=False, no_ticks=False,
            x_axis_label=None, y_axis_label=None, title=None, flip=False,
            saturate_channels=True, min_intensity=None, max_intensity=None):
    """Draw and record polygonal regions of interest on a plot of a
    Bokeh image.

    Parameters
    ----------
    im : 2D Numpy array
        Image to display while clicking.
    notebook_url : str, default 'localhost:8888'
        URL of notebook for display.
    table_height : int, default 200
        Height, in pixels, of table displaying polygon vertex locations.
    crosshair_alpha : float, default 0.5
        Opacity value for crosshairs when using the crosshair tool.
    color : str, default 'white'
        Color of the ROI polygons (lines and fill).
    fill_alpha : float, default 0.1
        Opacity of drawn ROI polygons.
    vertex_color : str, default 'red'
        Color of vertices of the ROI polygons while using the polygon
        edit tool.
    vertex_size: int, default 10
        Size, in pixels, of vertices of the ROI polygons while using the
        polygon edit tool.
    color_mapper : str or bokeh.models.LinearColorMapper, default None
        If `im` is an intensity image, `color_mapper` is a mapping of
        intensity to color. If None, default is 256-level Viridis.
        If `im` is a color image, then `color_mapper` can either be
        'rgb' or 'cmy' (default), for RGB or CMY merge of channels.
    plot_height : int
        Height of the plot in pixels. The width is scaled so that the
        x and y distance between pixels is the same.
    plot_width : int or None (default)
        If None, the width is scaled so that the x and y distance
        between pixels is approximately the same. Otherwise, the width
        of the plot in pixels.
    length_units : str, default 'pixels'
        The units of length in the image.
    interpixel_distance : float, default 1.0
        Interpixel distance in units of `length_units`.
    x_range : bokeh.models.Range1d instance, default None
        Range of x-axis. If None, determined automatically.
    y_range : bokeh.models.Range1d instance, default None
        Range of y-axis. If None, determined automatically.
    colorbar : bool, default False
        If True, include a colorbar.
    no_ticks : bool, default False
        If True, no ticks are displayed. See note below.
    x_axis_label : str, default None
        Label for the x-axis. If None, labeled with `length_units`.
    y_axis_label : str, default None
        Label for the y-axis. If None, labeled with `length_units`.
    title : str, default None
        The title of the plot.
    flip : bool, default False
        If True, flip image so it displays right-side up. This is
        necessary because traditionally images have their 0,0 pixel
        index in the top left corner, and not the bottom left corner.
        If you are going to use the clicks you record in further image
        processing applicaitons, you should have `flip` set to False.
    saturate_channels : bool, default True
        If True, each of the channels have their displayed pixel values
        extended to range from 0 to 255 to show the full dynamic range.
    min_intensity : int or float, default None
        Minimum possible intensity of a pixel in the image. If None,
        the image is scaled based on the dynamic range in the image.
    max_intensity : int or float, default None
        Maximum possible intensity of a pixel in the image. If None,
        the image is scaled based on the dynamic range in the image.

    Returns
    -------
    output : Bokeh ColumnDataSource
        A Bokeh ColumnDataSource instance. This can be immediately
        converted to a Pandas DataFrame `roicds_to_df()` function. For
        example, `bi1x.viz.roicds_to_df(output)`.

    Notes
    -----
    .. The displayed table is not particularly useful because it
       displays a list of points. It helps to make sure your clicks are
       getting registered and to select which ROI number is which
       polygon.
    """

    poly_source = bokeh.models.ColumnDataSource({'xs': [], 'ys': []})

    def modify_doc(doc):
        p = imshow(im,
                   color_mapper=color_mapper,
                   plot_height=plot_height,
                   plot_width=plot_width,
                   length_units=length_units,
                   interpixel_distance=interpixel_distance,
                   x_range=x_range,
                   y_range=y_range,
                   colorbar=colorbar,
                   no_ticks=no_ticks,
                   x_axis_label=x_axis_label,
                   y_axis_label=y_axis_label,
                   title=title,
                   flip=flip,
                   return_im=False,
                   saturate_channels=saturate_channels,
                   min_intensity=min_intensity,
                   max_intensity=max_intensity)

        view = bokeh.models.CDSView(source=poly_source)
        renderer = p.patches(xs='xs', ys='ys', source=poly_source, view=view,
                             fill_alpha=fill_alpha, color=color)
        vertex_renderer = p.circle([], [], size=vertex_size, color='red')

        columns = [bokeh.models.TableColumn(field='xs', title='xs'),
                   bokeh.models.TableColumn(field='ys', title='ys')]

        table = bokeh.models.DataTable(source=poly_source,
                                       index_header='roi',
                                       columns=columns,
                                       height=table_height)
        draw_tool = bokeh.models.PolyDrawTool(renderers=[renderer])
        edit_tool = bokeh.models.PolyEditTool(renderers=[renderer],
                                              vertex_renderer=vertex_renderer)
        p.add_tools(draw_tool)
        p.add_tools(edit_tool)
        p.add_tools(bokeh.models.CrosshairTool(line_alpha=crosshair_tool_alpha))
        p.toolbar.active_tap = draw_tool

        doc.add_root(bokeh.layouts.column(p, table))

    bokeh.io.show(modify_doc, notebook_url=notebook_url)

    return poly_source


def roicds_to_df(cds):
    """Convert a ColumnDataSource outputted by `draw_rois()` to a Pandas
    DataFrame.

    Parameter
    ---------
    cds : Bokeh ColumnDataSource
        ColumnDataSource outputted by `draw_rois()`

    Returns
    -------
    output : Pandas DataFrame
        DataFrame with columns ['roi', 'x', 'y'] containing the
        positions of the vertices of the respective polygonal ROIs.
    """
    roi = np.concatenate([[i]*len(x_data) for i, x_data in enumerate(cds.data['xs'])])
    x = np.concatenate(cds.data['xs'])
    y = np.concatenate(cds.data['ys'])

    return pd.DataFrame(data=dict(roi=roi, x=x, y=y))


def im_merge(im_0, im_1, im_2=None, im_0_max=None,
             im_1_max=None, im_2_max=None, im_0_min=None,
             im_1_min=None, im_2_min=None, cmy=True):
    """
    Merge channels to make RGB image.

    Parameters
    ----------
    im_0: array_like
        Image represented in first channel.  Must be same shape
        as `im_1` and `im_2` (if not None).
    im_1: array_like
        Image represented in second channel.  Must be same shape
        as `im_1` and `im_2` (if not None).
    im_2: array_like, default None
        Image represented in third channel.  If not None, must be same
        shape as `im_0` and `im_1`.
    im_0_max : float, default max of inputed first channel
        Maximum value to use when scaling the first channel. If None,
        scaled to span entire range.
    im_1_max : float, default max of inputed second channel
        Maximum value to use when scaling the second channel
    im_2_max : float, default max of inputed third channel
        Maximum value to use when scaling the third channel
    im_0_min : float, default min of inputed first channel
        Maximum value to use when scaling the first channel
    im_1_min : float, default min of inputed second channel
        Minimum value to use when scaling the second channel
    im_2_min : float, default min of inputed third channel
        Minimum value to use when scaling the third channel
    cmy : bool, default True
        If True, first channel is cyan, second is magenta, and third is
        yellow. Otherwise, first channel is red, second is green, and
        third is blue.

    Returns
    -------
    output : array_like, dtype float, shape (*im_0.shape, 3)
        RGB image.
    """

    # Compute max intensities if needed
    if im_0_max is None:
        im_0_max = im_0.max()
    if im_1_max is None:
        im_1_max = im_1.max()
    if im_2 is not None and im_2_max is None:
        im_2_max = im_2.max()

    # Compute min intensities if needed
    if im_0_min is None:
        im_0_min = im_0.min()
    if im_1_min is None:
        im_1_min = im_1.min()
    if im_2 is not None and im_2_min is None:
        im_2_min = im_2.min()

    # Make sure maxes are ok
    if im_0_max < im_0.max() or im_1_max < im_1.max() \
            or (im_2 is not None and im_2_max < im_2.max()):
        raise RuntimeError(
                'Inputted max of channel < max of inputted channel.')

    # Make sure mins are ok
    if im_0_min > im_0.min() or im_1_min > im_1.min() \
            or (im_2 is not None and im_2_min > im_2.min()):
        raise RuntimeError(
                'Inputted min of channel > min of inputted channel.')

    # Scale the images
    if im_0_max > im_0_min:
        im_0 = (im_0 - im_0_min) / (im_0_max - im_0_min)
    else:
        im_0 = (im_0 > 0).astype(float)

    if im_1_max > im_1_min:
        im_1 = (im_1 - im_1_min) / (im_1_max - im_1_min)
    else:
        im_0 = (im_0 > 0).astype(float)

    if im_2 is None:
        im_2 = np.zeros_like(im_0)
    elif im_2_max > im_2_min:
        im_2 = (im_2 - im_2_min) / (im_2_max - im_2_min)
    else:
        im_0 = (im_0 > 0).astype(float)

    # Convert images to RGB
    if cmy:
        im_c = np.stack((np.zeros_like(im_0), im_0, im_0), axis=2)
        im_m = np.stack((im_1, np.zeros_like(im_1), im_1), axis=2)
        im_y = np.stack((im_2, im_2, np.zeros_like(im_2)), axis=2)
        im_rgb = im_c + im_m + im_y
        for i in [0, 1, 2]:
            im_rgb[:,:,i] /= im_rgb[:,:,i].max()
    else:
        im_rgb = np.empty((*im_0.shape, 3))
        im_rgb[:,:,0] = im_0
        im_rgb[:,:,1] = im_1
        im_rgb[:,:,2] = im_2

    return im_rgb


def rgb_to_rgba32(im, flip=True):
    """
    Convert an RGB image to a 32 bit-encoded RGBA image.

    Parameters
    ----------
    im : ndarray, shape (nrows, ncolums, 3)
        Input image. All pixel values must be between 0 and 1.
    flip : bool, default True
        If True, flip image so it displays right-side up. This is
        necessary because traditionally images have their 0,0 pixel
        index in the top left corner, and not the bottom left corner.

    Returns
    -------
    output : ndarray, shape (nros, ncolumns), dtype np.uint32
        Image decoded as a 32 bit RBGA image.
    """
    # Ensure it has three channels
    if im.ndim != 3 or im.shape[2] !=3:
        raise RuntimeError('Input image is not RGB.')

    # Make sure all entries between zero and one
    if (im < 0).any() or (im > 1).any():
        raise RuntimeError('All pixel values must be between 0 and 1.')

    # Get image shape
    n, m, _ = im.shape

    # Convert to 8-bit, which is expected for viewing
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        im_8 = skimage.img_as_ubyte(im)

    # Add the alpha channel, which is expected by Bokeh
    im_rgba = np.stack((*np.rollaxis(im_8, 2),
                        255*np.ones((n, m), dtype=np.uint8)), axis=2)

    # Reshape into 32 bit. Must flip up/down for proper orientation
    if flip:
        return np.flipud(im_rgba.view(dtype=np.int32).reshape((n, m)))
    else:
        return im_rgba.view(dtype=np.int32).reshape((n, m))


def rgb_frac_to_hex(rgb_frac):
    """
    Convert fractional RGB values to hexidecimal color string.

    Parameters
    ----------
    rgb_frac : array_like, shape (3,)
        Fractional RGB values; each entry is between 0 and 1.

    Returns
    -------
    str
        Hexidecimal string for the given RGB color.

    Examples
    --------
    >>> rgb_frac_to_hex((0.65, 0.23, 1.0))
    '#a53aff'

    >>> rgb_frac_to_hex((1.0, 1.0, 1.0))
    '#ffffff'
    """

    if len(rgb_frac) != 3:
        raise RuntimeError('`rgb_frac` must have exactly three entries.')

    if (np.array(rgb_frac) < 0).any() or (np.array(rgb_frac) > 1).any():
        raise RuntimeError('RGB values must be between 0 and 1.')

    return '#{0:02x}{1:02x}{2:02x}'.format(int(rgb_frac[0] * 255),
                                           int(rgb_frac[1] * 255),
                                           int(rgb_frac[2] * 255))


def boxwhisker(data, cats, val, p=None, horizontal=False, x_axis_label=None,
        y_axis_label=None, title=None, plot_height=300, plot_width=400,
        palette=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f',
                 '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac'],
        width=0.4, order=None, val_axis_type='linear', display_outliers=True,
        box_kwargs=None, whisker_kwargs=None, outlier_kwargs=None):
    """Deprecated, see `box`."""
    warnings.warn('`boxwhisker` is deprecated and will be removed in future versions. Use `box`.', DeprecationWarning)

    return box(data, cats, val, p, horizontal, x_axis_label, y_axis_label,
               title, plot_height, plot_width, palette, width, order,
               val_axis_type, display_outliers, box_kwargs, whisker_kwargs,
               outlier_kwargs)


def mpl_cmap_to_color_mapper(cmap):
    """
    Convert a Matplotlib colormap to a bokeh.models.LinearColorMapper
    instance.

    Parameters
    ----------
    cmap : str
        A string giving the name of the color map.

    Returns
    -------
    output : bokeh.models.LinearColorMapper instance
        A linear color_mapper with 25 gradations.

    Notes
    -----
    .. See https://matplotlib.org/examples/color/colormaps_reference.html
       for available Matplotlib colormaps.
    """
    cm = mpl_get_cmap(cmap)
    palette = [rgb_frac_to_hex(cm(i)[:3]) for i in range(256)]
    return bokeh.models.LinearColorMapper(palette=palette)


def _ecdf_vals(data, formal=False, complementary=False):
    """Get x, y, values of an ECDF for plotting.
    Parameters
    ----------
    data : ndarray
        One dimensional Numpy array with data.
    formal : bool, default False
        If True, generate x and y values for formal ECDF (staircase). If
        False, generate x and y values for ECDF as dots.
    complementary : bool
        If True, return values for ECCDF.

    Returns
    -------
    x : ndarray
        x-values for plot
    y : ndarray
        y-values for plot
    """
    x = np.sort(data)
    y = np.arange(1, len(data)+1) / len(data)

    if formal:
        x, y = _to_formal(x, y)
        if complementary:
            y = 1 - y
    elif complementary:
        y = 1 - y + 1/len(y)

    return x, y


@numba.jit(nopython=True)
def _ecdf_arbitrary_points(data, x):
    """Give the value of an ECDF at arbitrary points x."""
    y = np.arange(len(data) + 1) / len(data)
    return y[np.searchsorted(np.sort(data), x, side='right')]


def _ecdf_from_samples(df, name, ptiles, x):
    """Compute ECDFs and percentiles from samples."""
    df_ecdf = pd.DataFrame()
    df_ecdf_vals = pd.DataFrame()
    grouped = df.groupby(['chain', 'chain_idx'])
    for i, g in grouped:
        df_ecdf_vals[i] = _ecdf_arbitrary_points(g[name].values, x)

    for ptile in ptiles:
        df_ecdf[str(ptile)] = df_ecdf_vals.quantile(
                            ptile/100, axis=1, interpolation='higher')
    df_ecdf['x'] = x

    return df_ecdf


def _to_formal(x, y):
    """Convert to formal ECDF."""
    # Set up output arrays
    x_formal = np.empty(2*len(x))
    y_formal = np.empty(2*len(x))

    # y-values for steps
    y_formal[0] = 0
    y_formal[1::2] = y
    y_formal[2::2] = y[:-1]

    # x- values for steps
    x_formal[::2] = x
    x_formal[1::2] = x

    return x_formal, y_formal


@numba.jit(nopython=True)
def _y_ecdf(data, x):
    y = np.arange(len(data) + 1) / len(data)
    return y[np.searchsorted(np.sort(data), x, side='right')]


@numba.jit(nopython=True)
def _draw_ecdf_bootstrap(L, n, n_bs_reps=100000):
    x = np.arange(L+1)
    ys = np.empty((n_bs_reps, len(x)))
    for i in range(n_bs_reps):
        draws = np.random.randint(0, L+1, size=n)
        ys[i, :] = _y_ecdf(draws, x)
    return ys


def _ecdf_diff(data, L, formal=False):
    x, y = _ecdf_vals(data)
    y_uniform = (x + 1)/L
    if formal:
        x, y = _to_formal(x, y)
        _, y_uniform = _to_formal(np.arange(len(data)), y_uniform)
    y -= y_uniform

    return x, y


def _get_cat_range(df, grouped, order, color_column, horizontal):
    if order is None:
        if isinstance(list(grouped.groups.keys())[0], tuple):
            factors = tuple([tuple([str(k) for k in key])
                                for key in grouped.groups.keys()])
        else:
            factors = tuple([str(key) for key in grouped.groups.keys()])
    else:
        if type(order[0]) in [list, tuple]:
            factors = tuple([tuple([str(k) for k in key]) for key in order])
        else:
            factors = tuple([str(entry) for entry in order])

    if horizontal:
        cat_range = bokeh.models.FactorRange(*(factors[::-1]))
    else:
        cat_range = bokeh.models.FactorRange(*factors)

    if color_column is None:
        color_factors = factors
    else:
        color_factors = tuple(sorted(list(
                                df[color_column].unique().astype(str))))

    return cat_range, factors, color_factors


def _cat_figure(df, grouped, plot_height, plot_width, x_axis_label,
                y_axis_label, title, order, color_column, tooltips,
                horizontal, val_axis_type):
    fig_kwargs = dict(plot_height=plot_height,
                      plot_width=plot_width,
                      x_axis_label=x_axis_label,
                      y_axis_label=y_axis_label,
                      title=title,
                      tooltips=tooltips)

    cat_range, factors, color_factors = _get_cat_range(df,
                                                       grouped,
                                                       order,
                                                       color_column,
                                                       horizontal)

    if horizontal:
        fig_kwargs['y_range'] = cat_range
        fig_kwargs['x_axis_type'] = val_axis_type
    else:
        fig_kwargs['x_range'] = cat_range
        fig_kwargs['y_axis_type'] = val_axis_type

    return bokeh.plotting.figure(**fig_kwargs), factors, color_factors


def _cat_source(df, cats, cols, color_column):
    if type(cats) in [list, tuple]:
        cat_source = list(zip(*tuple([df[cat].astype(str) for cat in cats])))
        labels = [', '.join(cat) for cat in cat_source]
    else:
        cat_source = list(df[cats].astype(str).values)
        labels = cat_source

    if type(cols) in [list, tuple, pd.core.indexes.base.Index]:
        source_dict = {col: list(df[col].values) for col in cols}
    else:
        source_dict = {cols: list(df[cols].values)}

    source_dict['cat'] = cat_source
    if color_column in [None, 'cat']:
        source_dict['__label'] = labels
    else:
        source_dict['__label'] = list(df[color_column].astype(str).values)
        source_dict[color_column] = list(df[color_column].astype(str).values)

    return bokeh.models.ColumnDataSource(source_dict)


def _tooltip_cols(tooltips):
    if tooltips is None:
        return []
    if type(tooltips) not in [list, tuple]:
        raise RuntimeError(
                '`tooltips` must be a list or tuple of two-tuples.')

    cols = []
    for tip in tooltips:
        if type(tip) not in [list, tuple] or len(tip) != 2:
            raise RuntimeError('Invalid tooltip.')
        if tip[1][0] == '@':
            if tip[1][1] == '{':
                cols.append(tip[1][2:tip[1].find('}')])
            elif '{' in tip[1]:
                cols.append(tip[1][1:tip[1].find('{')])
            else:
                cols.append(tip[1][1:])

    return cols


def _cols_to_keep(cats, val, color_column, tooltips):
    cols = _tooltip_cols(tooltips)
    cols += [val]

    if type(cats) in [list, tuple]:
        cols += list(cats)
    else:
        cols += [cats]

    if color_column is not None:
        cols += [color_column]

    return list(set(cols))


def _check_cat_input(df, cats, val, color_column, tooltips, palette, kwargs):
    if df is None:
        raise RuntimeError('`df` argument must be provided.')
    if cats is None:
        raise RuntimeError('`cats` argument must be provided.')
    if val is None:
        raise RuntimeError('`val` argument must be provided.')

    if type(palette) not in [list, tuple]:
        raise RuntimeError('`palette` must be a list or tuple.')

    if val not in df.columns:
        raise RuntimeError(
            f'{val} is not a column in the inputted data frame')

    cats_array = type(cats) in [list, tuple]

    if cats_array:
        for cat in cats:
            if cat not in df.columns:
                raise RuntimeError(
                        f'{cat} is not a column in the inputted data frame')
    else:
        if cats not in df.columns:
            raise RuntimeError(
                        f'{cats} is not a column in the inputted data frame')

    if color_column is not None and color_column not in df.columns:
        raise RuntimeError(
                f'{color_column} is not a column in the inputted data frame')

    cols = _cols_to_keep(cats, val, color_column, tooltips)

    for col in cols:
        if col not in df.columns:
            raise RuntimeError(
                    f'{col} is not a column in the inputted data frame')

    bad_kwargs = ['x', 'y', 'source', 'cat', 'legend']
    if (kwargs is not None
            and any([key in kwargs for key in bad_kwargs])):
        raise RuntimeError(', '.join(bad_kwargs) + ' are not allowed kwargs.')

    if val == 'cat':
        raise RuntimeError("`'cat'` cannot be used as `val`.")

    if (    val == '__label'
         or (cats == '__label' or (cats_array and '__label' in cats))):
        raise RuntimeError("'__label' cannot be used for `val` or `cats`.")

    return cols


def _outliers(data):
    bottom, middle, top = np.percentile(data, [25, 50, 75])
    iqr = top - bottom
    top_whisker = min(top + 1.5*iqr, data.max())
    bottom_whisker = max(bottom - 1.5*iqr, data.min())
    outliers = data[(data > top_whisker) | (data < bottom_whisker)]
    return outliers


def _box_and_whisker(data):
    middle = data.median()
    bottom = data.quantile(0.25)
    top = data.quantile(0.75)
    iqr = top - bottom
    top_whisker = min(top + 1.5*iqr, data.max())
    bottom_whisker = max(bottom - 1.5*iqr, data.min())
    return pd.Series({'middle': middle,
                      'bottom': bottom,
                      'top': top,
                      'top_whisker': top_whisker,
                      'bottom_whisker': bottom_whisker})


def _box_source(df, cats, val, cols):
    """Construct a data frame for making box plot."""

    # Need to reset index for use in slicing outliers
    df_source = df.reset_index(drop=True)

    if type(cats) in [list, tuple]:
        level = list(range(len(cats)))
    else:
        level = 0

    if cats is None:
        grouped = df_source
    else:
        grouped = df_source.groupby(cats)

    # Data frame for boxes and whiskers
    df_box = grouped[val].apply(_box_and_whisker).unstack().reset_index()
    source_box = _cat_source(df_box,
                             cats,
                             ['middle', 'bottom', 'top',
                              'top_whisker', 'bottom_whisker'],
                             None)

    # Data frame for outliers
    df_outliers = grouped[val].apply(_outliers).reset_index(level=level)
    df_outliers[cols] = df_source.loc[df_outliers.index, cols]
    source_outliers = _cat_source(df_outliers, cats, cols, None)

    return source_box, source_outliers


def _ecdf_y(data, complementary=False):
    """Give y-values of an ECDF for an unsorted column in a data frame.

    Parameters
    ----------
    data : Pandas Series
        Series (or column of a DataFrame) from which to generate ECDF
        values
    complementary : bool, default False
        If True, give the ECCDF values.

    Returns
    -------
    output : Pandas Series
        Corresponding y-values for an ECDF when plotted with dots.

    Notes
    -----
    .. This only works for plotting an ECDF with points, not for formal
       ECDFs
    """
    if complementary:
        return 1 - data.rank(method='first') / len(data) + 1 / len(data)
    else:
        return data.rank(method='first') / len(data)


def _point_ecdf_source(data, val, cats, cols, complementary, colored):
    """DataFrame for making point-wise ECDF."""
    df = data.copy()

    if complementary:
        col = '__ECCDF'
    else:
        col = '__ECDF'

    if cats is None or colored:
        df[col] = _ecdf_y(df[val], complementary)
    else:
        df[col] = df.groupby(cats)[val].transform(_ecdf_y, complementary)

    cols += [col]

    return _cat_source(df, cats, cols, None)


def _ecdf_collection_dots(df, val, cats, cols, complementary, order, palette,
                          show_legend, y, p, **kwargs):
    _, _, color_factors = _get_cat_range(df,
                                         df.groupby(cats),
                                         order,
                                         None,
                                         False)

    source = _point_ecdf_source(df, val, cats, cols, complementary, False)

    if 'color' not in kwargs:
        kwargs['color'] = bokeh.transform.factor_cmap('cat',
                                                    palette=palette,
                                                    factors=color_factors)

    if show_legend:
        kwargs['legend'] = '__label'

    p.circle(source=source,
             x=val,
             y=y,
             **kwargs)

    return p


def _ecdf_collection_formal(df, val, cats, complementary, order, palette,
                            show_legend, p, **kwargs):
    grouped = df.groupby(cats)

    color_not_in_kwargs = 'color' not in kwargs

    if order is None:
        order = list(grouped.groups.keys())
    grouped_iterator = [(order_val, grouped.get_group(order_val))
                        for order_val in order]

    for i, g in enumerate(grouped_iterator):
        if show_legend:
            if type(g[0]) == tuple:
                legend = ', '.join([str(c) for c in g[0]])
            else:
                legend = str(g[0])
        else:
            legend = None

        if color_not_in_kwargs:
            kwargs['color'] = palette[i % len(palette)]

        ecdf(g[1][val],
             formal=True,
             p=p,
             legend=legend,
             complementary=complementary,
             **kwargs)

    return p


def _display_clicks(div, attributes=[],
                    style='float:left;clear:left;font_size=0.5pt'):
    """Build a suitable CustomJS to display the current event
    in the div model."""
    return bokeh.models.CustomJS(args=dict(div=div), code="""
        var attrs = %s; var args = [];
        for (var i=0; i<attrs.length; i++ ) {
            args.push(Number(cb_obj[attrs[i]]).toFixed(4));
        }
        var line = "<span style=%r>[" + args.join(", ") + "], </span>\\n";
        var text = div.text.concat(line);
        var lines = text.split("\\n")
        if ( lines.length > 35 ) { lines.shift(); }
        div.text = lines.join("\\n");
    """ % (attributes, style))


def _data_range(df, x, y, margin=0.02):
    x_range = df[x].max() - df[x].min()
    y_range = df[y].max() - df[y].min()
    return ([df[x].min() - x_range*margin, df[x].max() + x_range*margin],
            [df[y].min() - y_range*margin, df[y].max() + y_range*margin])


def im_click(im, color_mapper=None, plot_height=400, plot_width=None,
             length_units='pixels', interpixel_distance=1.0,
             x_range=None, y_range=None,
             no_ticks=False, x_axis_label=None, y_axis_label=None,
             title=None, flip=True):
    """
    """

    warnings.warn('`im_click` is deprecated. Use `imshow` instead.',
                  DeprecationWarning)

    def display_event(div, attributes=[],
                      style='float:left;clear:left;font_size=0.5pt'):
        """Build a suitable CustomJS to display the current event
        in the div model."""
        return bokeh.models.CustomJS(args=dict(div=div), code="""
            var attrs = %s; var args = [];
            for (var i=0; i<attrs.length; i++ ) {
                args.push(Number(cb_obj[attrs[i]]).toFixed(4));
            }
            var line = "<span style=%r>[" + args.join(", ") + "],</span>\\n";
            var text = div.text.concat(line);
            var lines = text.split("\\n")
            if ( lines.length > 35 ) { lines.shift(); }
            div.text = lines.join("\\n");
        """ % (attributes, style))

    p = imshow(im,
               color_mapper=color_mapper,
               plot_height=plot_height,
               plot_width=plot_width,
               length_units=length_units,
               interpixel_distance=interpixel_distance,
               x_range=x_range,
               y_range=y_range,
               no_ticks=no_ticks,
               x_axis_label=x_axis_label,
               y_axis_label=y_axis_label,
               title=title,
               flip=flip)

    div = bokeh.models.Div(width=200)
    layout = bokeh.layouts.row(p, div)

    p.js_on_event(bokeh.events.Tap, display_event(div, attributes=['x', 'y']))

    return layout
