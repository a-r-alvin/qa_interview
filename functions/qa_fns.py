import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def color_negative_red(val):
    '''
    Takes a scalar and returns a string with the css property `'color: red'` for negative strings, black otherwise.
    Source: pandas.pydata.org/pandas-docs/version/1.1.5/user_guide/style.html.
    '''
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color


def highlight(srs: pd.Series, light_colour: str, dark_colour: str):
    return ['background-color: {}'.format(light_colour if i % 2 == 0 else dark_colour) for i in range(len(srs))]


def sales_dataframe_styler(df: pd.DataFrame, period_id_0: str, period_id_1: str) -> pd.DataFrame:
    gradient_fill_colnames = ['{}_>_{}_frac'.format(period_id_1, period_id_0)]
    return df.style.background_gradient(
        cmap=sns.color_palette('RdYlGn', as_cmap=True),
        subset=list(set(df.columns).intersection(set(gradient_fill_colnames)))
    ).format(
        "{:+,.2%}", subset=[colname for colname in df.columns if 'rel_change_sales' in colname]
    ).format(
        "£{:,.2f}", subset=[colname for colname in df.columns if colname[:6] == 'sales_']
    ).format(
        "£{:+,.2f}", subset=[colname for colname in df.columns if 'Δ_sales' in colname]
    ).format(
        "{:,.0f}", subset=[colname for colname in df.columns if colname[:9] == 'n_orders_']
    ).applymap(
        color_negative_red,
        subset=list(set(df.columns) - set(gradient_fill_colnames))
    ).apply(
        highlight,
        light_colour='#fffec7',
        dark_colour='#f5f4bf',
        subset=[colname for colname in df.columns if 'Δ_sales' in colname]
    ).apply(
        highlight,
        light_colour='#deefff',
        dark_colour='#d5e6f5',
        subset=[colname for colname in df.columns if 'rel_change_sales' in colname]
    )


def seaborn_histplot_grid(df: pd.DataFrame, value_colname: str, groupby_colname: str, groupby_categories: list):
    '''
    Plot histograms in a grid using seaborn. Prettier than `pd.DataFrame.hist()`.
    '''
    # Assuming the screen is wide enough to fit around 4 columns of plots side by side, set the number of rows accordingly.
    n_col = 4
    n_row = int(np.ceil(len(groupby_categories) / n_col))

    fix, axes = plt.subplots(n_row, n_col, figsize=(15, 7))
    
    for i, category in enumerate(groupby_categories):
        srs = df.loc[df[groupby_colname] == category][value_colname]
        percentiles = np.percentile(srs, q=[1, 99])
        sns.histplot(
            srs[srs.between(percentiles[0], percentiles[1])],
            ax=axes[i // n_col, i % n_col],
            kde=True,
            legend=False
        ).set(title=category, xlabel=None, ylabel=None)

    plt.tight_layout(pad=0.4, w_pad=0.7, h_pad=0.8);