import sys

from app import App
from vita.vitamodule import VitaModule
from alpha.alphamodule import AlphaModule

app = App()
app.add_module(VitaModule())
app.add_module(AlphaModule())

sys.exit(app.run())
