# Merchant Deposit Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/createAppOrderDepositAddress` -> `CreateAppOrderDepositAddress` (Create a deposit address for an order)
- `/getOrCreateAppDepositAddress` -> `GetOrCreateAppDepositAddress` (Direct address mode)
- `/getAppDepositRecord` -> `GetAppDepositRecord` (Query a deposit record)
- `/getAppDepositRecordList` -> `GetAppDepositRecordList` (Query deposit record list)

## Interface Details

### CreateAppOrderDepositAddress

- HTTP: `POST /createAppOrderDepositAddress`
- Request Type: `CreateAppOrderDepositAddressReq`
- Response Type: `CreateAppOrderDepositAddressReply`
- Description: Create a deposit address for an order

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `fiatId` | `uint64` | No | Fiat currency ID |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `price` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `expiredAt` | `int64` | No | validation: `(validate.rules).int64 = {ignore_empty: true, gte: 1}` |
| `buyerEmail` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, email: true}` |
| `generateCheckoutURL` | `bool` | No |  |
| `product` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:120}` |
| `returnUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |
| `closeUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `address` | `string` | No |  |
| `amount` | `string` | No |  |
| `memo` | `string` | No |  |
| `checkoutUrl` | `string` | No |  |
| `confirmsNeeded` | `uint64` | No |  |

### GetOrCreateAppDepositAddress

- HTTP: `POST /getOrCreateAppDepositAddress`
- Request Type: `GetOrCreateAppDepositAddressReq`
- Response Type: `GetOrCreateAppDepositAddressReply`
- Description: Direct address mode

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `referenceId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `address` | `string` | No |  |
| `memo` | `string` | No |  |

### GetAppDepositRecord

- HTTP: `POST /getAppDepositRecord`
- Request Type: `GetAppDepositRecordReq`
- Response Type: `GetAppDepositRecordReply`
- Description: Query a deposit record

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `AppDepositRecordEntity` | No |  |

### GetAppDepositRecordList

- HTTP: `POST /getAppDepositRecordList`
- Request Type: `GetAppDepositRecordListReq`
- Response Type: `GetAppDepositRecordListReply`
- Description: Query deposit record list

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `referenceId` | `string` | No |  |
| `orderId` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |
| `recordIds` | `string[]` | No | validation: `(validate.rules).repeated = {ignore_empty: true, max_items: 50}` |
| `referenceIds` | `string[]` | No | validation: `(validate.rules).repeated = {ignore_empty: true, max_items: 50}` |
| `orderIds` | `string[]` | No | validation: `(validate.rules).repeated = {ignore_empty: true, max_items: 50}` |
| `limit` | `uint64` | No | validation: `(validate.rules).uint64 = {lte: 100}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `AppDepositRecordEntity[]` | No |  |
| `nextId` | `string` | No | Pagination cursor; intended to be hidden from end users later. |

## Data Models

### CreateAppOrderDepositAddressReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `fiatId` | `uint64` | No | Fiat currency ID |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `price` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `expiredAt` | `int64` | No | validation: `(validate.rules).int64 = {ignore_empty: true, gte: 1}` |
| `buyerEmail` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, email: true}` |
| `generateCheckoutURL` | `bool` | No |  |
| `product` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:120}` |
| `returnUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |
| `closeUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |

### CreateAppOrderDepositAddressReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `address` | `string` | No |  |
| `amount` | `string` | No |  |
| `memo` | `string` | No |  |
| `checkoutUrl` | `string` | No |  |
| `confirmsNeeded` | `uint64` | No |  |

### GetOrCreateAppDepositAddressReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `referenceId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### GetOrCreateAppDepositAddressReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `address` | `string` | No |  |
| `memo` | `string` | No |  |

### GetAppDepositRecordReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### GetAppDepositRecordReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `AppDepositRecordEntity` | No |  |

### AppDepositRecordEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `referenceId` | `string` | No |  |
| `orderId` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `chain` | `string` | No |  |
| `contract` | `string` | No |  |
| `coinUSDPrice` | `string` | No |  |
| `fromAddress` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `toMemo` | `string` | No |  |
| `amount` | `string` | No |  |
| `serviceFee` | `string` | No |  |
| `txId` | `string` | No |  |
| `txIndex` | `uint64` | No |  |
| `status` | `string` | No |  |
| `arrivedAt` | `int64` | No |  |
| `isFlaggedAsRisky` | `bool` | No |  |

### GetAppDepositRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `referenceId` | `string` | No |  |
| `orderId` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |
| `recordIds` | `string[]` | No | validation: `(validate.rules).repeated = {ignore_empty: true, max_items: 50}` |
| `referenceIds` | `string[]` | No | validation: `(validate.rules).repeated = {ignore_empty: true, max_items: 50}` |
| `orderIds` | `string[]` | No | validation: `(validate.rules).repeated = {ignore_empty: true, max_items: 50}` |
| `limit` | `uint64` | No | validation: `(validate.rules).uint64 = {lte: 100}` |

### GetAppDepositRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `AppDepositRecordEntity[]` | No |  |
| `nextId` | `string` | No | Pagination cursor; intended to be hidden from end users later. |
