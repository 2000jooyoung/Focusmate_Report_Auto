from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pymongo
from bson import ObjectId

from src.Repositories.Repository_interface import Repository


class MongoDBRepository(Repository):
    """
    MongoDB 저장소 클래스
    """

    def connect(self, connection_string, dev_mode: bool = True):
        self.client = pymongo.MongoClient(connection_string)

        self.db_name: str = "focusmate-dev"
        if dev_mode is False:
            self.db_name = "focusmate"
        self.db = self.client[self.db_name]

    def disconnect(self):
        self.client.close()

    def request_query(
        self, collection_name: str, query: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:
        user_collection: pymongo.collection.Collection = self.client[collection_name]
        result: List[Dict[str, Any]] = user_collection.find(query)

        return result

    def get_user_id_from_email(self, email: str) -> Optional[str]:
        """
        Find the user id from user's email. If not found, return None
        """
        query: Dict[str:str] = {"email": email}
        result: List[Any] = self.request_query("users", query)

        if result == []:
            return None

        return result[0]["_id"]

    def get_focustimer_id_from_user_id(
        self,
        user_id: str,
        start_time: datetime,
    ) -> Optional[str]:
        start_timestamp, end_timestamp = self._convert_timestamp(start_time)
        query = {
            "userId": user_id,
            "startedAt": {"$gte": start_timestamp, "$lte": end_timestamp},
        }
        result: List[Any] = self.request_query("focustimers", query)

        if result == []:
            print(f"Focustimer id not found for {user_id} at {start_time}")
            return None

        return result[-1]["_id"]

    # def get_focustimer_ids_from_user_id_and_range(
    def get_focustimer_ids_from_user_id_and_range(
        self,
        user_id: str,
        start_time: datetime,
        duration: timedelta,
    ) -> Optional[List[str]]:

        query = {
            "userId": ObjectId(user_id),
            "startedAt": {
                "$gte": start_time + timedelta(hours=18),  # hmm
                "$lte": start_time + duration + timedelta(hours=18),
            },
        }

        result: List[Any] = self.request_query("focustimers", query)

        for idx, element in enumerate(result):
            result[idx] = {
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

    def _convert_timestamp(
        self, start_time: datetime, start_delay: int = 0, end_delay: int = 1
    ) -> Tuple[int, int]:
        """
        일단은 임시로 이렇게 해두고 정석적인 시간 변환은 나중에 바꾸도록 하자
        """

        return datetime.fromtimestamp(
            (
                start_time - timedelta(minutes=start_delay) - timedelta(hours=18)
            ).timestamp()
        ), datetime.fromtimestamp(
            (
                start_time + timedelta(minutes=end_delay) - timedelta(hours=18)
            ).timestamp()
        )

    def get_total_efficiencies_from_focus_id(self, focus_id):
        focus_timer_records = self.db["focustimerrecords"]
        sepcific_focus_timer_records_list = list(
            focus_timer_records.find({"focusTimerId": focus_id})
        )

        total_efficiencies = []
        for seg in sepcific_focus_timer_records_list:
            efficiencies = seg["efficiencies"]
            total_efficiencies += efficiencies

        return total_efficiencies
