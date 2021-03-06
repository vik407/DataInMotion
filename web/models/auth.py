#!/usr/bin/python3
"""
Simple auth signatures, key generation
should be avoided
and construct a more data dependent work
"""


from hashlib import sha1
import hmac, random, codecs, time
from urllib.parse import quote
import base64
import os

class Auth():
    """
    Defines the common auth operations
    """
    def __init__(self):
        self.nonce = ''


    def get_time(self):
        return str(int(time.time()))


    def gen_header(self, sig_data):
        """Contructs a header for the request"""
        # if 'status' in sig_data:
        #     del sig_data['status']
        keys = [st for st in sig_data.keys()]
        keys = sorted(keys)
        header_str = "OAuth "
        for par in keys:
            header_str += par
            header_str += '="'
            header_str += sig_data[par]
            header_str += '", '
        header_str = header_str[:-2]
        return header_str


    def gen_nonce(self):
        """This method generates the nonce string"""
        nonce = lambda length: list(filter(lambda s: chr(s).isalpha(), base64.b64encode(os.urandom(length * 2))))[:length]
        nonce = codecs.encode(bytes(nonce(32)), "base64").rstrip(bytes([10]))
        nonce = ''.join([chr(x) for x in nonce])[:-1]
        self.nonce = nonce
        return self.nonce


    def gen_sig(self, key1, key2, dic, url="", method=""):
            """This method generates the authorization signature"""
            print("========================\nGenerating signature\n")
            keys = [st for st in dic.keys()]
            keys = sorted(keys)
            out_s = ""
            # join the dict using = and &
            for attr in keys:
                key = quote(bytes(attr, "ascii"), safe="")
                out_s += key + "="
                out_s += quote(bytes(dic[attr], "UTF-8"), safe="")
                out_s += "&"
            # print(out_s)
            out_s = quote(bytes([ord(x) for x in out_s[:-1]]), safe="")
            url = quote(bytes([ord(x) for x in url]), safe="")
            # Adding the url and method
            par_str = "&".join([method, url, out_s])
            # print(par_str)
            par_str = bytes([ord(x) for x in par_str])
            sig_key = quote(bytes([ord(x) for x in key1]), safe="") + "&"
            sig_key += quote(bytes([ord(x) for x in key2]), safe="")
            sig_key = bytes([ord(x) for x in sig_key])
            # print(sig_key)
            # Hashing with hmac-sha1
            hashed = hmac.new(sig_key, par_str, sha1)
            # print(hashed)
            hashed = codecs.encode(hashed.digest(), "base64").rstrip(bytes([10]))
            # print(hashed)
            hashed = quote(hashed, safe="")
            print(hashed)
            print("========================")
            return hashed

