import os
import json
import scipy
import boto3
import s3fs
import glob
import scipy.signal.windows
import numpy as np
import pandas as pd
import requests
import pymongo

from scipy.signal import welch, iirfilter, lfilter
from scipy import signal
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


import math
import pickle

#Gradient Color Bar Plots
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import colors as mcolors, path

from datetime import timedelta
from datetime import datetime, timezone
from typing import Any, List, Optional, Tuple
from pytz import UTC


import pandas as pd
import boto3
import json
import pymongo
import pandas as pd

from bson import ObjectId
import random

from src.eeg_treatement import *

connection_string = "mongodb://looxidlabs:looxidlabs.vkdlxld!@3.36.42.241:39632/m-project-dev?authSource=admin&readPreference=primary&directConnection=true&ssl=false"


class MongoDBChecker():
    def __init__(self, connection_string : str, dev_mode : bool = True) -> None:
        self.client : str = pymongo.MongoClient(connection_string)
        self.db_name : str = "focusmate-dev"
        if dev_mode == False:
            self.db_name = "focusmate"
            
        
    def get_user_id_from_email(self, email : str) -> Optional[str]:
        """
            Find the user id from user's email. If not found, return None
        """
        
        db : pymongo.database.Database = self.client[self.db_name]
        user_collection : pymongo.collection.Collection = db["users"]
        
        result : List[Any] = user_collection.find_one({"email": email})
        try:
            user_id : str = result["_id"]

            return user_id
        except:
            return None
    
    def _convert_timestamp(self, start_time : datetime, start_delay : int = 0, end_delay : int = 1) -> Tuple[int, int]:
        """
        일단은 임시로 이렇게 해두고 정석적인 시간 변환은 나중에 바꾸도록 하자
        """
        
        return datetime.fromtimestamp((start_time - timedelta(minutes=start_delay) - timedelta(hours=18)).timestamp()), datetime.fromtimestamp((start_time + timedelta(minutes=end_delay) - timedelta(hours=18)).timestamp())
    
    def get_focustimer_id_from_user_id(self, user_id : str, start_time : datetime) -> Optional[str]:
        """
            Toto
        """
        
        db : pymongo.database.Database = self.client[self.db_name]
        focustimer_collection : pymongo.collection.Collection = db["focustimers"]
            
        start_timestamp, end_timestamp = self._convert_timestamp(start_time)
        
        
        print(start_time, start_timestamp, end_timestamp)
            
        query = {
                    "userId": user_id,
                    "startedAt": {
                        "$gte": start_timestamp,
                        "$lte": end_timestamp
                    }
                }
        
        result = list(focustimer_collection.find(query))
        
        try:
            result = result[-1]
            focus_timer_id = result["_id"]

            return focus_timer_id
        except IndexError:
            return None
        
    def get_focustimer_ids_from_user_id_and_range(self, user_id : str, start_time : datetime, duration : timedelta) -> Optional[List[str]]:
        """
        MMECOCO WE WILL USE THIS
        """
        
        db : pymongo.database.Database = self.client[self.db_name]
        focustimer_collection : pymongo.collection.Collection = db["focustimers"]
                            
        query = {
                    "userId": ObjectId(user_id),
                    "startedAt": {
                        "$gte": start_time + timedelta(hours=18),
                        "$lte": start_time + duration + timedelta(hours=18),
                    }
                }
        
        
        result = list(focustimer_collection.find(query))
        
        for idx, element in enumerate(result):
            result[idx] = {
                "goalTime" : self.get_goal_time_from_goal_id(element["goalId"]),
                "startedAt" : self._convert_timestamp(element["startedAt"])[0],
                "time" : element["time"],
                "endAt" : self._convert_timestamp(element["startedAt"] + timedelta(seconds=element["time"]))[0],
                "focusId" : element["_id"],
                "userId" : element["userId"],
                "date" : self._convert_timestamp(element["startedAt"])[0].date(),
                "weekday" : self._convert_timestamp(element["startedAt"])[0].strftime("%A"),
            }
        
        return result

        
    def get_name_from_user_id(self, user_id : str) -> Optional[str]:
        """
        """
        
        db : pymongo.database.Database = self.client[self.db_name]
        users_collection : pymongo.collection.Collection = db["users"]
            
        query = {"_id": user_id}
        
        result = users_collection.find_one(query)
        
        if result:
            return result["nickname"]
        return None
    
    def get_goal_time_from_goal_id(self, goal_id : str) -> Optional[str]:
        """
        """
        
        db : pymongo.database.Database = self.client[self.db_name]
        users_collection : pymongo.collection.Collection = db["goals"]
            
        query = {"_id": goal_id}
        
        result = users_collection.find_one(query)
        
        if result:
            return result["goalTime"]
        return None
    
    def get_efficiencies_from_focus_id(self, focus_id):
        db : pymongo.database.Database = self.client[self.db_name]
        users_collection : pymongo.collection.Collection = db["focustimers"]
            
        query = {"_id": focus_id}
        
        result = users_collection.find_one(query)
        
        if result:
            return np.array(result["efficiencies"]) / 100
        return 0


