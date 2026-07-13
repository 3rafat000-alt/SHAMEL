# Swap Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/getSwapCoinList` -> `GetSwapCoinList` (====================================Swap========= Swap token list)
- `/estimate` -> `SwapEstimate` (No proto comment.)
- `/getSwapRecord` -> `GetSwapRecord` (No proto comment.)
- `/getSwapRecordList` -> `GetSwapRecordList` (No proto comment.)
- `/swap` -> `Swap` (No proto comment.)

## Interface Details

### GetSwapCoinList

- HTTP: `POST /getSwapCoinList`
- Request Type: `Empty`
- Response Type: `GetSwapCoinListReply`
- Description: ====================================Swap========= Swap token list

#### Request Parameters

No body.

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coins` | `SwapCoinEntity[]` | No |  |

### SwapEstimate

- HTTP: `POST /estimate`
- Request Type: `SwapReq`
- Response Type: `SwapEstimateReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | No | [(validate.rules).string = {min_len: 3, max_len:64}]; |
| `userId` | `string` | No | [(validate.rules).string = {ignore_empty: true, min_len: 3, max_len:64}]; //{ignore_empty: true, max_len:120}] |
| `coinIdIn` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `amountIn` | `string` | Yes | Input amount ; validation: `(validate.rules).string.min_len = 1` |
| `coinIdOut` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `amountOutMinimum` | `string` | No |  |
| `extraFeeRate` | `string` | No |  |
| `appId` | `string` | No | Reserved for business-side use |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinIdIn` | `uint64` | No |  |
| `coinIdOut` | `uint64` | No | Token ID |
| `amountOut` | `string` | No |  |
| `amountIn` | `string` | No |  |
| `swapRate` | `string` | No |  |
| `feeRate` | `string` | No |  |
| `fee` | `string` | No |  |
| `extraFee` | `string` | No |  |
| `netAmountOut` | `string` | No | Net amount received |

### GetSwapRecord

- HTTP: `POST /getSwapRecord`
- Request Type: `GetSwapRecordReq`
- Response Type: `GetSwapRecordReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |
| `ty` | `int32` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `SwapRecordEntity` | No |  |

### GetSwapRecordList

- HTTP: `POST /getSwapRecordList`
- Request Type: `GetSwapRecordListReq`
- Response Type: `GetSwapRecordListReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordIds` | `string[]` | No | validation: `(validate.rules).repeated.max_items = 20` |
| `orderIds` | `string[]` | No | validation: `(validate.rules).repeated.max_items = 20` |
| `userId` | `string` | No |  |
| `coinIdIn` | `uint64` | No |  |
| `coinIdOut` | `uint64` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `SwapRecordEntity[]` | No |  |
| `nextId` | `string` | No | Pagination cursor; intended to be hidden from end users later. |

### Swap

- HTTP: `POST /swap`
- Request Type: `SwapReq`
- Response Type: `SwapReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | No | [(validate.rules).string = {min_len: 3, max_len:64}]; |
| `userId` | `string` | No | [(validate.rules).string = {ignore_empty: true, min_len: 3, max_len:64}]; //{ignore_empty: true, max_len:120}] |
| `coinIdIn` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `amountIn` | `string` | Yes | Input amount ; validation: `(validate.rules).string.min_len = 1` |
| `coinIdOut` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `amountOutMinimum` | `string` | No |  |
| `extraFeeRate` | `string` | No |  |
| `appId` | `string` | No | Reserved for business-side use |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |
| `coinIdIn` | `uint64` | No |  |
| `coinIdOut` | `uint64` | No | Token ID |
| `amountOut` | `string` | No |  |
| `amountIn` | `string` | No |  |
| `amountOutMinimum` | `string` | No |  |
| `swapRate` | `string` | No |  |
| `fee` | `string` | No |  |
| `feeRate` | `string` | No |  |
| `extraFee` | `string` | No |  |
| `netAmountOut` | `string` | No | Net amount received |
| `to_coin_price` | `string` | No | Price |
| `from_coin_price` | `string` | No | Price |

## Data Models

### GetSwapCoinListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coins` | `SwapCoinEntity[]` | No |  |

### SwapCoinEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |
| `symbol` | `string` | No |  |
| `logoUrl` | `string` | No |  |

### SwapReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | No | [(validate.rules).string = {min_len: 3, max_len:64}]; |
| `userId` | `string` | No | [(validate.rules).string = {ignore_empty: true, min_len: 3, max_len:64}]; //{ignore_empty: true, max_len:120}] |
| `coinIdIn` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `amountIn` | `string` | Yes | Input amount ; validation: `(validate.rules).string.min_len = 1` |
| `coinIdOut` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `amountOutMinimum` | `string` | No |  |
| `extraFeeRate` | `string` | No |  |
| `appId` | `string` | No | Reserved for business-side use |

### SwapEstimateReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinIdIn` | `uint64` | No |  |
| `coinIdOut` | `uint64` | No | Token ID |
| `amountOut` | `string` | No |  |
| `amountIn` | `string` | No |  |
| `swapRate` | `string` | No |  |
| `feeRate` | `string` | No |  |
| `fee` | `string` | No |  |
| `extraFee` | `string` | No |  |
| `netAmountOut` | `string` | No | Net amount received |

### GetSwapRecordReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |
| `ty` | `int32` | No |  |

### GetSwapRecordReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `SwapRecordEntity` | No |  |

### SwapRecordEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |
| `coinInSymbol` | `string` | No |  |
| `coinIdIn` | `uint64` | No |  |
| `coinOutSymbol` | `string` | No |  |
| `coinIdOut` | `uint64` | No |  |
| `amountOut` | `string` | No |  |
| `amountIn` | `string` | No |  |
| `amountOutMinimum` | `string` | No |  |
| `netAmountOut` | `string` | No | Net amount received |
| `userId` | `string` | No |  |
| `extraFee` | `string` | No |  |
| `extraFeeRate` | `string` | No |  |
| `swapRate` | `string` | No |  |
| `feeRate` | `string` | No |  |
| `fee` | `string` | No |  |
| `status` | `string` | No |  |
| `createdAt` | `int64` | No |  |
| `arrivedAt` | `int64` | No |  |

### GetSwapRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordIds` | `string[]` | No | validation: `(validate.rules).repeated.max_items = 20` |
| `orderIds` | `string[]` | No | validation: `(validate.rules).repeated.max_items = 20` |
| `userId` | `string` | No |  |
| `coinIdIn` | `uint64` | No |  |
| `coinIdOut` | `uint64` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |

### GetSwapRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `SwapRecordEntity[]` | No |  |
| `nextId` | `string` | No | Pagination cursor; intended to be hidden from end users later. |

### SwapReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |
| `coinIdIn` | `uint64` | No |  |
| `coinIdOut` | `uint64` | No | Token ID |
| `amountOut` | `string` | No |  |
| `amountIn` | `string` | No |  |
| `amountOutMinimum` | `string` | No |  |
| `swapRate` | `string` | No |  |
| `fee` | `string` | No |  |
| `feeRate` | `string` | No |  |
| `extraFee` | `string` | No |  |
| `netAmountOut` | `string` | No | Net amount received |
| `to_coin_price` | `string` | No | Price |
| `from_coin_price` | `string` | No | Price |
