// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "forge-std/console.sol";

/**
 * @title RAPHA
 * @dev Research Assistant on Pharos - On-chain research tool for wallet forensics, token analysis, and protocol intelligence
 */
contract RAPHA is Script {

    // Network configuration
    string constant MAINNET_RPC = "https://rpc.pharos.xyz";
    string constant TESTNET_RPC = "https://atlantic.dplabs-internal.com";
    string constant VERSION = "1.0.0";
    string constant NAME = "RAPHA - Research Assistant on Pharos";

    struct WalletAnalysis {
        address walletAddress;
        uint256 nativeBalance;
        uint256 transactionCount;
        uint256 firstActivityBlock;
        uint256 lastActivityBlock;
        string[] tokenHolders;
        uint256 totalTokensHeld;
    }

    struct TokenInfo {
        string name;
        string symbol;
        uint256 decimals;
        uint256 totalSupply;
        address contractAddress;
    }

    struct MarketData {
        string tokenName;
        uint256 priceUSD;
        uint256 marketCap;
        uint256 volume24h;
        uint256 totalSupply;
    }

    function run() external view {
        console.log("================================================");
        console.log("  RAPHA - Research Assistant on Pharos");
        console.log("  Version:", VERSION);
        console.log("================================================");
        console.log("");
        console.log("Mainnet RPC:", MAINNET_RPC);
        console.log("Testnet RPC:", TESTNET_RPC);
        console.log("");
    }

    /**
     * @dev Analyze a wallet address
     */
    function analyzeWallet(address wallet) external view returns (WalletAnalysis memory) {
        WalletAnalysis memory analysis;
        analysis.walletAddress = wallet;

        // Get native balance
        analysis.nativeBalance = wallet.balance;
        console.log("================================================");
        console.log("  WALLET ANALYSIS");
        console.log("================================================");
        console.log("Wallet Address:", wallet);
        console.log("Native Balance:", analysis.nativeBalance / 1e18, "PROS");
        console.log("");

        return analysis;
    }

    /**
     * @dev Get token information
     */
    function getTokenInfo(address tokenAddress) external view returns (TokenInfo memory) {
        TokenInfo memory info;
        info.contractAddress = tokenAddress;

        console.log("================================================");
        console.log("  TOKEN ANALYSIS");
        console.log("================================================");
        console.log("Token Address:", tokenAddress);
        console.log("");
        console.log("Use the following commands to get token info:");
        console.log("- cast call TOKEN_ADDR \"name()(string)\" --rpc-url $PHAROS_RPC");
        console.log("- cast call TOKEN_ADDR \"symbol()(string)\" --rpc-url $PHAROS_RPC");
        console.log("- cast call TOKEN_ADDR \"totalSupply()(uint256)\" --rpc-url $PHAROS_RPC");
        console.log("- cast call TOKEN_ADDR \"decimals()(uint8)\" --rpc-url $PHAROS_RPC");
        console.log("");

        return info;
    }

    /**
     * @dev Get block statistics
     */
    function getBlockStats(uint256 blockNumber) external view {
        console.log("================================================");
        console.log("  BLOCK ANALYSIS");
        console.log("================================================");
        console.log("Block Number:", blockNumber);
        console.log("");
        console.log("Use: cast block", blockNumber, "--rpc-url $PHAROS_RPC");
        console.log("");
    }

    /**
     * @dev Generate comprehensive research report
     */
    function generateReport(address wallet, address token) external view {
        console.log("================================================");
        console.log("  RAPHA RESEARCH REPORT");
        console.log("================================================");
        console.log("");

        // Wallet Analysis
        console.log("--- WALLET ANALYSIS ---");
        analyzeWallet(wallet);
        console.log("");

        // Token Analysis
        console.log("--- TOKEN ANALYSIS ---");
        getTokenInfo(token);
        console.log("");

        console.log("================================================");
        console.log("  END OF REPORT");
        console.log("================================================");
    }

    /**
     * @dev Parse transaction data
     */
    function parseTransaction(string memory txHash) external pure {
        console.log("================================================");
        console.log("  TRANSACTION ANALYSIS");
        console.log("================================================");
        console.log("Transaction Hash:", txHash);
        console.log("");
        console.log("Use: cast receipt TX_HASH --rpc-url $PHAROS_RPC");
        console.log("Use: cast tx TX_HASH --rpc-url $PHAROS_RPC");
        console.log("");
    }

    /**
     * @dev Compare two addresses
     */
    function compareAddresses(address addr1, address addr2) external view {
        console.log("================================================");
        console.log("  ADDRESS COMPARISON");
        console.log("================================================");
        console.log("");
        console.log("Address 1:", addr1);
        console.log("  Balance:", addr1.balance / 1e18, "PROS");
        console.log("");
        console.log("Address 2:", addr2);
        console.log("  Balance:", addr2.balance / 1e18, "PROS");
        console.log("");
    }

    /**
     * @dev Get market data for PROS token
     */
    function getMarketData() external view {
        console.log("================================================");
        console.log("  MARKET DATA");
        console.log("================================================");
        console.log("");
        console.log("Use CoinGecko API to get PROS price:");
        console.log("curl \"https://api.coingecko.com/api/v3/simple/price?ids=pharos&vs_currencies=usd\"");
        console.log("");
    }

    /**
     * @dev Contract research - analyze contract code
     */
    function analyzeContract(address contractAddr) external view {
        console.log("================================================");
        console.log("  CONTRACT ANALYSIS");
        console.log("================================================");
        console.log("Contract Address:", contractAddr);
        console.log("");
        console.log("Commands:");
        console.log("- cast code CONTRACT_ADDR --rpc-url $PHAROS_RPC");
        console.log("- cast nonce CONTRACT_ADDR --rpc-url $PHAROS_RPC");
        console.log("");
    }
}

