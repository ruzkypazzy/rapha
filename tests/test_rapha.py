"""
Smoke tests for rapha — Research Assistant on Pharos.

Covers:
  - Pure helpers (hex/address/ABI decoding)
  - PharosRPC basics
  - Sub-command error handling
  - Live RPC end-to-end via demo
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402

import rapha  # noqa: E402
from rapha import (  # noqa: E402
    _hex_to_int, _hex_to_str, _hex_to_address, _addr_padded, _strip_hex,
    PharosRPC, KNOWN_TOKENS,
)


# -------- pure helpers --------

def test_hex_to_int_handles_zero():
    assert _hex_to_int("0x") == 0
    assert _hex_to_int("0x0") == 0
    assert _hex_to_int(None) == 0
    assert _hex_to_int("0xff") == 255
    assert _hex_to_int("0x1234") == 0x1234


def test_strip_hex_drops_prefix():
    assert _strip_hex("0x1234") == "1234"
    assert _strip_hex("1234") == "1234"
    assert _strip_hex("0x") == ""


def test_addr_padded_is_64_hex_chars():
    p = _addr_padded("0x67992af9a87f2d6a3062c333d8a06abbe3929438")
    assert p.startswith("0x")
    assert len(p) == 66
    assert p.endswith("67992af9a87f2d6a3062c333d8a06abbe3929438")


def test_hex_to_str_decodes_abi_string():
    # name() USDC = 0x000...002000...0455534443...
    h = ("0x0000000000000000000000000000000000000000000000000000000000000020"
         "0000000000000000000000000000000000000000000000000000000000000004"
         "5553444300000000000000000000000000000000000000000000000000000000")
    assert _hex_to_str(h) == "USDC"


def test_hex_to_str_handles_short():
    assert _hex_to_str("0x") == ""
    assert _hex_to_str(None) == ""


def test_hex_to_address_extracts_last_20_bytes():
    # The balanceOf selector + 32-byte zero-padded address
    h = "0x000000000000000000000000" + "67992af9a87f2d6a3062c333d8a06abbe3929438"
    assert _hex_to_address(h) == "0x67992af9a87f2d6a3062c333d8a06abbe3929438"


# -------- PharosRPC --------

def test_pharos_rpc_known_chains():
    """Both mainnet and testnet must be configured."""
    for k in ("mainnet", "testnet"):
        assert k in rapha.CHAINS
        assert "rpc" in rapha.CHAINS[k]
        assert "explorer" in rapha.CHAINS[k]
        assert "chain_id" in rapha.CHAINS[k]
        assert "symbol" in rapha.CHAINS[k]


def test_pharos_rpc_rejects_unknown_chain():
    with pytest.raises(ValueError):
        PharosRPC("bitcoin_mainnet")


def test_known_tokens_at_least_one():
    """KNOWN_TOKENS list should have at least one Pharos ERC-20."""
    assert len(KNOWN_TOKENS) >= 1
    for t in KNOWN_TOKENS:
        assert t.startswith("0x")
        assert len(t) == 42


# -------- live RPC tests --------

@pytest.mark.skipif(
    not os.environ.get("PHAROS_LIVE", "1") == "1",
    reason="set PHAROS_LIVE=1 to run live RPC tests",
)
def test_live_mainnet_balance():
    rpc = PharosRPC("mainnet")
    bal = rpc.get_balance("0x67992af9a87f2d6a3062c333d8a06abbe3929438")
    assert isinstance(bal, int)
    assert bal > 0


@pytest.mark.skipif(
    not os.environ.get("PHAROS_LIVE", "1") == "1",
    reason="set PHAROS_LIVE=1 to run live RPC tests",
)
def test_live_mainnet_tx_count():
    rpc = PharosRPC("mainnet")
    cnt = rpc.get_tx_count("0x67992af9a87f2d6a3062c333d8a06abbe3929438")
    assert isinstance(cnt, int)
    assert cnt > 0


@pytest.mark.skipif(
    not os.environ.get("PHAROS_LIVE", "1") == "1",
    reason="set PHAROS_LIVE=1 to run live RPC tests",
)
def test_live_mainnet_eth_call_name():
    """name() on USDC should return 'USDC'."""
    rpc = PharosRPC("mainnet")
    h = rpc.eth_call("0xc879c018db60520f4355c26ed1a6d572cdac1815", "0x06fdde03")
    assert _hex_to_str(h) == "USDC"


@pytest.mark.skipif(
    not os.environ.get("PHAROS_LIVE", "1") == "1",
    reason="set PHAROS_LIVE=1 to run live RPC tests",
)
def test_live_mainnet_eth_call_decimals():
    """decimals() on USDC should return 6."""
    rpc = PharosRPC("mainnet")
    h = rpc.eth_call("0xc879c018db60520f4355c26ed1a6d572cdac1815", "0x313ce567")
    assert _hex_to_int(h) == 6
