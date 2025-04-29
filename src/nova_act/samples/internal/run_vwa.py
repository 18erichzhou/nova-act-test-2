"""
Dependencies:
    "browsergym-visualwebarena>=0.13.0",
    "fire>=0.5.0",
    "rich>=13.0.0",
    "install_playwright==0.0.1"

This script is used to run a task in VisualWebArena.

You need to set the following environment variables before running this script:
```
export VWA_SHOPPING="http://..."
export VWA_REDDIT="http://..."
export VWA_WIKIPEDIA="http://..."
export VWA_CLASSIFIEDS="http://..."
export VWA_CLASSIFIEDS_RESET_TOKEN="4b61655535e7ed388f0d40a93600254c"
export VWA_HOMEPAGE="http://..."
# You need a valid OpenAI API key if you're running a task with an evaluator config using fuzzy_match
export OPENAI_API_KEY="none"
```

Usage:
    python run_vwa.py <TASK_ID>

    TASK_ID: The task ID to run. You can find the complete list of tasks on this path:

    $ python -c 'import importlib.resources, visualwebarena;
        print((importlib.resources.files(visualwebarena).joinpath("test_raw.json")))'

"""

import importlib.resources
import json
import logging
import sys
import tempfile

import playwright.sync_api
import requests
import torch
import visualwebarena
from browsergym.visualwebarena.instance import VisualWebArenaInstance
from rich import print_json

from nova_act import NovaAct

logger = logging.getLogger(__name__)


class VisualWebArenaTask:
    def __init__(
        self,
        webarena_instance: VisualWebArenaInstance,
        config: dict,
    ) -> None:
        self.webarena_instance = webarena_instance
        self.config = config

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            json.dump(self.config, f)
            f.flush()
            self.config_file = f.name

    def setup(self, page: playwright.sync_api.Page) -> None:
        # import webarena on instanciation
        # build the evaluator
        from transformers.utils.logging import disable_progress_bar, enable_progress_bar, is_progress_bar_enabled
        from visualwebarena.evaluation_harness.evaluators import evaluator_router
        from visualwebarena.evaluation_harness.image_utils import get_captioning_fn

        hide_progress_bar = is_progress_bar_enabled()
        if hide_progress_bar:
            disable_progress_bar()
        captioning_fn = get_captioning_fn(
            device=("cuda" if torch.cuda.is_available() else "cpu"),
            dtype=(torch.float16 if torch.cuda.is_available() else torch.float32),
            model_name="Salesforce/blip2-flan-t5-xl",
        )
        if hide_progress_bar:
            enable_progress_bar()
        self.evaluator = evaluator_router(self.config_file, captioning_fn=captioning_fn)

        # reset instance if needed (classifieds domain only)
        if self.config.get("require_reset", False):
            if "classifieds" in self.config["sites"]:
                # Send POST request to __CLASSIFIEDS__/index.php?page=reset with token=CLASSIFIEDS_TOKEN
                response = requests.post(
                    f'{self.webarena_instance.urls["classifieds"]}/index.php?page=reset',
                    data={"token": self.webarena_instance.classifieds_reset_token},
                )

                # Check if the request was successful
                if not response.status_code == 200:
                    raise Exception(f"Failed to reset Classifieds site: {response.status_code}")

                logger.info("Reset Classifieds site successful.")

        # authenticate
        for site in self.config["sites"]:
            print(f"Authenticating user on the {site} website")
            self.webarena_instance.ui_login(site=site, page=page)

        # set geolocation
        page.context.set_geolocation(self.config["geolocation"])

    def evaluate(self, page: playwright.sync_api.Page, answer: str) -> tuple[float, bool, str, dict]:
        # import webarena dynamically
        from visualwebarena.browser_env.actions import ActionTypes

        # hack: fake trajectory for evaluation (only last_action["answer"] is used in the webarena evaluation codebase)
        trajectory = [
            {},
            {"action_type": ActionTypes.NONE, "answer": answer},
        ]  # StateInfo, Action

        # call the evaluator
        try:
            score = self.evaluator(
                trajectory=trajectory,
                config_file=self.config_file,
                page=page,  # none of webarena's evaluators requires a cdp session
            )
        # llm_fuzzy_match() bugfix (assert "correct" in response)
        except AssertionError:
            logger.info("llm_fuzzy_match() bugfix applied: AssertionError in evaluator, using score = 0.0")
            score = 0.0

        return score

    @property
    def intent(self):
        return self.config.get("intent")

    @property
    def start_url(self):
        return self.config.get("start_url")


def main(task_id) -> None:
    task_id = int(task_id)
    webarena_instance = VisualWebArenaInstance()
    all_configs_str = importlib.resources.files(visualwebarena).joinpath("test_raw.json").read_text()

    # substitute URLs
    for pattern, url_key in {
        "__REDDIT__": "reddit",
        "__SHOPPING__": "shopping",
        "__CLASSIFIEDS__": "classifieds",
        "__WIKIPEDIA__": "wikipedia",
    }.items():
        all_configs_str = all_configs_str.replace(pattern, webarena_instance.urls[url_key])

    config = next(
        (config for config in json.loads(all_configs_str) if config.get("task_id") == task_id),
        None,
    )

    if config is None:
        raise ValueError(f"No config found for task_id={task_id}")

    task = VisualWebArenaTask(webarena_instance, config)
    print("Task config")
    print_json(json.dumps(task.config))
    print(f"Task: {task.intent}")

    with NovaAct(starting_page=task.start_url, headless=False, quiet=True) as client:
        task.setup(client.page)
        client.go_to_url(task.start_url)

        answer = client.act(task.intent)
        if answer:
            print(f"Answer: {answer}")

        print("Running the evaluator")
        score = task.evaluate(client.page, answer)

        print(f"Score: {score}")


if __name__ == "__main__":
    main(sys.argv[1])