/**
 * @title RAPHA Commands
 * @dev Reference script with all available RAPHA commands
 */
contract RAPHACmds is Script {

    function run() external {
        console.log("================================================");
        console.log("  RAPHA - Available Commands Reference");
        console.log("================================================");
        console.log("");
        console.log("Version: 1.0.0");
        console.log("Network: Pharos Blockchain");
        console.log("");
        console.log("================================================");
        console.log("  WALLET FORENSICS COMMANDS");
        console.log("================================================");
        console.log("");
        console.log("# Check wallet balance");
        console.log("cast balance 0x... --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get transaction count (nonce)");
        console.log("cast nonce 0x... --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("================================================");
        console.log("  TOKEN ANALYSIS COMMANDS");
        console.log("================================================");
        console.log("");
        console.log("# Get token name");
        console.log("cast call TOKEN_ADDR \"name()(string)\" --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get token symbol");
        console.log("cast call TOKEN_ADDR \"symbol()(string)\" --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get total supply");
        console.log("cast call TOKEN_ADDR \"totalSupply()(uint256)\" --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get decimals");
        console.log("cast call TOKEN_ADDR \"decimals()(uint8)\" --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get balance of an address");
        console.log("cast call TOKEN_ADDR \"balanceOf(address)(uint256)\" WALLET_ADDR --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("================================================");
        console.log("  CONTRACT RESEARCH COMMANDS");
        console.log("================================================");
        console.log("");
        console.log("# Check if contract exists");
        console.log("cast code 0x... --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get contract nonce");
        console.log("cast nonce 0x... --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Estimate gas");
        console.log("cast estimate ... --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("================================================");
        console.log("  BLOCK ANALYSIS COMMANDS");
        console.log("================================================");
        console.log("");
        console.log("# Get latest block");
        console.log("cast block latest --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get specific block");
        console.log("cast block BLOCK_NUM --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get gas price");
        console.log("cast gas-price --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get current block number");
        console.log("cast block-number --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("================================================");
        console.log("  TRANSACTION COMMANDS");
        console.log("================================================");
        console.log("");
        console.log("# Get transaction receipt");
        console.log("cast receipt TX_HASH --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Get transaction details");
        console.log("cast tx TX_HASH --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("# Parse transaction logs");
        console.log("cast logs address TOPICS... --rpc-url https://rpc.pharos.xyz");
        console.log("");
        console.log("================================================");
        console.log("  MARKET DATA COMMANDS");
        console.log("================================================");
        console.log("");
        console.log("# Get PROS price from CoinGecko");
        console.log("curl \"https://api.coingecko.com/api/v3/simple/price?ids=pharos&vs_currencies=usd\"");
        console.log("");
        console.log("# Get PROS market data");
        console.log("curl \"https://api.coingecko.com/api/v3/coins/pharos\"");
        console.log("");
        console.log("================================================");
        console.log("  RAPHA - Research Assistant on Pharos");
        console.log("================================================");
    }
}
