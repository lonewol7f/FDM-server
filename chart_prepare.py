import pandas as pd

data = pd.read_csv('DATA/hotel_booking_with_cluster.csv')


def month_wise():
    global data
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
              'December']

    month_wise_cancelled_col = data[data['is_canceled'] == 1]['arrival_date_month'].value_counts()
    month_wise_not_cancelled_col = data[data['is_canceled'] == 0]['arrival_date_month'].value_counts()

    month_wise_cancelled = []
    month_wise_not_cancelled = []
    for month in months:
        month_wise_cancelled.append(str(month_wise_cancelled_col[month]))
        month_wise_not_cancelled.append(str(month_wise_not_cancelled_col[month]))

    month_wise_cancelled = (':').join(month_wise_cancelled)
    month_wise_not_cancelled = (':').join(month_wise_not_cancelled)

    return month_wise_cancelled, month_wise_not_cancelled


def cluster_wise():
    global data
    clusters = ['Type 1', 'Type 2', 'Type 3', 'Type 4']

    cluster_wise_cancelled_col = data[data['is_canceled'] == 1]['clusters'].value_counts()
    cluster_wise_not_cancelled_col = data[data['is_canceled'] == 0]['clusters'].value_counts()

    cluster_wise_cancelled = []
    cluster_wise_not_cancelled = []
    for cluster in clusters:
        cluster_wise_cancelled.append(str(cluster_wise_cancelled_col[cluster]))
        cluster_wise_not_cancelled.append(str(cluster_wise_not_cancelled_col[cluster]))

    cluster_wise_cancelled = (':').join(cluster_wise_cancelled)
    cluster_wise_not_cancelled = (':').join(cluster_wise_not_cancelled)

    return cluster_wise_cancelled, cluster_wise_not_cancelled
