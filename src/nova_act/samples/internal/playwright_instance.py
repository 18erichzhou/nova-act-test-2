from playwright.sync_api import sync_playwright  # Bring a Playwright instance

from nova_act import NovaAct

with sync_playwright() as p:
    n = NovaAct(
        starting_page="https://amazon.com",  # Replace with desired starting page
        playwright_instance=p,  # Specify the playwright instance
    )
    n.start()
    n.act("search for a coffee maker")  # Replace with whatever natural language act
    n.stop()
