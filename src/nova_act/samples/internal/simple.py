from nova_act import NovaAct

with NovaAct(starting_page="https://www.google.com") as client:
    client.act("search for images of sunshine.")
    result = client.act("what are the dominant colors on the screen")
    print(f"I got {result}")
