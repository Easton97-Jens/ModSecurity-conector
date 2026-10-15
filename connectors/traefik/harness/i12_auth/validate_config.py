"""Check the actual generated Traefik YAML before any host starts."""
import json
from pathlib import Path
import sys
import yaml


def validate(text):
    value=yaml.safe_load(text)['http']
    assert set(value['routers'])=={'smoke','fault'}
    assert value['routers']['smoke']['middlewares']==['modsecurity-forwardauth','modsecurity-response-observer']
    assert value['routers']['smoke']['service']=='upstream'
    assert value['routers']['fault']['middlewares']==['modsecurity-forwardauth','observer-fault']
    assert value['routers']['fault']['rule']=='Path(`/mrc1-error`)'
    assert set(value['middlewares'])=={'modsecurity-forwardauth','modsecurity-response-observer','observer-fault'}
    auth=value['middlewares']['modsecurity-forwardauth']['forwardAuth']
    assert auth['forwardBody'] is True and auth['maxBodySize']==4096
    assert auth['maxResponseBodySize']==32768
    assert value['middlewares']['observer-fault']['plugin']['modsecurityResponseObserver']['socketPath']=='/task/sockets/fault.sock'
    assert value['services']['upstream']['loadBalancer']['servers']
    return value

if __name__=='__main__':
    validate(Path(sys.argv[1]).read_text());print(json.dumps({'yaml':'valid','routers':['smoke','fault'],'maxBodySize':4096,'maxResponseBodySize':32768}))
