# Basic Info Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/getCoinList` -> `GetCoinList` (All supported tokens)
- `/getFiatList` -> `GetFiatList` (All supported fiat currencies)
- `/getCoin` -> `GetCoin` (Single token)
- `/getCoinUSDTPrice` -> `GetCoinUSDTPrice` (Token price in USDT)
- `/getChainList` -> `GetChainList` (Query chain status by `chainIds`; returns all chains when `chainIds` is omitted.)
- `/all/chain` -> `GetAllChainList` (No proto comment.)
- `/getMainCoinList` -> `GetMainCoinList` (Retrieve the main-chain token list)

## Interface Details

### GetCoinList

- HTTP: `POST /getCoinList`
- Request Type: `GetCoinListReq`
- Response Type: `GetCoinListReply`
- Description: All supported tokens

#### Request Parameters

No fields defined.

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coins` | `CoinEntity[]` | No |  |

### GetFiatList

- HTTP: `POST /getFiatList`
- Request Type: `Empty`
- Response Type: `GetFiatListReply`
- Description: All supported fiat currencies

#### Request Parameters

No body.

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `fiats` | `FiatEntity[]` | No |  |

### GetCoin

- HTTP: `POST /getCoin`
- Request Type: `GetCoinReq`
- Response Type: `GetCoinReply`
- Description: Single token

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coin` | `CoinEntity` | No |  |

### GetCoinUSDTPrice

- HTTP: `POST /getCoinUSDTPrice`
- Request Type: `GetCoinUSDTPriceReq`
- Response Type: `GetCoinUSDTPriceReply`
- Description: Token price in USDT

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinIds` | `uint64[]` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `prices` | `map<uint64, string>` | No | coinId:price |

### GetChainList

- HTTP: `POST /getChainList`
- Request Type: `GetChainListReq`
- Response Type: `ChainListReply`
- Description: Query chain status by `chainIds`; returns all chains when `chainIds` is omitted.

#### Request Parameters

No fields defined.

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chains` | `ChainList[]` | No |  |

### GetAllChainList

- HTTP: `POST /all/chain`
- Request Type: `GetChainListReq`
- Response Type: `GetChainListReply`

#### Request Parameters

No fields defined.

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chains` | `Chain[]` | No |  |

### GetMainCoinList

- HTTP: `POST /getMainCoinList`
- Request Type: `GetMainCoinListReq`
- Response Type: `GetMainCoinListReply`
- Description: Retrieve the main-chain token list

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `appId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinChainList` | `CoinChainEntity[]` | No |  |

## Data Models

### GetCoinListReq

No fields defined.

### GetCoinListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coins` | `CoinEntity[]` | No |  |

### CoinEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |
| `symbol` | `string` | No |  |
| `coinFullName` | `string` | No |  |
| `logoUrl` | `string` | No |  |
| `status` | `string` | No |  |
| `networks` | `map<string, NetworkEntity>` | No | chain:network |
| `price` | `string` | No |  |

### GetFiatListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `fiats` | `FiatEntity[]` | No |  |

### FiatEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `fiatId` | `uint64` | No |  |
| `symbol` | `string` | No |  |
| `logoUrl` | `string` | No |  |
| `mark` | `string` | No |  |
| `usdRate` | `string` | No |  |

### GetCoinReq

Retrieve a single token

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |

### GetCoinReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coin` | `CoinEntity` | No |  |

### GetCoinUSDTPriceReq

Retrieve the USDT price for specific tokens

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinIds` | `uint64[]` | No |  |

### GetCoinUSDTPriceReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `prices` | `map<uint64, string>` | No | coinId:price |

### GetChainListReq

No fields defined.

### ChainListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chains` | `ChainList[]` | No |  |

### ChainList

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `chainFullName` | `string` | No |  |
| `explorer` | `string` | No |  |
| `logoUrl` | `string` | No |  |
| `status` | `string` | No | Normal/Maintain |
| `confirmations` | `int32` | No |  |
| `baseUrl` | `string` | No |  |
| `isEVM` | `bool` | No |  |
| `supportMemo` | `bool` | No |  |

### GetChainListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chains` | `Chain[]` | No |  |

### Chain

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `chainFullName` | `string` | No |  |
| `explorer` | `string` | No |  |
| `logoUrl` | `string` | No |  |
| `status` | `string` | No | Normal/Maintain |
| `confirmNum` | `int32` | No |  |
| `isEVM` | `bool` | No |  |

### GetMainCoinListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `appId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |

### GetMainCoinListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinChainList` | `CoinChainEntity[]` | No |  |

### CoinChainEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |
| `symbol` | `string` | No |  |
| `logoUrl` | `string` | No |  |
| `status` | `string` | No |  |
| `chain` | `string` | No |  |
| `network` | `string` | No |  |
