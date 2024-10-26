from fastcore.script import call_parse

from aifront.dashboard import Dashboard
from aifront.overlay.main import EnvOverlay


@call_parse
def main(
    i: int = 20,  # figure switching interval
    ema: int = 50,  # collect figure ema
):
    dashboard = Dashboard(interval=i * 1000, ema=ema)
    overlay = EnvOverlay()
    input("Press any key to shutdown the front ...")
    print("Bye bye")
