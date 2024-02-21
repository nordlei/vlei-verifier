# -*- encoding: utf-8 -*-
import argparse
import logging
import falcon
from hio.core import http
from keri.app import keeping, configing, habbing, oobiing, directing
from keri.app.cli.common import existing
from keri.vdr.viring import Reger
from keri.vdr.eventing import Tevery
from keri.vdr.verifying import Verifier
from verifier import endpoints
from keri import help

parser = argparse.ArgumentParser(description='Launch vLEI Verification Service')
parser.set_defaults(handler=lambda args: launch(args),
                    transferable=True)
parser.add_argument('-p', '--http',
                    action='store',
                    default='7676',
                    help="Port on which to listen for verification requests")
parser.add_argument('-n', '--name',
                    action='store',
                    default="vdb",
                    help="Name of controller. Default is vdb.")
parser.add_argument('--base', '-b', help='additional optional prefix to file location of KERI keystore',
                    required=False, default="")
parser.add_argument('--passcode', help='22 character encryption passcode for keystore (is not saved)',
                    dest="bran", default=None)  # passcode => bran
parser.add_argument("--config-dir",
                    "-c",
                    dest="configDir",
                    help="directory override for configuration data",
                    default=None)
parser.add_argument('--config-file',
                    dest="configFile",
                    action='store',
                    default="dkr",
                    help="configuration filename override")

help.ogler.level = logging.INFO
help.ogler.reopen(name="verifer", temp=True, clear=True)

def launch(args: argparse.Namespace):
    name = args.name
    base = args.base
    bran = args.bran
    httpPort = int(args.http)

    configFile = args.configFile
    configDir = args.configDir

    ks = keeping.Keeper(name=name,
                        base=base,
                        temp=False,
                        reopen=True)

    aeid = ks.gbls.get('aeid')

    cf = configing.Configer(name=configFile,
                            base=base,
                            headDirPath=configDir,
                            temp=False,
                            reopen=True,
                            clear=False)

    if aeid is None:
        hby = habbing.Habery(name=name, base=base, bran=bran, cf=cf)
    else:
        hby = existing.setupHby(name=name, base=base, bran=bran)

    hbyDoer = habbing.HaberyDoer(habery=hby)
    obl = oobiing.Oobiery(hby=hby)

    reger = Reger(name=hby.name, temp=hby.temp)

    app = falcon.App(
        middleware=falcon.CORSMiddleware(
            allow_origins='*',
            allow_credentials='*',
            expose_headers=['cesr-attachment', 'cesr-date', 'content-type']))

    server = http.Server(port=httpPort, app=app)
    httpServerDoer = http.ServerDoer(server=server)

    tvy = Tevery(reger=reger, db=hby.db)
    vry = Verifier(hby=hby, reger=reger)

    presentEnd = endpoints.PresentationCollectionResourceEndpoint(hby=hby, tvy=tvy, vry=vry, reger=reger)
    app.add_route("/", presentEnd)

    doers = obl.doers + [hbyDoer, httpServerDoer]

    print(f"vLEI Verification Service running and listening on: {httpPort}")
    return doers

def main():
    args = parser.parse_args()

    try:
        doers = launch(args)
        directing.runController(doers=doers, expire=0.0)

    except Exception as ex:
        raise ex


if __name__ == "__main__":
    main()
