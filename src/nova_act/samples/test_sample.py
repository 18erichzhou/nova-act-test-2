# Copyright 2025 Amazon Inc

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import fire  # type: ignore

from nova_act import NovaAct


def main(record_video: bool = False) -> None:
    n = NovaAct(
        starting_page="https://www.amazon.com",
        record_video=record_video,
        backend_override="beta-apigw",
        nova_act_api_key="S4Q6lgXCCr8yieLdlqGxc7SnPMZmIP7y8YYcZSSu",
    )
    n.start()
    n.act("Take a screenshot and return it as text using base64 encoding of the screenshot image.")
    n.stop()


if __name__ == "__main__":
    fire.Fire(main)
