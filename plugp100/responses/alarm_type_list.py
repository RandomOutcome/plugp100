from dataclasses import dataclass
from typing import List, Any, Dict

from plugp100.common.functional.tri import Try


@dataclass
class AlarmTypeList(object):
    tones: List[str]

    @staticmethod
    def try_from_json(kwargs: Dict[str, Any]) -> Try["AlarmTypeList"]:
        return Try.of(lambda: AlarmTypeList(kwargs.get("alarm_type_list", [])))
