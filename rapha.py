#!/usr/bin/env python3
"""
rapha — Research Assistant on Pharos.

A multi-tool on-chain research CLI for AI agents. It exposes three
sub-commands that the agent can call from a single prompt:

  1. wallet  — forensics on any address (balance, tx count, ERC-20 holdings)
  2. token   — token intelligence (name, symbol, decimals, supply, total transfers)
  3. report  — composite "research report" that runs wallet + token in one shot

Each sub-command is a thin wrapper around JSON-RPC calls to the
Pharos Pacific Mainnet (default) or Atlantic Testnet.

Usage:
  python rapha.py wallet <ADDRESS> [--chain mainnet|testnet]
  python rapha.py token <TOKEN_ADDRESS> [--chain mainnet|testnet]
  python rapha.py report <ADDRESS> <TOKEN_ADDRESS> [--chain mainnet|testnet]
  python rapha.py demo
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from typing import Any, Dict, List, Optional


CHAINS = {
    "mainnet": {
        "label": "Pharos Pacific Mainnet",
        "chain_id": 1672,
        "rpc": "https://rpc.pharos.xyz",
        "explorer": "https://www.pharosscan.xyz",
        "symbol": "PROS",
    },
    "testnet": {
        "label": "Pharos Atlantic Testnet",
        "chain_id": 688689,
        "rpc": "https://atlantic.dplabs-internal.com",
        "explorer": "https://atlantic.pharosscan.xyz",
        "symbol": "PHRS",
    },
}

# ERC-20 selectors we need
SEL_BALANCE_OF   = "0x70a08231"  # balanceOf(address)
SEL_NAME         = "0x06fdde03"  # name()
SEL_SYMBOL       = "0x95d89b41"  # symbol()
SEL_DECIMALS     = "0x313ce567"  # decimals()
SEL_TOTAL_SUPPLY = "0x18160ddd"  # totalSupply()

# Some "well-known" ERC-20 tokens on Pharos Pacific mainnet.
# Used by `wallet --tokens` to do a quick holdings scan without
# requiring a third-party indexer.
KNOWN_TOKENS = [
    "0xc879c018db60520f4355c26ed1a6d572cdac1815",  # USDC (6 decimals)
    # Add more as the ecosystem grows.
]


class PharosRPC:
    def __init__(self, chain: str = "mainnet"):
        if chain not in CHAINS:
            raise ValueError(f"unknown chain: {chain!r}; expected one of {list(CHAINS)}")
        self.chain = chain
        self.cfg = CHAINS[chain]

    def call(self, method: str, params: List[Any], retries: int = 2) -> Any:
        """JSON-RPC call with simple retry on transient failures."""
        payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
        last_err = None
        for attempt in range(retries + 1):
            try:
                req = urllib.request.Request(
                    self.cfg["rpc"], data=payload,
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=20) as r:
                    resp = json.loads(r.read())
                if "error" in resp:
                    raise RuntimeError(f"RPC error: {resp['error']}")
                return resp.get("result")
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
                last_err = e
                if attempt < retries:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raise RuntimeError(f"RPC failed after {retries+1} tries: {e}")

    # -------- high-level helpers --------

    def get_balance(self, addr: str) -> int:
        h = self.call("eth_getBalance", [addr, "latest"])
        return int(h, 16) if h and h != "0x" else 0

    def get_tx_count(self, addr: str) -> int:
        h = self.call("eth_getTransactionCount", [addr, "latest"])
        return int(h, 16) if h and h != "0x" else 0

    def get_code(self, addr: str) -> str:
        return self.call("eth_getCode", [addr, "latest"]) or "0x"

    def get_block_number(self) -> int:
        h = self.call("eth_blockNumber", [])
        return int(h, 16) if h and h != "0x" else 0

    def get_logs(self, addr: str, from_block: str = "0x0", to_block: str = "latest",
                 topic0: Optional[str] = None) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {
            "address": addr,
            "fromBlock": from_block,
            "toBlock": to_block,
        }
        if topic0:
            params["topics"] = [topic0]
        return self.call("eth_getLogs", [params]) or []

    def eth_call(self, to: str, data: str) -> str:
        return self.call("eth_call", [{"to": to, "data": data}, "latest"]) or "0x"


# -------- pure helpers --------

def _hex_to_int(h: Optional[str]) -> int:
    if not h or h == "0x": return 0
    return int(h, 16)

def _strip_hex(s: str) -> str:
    if s.startswith("0x"): s = s[2:]
    return s

def _addr_padded(addr: str) -> str:
    """Encode an address as 32-byte ABI-encoded hex (for eth_call args)."""
    return "0x" + addr.lower().replace("0x", "").rjust(64, "0")

def _hex_to_str(h: Optional[str]) -> str:
    """Decode an ABI-encoded string (offset + len + data) from an eth_call result."""
    if not h or h == "0x" or len(h) < 130: return ""
    s = _strip_hex(h)
    try:
        length = int(s[64:128], 16)
        data = bytes.fromhex(s[128:128 + 2*length])
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""

def _hex_to_address(h: Optional[str]) -> str:
    if not h or h == "0x": return ""
    s = _strip_hex(h)
    return "0x" + s[-40:]


# -------- sub-commands --------

def cmd_wallet(args: argparse.Namespace) -> int:
    """Wallet forensics: balance, tx count, code status, ERC-20 holdings."""
    rpc = PharosRPC(args.chain)
    if not args.address.startswith("0x") or len(args.address) != 42:
        print(f"❌ invalid address: {args.address}")
        return 2

    address = args.address.lower()
    try:
        balance = rpc.get_balance(address)
        tx_count = rpc.get_tx_count(address)
        code = rpc.get_code(address)
        is_contract = code not in ("0x", "0x0", "", None)
        block = rpc.get_block_number()
    except Exception as e:
        print(f"❌ RPC error: {e}")
        return 1

    # Optional: scan known ERC-20 holdings
    holdings: List[Dict[str, Any]] = []
    if not args.no_tokens:
        for token in KNOWN_TOKENS:
            try:
                bal_h = rpc.eth_call(token, SEL_BALANCE_OF + _addr_padded(address)[2:])
                bal = _hex_to_int(bal_h)
                if bal > 0:
                    sym_h = rpc.eth_call(token, SEL_SYMBOL)
                    dec_h = rpc.eth_call(token, SEL_DECIMALS)
                    symbol = _hex_to_str(sym_h) or "?"
                    decimals = _hex_to_int(dec_h) or 18
                    holdings.append({
                        "token": token,
                        "symbol": symbol,
                        "decimals": decimals,
                        "balance_raw": bal,
                        "balance_human": bal / (10 ** decimals),
                    })
            except Exception:
                continue

    if args.json:
        print(json.dumps({
            "type": "rapha_wallet_report",
            "chain": args.chain,
            "address": address,
            "balance_native": balance / 1e18,
            "balance_wei": balance,
            "tx_count": tx_count,
            "is_contract": is_contract,
            "code_size_bytes": (len(code) - 2) // 2 if is_contract else 0,
            "block_number": block,
            "holdings": holdings,
            "explorer_url": f"{rpc.cfg['explorer']}/address/{address}",
        }, indent=2))
        return 0

    print("=" * 72)
    print(f"  RAPHA — Wallet Forensics on {rpc.cfg['label']}")
    print("=" * 72)
    print(f"  address:    {address}")
    print(f"  balance:    {balance / 1e18:,.6f} {rpc.cfg['symbol']} ({balance:,} wei)")
    print(f"  tx count:   {tx_count:,}")
    print(f"  contract:   {'yes (' + str((len(code) - 2) // 2) + ' bytes code)' if is_contract else 'no (EOA)'}")
    print(f"  block:      {block:,}")
    print(f"  explorer:   {rpc.cfg['explorer']}/address/{address}")
    print()
    if holdings:
        print(f"  ERC-20 holdings (of {len(KNOWN_TOKENS)} known tokens):")
        for h in holdings:
            print(f"    • {h['symbol']:6s}  {h['balance_human']:,.4f}  ({h['token']})")
    else:
        print(f"  ERC-20 holdings: none found in known-token list ({len(KNOWN_TOKENS)} tokens scanned)")
        print(f"  (add addresses to KNOWN_TOKENS in rapha.py to expand coverage)")
    print("=" * 72)
    return 0


def cmd_token(args: argparse.Namespace) -> int:
    """Token intelligence: name, symbol, decimals, supply, transfer count."""
    rpc = PharosRPC(args.chain)
    if not args.token.startswith("0x") or len(args.token) != 42:
        print(f"❌ invalid token address: {args.token}")
        return 2

    token = args.token.lower()
    try:
        name_h = rpc.eth_call(token, SEL_NAME)
        sym_h  = rpc.eth_call(token, SEL_SYMBOL)
        dec_h  = rpc.eth_call(token, SEL_DECIMALS)
        sup_h  = rpc.eth_call(token, SEL_TOTAL_SUPPLY)
        # count Transfer events (capped to last 1,000 blocks to avoid huge RPCs)
        block = rpc.get_block_number()
        from_block = max(0, block - 1000)
        logs = rpc.get_logs(token, hex(from_block), "latest",
                            topic0="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef")
    except Exception as e:
        print(f"❌ RPC error: {e}")
        return 1

    name = _hex_to_str(name_h) or "?"
    symbol = _hex_to_str(sym_h) or "?"
    decimals = _hex_to_int(dec_h)
    total_supply = _hex_to_int(sup_h) / (10 ** decimals if decimals else 1)
    transfer_count = len(logs)

    if args.json:
        print(json.dumps({
            "type": "rapha_token_report",
            "chain": args.chain,
            "token": token,
            "name": name,
            "symbol": symbol,
            "decimals": decimals,
            "total_supply": total_supply,
            "transfer_count_recent": transfer_count,
            "sample_window_blocks": 1000,
            "explorer_url": f"{rpc.cfg['explorer']}/address/{token}",
        }, indent=2))
        return 0

    print("=" * 72)
    print(f"  RAPHA — Token Intelligence on {rpc.cfg['label']}")
    print("=" * 72)
    print(f"  token:        {token}")
    print(f"  name:         {name}")
    print(f"  symbol:       {symbol}")
    print(f"  decimals:     {decimals}")
    print(f"  total supply: {total_supply:,.4f} {symbol}")
    print(f"  transfers:    {transfer_count:,} in last 1,000 blocks")
    print(f"  explorer:     {rpc.cfg['explorer']}/address/{token}")
    print("=" * 72)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Composite: wallet + token in one shot — useful for "research this address's USDC bag" prompts."""
    rpc = PharosRPC(args.chain)
    if not args.address.startswith("0x") or len(args.address) != 42:
        print(f"❌ invalid address: {args.address}")
        return 2
    if not args.token.startswith("0x") or len(args.token) != 42:
        print(f"❌ invalid token: {args.token}")
        return 2

    try:
        # Wallet facts
        address = args.address.lower()
        token = args.token.lower()
        balance = rpc.get_balance(address) / 1e18
        tx_count = rpc.get_tx_count(address)
        # Token facts
        sym = _hex_to_str(rpc.eth_call(token, SEL_SYMBOL)) or "?"
        dec = _hex_to_int(rpc.eth_call(token, SEL_DECIMALS)) or 18
        bal_raw = _hex_to_int(rpc.eth_call(token, SEL_BALANCE_OF + _addr_padded(address)[2:]))
        bal_human = bal_raw / (10 ** dec)
        # Activity
        block = rpc.get_block_number()
        logs = rpc.get_logs(token, hex(max(0, block - 1000)), "latest",
                            topic0="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef")
        # Count how many of those recent transfers involved `address`
        addr_lc = address.lower()
        recent_actor_count = 0
        for log in logs:
            t1 = log.get("topics", ["", "", ""])[1].lower() if len(log.get("topics", [])) > 1 else ""
            t2 = log.get("topics", ["", "", ""])[2].lower() if len(log.get("topics", [])) > 2 else ""
            if addr_lc in t1 or addr_lc in t2:
                recent_actor_count += 1
    except Exception as e:
        print(f"❌ RPC error: {e}")
        return 1

    if args.json:
        print(json.dumps({
            "type": "rapha_research_report",
            "chain": args.chain,
            "address": address,
            "token": token,
            "balance_native": balance,
            "tx_count": tx_count,
            "token_symbol": sym,
            "token_decimals": dec,
            "token_balance_human": bal_human,
            "recent_token_transfers_actor": recent_actor_count,
            "sample_window_blocks": 1000,
            "explorer_address": f"{rpc.cfg['explorer']}/address/{address}",
            "explorer_token": f"{rpc.cfg['explorer']}/address/{token}",
        }, indent=2))
        return 0

    print("=" * 72)
    print(f"  RAPHA — Research Report ({rpc.cfg['label']})")
    print("=" * 72)
    print(f"  Wallet:    {address}")
    print(f"    native:   {balance:,.6f} {rpc.cfg['symbol']}")
    print(f"    tx count: {tx_count:,}")
    print()
    print(f"  Token:     {token}")
    print(f"    symbol:   {sym}")
    print(f"    holding:  {bal_human:,.6f} {sym} (decimals {dec})")
    print()
    print(f"  Activity (last 1,000 blocks):")
    print(f"    {sym} transfers involving this wallet: {recent_actor_count:,} of {len(logs):,} total")
    print()
    print(f"  Explorer:")
    print(f"    wallet: {rpc.cfg['explorer']}/address/{address}")
    print(f"    token:  {rpc.cfg['explorer']}/address/{token}")
    print("=" * 72)
    return 0


