import trio
from ghunt.modules import login

trio.run(login.check_and_login, None, False)