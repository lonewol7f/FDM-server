import calendar
import numpy as np
import pandas as pd
import pickle
from datetime import date, datetime, timedelta


def get_prediction(input_params):
    hotel_type = input_params['hotel_type']
    arrival_date = input_params['arrival_date']
    no_of_staying_days = int(input_params['staying_days'])
    no_of_adults = int(input_params['adults'])
    no_of_children = int(input_params['children'])
    no_of_babies = int(input_params['babies'])
    meal_type = input_params['meal_type']
    market_segment = input_params['market_segment']
    dist_channel = input_params['distribution_channel']
    repeated_guest = input_params['repeated_guest']
    no_of_prev_cancel = int(input_params['prev_cancel'])
    no_of_prev_not_cancel = int(input_params['prev_not_cancel'])
    reserved_room_type = input_params['r_room_type']
    assigned_room_type = input_params['a_room_type']
    no_of_booking_changes = int(input_params['booking_changes'])
    deposit_type = input_params['deposit_type']
    customer_type = input_params['cus_type']
    adr = int(input_params['adr'])
    car_parking_space = int(input_params['car_parking'])
    special_request = int(input_params['special_request'])

    booking_date = date.today()
    days_in_waiting_list = 0

    # =======================================================
    arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()
    end_date = arrival_date + timedelta(days=no_of_staying_days)

    lead_time = (arrival_date - booking_date).days
    arrival_date_year = arrival_date.year
    arrival_date_month = calendar.month_name[arrival_date.month]
    arrival_date_week_no = arrival_date.isocalendar().week
    arrival_date_day_of_month = arrival_date.day
    stays_in_week_nights = np.busday_count(arrival_date, end_date)
    stays_in_weekend_nights = no_of_staying_days - stays_in_week_nights

    if meal_type == 'Bead & Breakfast':
        meal_type = 'BB'
    elif meal_type == 'Half Board':
        meal_type = 'HB'
    elif meal_type == 'Full Board':
        meal_type = 'FB'
    elif meal_type == 'Self Catering':
        meal_type = 'SC'
    else:
        meal_type = 'Undefined'

    if repeated_guest == 'Yes':
        repeated_guest = 1
    else:
        repeated_guest = 0

    if hotel_type == 'Resort Hotel':
        is_h1 = 1
    else:
        is_h1 = 0

    status_minus_arrival_date = np.random.randint(0, 9)

    # =======================================================

    data_dict = {
        'is_canceled': None,
        'lead_time': lead_time,
        'arrival_date_year': arrival_date_year,
        'arrival_date_month': arrival_date_month,
        'arrival_date_week_number': arrival_date_week_no,
        'arrival_date_day_of_month': arrival_date_day_of_month,
        'stays_in_weekend_nights': stays_in_weekend_nights,
        'stays_in_week_nights': stays_in_week_nights,
        'adults': no_of_adults,
        'children': no_of_children,
        'babies': no_of_babies,
        'meal': meal_type,
        'country': None,
        'market_segment': market_segment,
        'distribution_channel': dist_channel,
        'is_repeated_guest': repeated_guest,
        'previous_cancellations': no_of_prev_cancel,
        'previous_bookings_not_canceled': no_of_prev_not_cancel,
        'reserved_room_type': reserved_room_type,
        'assigned_room_type': assigned_room_type,
        'booking_changes': no_of_booking_changes,
        'deposit_type': deposit_type,
        'agent': None,
        'company': None,
        'days_in_waiting_list': days_in_waiting_list,
        'customer_type': customer_type,
        'adr': adr,
        'required_car_parking_spaces': car_parking_space,
        'total_of_special_requests': special_request,
        'reservation_status': None,
        'reservation_status_date': None,
        'is_h1': is_h1,
        'arrival_date_full': arrival_date,
        'status_minus_arrival_date': status_minus_arrival_date
    }

    data = pd.DataFrame(data=data_dict, index=[0])

    return predict_is_cancelled(data)


