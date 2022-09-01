def get_first_name(full_name):
    return full_name.split(" ")[0]


def find_row(series, col, value):
    for i, row in series.iterrows():
        if row[col] == value:
            return i

    return -1


def date_diff(base, diff, value_col, date_col):
    filter_ = []

    for _, row in base.iterrows():
        index = find_row(diff, value_col, row[value_col])

        if index > 0:
            filter_.append(row[date_col] > diff.loc[index][date_col])
        else:
            filter_.append(True)

    return base[filter_]
