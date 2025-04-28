from attrs import define, field
from attrs.setters import frozen


@define
class PageState:
    # Required constructor params (immutable)
    session_id: str = field(on_setattr=frozen)
    is_settled: bool = field(factory=lambda: False, init=False)
