import pandas as pd
from datetime import timedelta

# You should download CSV file with funding rates from Perp (https://app.redash.io/perp/embed/query/717699/visualization/1197815?api_key=RfFGcsZN68RAGKKouqvTxHMJeQQh7J7hfo8LADqR&)
# Enter path to CSV file
perp = pd.read_csv("Path to CSV file", parse_dates=['time'], na_values='n/a')


def year(x):
    return 24 * 365 * x


def get_mean_funding_rate_period(df, last_days=None):
    if last_days is None:
        df_filtered = df
    else:
        max_date = df['time'].max()
        filter_date = max_date - timedelta(days=last_days)
        df_filtered = df[df['time'] >= filter_date]

    res = df_filtered.groupby(['ammAddr'])[['fundingRate']].mean()
    res['year_funding_rate'] = year(res['fundingRate'])
    return res[['year_funding_rate']]


def get_all_funding_data(perp, periods):
    mean_funding_rates = {}
    for period in periods:
        mean_funding_rates[period] = get_mean_funding_rate_period(perp, period)
    funding_list = []
    for period in periods:
        funding_list.append(mean_funding_rates[period])
        column_name = 'period_{}'.format(period if period is not None else 'all')
        funding_list[-1] = funding_list[-1].rename(columns={'year_funding_rate': column_name})
    all_fundings = pd.concat(funding_list, axis=1, join='inner')
    return all_fundings


periods = [None, 14, 7, 3, 1]

all_fundings = get_all_funding_data(perp, periods)
print(all_fundings)
