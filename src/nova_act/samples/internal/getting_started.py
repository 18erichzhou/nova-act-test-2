from nova_act import NovaAct

# Use a context manager to navigate to the desired start page
with NovaAct(starting_page="https://www.amazon.com/fresh") as client:
    client.act("natural language here...")

# The client will be automatically stopped when exiting the 'with' block
# client.start() and client.stop() can also be called explicitly as well