def eeg_filter(eeg, btype, eeg_sr=250, freq_high=0.5, freq_stop=60, freq_band=[1, 50], eeg_butter_order=3, ):
    f_n = eeg_sr / 2
    b = 1
    a = 1
    if btype == "highpass":
        b, a = signal.butter(
            eeg_butter_order, freq_high / f_n, btype=btype, analog=False
        )
    elif btype == "bandstop":
        b, a = signal.butter(
            eeg_butter_order,
            [(freq_stop - 1) / f_n, (freq_stop + 1) / f_n],
            btype,
            analog=False,
        )
    elif btype == "bandpass":
        b, a = signal.butter(
            eeg_butter_order,
            np.array(freq_band) / f_n,
            btype,
            analog=False,
        )

    filtered_eeg = signal.filtfilt(
        b,
        a,
        eeg,
        axis=0,
        padtype="odd",
        padlen=3 * (max(len(b), len(a)) - 1),
    )
    return filtered_eeg


def apply_filter(eeg_raw_data):
    applied_notch = eeg_filter(eeg_raw_data, "bandstop")
    applied_highpass = eeg_filter(applied_notch, "highpass")
    applied_bandpass = eeg_filter(applied_highpass, "bandpass")
    return applied_bandpass


def segment_per_second(eeg, nperseg):
    segments = [eeg[i * nperseg: (i + 1) * nperseg] for i in range(len(eeg) // nperseg)]
    return segments


def fft_norm_without_epoch(psd):
    denom = psd.sum(axis=0, keepdims=True)
    normed = psd / denom
    return normed


def calculate_fft(eeg, nperseg, relative=True):
    MIN_FREQ_INDEX = 1
    MAX_FREQ_INDEX = 50

    all_fft = []
    segments = segment_per_second(eeg, nperseg)
    for segment in segments:
        fft_result = np.fft.fft(segment)
        power_spectrum = np.sqrt(np.abs(fft_result) ** 2)
        # 아랫줄만 밀어넣을 것
        power_spectrum = np.array(power_spectrum)

        f = np.fft.fftfreq(len(segment), 1 / 250)
        idx_crop = (MIN_FREQ_INDEX <= f) & (f <= MAX_FREQ_INDEX)
        power_spectrum = power_spectrum[idx_crop]
        f = f[idx_crop]

        if relative:
            power_spectrum = fft_norm_without_epoch(power_spectrum)
        all_fft.append(power_spectrum)
    return np.array(all_fft)
    
    
def get_eeg_frequency(fft):
    delta = np.sum(fft[:, 0:3], axis=1)
    theta = np.sum(fft[:, 3:7], axis=1)
    alpha = np.sum(fft[:, 7:13], axis=1)
    beta = np.sum(fft[:, 13:30], axis=1)
    gamma = np.sum(fft[:, 30:], axis=1)

    return delta, theta, alpha, beta, gamma


def chunk_data(data, n, axis=1):
    main_data_len = (len(data) // n)* n
    
    main_data = data[:main_data_len]
    main_data = main_data.reshape(-1, n)
    meaned_main_data = list(np.mean(main_data, axis=axis))
    
    sub_data = data[main_data_len:]
    
    if len(sub_data) == 0:
        editted_data = meaned_main_data
    elif len(sub_data) == 1:
        editted_data = meaned_main_data + list(sub_data)
        editted_data = np.array(editted_data)
    else:
        meaned_sub_data = [np.mean(sub_data)]
        editted_data = np.array(meaned_main_data + meaned_sub_data)
    
    return editted_data


def abs_mapping_to_energy(x):
    result = 1 / (1 + np.e ** (- x + 9.718946665209524))
    if result < 0.01:
        result = random.uniform(0.4, 0.6)
    # result *= 100
    return result

    
def check_leadoff(raw_json):
    ref = raw_json["eegRefLeadOff"]
    ch2 = raw_json["eegChannel2LeadOff"]
    
    return ((ref.count(1) / len(ref) >= 0.1) or (ch2.count(1) / len(ch2) >= 0.1))

    
    
def get_id_focus_timer_id_index(file_name):
    
    current_file_index = int(file_name.split("_")[-1][:-5])
    chunked_path = file_name.split("/")
    
    focus_timer_id = chunked_path[2]
    json_file_name = chunked_path[3]
    
    _id = json_file_name.split("_")[0]
    
    
    # return _id, focusTimerId and index
    return (_id, focus_timer_id, current_file_index)

def add_ids_in_df(df : pd.DataFrame) -> pd.DataFrame:
    user_ids = []
    focus_timer_ids = []


    for idx, row in df.iterrows():
        checker = MongoDBChecker(connection_string, dev_mode=row["IsDev"])

        user_id = checker.get_user_id_from_email(row["Email"])
        result = checker.get_focustimer_ids_from_user_id_and_range(user_id, row["datetime"].tz_localize(UTC), timedelta(minutes=1))
        
        print(row["Name"], row["Label"], row["Trial"], user_id)
        print(result)
        
        try:
            user_ids.append(result[-1]["userId"])
            focus_timer_ids.append(result[-1]["_id"])
        except Exception as e:
            print("MMECOCO:", e)
            continue
        
    df["user_id"] = user_ids
    df["focus_timer_id"] = focus_timer_ids
    
    return df


def downsample_list(input_list, target_length=10):
    """
    Downsample a list to the specified target length.

    Parameters:
    - input_list: The input list to be downsampled.
    - target_length: The desired length of the downsampled list.

    Returns:
    - downsampled_list: The downsampled list.
    """
    if len(input_list) <= target_length:
        # No downsampling needed, return the original list
        return input_list

    # Calculate the step size for downsampling
    step_size = len(input_list) / target_length

    # Create an index array to select evenly spaced elements
    indices = (np.arange(target_length) * step_size).astype(int)

    # Use the indices to extract the downsampled list
    downsampled_list = [input_list[i] for i in indices]

    return np.array(downsampled_list)


def get_proportion(abs_eng):
    if len(abs_eng) == 0:
        return 0, 0, 0, 0
    abs_eng = np.array(abs_eng)
    abs_mapping_thresholds = [0.632873044029435, 0.47623607242657157, 0.3836650852151003]

    very_high = sum(abs_eng > abs_mapping_thresholds[0]) / len(abs_eng)
    high = np.sum((abs_eng >= abs_mapping_thresholds[1]) & (abs_eng <= abs_mapping_thresholds[0])) / len(abs_eng)
    middle = np.sum((abs_eng >= abs_mapping_thresholds[2]) & (abs_eng <= abs_mapping_thresholds[1])) / len(abs_eng)
    low = sum(abs_eng < abs_mapping_thresholds[2]) / len(abs_eng)
    
    return very_high, high, middle, low

def get_data_from_db(user_id, date, checker):
    res = checker.get_focustimer_ids_from_user_id_and_range(user_id, date, timedelta(days=7))
    df = pd.DataFrame(res)
    
    return df

def date_treatement(df):
    df = df[df["time"] > 0]

    df['startedAt'] = pd.to_datetime(df['startedAt'])
    df['endAt'] = pd.to_datetime(df['endAt'])

    df['duration'] = (df['endAt'] - df['startedAt']).dt.total_seconds()

    result_df = df.groupby('date')['duration'].sum().reset_index()


    result_df['date'] = pd.to_datetime(result_df['date'])
    date_range = pd.date_range(start=result_df['date'].min(), end=result_df['date'].max(), freq='D')
    date_range_df = pd.DataFrame({'date': date_range})
    merged_df = pd.merge(date_range_df, result_df, on='date', how='left')
    merged_df['duration'].fillna(0, inplace=True)
    merged_df["time_variation"] = merged_df['duration'].diff()
    
    return df, merged_df

def load_raw_data_list(user_id, focus_id, bucket):
    sf = s3fs.S3FileSystem(anon=False)
    path_obj = f'{bucket}/focus-timer/{user_id}/{focus_id}'
    raw_data_files = sf.glob(f'{path_obj}//**')
    raw_data_files.sort()
    
    return raw_data_files


def get_boa_bor(user_id, focus_id, dev_mode=True):
    if dev_mode == False:
        bucket = 'focusmate-public'
    else:
        bucket = 'focusmate-public-dev'
    sf = s3fs.S3FileSystem(anon=False)
    s3 = boto3.resource('s3')
    raw_data_files = load_raw_data_list(user_id, focus_id, bucket)
    raw_data_files = load_raw_data_list(user_id, focus_id, bucket)

    total_raw_ch1 = []
    total_raw_ch2 = []
    
    try:
        for raw_data_file in raw_data_files:
            path_split = raw_data_file.split('/')
            key1 = path_split[0]
            key2 = f'{path_split[1]}/{path_split[2]}/{path_split[3]}/{path_split[4]}'
            uploaded_file_s3_obj = s3.Object(key1, key2)
            raw_json = json.loads(uploaded_file_s3_obj.get()['Body'].read())

            eeg_raw_ch1 = raw_json['eegChannel1']
            eeg_raw_ch2 = raw_json['eegChannel2']

            lead_off_ch1 = raw_json['eegChannel1LeadOff']
            ppg = raw_json['ppg']

            total_raw_ch1 += eeg_raw_ch1
            total_raw_ch2 += eeg_raw_ch2

        filtered_ch1 = apply_filter(total_raw_ch1)
        filtered_ch2 = apply_filter(total_raw_ch2)


        f1, fft1 = calculate_psd_from_fft(filtered_ch1, 250, False) # 1초 단위라서 250
        f2, fft2 = calculate_psd_from_fft(filtered_ch2, 250, False) # 1초 단위라서 250

        delta1, theta1, alpha1, beta1, gamma1 = get_eeg_frequency(fft1)
        delta2, theta2, alpha2, beta2, gamma2 = get_eeg_frequency(fft2)
        
        beta1 = chunk_data(beta1, 10)
        gamma1 = chunk_data(gamma1, 10)

        beta2 = chunk_data(beta2, 10)
        gamma2 = chunk_data(gamma2, 10)

        abs_beta_gamma1 = np.log10(beta1) + np.log10(gamma1)
        abs_beta_gamma2 = np.log10(beta2) + np.log10(gamma2)

        abs_beta_gamma = (abs_beta_gamma1 + abs_beta_gamma2) / 2
        
        print(beta2)

        abs_brain_energies = [abs_mapping_to_energy(bet) for bet in abs_beta_gamma]


        return get_proportion(abs_brain_energies), np.mean(abs_brain_energies), abs_brain_energies
    except Exception as e:
        print(e)
        return (0, 0, 0, 1), 0, []

def get_boas(df):
    boas = []
    veryHighFocus = []
    highFocus = []
    middleFocus = []
    lowFocus = []
    abs_brain_energies_list = []

    for idx, row in df.iterrows():
        # efficiencies = checker.get_efficiencies_from_focus_id(row["focusId"])
        proportion, mean, boa = get_boa_bor(row["userId"], row["focusId"], dev_mode=False)
        
        vh, h, m, l = proportion
        boas.append(boa)
        
        veryHighFocus.append(vh)
        highFocus.append(h)
        middleFocus.append(m)
        lowFocus.append(l)
        abs_brain_energies_list.append(np.array(boa))
        
    return boas, veryHighFocus, highFocus, middleFocus, lowFocus, abs_brain_energies_list

def add_mean_features_to_df(df):
    df['veryHighFocusMean'] = df.groupby('date')['veryHighFocus'].transform('mean')
    df['highFocusMean'] = df.groupby('date')['highFocus'].transform('mean')
    df['middleFocusMean'] = df.groupby('date')['middleFocus'].transform('mean')
    df['lowFocusMean'] = df.groupby('date')['lowFocus'].transform('mean')
    
    return df

def missing_week_treatement(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    all_weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    existing_weekdays = df['weekday'].unique()

    missing_weekdays = set(all_weekdays) - set(existing_weekdays)

    missing_weekdays_df = []
    for missing_weekday in missing_weekdays:
        date_for_missing_weekday = pd.to_datetime('now').normalize()  # You can replace this with an appropriate date
        missing_weekdays_df.append({'date': date_for_missing_weekday, 'weekday': missing_weekday})

    missing_weekdays_df = pd.DataFrame(missing_weekdays_df)
    df = pd.concat([df, missing_weekdays_df], ignore_index=True, sort=False)

    numeric_columns = ['duration', 'time_variation', 'goalAccomplished', 'boa', 'veryHighFocus', 'highFocus', 'middleFocus', 'lowFocus', 'time', 'veryHighFocusMean', 'highFocusMean', 'middleFocusMean', 'lowFocusMean', 'goalProportion']
    df[numeric_columns] = df[numeric_columns].fillna(0)

    string_columns = ['focusId', 'userId', 'abs_brain_energies']
    df[string_columns] = df[string_columns].fillna('Noexist')

    list_columns = ['abs_brain_energies']  # Add other list columns as needed
    df[list_columns] = df[list_columns].applymap(lambda x: [0] if type(x) == str else x)
    
    return df

def sort_df_bt_weekday(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    max_time_rows = df.loc[df.groupby('weekday')['time'].idxmax()]

    weekday_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    sorted_df = max_time_rows.sort_values(by='weekday', key=lambda x: x.map({day: i for i, day in enumerate(weekday_order)}))
    return sorted_df

def create_user_df(user_id, date):
    checker = MongoDBChecker(connection_string, dev_mode=False)
    df = get_data_from_db(user_id, date, checker)
    df, merged_df = date_treatement(df)

    new_col = []

    for idx, row in df.iterrows():
        new_col.append(list(merged_df[merged_df["date"] == str(row["date"])]["time_variation"])[0])

    df["time_variation"] = new_col
    df["goalAccomplished"] = True # 여기서는 목표설정 잘 해야함 원래대로

    boas, veryHighFocus, highFocus, middleFocus, lowFocus, abs_brain_energies_list = get_boas(df)
    
    df["boa"] = boas
    df["veryHighFocus"] = veryHighFocus
    df["highFocus"] = highFocus
    df["middleFocus"] = middleFocus
    df["lowFocus"] = lowFocus
    df["abs_brain_energies"] = abs_brain_energies_list
    
    df['goalProportion'] = df['time'] - df['goalTime']
    df.loc[df['time'] < 600, 'goalProportion'] = 0
    df["goalAccomplished"] = df['goalProportion'] >= 0

    df = add_mean_features_to_df(df)
    df = missing_week_treatement(df)
    df = sort_df_bt_weekday(df)
    
    
    ### mmecoco Testing
    
    weekday_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    target_week = df.sort_values("startedAt")["weekday"].iloc[0]
    week_index = weekday_order.index(target_week)

    new_weekday_order = weekday_order[week_index:] + weekday_order[:week_index]

    df.sort_values(by='weekday', key=lambda x: x.map({day: i for i, day in enumerate(new_weekday_order)}), inplace=True)

    return df
