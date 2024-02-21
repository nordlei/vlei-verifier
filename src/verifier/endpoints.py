import json

import falcon
from keri.core import parsing, serdering,coring
from keri.vdr import verifying, eventing, viring
from keri.app import habbing


class PresentationCollectionResourceEndpoint:
    def __init__(self, hby: habbing.Habery, tvy: eventing.Tevery, vry: verifying.Verifier, reger: viring.Reger):
        self.habery = hby
        self.tvy = tvy
        self.verifier = vry
        self.reger = reger

    def on_post(self, req: falcon.Request, rep: falcon.Response):
        if req.content_type not in ("application/json+cesr",):
            raise falcon.HTTPBadRequest(description=f"invalid content type={req.content_type} for VC presentation")

        ims = req.bounded_stream.read()

        self.verifier.cues.clear()
        parsing.Parser().parse(ims=ims, kvy=self.habery.kvy, tvy=self.tvy, vry=self.verifier)

        found = False
        while self.verifier.cues:
            msg = self.verifier.cues.popleft()
            if "creder" in msg:
                creder: serdering.SerderACDC = msg["creder"]
                print(f"Got credential {creder.said}")
                found = True

        if not found:
            raise falcon.HTTPBadRequest(description=f"credential not processed in body of request")

        creds = self.reger.cloneCreds([coring.Saider(qb64=creder.said)], db=self.habery.db)
        if not creds:
            raise falcon.HTTPNotFound(description=f"credential for said {creder.said} not found.")

        rep.status = falcon.HTTP_200
        rep.content_type = "application/json"
        rep.data = bytes(json.dumps(creds[0]).encode("utf-8"))

