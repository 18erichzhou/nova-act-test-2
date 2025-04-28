import concurrent.futures
import os

from nova_act import NovaAct

# Remove this once no need to use special extension path to get product
# stack variant of extension.
# EXT_PATH has unzipped folder with the product stack compatible extension
# talking to NovaAct Gateway Service.
ext_path = os.environ.get("EXT_PATH")


def run_acts_in_session(session):
    nova_act = NovaAct(
        extension_path=ext_path,
        starting_page=session.get("url", "https://google.com"),
    )
    nova_act.start()
    return_values = []
    for prompt in session.get("acts"):
        return_values.append(nova_act.act(prompt))
    nova_act.stop()
    return return_values


if __name__ == "__main__":

    print("Running sessions")

    sessions = [
        {
            "url": "https://google.com",
            "acts": [
                "find images of kittens",
                "select one that has black hair",
                "find the type of that cat",
                "return the name of cat",
            ],
        },
        {
            "url": "https://amazon.com",
            "acts": [
                "find mbot robot",
                "find one that works with python",
                "add it to cart",
                "return total price",
            ],
        },
        {
            "url": "https://bestbuy.com",
            "acts": [
                "find robots for kids education",
                "find one that works with python",
                "add it to cart",
                "return total price",
            ],
        },
        {
            "url": "https://walmart.com",
            "acts": ["find red roses made of plastic", "select one that ships today", "add to cart"],
        },
        {
            "url": "https://costco.com",
            "acts": ["find red roses", "select one that has variety", "add to cart"],
        },
        {
            "url": "https://amazon.com",
            "acts": ["find red roses", "select one that has variety", "add to cart"],
        },
        {
            "url": "https://google.com",
            "acts": [
                "find images of cat",
                "select one that has no hair",
                "find name of cat",
                "return the name of cat",
            ],
        },
        {
            "url": "https://kayak.com",
            "acts": [
                "find cheapest ticket to kathmandu from boston",
                "tell me if that has more than one stop",
            ],
        },
    ]

    executor = concurrent.futures.ThreadPoolExecutor()

    worker_threads = [executor.submit(run_acts_in_session, session) for session in sessions]
    results = [thread.result() for thread in concurrent.futures.as_completed(worker_threads)]
    for result in results:
        print(results)