def get_cluster(dataframe):
    kproto = pickle.load(open('model/kproto.pkl', 'rb'))

    X = dataframe.drop(
        columns=['is_canceled', 'reservation_status', 'agent', 'company', 'country', 'reservation_status_date',
                 'arrival_date_full'])
    cluster = kproto.predict(X, categorical=[2, 10, 11, 12, 13, 16, 17, 19, 21, 25])

    print(cluster)

    return cluster[0]

    # cluster_lst = ['lead_time', 'arrival_date_year', 'arrival_date_month', 'arrival_date_week_number',
    #                'arrival_date_day_of_month', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children',
    #                'babies', 'meal', 'market_segment', 'distribution_channel', 'is_repeated_guest',
    #                'previous_cancellations', 'previous_bookings_not_canceled', 'reserved_room_type',
    #                'assigned_room_type', 'booking_changes', 'deposit_type', 'days_in_waiting_list', 'customer_type',
    #                'adr', 'required_car_parking_spaces', 'total_of_special_requests', 'is_h1',
    #                'status_minus_arrival_date']

    # rf_list = ['lead_time', 'arrival_date_year', 'arrival_date_week_number', 'arrival_date_day_of_month',
    #            'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies', 'is_repeated_guest',
    #            'previous_cancellations', 'previous_bookings_not_canceled', 'booking_changes', 'days_in_waiting_list',
    #            'adr', 'required_car_parking_spaces', 'total_of_special_requests', 'is_h1', 'status_minus_arrival_date',
    #            '*arrival_date_month_April', 'arrival_date_month_August', 'arrival_date_month_December',
    #            'arrival_date_month_February', 'arrival_date_month_January', 'arrival_date_month_July',
    #            'arrival_date_month_June', 'arrival_date_month_March', 'arrival_date_month_May',
    #            'arrival_date_month_November', 'arrival_date_month_October', 'arrival_date_month_September', 'meal_BB',
    #            'meal_FB', 'meal_HB', 'meal_SC', 'meal_Undefined', 'market_segment_Aviation',
    #            'market_segment_Complementary', 'market_segment_Corporate', 'market_segment_Direct',
    #            'market_segment_Groups', 'market_segment_Offline TA/TO', 'market_segment_Online TA',
    #            'distribution_channel_Corporate', 'distribution_channel_Direct', 'distribution_channel_GDS',
    #            'distribution_channel_TA/TO', 'distribution_channel_Undefined', 'reserved_room_type_A',
    #            'reserved_room_type_B', 'reserved_room_type_C', 'reserved_room_type_D', 'reserved_room_type_E',
    #            'reserved_room_type_F', 'reserved_room_type_G', 'reserved_room_type_H', 'reserved_room_type_L',
    #            'reserved_room_type_P', 'assigned_room_type_A', 'assigned_room_type_B', 'assigned_room_type_C',
    #            'assigned_room_type_D', 'assigned_room_type_E', 'assigned_room_type_F', 'assigned_room_type_G',
    #            'assigned_room_type_H', 'assigned_room_type_I', 'assigned_room_type_K', 'assigned_room_type_L',
    #            'assigned_room_type_P', 'deposit_type_No Deposit', 'deposit_type_Non Refund', 'deposit_type_Refundable',
    #            'customer_type_Contract', 'customer_type_Group', 'customer_type_Transient',
    #            'customer_type_Transient-Party', 'clusters_Type 1', 'clusters_Type 2', 'clusters_Type 3',
    #            'clusters_Type 4']


def predict_is_cancelled(dataframe):
    rf = pickle.load(open('model/random_forest_classifire_gs.pkl', 'rb'))
    cluster = get_cluster(dataframe)

    if cluster == 0:
        dataframe['clusters'] = 'Type 1'
    elif cluster == 1:
        dataframe['clusters'] = 'Type 2'
    elif cluster == 2:
        dataframe['clusters'] = 'Type 3'
    else:
        dataframe['clusters'] = 'Type 4'

    dataframe_2 = pd.read_csv('DATA/hotel_booking_with_cluster.csv')
    dataframe_2 = dataframe_2.append(dataframe, ignore_index=True)
    dataframe_2 = pd.get_dummies(dataframe_2,
                                   columns=['arrival_date_month', 'meal', 'market_segment', 'distribution_channel',
                                            'reserved_room_type', 'assigned_room_type', 'deposit_type', 'customer_type',
                                            'clusters'])

    dataframe = dataframe_2.tail(1)

    X = dataframe.drop(columns=['is_canceled','reservation_status', 'agent', 'company', 'country',
                                    'reservation_status_date', 'arrival_date_full'])
    is_cancelled = rf.predict(X)

    print(is_cancelled)

    return is_cancelled
