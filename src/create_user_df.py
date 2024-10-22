import random
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import pymongo
from bson import ObjectId
from pytz import UTC
from scipy import signal
import pytz
from src.Repositories.MongoDBRepository import MongoDBRepository


connection_string = "mongodb://looxidlabs:looxidlabs.vkdlxld%21@43.203.3.210:39632/m-project-dev?authSource=admin&readPreference=primary&directConnection=true&ssl=false"


def study_session_factory(df):
    weeks = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]
    study_sessions = []
    
    for week in weeks:
        current_df = df[df["weekday"] == week]
        current_study_sessions = []
        
        for _, row in current_df.iterrows():
            start, end = row["startedAt"], row["endAt"]
            current_study_sessions.append(StudySession(start, end))
        study_sessions.append(current_study_sessions)
        
    return study_sessions

class StudySession:
    def __init__(self, starting_datetime, ending_datetime) -> None:
        
        self.start_hour = starting_datetime.hour
        self.start_minute = starting_datetime.minute
        self.end_hour = ending_datetime.hour
        self.end_minute = ending_datetime.minute
        
        self.weekday = starting_datetime.strftime("%A")
        
    def _convert_to_bar_from_time(self, hour, minute):
        hour_coef = 100 / 24 # (이게 한시간이라는 뜻)
        minute_coef = 100 / 24 / 60 # (이게 1분이라는 뜻)
        
        return (hour * hour_coef + minute * minute_coef) - 4 * hour_coef
        
    def get_source_df(self):
        
        source = pd.DataFrame(
            {
                "x": [0, 1],
                "y1": [self._convert_to_bar_from_time(self.start_hour, self.start_minute), 0],
                "y2": [self._convert_to_bar_from_time(self.end_hour, self.end_minute), 100],
                "color": ["#9494FF", "#00000000"],
            }
        )
        
        return source

