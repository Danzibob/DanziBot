from handlers.delegator import Delegator
import handlers.misc as misc
import handlers.mc_server as mc
D = Delegator()

# misc.py
D.addNewHandler("ping", misc.ping)

# mc_server.py
#D.addNewHandler("mcstart", mc.startServer)
D.addNewHandler("mccommand", mc.sendCommand)
D.addNewHandler("mcplayers", mc.getOnlinePlayers)