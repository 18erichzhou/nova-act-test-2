# this might trigger model error, might need multiple runs and its not guaranteed
# to trigger a model error
import fire  # type: ignore

from nova_act import NovaAct


def main(record_video: bool = False) -> None:
    n = NovaAct(starting_page="https://www.amazon.com", record_video=record_video, backend_override="beta")
    # n._backend_info.api_uri = "https://<add if needed>.execute-api.us-west-2.amazonaws.com/personal"
    n.start()
    n.act("Take a screenshot and return it as text using base64 encoding of the screenshot image.")
    n.stop()


if __name__ == "__main__":
    fire.Fire(main)
