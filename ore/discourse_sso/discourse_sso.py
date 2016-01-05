import hashlib
import hmac
import base64
import json
import urllib.parse
import time


def newrand():
    with open('/dev/urandom', 'rb') as f:
        return f.read(16)


def newnonce(key):
    inner_nonce = base64.b64encode(newrand()).decode('utf-8')
    timestamp = time.time()
    nonce_pair = '{}:{}'.format(timestamp, inner_nonce)
    signature = signdata(nonce_pair.encode('utf-8'), key)
    signed_nonce_pair = '{}:{}'.format(signature, nonce_pair)
    return signed_nonce_pair


def checknonce(nonce, key, now=None, allowed_skew=10):
    now = now or time.time()
    signature, _, nonce_pair = nonce.partition(':')
    valid_signature = signdata(nonce_pair.encode('utf-8'), key)
    if not hmac.compare_digest(valid_signature, signature):
        raise Exception('NOPE')
    timestamp_str, _, inner_nonce = nonce_pair.partition(':')
    timestamp = float(timestamp_str)
    return timestamp >= (now - allowed_skew)


def newpayload(d):
    return base64.b64encode(urllib.parse.urlencode(d).encode('utf-8'))


def signdata(text, key):
    return hmac.new(key.encode('utf-8'), text, hashlib.sha256).hexdigest()


def unsigndata(sso, sig, key):
    valid_sig = signdata(sso.encode('utf-8'), key)
    if not hmac.compare_digest(valid_sig, sig):
        raise Exception('NOPE')

    qs = base64.b64decode(sso)
    data = urllib.parse.parse_qs(qs)
    data = {k.decode('utf-8'): v[0].decode('utf-8') for k, v in data.items()}
    bools = ['avatar_force_update', 'admin', 'moderator',
             'require_activation', 'suppress_welcome_message']
    for booln in bools:
        if booln not in data.keys():
            continue
        if data[booln] not in ('true', 'false'):
            data[booln] = None
            continue
        data[booln] = data[booln] == 'true'
    return data


def generate_payload(ret_url, privkey):
    return newpayload({
        'return_sso_url': ret_url,
        'nonce': newnonce(privkey),
    })


def generate_signed_query(ret_url, key, privkey):
    payload = generate_payload(ret_url, privkey)
    payload_sig = signdata(payload, key)
    return urllib.parse.urlencode({
        'sso': payload,
        'sig': payload_sig,
    })


def unsign_query(query, key, privkey):
    resp_url_qsd = {k: v[0] for k, v in urllib.parse.parse_qs(query).items()}
    ddata = unsigndata(
        resp_url_qsd['sso'].encode('utf-8'), resp_url_qsd['sig'], key)
    if not checknonce(ddata['nonce']):
        raise Exception('nonce out of data or invalid')
    return ddata

#print(BASE_URL + generate_signed_query('http://localhost', SEKRIT, MY_SEKRIT))
#
#resp_url = input('>>> ')
#resp_url_data = urllib.parse.urlparse(resp_url)
#import pprint
#pprint.pprint(unsign_query(resp_url_data.query, SEKRIT, MY_SEKRIT))
