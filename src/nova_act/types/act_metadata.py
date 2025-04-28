import dataclasses
from datetime import datetime


@dataclasses.dataclass(frozen=True)
class ActMetadata:
    session_id: str
    act_id: str
    num_steps_executed: int
    start_time: float | None
    end_time: float | None
    prompt: str

    def __repr__(self) -> str:
        local_tz = datetime.now().astimezone().tzinfo

        # Convert Unix timestamps to readable format if they exist
        start_time_str = (
            datetime.fromtimestamp(self.start_time, tz=local_tz).strftime("%Y-%m-%d %H:%M:%S.%f %Z")
            if self.start_time is not None
            else "None"
        )
        end_time_str = (
            datetime.fromtimestamp(self.end_time, tz=local_tz).strftime("%Y-%m-%d %H:%M:%S.%f %Z")
            if self.end_time is not None
            else "None"
        )

        return (
            f"ActMetadata(\n"
            f"    session_id = {self.session_id}\n"
            f"    act_id = {self.act_id}\n"
            f"    num_steps_executed = {self.num_steps_executed}\n"
            f"    start_time = {start_time_str}\n"
            f"    end_time = {end_time_str}\n"
            f"    prompt = '{self.prompt}'\n"
            f")"
        )
