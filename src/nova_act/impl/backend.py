from dataclasses import dataclass
from enum import Enum


class Backend(Enum):
    PROD = "prod"


@dataclass
class BackendInfo:
    api_uri: str
    keygen_uri: str




URLS_BY_BACKEND = {
    Backend.PROD: BackendInfo(
        "https://nova.amazon.com/agent",
        "https://nova.amazon.com/act",
    ),
}


def get_urls_for_backend(backend: Backend) -> BackendInfo:
    return URLS_BY_BACKEND[backend]
