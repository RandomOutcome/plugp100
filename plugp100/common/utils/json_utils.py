import dataclasses
from typing import Any, Dict

Json = Dict[str, Any] 


def dataclass_encode_json(obj):
    return {k: v for k, v in dataclasses.asdict(obj).items() if v is not None}