class MongoDBChecker:
    def __init__(self, connection_string: str, dev_mode: bool = True) -> None:
        self.client: str = pymongo.MongoClient(connection_string)
        self.db_name: str = "focusmate-dev"
        if dev_mode is False:
            self.db_name = "focusmate"

    def get_user_id_from_email(self, email: str) -> Optional[str]:
        """
        Find the user id from user's email. If not found, return None
        """

        db: pymongo.database.Database = self.client[self.db_name]
        user_collection: pymongo.collection.Collection = db["users"]

        result: List[Any] = user_collection.find_one({"email": email})
        try:
            user_id: str = result["_id"]

            return user_id
        except:
            return None

    def _convert_timestamp(
        self, start_time: datetime, start_delay: int = 0, end_delay: int = 1
    ) -> Tuple[int, int]:
        """
        일단은 임시로 이렇게 해두고 정석적인 시간 변환은 나중에 바꾸도록 하자
        """

        utc_plus_9 = pytz.timezone("Asia/Tokyo")
        utc = pytz.timezone("UTC")
        start_time = utc.localize(start_time).astimezone(utc_plus_9)
        return datetime.fromtimestamp(start_time.timestamp()), None

    def get_focustimer_id_from_user_id(
        self, user_id: str, start_time: datetime
    ) -> Optional[str]:
        """
        Toto
        """

        db: pymongo.database.Database = self.client[self.db_name]
        focustimer_collection: pymongo.collection.Collection = db["focustimers"]

        start_timestamp, end_timestamp = self._convert_timestamp(start_time)

        query = {
            "userId": user_id,
            "startedAt": {"$gte": start_timestamp, "$lte": end_timestamp},
        }

        result = list(focustimer_collection.find(query))

        try:
            result = result[-1]
            focus_timer_id = result["_id"]

            return focus_timer_id
        except IndexError:
            return None

    def get_email_from_user_id(self, user_id: str) -> Optional[str]:
        db: pymongo.database.Database = self.client[self.db_name]
        focustimer_collection: pymongo.collection.Collection = db["users"]

        query = {"_id": ObjectId(user_id)}
        result = list(focustimer_collection.find(query))

        if result == []:
            return None
        else:
            return result[0]["email"]

    def get_focustimer_ids_from_range_for_each_user_ids(
        self, start_time: datetime, duration: timedelta
    ) -> Optional[List[str]]:
        """
        gets all needed focus_id datas only from range and split
        into chunk of dfs by their userid
        """

        db: pymongo.database.Database = self.client[self.db_name]
        focustimer_collection: pymongo.collection.Collection = db["focustimers"]

        query = {
            "startedAt": {
                "$gte": start_time,
                "$lte": start_time
                + duration
                + timedelta(hours=23)
                + timedelta(minutes=59),
            },
        }

        result = list(focustimer_collection.find(query))

        for idx, element in enumerate(result):
            result[idx] = {
                "email": self.get_email_from_user_id(user_id=element["userId"]),
                "goalId": element["goalId"],
                # "goalTime": self.get_goal_time_from_goal_id(element["goalId"]),
                "startedAt": self._convert_timestamp(element["startedAt"])[0],
                "time": element["time"],
                "endAt": self._convert_timestamp(
                    element["startedAt"] + timedelta(seconds=element["time"])
                )[0],
                "focusId": element["_id"],
                "userId": element["userId"],
                "date": self._convert_timestamp(element["startedAt"])[0].date(),
                "weekday": self._convert_timestamp(element["startedAt"])[0].strftime(
                    "%A"
                ),
            }

        result_df = pd.DataFrame(result)

        return [group for _, group in result_df.groupby("userId")]

    def get_focustimer_ids_from_user_id_and_range(
        self, user_id: str, start_time: datetime, duration: timedelta
    ) -> Optional[List[str]]:
        """
        MMECOCO WE WILL USE THIS
        """

        db: pymongo.database.Database = self.client[self.db_name]
        focustimer_collection: pymongo.collection.Collection = db["focustimers"]

        query = {
            "userId": ObjectId(user_id),
            "startedAt": {
                "$gte": start_time,
                "$lte": start_time
                + duration
                + timedelta(hours=23)
                + timedelta(minutes=59),
            },
        }

        result = list(focustimer_collection.find(query))

        for idx, element in enumerate(result):
            result[idx] = {
                "email": self.get_email_from_user_id(user_id=user_id),
                "goalId": element["goalId"],
                "goalTime": self.get_goal_time_from_goal_id(element["goalId"]),
                "startedAt": self._convert_timestamp(element["startedAt"])[0],
                "time": element["time"],
                "endAt": self._convert_timestamp(
                    element["startedAt"] + timedelta(seconds=element["time"])
                )[0],
                "focusId": element["_id"],
                "userId": element["userId"],
                "date": self._convert_timestamp(element["startedAt"])[0].date(),
                "weekday": self._convert_timestamp(element["startedAt"])[0].strftime(
                    "%A"
                ),
            }

        return result

    def get_name_from_user_id(self, user_id: str) -> Optional[str]:
        """ """

        db: pymongo.database.Database = self.client[self.db_name]
        users_collection: pymongo.collection.Collection = db["users"]

        query = {"_id": user_id}

        result = users_collection.find_one(query)

        if result:
            return result["nickname"]
        return None

    def get_goal_time_from_goal_id(self, goal_id: str) -> Optional[str]:
        """ """

        db: pymongo.database.Database = self.client[self.db_name]
        users_collection: pymongo.collection.Collection = db["goals"]

        query = {"_id": goal_id}

        result = users_collection.find_one(query)

        if result:
            return result["goalTime"]
        return None

    def get_efficiencies_from_focus_id(self, focus_id):
        db: pymongo.database.Database = self.client[self.db_name]
        users_collection: pymongo.collection.Collection = db["focustimers"]

        query = {"_id": focus_id}

        result = users_collection.find_one(query)

        if result:
            return np.array(result["efficiencies"]) / 100
        return 0


