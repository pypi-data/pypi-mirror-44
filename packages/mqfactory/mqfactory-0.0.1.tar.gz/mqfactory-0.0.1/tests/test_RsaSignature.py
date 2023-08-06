import pytest

import base64

from mqfactory.message.security.rsa import RsaSignature
from mqfactory.message.security.rsa import sign, validate
from mqfactory.message.security.rsa import serialize, encode, decode

def test_own_key_loading(keys, me):
  signer = RsaSignature(keys, me=me)
  assert encode(signer.key) == keys[me]["private"]

def test_signing(message, keys, me):
  signer = RsaSignature(keys, me=me)
  signer.sign(message, ts="now")
  assert "signature" in message.tags
  assert "origin" in message.tags["signature"]
  assert message.tags["signature"]["origin"] == me
  assert "ts" in message.tags["signature"]
  assert message.tags["signature"]["ts"] == "now"
  assert "hash" in message.tags["signature"]
  hash = base64.b64decode(message.tags["signature"].pop("hash"))
  # must use validation, cannot compare signatures as such
  validate(serialize(message), hash, decode(keys[me]["public"]))

def test_validation(message, keys, me):
  message.tags["signature"] = {
    "origin": me,
    "ts"    : "now"
  }
  message.tags["signature"]["hash"] = base64.b64encode(
    sign(serialize(message), decode(keys[me]["private"]))
  )
  signer = RsaSignature(keys, me=me)
  signer.validate(message)
