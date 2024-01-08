from atop.atop import Ton_retriever
import sys, os

BASE_DIR = os.path.dirname(__file__)
CONFIGFILE: str = os.path.join(BASE_DIR,'.env')

if len(sys.argv) < 2:
    print("Please, use 'on' or 'off' argument")
    sys.exit(1)
create = sys.argv[1]
if create == "on":
    Ton_retriever.telegram_generate_session(CONFIGFILE)
    print("Session created")
elif create == "off":
    os.remove(CONFIGFILE)
    print("Session deleted")
else:
    print("Please, use 'on' or 'off' argument")
    sys.exit(1)


