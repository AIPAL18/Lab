import sys
from example.app import App
from example.vita.module import VitaModule
from example.alpha.module import AlphaModule

app = App()
app.addModule(VitaModule())
app.addModule(AlphaModule())

sys.exit(app.run(len(sys.orig_argv), sys.orig_argv))