def eeg_filter(
    eeg,
    btype,
    eeg_sr=250,
    freq_high=0.5,
    freq_stop=60,
    freq_band=[1, 50],
    eeg_butter_order=3,
):
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
    segments = [
        eeg[i * nperseg : (i + 1) * nperseg] for i in range(len(eeg) // nperseg)
    ]
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
    main_data_len = (len(data) // n) * n

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
    result = 1 / (1 + np.e ** (-x + 9.718946665209524))
    if result < 0.01:
        result = random.uniform(0.4, 0.6)
    # result *= 100
    return result


def check_leadoff(raw_json):
    ref = raw_json["eegRefLeadOff"]
    ch2 = raw_json["eegChannel2LeadOff"]

    return (ref.count(1) / len(ref) >= 0.1) or (ch2.count(1) / len(ch2) >= 0.1)


def get_id_focus_timer_id_index(file_name):
    current_file_index = int(file_name.split("_")[-1][:-5])
    chunked_path = file_name.split("/")

    focus_timer_id = chunked_path[2]
    json_file_name = chunked_path[3]

    _id = json_file_name.split("_")[0]

    # return _id, focusTimerId and index
    return (_id, focus_timer_id, current_file_index)


def add_ids_in_df(df: pd.DataFrame) -> pd.DataFrame:
    user_ids = []
    focus_timer_ids = []

    for idx, row in df.iterrows():
        checker = MongoDBChecker(connection_string, dev_mode=row["IsDev"])

        user_id = checker.get_user_id_from_email(row["Email"])
        result = checker.get_focustimer_ids_from_user_id_and_range(
            user_id, row["datetime"].tz_localize(UTC), timedelta(minutes=1)
        )
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
    abs_mapping_thresholds = [
        0.632873044029435,
        0.47623607242657157,
        0.3836650852151003,
    ]

    very_high = sum(abs_eng > abs_mapping_thresholds[0]) / len(abs_eng)
    high = np.sum(
        (abs_eng >= abs_mapping_thresholds[1]) & (abs_eng <= abs_mapping_thresholds[0])
    ) / len(abs_eng)
    middle = np.sum(
        (abs_eng >= abs_mapping_thresholds[2]) & (abs_eng <= abs_mapping_thresholds[1])
    ) / len(abs_eng)
    low = sum(abs_eng < abs_mapping_thresholds[2]) / len(abs_eng)

    return very_high, high, middle, low


def get_data_from_db(user_id, date, checker):

    res = checker.get_focustimer_ids_from_user_id_and_range(
        user_id, date, timedelta(days=6)
    )
    df = pd.DataFrame(res)

    return df


def date_treatement(df):
    df = df[df["time"] > 0]

    df.loc[:, "startedAt"] = pd.to_datetime(df["startedAt"])
    df.loc[:, "endAt"] = pd.to_datetime(df["endAt"])

    df = df.copy()
    df.loc[:, "duration"] = (df["endAt"] - df["startedAt"]).dt.total_seconds()

    result_df = df.groupby("date")["duration"].sum().reset_index()

    result_df["date"] = pd.to_datetime(result_df["date"])
    date_range = pd.date_range(
        start=result_df["date"].min(), end=result_df["date"].max(), freq="D"
    )
    date_range_df = pd.DataFrame({"date": date_range})
    merged_df = pd.merge(date_range_df, result_df, on="date", how="left")
    merged_df["duration"].fillna(0, inplace=True)
    merged_df["time_variation"] = merged_df["duration"].diff()

    return df, merged_df


def get_boa_bor(user_id, focus_id, dev_mode=True):

    mongo_repository = MongoDBRepository()
    mongo_repository.connect(
        "mongodb://looxidlabs:looxidlabs.vkdlxld%21@43.203.3.210:39632/m-project-dev?authSource=admin&readPreference=primary&directConnection=true&ssl=false",
        dev_mode=dev_mode,
    )

    try:
        total_efficiencies = (
            np.array(
                mongo_repository.get_total_efficiencies_from_focus_id(focus_id=focus_id)
            )
            / 100
        )

        return (
            get_proportion(total_efficiencies),
            np.mean(total_efficiencies),
            total_efficiencies,
        )
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
        proportion, mean, boa = get_boa_bor(
            row["userId"], row["focusId"], dev_mode=False
        )

        vh, h, m, l = proportion
        boas.append(boa)

        veryHighFocus.append(vh)
        highFocus.append(h)
        middleFocus.append(m)
        lowFocus.append(l)
        abs_brain_energies_list.append(np.array(boa))

    return (
        boas,
        veryHighFocus,
        highFocus,
        middleFocus,
        lowFocus,
        abs_brain_energies_list,
    )


def add_summed_total_goal_in_df(df):
    df["summed_total_goal"] = 0
    grouped_by_date = df.groupby("date")

    for date, group_df in grouped_by_date:
        df.loc[df["date"] == date, "summed_total_goal"] = sum(
            group_df.drop_duplicates(subset="goalId", keep="first")["goalTime"]
        )

    return df


def get_summed_abs_brain_energies_from_df(df):

    boas = []
    for _, value in df.iterrows():
        day = value["weekday"]
        boa = np.sum(value["abs_brain_energies"])

        boas.append(boa)

    df["abs_brain_energie"] = boas
    df["summed_abs_brain_energies"] = df.groupby("date")["abs_brain_energie"].transform(
        "sum"
    )

    return df


def add_mean_and_sum_features_to_df(df):

    # mean
    df["veryHighFocusMean"] = df.groupby("date")["veryHighFocus"].transform("mean")
    df["highFocusMean"] = df.groupby("date")["highFocus"].transform("mean")
    df["middleFocusMean"] = df.groupby("date")["middleFocus"].transform("mean")
    df["lowFocusMean"] = df.groupby("date")["lowFocus"].transform("mean")
    df["session_time_mean"] = df.groupby("date")["time"].transform("mean")

    # sum
    df["summed_total_boa"] = df.groupby("date")["total_boa"].transform("sum")
    df["summed_total_duration"] = df.groupby("date")["duration"].transform("sum")
    # df = add_summed_total_goal_in_df(df)
    df = get_summed_abs_brain_energies_from_df(df)
    df["summed_time"] = df.groupby("date")["time"].transform("sum")

    return df


def missing_week_treatement(df, date):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    all_weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    week = date.strftime("%A")
    all_weekdays = all_weekdays[all_weekdays.index(week):] + all_weekdays[:all_weekdays.index(week)]
    existing_weekdays = df["weekday"].unique()

    missing_weekdays = set(all_weekdays) - set(existing_weekdays)

    missing_weekdays_df = []
    for missing_weekday in missing_weekdays:
        date_for_missing_weekday = pd.to_datetime(
            "now"
        ).normalize()
        missing_weekdays_df.append(
            {"date": date_for_missing_weekday, "weekday": missing_weekday}
        )

    missing_weekdays_df = pd.DataFrame(missing_weekdays_df)
    df = pd.concat([df, missing_weekdays_df], ignore_index=True, sort=False)

    # numeric_columns = [
    #     "duration",
    #     "time_variation",
    #     "goalAccomplished",
    #     "boa",
    #     "veryHighFocus",
    #     "highFocus",
    #     "middleFocus",
    #     "lowFocus",
    #     "time",
    #     "veryHighFocusMean",
    #     "highFocusMean",
    #     "middleFocusMean",
    #     "lowFocusMean",
    #     "goalProportion",
    #     "total_boa",
    #     "summed_total_boa",
    #     "summed_total_duration",
    #     "summed_total_goal",
    # ]
    # df[numeric_columns] = df[numeric_columns].fillna(0)

    # string_columns = ["focusId", "userId", "abs_brain_energies"]
    # df[string_columns] = df[string_columns].fillna("Noexist")

    # list_columns = ["abs_brain_energies"]  # Add other list columns as needed
    # df[list_columns] = df[list_columns].applymap(lambda x: [0] if type(x) == str else x)

    return df


def sort_df_bt_weekday(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    max_time_rows = df.loc[df.groupby("weekday")["time"].idxmax()]

    weekday_order = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    sorted_df = max_time_rows.sort_values(
        by="weekday",
        key=lambda x: x.map({day: i for i, day in enumerate(weekday_order)}),
    )
    return sorted_df


def create_user_df(date):
    checker = MongoDBChecker(connection_string, dev_mode=False)
    dfs = checker.get_focustimer_ids_from_range_for_each_user_ids(
        date, timedelta(days=6)
    )

    final_dfs = []
    for df in dfs:

        if df[df["time"] > 30 * 60].empty:  # 30분 이상 하나라도 있어야함
            continue
        df, merged_df = date_treatement(df)

        time_variation_col = []
        duration_col = []

        for _, row in df.iterrows():
            time_variation_col.append(
                list(
                    merged_df[merged_df["date"] == str(row["date"])]["time_variation"]
                )[0]
            )
            duration_col.append(
                list(merged_df[merged_df["date"] == str(row["date"])]["duration"])[0]
            )

        df["time_variation"] = time_variation_col
        # df["duration"] = duration_col
        df["goalAccomplished"] = True  # 여기서는 목표설정 잘 해야함 원래대로

        (
            boas,
            veryHighFocus,
            highFocus,
            middleFocus,
            lowFocus,
            abs_brain_energies_list,
        ) = get_boas(df)

        df["boa"] = boas
        df["veryHighFocus"] = veryHighFocus
        df["highFocus"] = highFocus
        df["middleFocus"] = middleFocus
        df["lowFocus"] = lowFocus
        df["abs_brain_energies"] = abs_brain_energies_list

        total_boa = []
        for _, value in df.iterrows():
            total_boa.append(np.sum(value["abs_brain_energies"]))
        df["total_boa"] = total_boa

        # df["goalProportion"] = df["duration"] - df["goalTime"]
        # df.loc[df["time"] < 600, "goalProportion"] = 0
        # df["goalAccomplished"] = df["goalProportion"] >= 0
        
        # study_reg = study_session_factory(df)
        
        # df = add_mean_and_sum_features_to_df(df)
        # df = missing_week_treatement(df, date)
        # df = sort_df_bt_weekday(df)

        # weekday_order = [
        #     "Sunday",
        #     "Monday",
        #     "Tuesday",
        #     "Wednesday",
        #     "Thursday",
        #     "Friday",
        #     "Saturday",
        # ]

        # target_week = date.strftime("%A")
        # week_index = weekday_order.index(target_week)

        # new_weekday_order = weekday_order[week_index:] + weekday_order[:week_index]
        # df["study_regularity"] = study_reg

        # df.sort_values(
        #     by="weekday",
        #     key=lambda x: x.map({day: i for i, day in enumerate(new_weekday_order)}),
        #     inplace=True,
        # )

        # df["summed_goal_proportion"] = (
        #     df["summed_total_duration"] - df["summed_total_goal"]
        # )
        # df["summed_goal_proportion"] = df["summed_goal_proportion"].fillna(0)

        final_dfs.append(df)

    return final_dfs
