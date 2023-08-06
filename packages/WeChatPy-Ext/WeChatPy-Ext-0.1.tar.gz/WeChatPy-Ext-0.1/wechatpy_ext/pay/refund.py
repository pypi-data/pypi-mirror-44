# -*- coding: utf-8 -*-

import xmltodict
from xml.parsers.expat import ExpatError
from wechatpy.exceptions import InvalidSignatureException
import base64
import hashlib
from Crypto.Cipher import AES


def parse_refund_result(wechat_pay_api_key, xml):
    """
    解析退款结果
    https://github.com/jxtech/wechatpy/issues/266
    """
    try:
        data = xmltodict.parse(xml)
    except (xmltodict.ParsingInterrupted, ExpatError):
        raise InvalidSignatureException()

    if not data or 'xml' not in data:
        raise InvalidSignatureException()

    data = data['xml']
    req_info = base64.decodestring(data['req_info'].encode())

    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s: s[0:-ord(s[-1])]

    hash = hashlib.md5()
    hash.update(wechat_pay_api_key.encode())
    key = hash.hexdigest().encode()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypt_bytes = cipher.decrypt(req_info)
    decrypt_str = decrypt_bytes.decode()
    decrypt_str = unpad(decrypt_str)
    info = xmltodict.parse(decrypt_str)['root']
    data = dict(data, **info)
    data.pop('req_info')

    return data