def cmd_demo(_args: argparse.Namespace) -> int:
    """Run a demo against real public addresses."""
    print("RAPHA — DEMO (real public addresses on Pharos mainnet)\n")
    class A: pass
    a = A()
    a.chain = "mainnet"
    a.address = "0x67992af9a87f2d6a3062c333d8a06abbe3929438"
    a.no_tokens = False
    a.json = False
    rc1 = cmd_wallet(a)
    print()
    a2 = A()
    a2.chain = "mainnet"
    a2.token = "0xc879c018db60520f4355c26ed1a6d572cdac1815"  # USDC
    a2.json = False
    rc2 = cmd_token(a2)
    print()
    a3 = A()
    a3.chain = "mainnet"
    a3.address = "0x67992af9a87f2d6a3062c333d8a06abbe3929438"
    a3.token = "0xc879c018db60520f4355c26ed1a6d572cdac1815"
    a3.json = False
    rc3 = cmd_report(a3)
    return max(rc1, rc2, rc3)


def main() -> int:
    p = argparse.ArgumentParser(
        description="rapha — Research Assistant on Pharos (on-chain forensics, token intel, reports)"
    )
    sub = p.add_subparsers(dest="cmd")

    pw = sub.add_parser("wallet", help="Forensics on a wallet address")
    pw.add_argument("address")
    pw.add_argument("--chain", default="mainnet", choices=list(CHAINS))
    pw.add_argument("--no-tokens", action="store_true", help="skip the known-token holdings scan")
    pw.add_argument("--json", action="store_true")

    pt = sub.add_parser("token", help="Intelligence on a token contract")
    pt.add_argument("token")
    pt.add_argument("--chain", default="mainnet", choices=list(CHAINS))
    pt.add_argument("--json", action="store_true")

    pr = sub.add_parser("report", help="Composite wallet+token research report")
    pr.add_argument("address")
    pr.add_argument("token")
    pr.add_argument("--chain", default="mainnet", choices=list(CHAINS))
    pr.add_argument("--json", action="store_true")

    sub.add_parser("demo", help="Run against real public addresses")

    args = p.parse_args()
    if args.cmd == "wallet":  return cmd_wallet(args)
    if args.cmd == "token":   return cmd_token(args)
    if args.cmd == "report":  return cmd_report(args)
    if args.cmd == "demo":    return cmd_demo(args)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
