from dataclasses import dataclass
from enum import Enum


class Backend(Enum):
    PROD = "prod"
    # pragma: internal-start
    LOCAL = "local"
    PRODUCT_SERVER_STAGING = "product-server-staging"
    GAMMA = "gamma"
    BETA = "beta"
    BETA_APIGW = "beta-apigw"
    # pragma: internal-stop


@dataclass
class BackendInfo:
    api_uri: str
    keygen_uri: str


# pragma: internal-start
@dataclass
class LegacyBackendInfo(BackendInfo):
    internal_tools_uri: str


# pragma: internal-stop


URLS_BY_BACKEND = {
    Backend.PROD: BackendInfo(
        "https://nova.amazon.com/agent",
        "https://nova.amazon.com/act",
    ),
    # pragma: internal-start
    Backend.GAMMA: BackendInfo(
        "https://nova-preprod.aka.amazon.com/agent",
        "https://nova-preprod.aka.amazon.com/act",
    ),
    Backend.LOCAL: LegacyBackendInfo(
        "http://localhost:8080",
        "http://localhost:4444/api-keys",
        "http://localhost:4444",
    ),
    Backend.PRODUCT_SERVER_STAGING: LegacyBackendInfo(
        "https://product-server-internal.autonomy.agi.amazon.dev",
        "https://internal-tools.autonomy.agi.amazon.dev/api-keys",
        "https://internal-tools.autonomy.agi.amazon.dev",
    ),
    Backend.BETA_APIGW: BackendInfo(
        "https://u83po73hf9.execute-api.us-west-2.amazonaws.com/personal",
        "https://beta.console.harmony.a2z.com/agi-nexus",
    ),
    Backend.BETA: BackendInfo(
        "https://nova-beta.integ.amazon.com/agent",
        "https://nova-beta.integ.amazon.com/nexus",
    ),
    # pragma: internal-stop
}


def get_urls_for_backend(backend: Backend) -> BackendInfo:
    return URLS_BY_BACKEND[backend]
