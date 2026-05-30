---
name: rapha
description: Research Assistant on Pharos - AI Agent skill for on-chain research, wallet forensics, token analysis, and protocol intelligence
author: ruzkypazzy
version: 1.0.0
network: pharos
tags: [research, analytics, wallet, token, pharos, forensics, rapha]
---

# RAPHA - Research Assistant on Pharos

RAPHA (Research Assistant on Pharos) is an AI Agent skill that enables comprehensive on-chain research, wallet forensics, token analysis, and protocol intelligence on the Pharos blockchain.

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

## Usage

### Wallet Research
```
Research this wallet and show their transaction history:
Address: 0x...

What tokens does this address hold?
What are their most active trading pairs?
```

### Token Analysis
```
Analyze this token for investment research:
Token: 0x...

What's the total supply and holder count?
Show me the liquidity and trading volume.
```

### Protocol Comparison
```
Compare these two DeFi protocols:
Protocol A: 0x...
Protocol B: 0x...

Which has higher TVL and more users?
```

### Market Research
```
What's the current PROS price and market cap?
What are the gas trends on Pharos today?
Show me the latest block statistics.
```

## Commands Reference

### Using Foundry (cast)

```bash
# Check wallet balance
cast balance 0x... --rpc-url $PHAROS_RPC

# Get token info
cast call 0x... "name()(string)" --rpc-url $PHAROS_RPC
cast call 0x... "symbol()(string)" --rpc-url $PHAROS_RPC
cast call 0x... "totalSupply()(uint256)" --rpc-url $PHAROS_RPC

# Get transaction receipt
cast receipt TX_HASH --rpc-url $PHAROS_RPC

# Check contract code
cast code 0x... --rpc-url $PHAROS_RPC

# Get latest block
cast block latest --rpc-url $PHAROS_RPC

# Get gas price
cast gas-price --rpc-url $PHAROS_RPC
```

### Using CoinGecko API

```bash
# Get PROS price
curl "https://api.coingecko.com/api/v3/simple/price?ids=pharos&vs_currencies=usd"

# Get market data
curl "https://api.coingecko.com/api/v3/coins/pharos"
```

## Configuration

```bash
# Pharos RPC endpoints
export PHAROS_RPC=https://rpc.pharos.xyz
export PHAROS_TESTNET_RPC=https://atlantic.dplabs-internal.com

# Optional: API keys for extended data
export COINGECKO_API_KEY=your_api_key
```

## Supported Networks

| Network | Chain ID | RPC URL |
|---------|---------|---------|
| Pharos Pacific Mainnet | 1672 | https://rpc.pharos.xyz |
| Pharos Atlantic Testnet | 688689 | https://atlantic.dplabs-internal.com |

## Dependencies

- Foundry (cast, forge)
- curl (for API calls)
- Python (optional, for data processing)

## Example Research Reports

### Wallet Analysis Report
```
Address: 0x1234...
Balance: 1,234.56 PROS
Token Holdings: [PROS, USDC, ...]
Total Transactions: 5,678
First Activity: 2024-01-15
Last Activity: 2024-06-20
Top Trading Pairs: [PROS/USDC, ...]
Risk Assessment: LOW
```

### Token Research Report
```
Token: 0x5678...
Name: Example Token
Symbol: EXAMP
Decimals: 18
Total Supply: 1,000,000,000
Holders: 1,234
24h Volume: $567,890
Market Cap: $12,345,678
```

## Important Notes

- All on-chain data is publicly available
- Cross-reference multiple data sources for accuracy
- Use testnet for experimenting before mainnet
- Consider privacy implications of wallet analysis
