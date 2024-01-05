from atop.atop import Ton_retriever
import sys, os

if len(sys.argv) < 2:
    print("Please, use 'on' or 'off' argument")
    sys.exit(1)
create = sys.argv[1]
if create == "on":
    Ton_retriever.telegram_generate_session(".env")
    print("Session created")
elif create == "off":
    os.remove(".env")
    print("Session deleted")
else:
    print("Please, use 'on' or 'off' argument")
    sys.exit(1)


