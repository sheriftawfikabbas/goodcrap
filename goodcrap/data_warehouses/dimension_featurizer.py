import pandas as pd
from enum import Enum


class DatetimeFeature(Enum):
    day_name = 1
    day_number_in_week = 2
    day_number_in_month = 3
    day_number_in_year = 4
    week_number = 5
    week_last_day_date = 6
    month_number = 7
    days_in_month = 8
    month_last_day_date = 9
    month_name = 10
    quarter_number = 11
    days_in_quarter = 12
    quarter_last_date = 13
    year = 14
    days_in_year = 15
    year_last_day_date = 16


class DimensionFeaturizer:
    def featurize_date(date: pd.DatetimeIndex, feature: DatetimeFeature):
        if feature == DatetimeFeature.day_name:
            return date.day_name()
        elif feature == DatetimeFeature.day_number_in_week:
            return date.day_of_week
        elif feature == DatetimeFeature.day_number_in_month:
            return date.day
        elif feature == DatetimeFeature.day_number_in_year:
            return date.day_of_year
        elif feature == DatetimeFeature.week_number:
            return date.weekday
        elif feature == DatetimeFeature.week_last_day_date:
            return date.dayofweek
        elif feature == DatetimeFeature.month_number:
            return date.day_of_week
        elif feature == DatetimeFeature.days_in_month:
            return date.day_of_week
        elif feature == DatetimeFeature.month_last_day_date:
            return date.day_of_week
        elif feature == DatetimeFeature.month_name:
            return date.day_of_week
        elif feature == DatetimeFeature.quarter_number:
            return date.day_of_week
        elif feature == DatetimeFeature.days_in_quarter:
            return date.day_of_week
        elif feature == DatetimeFeature.quarter_last_date:
            return date.day_of_week
        elif feature == DatetimeFeature.year:
            return date.day_of_week
        elif feature == DatetimeFeature.days_in_year:
            return date.day_of_week.name, date.day_of_week

    def featurize_date_all(date: pd.DatetimeIndex):
        features = []
        feature_names = []
        for f in DatetimeFeature:
            features += [DimensionFeaturizer.featurize_date(date, f)]
            feature_names += [f.name]
        return feature_names, features
