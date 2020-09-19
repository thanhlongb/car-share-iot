from datetime import *
import numpy as np
import pandas as pd

from app.users.models import User
from app.cars.models import Car
from app.bookings.models import Booking, BookingAction

def get_line_chart_data():
    """
	Get users data from database and preprocess 
    for drawing line chart.

    :return: dict{
        -   labels: list of chart labels
        -   values: list of chart values
    }
    """
    users = User.query.all()
    if len(users) == 0:
        return {
            "labels" : [],
            "values" : []
        }
    data = [r.serialize_with_cols(['id', 'role', 'date']) 
        for r in users
    ]
    df = pd.DataFrame(data)
    users = df[df.role == 3]
    users.drop(columns=['role'], inplace=True)
    users_group_by_date = users.groupby('date').size()
    min_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    indexes = users_group_by_date.index
    for i in range(len(indexes)):
        if indexes[i] < min_date:
            users_group_by_date.drop(
                labels=[indexes[i]],
                inplace = True
            )
        index_split = indexes[i].split('-')
        new_index = index_split[1] + '/' + index_split[2]
        users_group_by_date.rename(
            {indexes[i]:new_index},
            inplace=True
        )

    return {
        "labels" : list(users_group_by_date.index),
        "values" : list(users_group_by_date.values)
    }

def get_pie_chart_data():
    """
	Get cars data from database and preprocess 
    for drawing pie chart.

    :return: dict{
        -   labels: list of chart labels
        -   values: list of chart values
    }
    """
    cars = Car.query.all()
    if len(cars) == 0:
        return {
            "labels" : [],
            "values" : []
        }
    data = [r.serialize_with_cols(['id', 'make']) for r in cars]
    df = pd.DataFrame(data)
    cars_group_by_make = df.groupby('make').size()
    return {
        "labels" : list(cars_group_by_make.index),
        "values" : list(cars_group_by_make.values)
    }

def get_bar_chart_data():
    """
	Get bookings data from database and preprocess 
    for drawing bar chart.

    :return: dict{
        -   labels: list of chart labels
        -   values: list of chart values
    }
    """
    cars = Car.query.all()
    bookings = Booking.query.all()
    ten_days_ago = datetime.now() - timedelta(days=10)
    booking_action = BookingAction.query \
            .filter(BookingAction.creation_time >= ten_days_ago) \
            .all()
    if len(cars) == 0 \
        or len(bookings) == 0 \
        or len(booking_action) == 0:
        return {
            "labels" : [],
            "values" : []
        }
    cars_list = [r.serialize_with_cols(['id', 'make'])
        for r in cars
    ]
    bookings_list = [r.serialize_with_cols(['id', 'car_id'])
        for r in bookings
    ]
    booking_acion_list = [
        r.serialize_with_cols(['id', 'booking_id', 'action'])
        for r in booking_action
    ]
    cars_df = pd.DataFrame(cars_list)
    bookings_df = pd.DataFrame(bookings_list)
    booking_action_df = pd.DataFrame(booking_acion_list)
    bookings_df.rename(
        columns={"id":"booking_id"},
        inplace=True
    )
    cars_df.rename(
        columns={"id":"car_id"},
        inplace=True
    )
    booking_created = booking_action_df[
        booking_action_df.action=='created'
    ]
    booking_created.drop(
        columns=['action'],
        inplace=True
    )
    booking_merged = booking_created.merge(
        bookings_df,
        on="booking_id"
    )
    booking_car_merged = booking_merged.merge(
        cars_df,
        on="car_id"
    )
    booking_group_by_make = booking_car_merged.groupby('make').size()
    return {
        "labels" : list(booking_group_by_make.index),
        "values" : list(booking_group_by_make.values)
    }
