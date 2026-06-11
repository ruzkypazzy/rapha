# RAPHA - Research Assistant on Pharos

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Pharos](https://img.shields.io/badge/Pharos-1672-green)
![Foundry](https://img.shields.io/badge/Foundry-Cast-orange)

**RAPHA** (Research Assistant on Pharos) is an AI Agent skill that enables comprehensive on-chain research, wallet forensics, token analysis, and protocol intelligence on the Pharos blockchain.

## About RAPHA

RAPHA empowers AI agents to perform deep blockchain analysis through natural language commands. Whether you're researching wallet activities, analyzing token metrics, comparing protocols, or generating comprehensive research reports, RAPHA has you covered.

## Features

### 1. Wallet Forensics
- Analyze transaction history for any address
- Identify trading patterns and behaviors
- Track token transfers and holdings
- Cluster related addresses
- Monitor whale movements

### 2. Token Intelligence
- Get token metadata (name, symbol, decimals, total supply)
- Analyze holder distribution
- Check liquidity and trading volume
- Verify contract source code
- Compare token metrics across chains

### 3. Protocol Analysis
- Analyze DeFi protocol TVL and users
- Track historical performance
- Compare multiple protocols
- Identify risk factors
- Monitor protocol activity

### 4. Contract Research
- Verify contract interactions
- Trace fund flows
- Analyze bytecode for vulnerabilities
- Check approval and permission patterns
- Decode function selectors

### 5. Market Insights
- Get PROS token price and market data
- Track trading volume trends
- Monitor gas price patterns
- Analyze block production stats
- Track market capitalization

### 6. Historical Analysis
- Track address activity over time
- Identify whale movements
- Monitor large transactions
- Analyze DeFi protocol usage
- Generate historical reports

## Install

### 1. Install Foundry (the engine the skill is built on)

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

Verify with `cast --version`. This gives you `cast`, `forge`, `anvil`, and `chisel` on your `$PATH`.

### 2. Install jq (used to parse JSON)

```bash
# macOS
brew install jq
# Debian/Ubuntu/Termux
apt install -y jq
# Alpine
apk add jq
```

Verify with `jq --version`.

### 3. Get the skill

```bash
git clone https://github.com/ruzkypazzy/rapha
cd rapha
chmod +x scripts/*.sh
```

That's it. No `pip install`, no `npm install`, no `forge build`, no compile. The skill is one or more bash scripts that use `cast` (from Foundry) for every RPC read. The `assets/networks.json` file already knows the Pharos Pacific Mainnet and Atlantic Testnet endpoints.

## Quick test (try it in 30 seconds)

After the 3-step install above, run the demo mode (no private key, no RPC, no setup):

```bash
bash scripts/research.sh demo
```

You should see a printed report. The demo uses synthetic data, so it works offline.

To run a real check on a Pharos transaction, wallet, or token, replace the placeholder:

```bash
bash scripts/research.sh wallet 0xYOUR_WALLET
```

## Use in an AI agent (Claude Code / Codex / OpenClaw / Pharos Agent Center)

The skill ships with a `SKILL.md` that AI agents auto-load. Once installed in your agent, just ask in natural language — the agent will read `SKILL.md` and run the bash script for you.

```text
"Research wallet 0xabc... on Pharos: balance, top tokens, recent activity, risk flags."
```

The agent will run `bash scripts/research.sh demo` (or the live command with the address you gave) and read the result back to you.

### Install in your agent

**Option A — Pharos Agent Center** (one-line install):

```bash
# from inside any agent that has the Pharos Agent Center CLI
pharos-skill install https://github.com/ruzkypazzy/rapha
```

**Option B — OpenClaw / Claude Code / Codex** (one-line via npm):

```bash
npx skills add https://github.com/ruzkypazzy/rapha
```

**Option C — Manual install** (drop into your agent's skills directory):

```bash
# Clone the skill
git clone https://github.com/ruzkypazzy/rapha
cd rapha

# Claude Code: copy to ~/.claude/skills/
mkdir -p ~/.claude/skills/rapha
cp -r . ~/.claude/skills/rapha/

# Codex: copy to ~/.codex/skills/
mkdir -p ~/.codex/skills/rapha
cp -r . ~/.codex/skills/rapha/

# OpenClaw: copy to ~/.openclaw/skills/
mkdir -p ~/.openclaw/skills/rapha
cp -r . ~/.openclaw/skills/rapha/

# Then restart the agent — the skill will be auto-loaded.
```
## Configuration

Set up your environment variables:

```bash
# Pharos RPC endpoints
export PHAROS_RPC=https://rpc.pharos.xyz
export PHAROS_TESTNET_RPC=https://atlantic.dplabs-internal.com

# Optional: API keys for extended data
export COINGECKO_API_KEY=your_api_key
```

## Usage

### Quick Start

```bash
# Run RAPHA research assistant
forge script RAPHA.sol:RAPHA --rpc-url $PHAROS_RPC

# Show all commands
forge script RAPHA.sol:RAPHACmds --rpc-url $PHAROS_RPC
```

### Wallet Research Commands

```bash
# Check wallet balance
cast balance 0x... --rpc-url $PHAROS_RPC

# Get transaction count
cast nonce 0x... --rpc-url $PHAROS_RPC

# Analyze wallet
forge script RAPHA.sol:RAPHA --rpc-url $PHAROS_RPC --sig "analyzeWallet(address)" 0x...
```

### Token Analysis Commands

```bash
# Get token name
cast call TOKEN_ADDR "name()(string)" --rpc-url $PHAROS_RPC

# Get token symbol
cast call TOKEN_ADDR "symbol()(string)" --rpc-url $PHAROS_RPC

# Get total supply
cast call TOKEN_ADDR "totalSupply()(uint256)" --rpc-url $PHAROS_RPC

# Get decimals
cast call TOKEN_ADDR "decimals()(uint8)" --rpc-url $PHAROS_RPC

# Get holder balance
cast call TOKEN_ADDR "balanceOf(address)(uint256)" WALLET_ADDR --rpc-url $PHAROS_RPC
```

### Contract Research Commands

```bash
# Check if contract exists
cast code 0x... --rpc-url $PHAROS_RPC

# Get contract nonce
cast nonce 0x... --rpc-url $PHAROS_RPC

# Analyze contract
forge script RAPHA.sol:RAPHA --rpc-url $PHAROS_RPC --sig "analyzeContract(address)" 0x...
```

### Block Analysis Commands

```bash
# Get latest block
cast block latest --rpc-url $PHAROS_RPC

# Get specific block
cast block BLOCK_NUM --rpc-url $PHAROS_RPC

# Get gas price
cast gas-price --rpc-url $PHAROS_RPC

# Get current block number
cast block-number --rpc-url $PHAROS_RPC
```

### Transaction Commands

```bash
# Get transaction receipt
cast receipt TX_HASH --rpc-url $PHAROS_RPC

# Get transaction details
cast tx TX_HASH --rpc-url $PHAROS_RPC

# Parse logs
cast logs address TOPICS... --rpc-url $PHAROS_RPC
```

### Market Data Commands

```bash
# Get PROS price
curl "https://api.coingecko.com/api/v3/simple/price?ids=pharos&vs_currencies=usd"

# Get PROS market data
curl "https://api.coingecko.com/api/v3/coins/pharos"
```

## AI Agent Prompts

### Wallet Research
```
Research this wallet and show their transaction history:
Address: 0x...

What tokens does this address hold?
What are their most active trading pairs?
Identify any unusual patterns in their activity.
```

### Token Research
```
Analyze this token for investment research:
Token: 0x...

What's the total supply and holder count?
Show me the liquidity and trading volume.
Compare this to similar tokens on Pharos.
```

### Protocol Analysis
```
Compare these two DeFi protocols:
Protocol A: 0x...
Protocol B: 0x...

Which has higher TVL and more users?
What are the key differences in their implementations?
```

### Contract Security Research
```
Analyze this contract for potential risks:
Contract: 0x...

What functions are callable by anyone?
Are there any unusual approval patterns?
Check for common vulnerability patterns.
```

### Market Research
```
What's the current PROS price and market cap?
What are the gas trends on Pharos today?
Show me the latest block statistics.
Compare with yesterday's metrics.
```

## Example Research Reports

### Wallet Analysis Report

```json
{
  "address": "0x1234...",
  "nativeBalance": "1234.56 PROS",
  "tokenHolders": ["PROS", "USDC", "..."],
  "totalTransactions": 5678,
  "firstActivity": "2024-01-15",
  "lastActivity": "2024-06-20",
  "topTradingPairs": ["PROS/USDC", "..."],
  "riskScore": "LOW"
}
```

### Token Research Report

```json
{
  "address": "0x5678...",
  "name": "Example Token",
  "symbol": "EXAMP",
  "decimals": 18,
  "totalSupply": "1000000000",
  "holders": 1234,
  "volume24h": "$567,890",
  "marketCap": "$12,345,678",
  "liquidity": "$1,234,567"
}
```

### Protocol Comparison Report

```json
{
  "protocols": [
    {
      "name": "Protocol A",
      "address": "0x...",
      "tvl": "$10,000,000",
      "users": 5000,
      "dailyVolume": "$500,000"
    },
    {
      "name": "Protocol B",
      "address": "0x...",
      "tvl": "$8,000,000",
      "users": 3500,
      "dailyVolume": "$400,000"
    }
  ],
  "recommendation": "Protocol A has higher TVL and more active users"
}
```

## Supported Networks

| Network | Chain ID | RPC URL |
|---------|----------|--------|
| Pharos Pacific Mainnet | 1672 | https://rpc.pharos.xyz |
| Pharos Atlantic Testnet | 688689 | https://atlantic.dplabs-internal.com |

## Dependencies

- [Foundry](https://book.getfoundry.sh/) (cast, forge)
- curl
- Node.js or Python (optional)

## API Integration

### CoinGecko API

```bash
# Get PROS price
curl "https://api.coingecko.com/api/v3/simple/price?ids=pharos&vs_currencies=usd"

# Get market data
curl "https://api.coingecko.com/api/v3/coins/pharos"

# Get token prices
curl "https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=TOKEN&vs_currencies=usd"
```

### Pharos RPC Methods

```bash
# eth_getBalance
cast balance ADDRESS --rpc-url $PHAROS_RPC

# eth_getCode
cast code ADDRESS --rpc-url $PHAROS_RPC

# eth_getTransactionReceipt
cast receipt TX_HASH --rpc-url $PHAROS_RPC

# eth_call
cast call TO FUNCTION_SIGNATURE --rpc-url $PHAROS_RPC
```

## Important Notes

- All on-chain data is publicly available and verifiable
- Cross-reference multiple data sources for accuracy
- Use testnet for experimenting before mainnet
- Consider privacy implications of wallet analysis
- Always verify contract source code independently
- Risk scores are for guidance, not financial advice

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.


## Framework

| Layer | Tool |
|---|---|
| Engine | bash + Foundry `cast` |
| JSON parsing | `jq` |
| Chain config | `assets/networks.json` (Pharos Skill Engine schema) |
| Skill loader | Pharos Agent Center / Claude Code / Codex / OpenClaw |

The skill is a thin bash wrapper that calls `cast` for every RPC read. No contracts are deployed, no private keys required.

## Dependencies

| Dependency | Required? | Notes |
|---|---|---|
| `cast` (Foundry) | **Yes** | `curl -L https://foundry.paradigm.xyz \| bash && foundryup` |
| `jq` | **Yes** | `apt install -y jq` or `brew install jq` |
| `bash` ≥ 4.0 | **Yes** | Ships with every Linux/macOS/WSL |
| `git` | Yes | To clone the repo |
| Python | **No** | Skill is bash-only |
| Node.js | **No** | Skill is bash-only |

## Tests

```bash
forge test -vvv
```

The test suite covers the engine's heuristics, the JSON output schema, and (when run with `cast` installed) a live RPC smoke test against Pharos Pacific Mainnet.

## Repository layout

```
.
├── README.md                  # this file
├── SKILL.md                   # Agent-side description (loaded by Claude/Codex/etc.)
├── scripts/
│   └── RAPHA.sol          # bash + cast engine — the entire skill
├── assets/
│   └── networks.json          # Pharos Skill Engine network config
└── tests/
    └── test_*.sh              # bash smoke test
```
## License

MIT License

---

**RAPHA** - Research Assistant on Pharos - Empowering AI agents with on-chain intelligence.
