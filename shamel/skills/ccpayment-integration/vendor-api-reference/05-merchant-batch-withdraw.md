# Merchant Batch Withdraw Module

Last Updated: 2026-07-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/checkWithdrawAddress` -> `CheckWithdrawAddress` (-------------------------batch withdraw---------------------------------------)
- `/applyBatchWithdraw` -> `ApplyBatchWithdraw` (No proto comment.)
- `/appendBatchWithdraw` -> `AppendBatchWithdraw` (No proto comment.)
- `/confirmBatchWithdraw` -> `ConfirmBatchWithdraw` (No proto comment.)
- `/abortBatchWithdraw` -> `AbortBatchWithdraw` (No proto comment.)
- `/getBatchWithdrawOrder` -> `GetBatchWithdrawOrder` (No proto comment.)
- `/getBatchWithdrawOrderRecordList` -> `GetBatchWithdrawOrderRecordList` (No proto comment.)

## Interface Details

### CheckWithdrawAddress

- HTTP: `POST /checkWithdrawAddress`
- Request Type: `CheckWithdrawAddressReq`
- Response Type: `CheckWithdrawAddressReply`
- Description: -------------------------batch withdraw---------------------------------------

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `addressInfoList` | `WithdrawAddress[]` | Yes | validation: `(validate.rules).repeated.min_items = 1,(validate.rules).repeated.max_items = 500` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `addressInfoResults` | `WithdrawAddressResult[]` | No | address -- result |

### ApplyBatchWithdraw

- HTTP: `POST /applyBatchWithdraw`
- Request Type: `ApplyBatchWithdrawReq`
- Response Type: `ApplyBatchWithdrawReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `taskName` | `string` | No |  |
| `orders` | `BatchWithdrawTaskEntity[]` | No | validation: `(validate.rules).repeated.min_items = 0,(validate.rules).repeated.max_items = 500` |
| `mode` | `string` | Yes | `Single|Batch`; execution mode: single transaction or batched submission ; validation: `(validate.rules).string.min_len = 1` |
| `notifyUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:120, uri:true}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | No |  |
| `billId` | `string` | No |  |

### AppendBatchWithdraw

- HTTP: `POST /appendBatchWithdraw`
- Request Type: `AppendBatchWithdrawReq`
- Response Type: `AppendBatchWithdrawReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `orders` | `BatchWithdrawTaskEntity[]` | Yes | validation: `(validate.rules).repeated.min_items = 1,(validate.rules).repeated.max_items = 500` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `appended` | `int32` | No |  |
| `total` | `int32` | No |  |
| `batch_order_id` | `string` | No |  |

### ConfirmBatchWithdraw

- HTTP: `POST /confirmBatchWithdraw`
- Request Type: `ConfirmBatchWithdrawReq`
- Response Type: `BatchWithdrawOrder`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `delaySeconds` | `int64` | No | validation: `(validate.rules).int64 = {ignore_empty: true, gte: 0, lte:3600}` |
| `confirmExecution` | `bool` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | No |  |
| `taskName` | `string` | No |  |
| `billId` | `string` | No |  |
| `coin` | `Coin` | No |  |
| `amount` | `string` | No |  |
| `networkFee` | `string` | No |  |
| `networkFeeCoin` | `Coin` | No |  |
| `status` | `string` | No | "Init|Reviewing｜Rejected|Pending|Processing|Completed", |
| `reason` | `string` | No |  |
| `mode` | `string` | No |  |
| `stats` | `BatchWithdrawStats` | No |  |
| `createdAt` | `int64` | No |  |
| `updatedAt` | `int64` | No |  |

### AbortBatchWithdraw

- HTTP: `POST /abortBatchWithdraw`
- Request Type: `AbortBatchWithdrawReq`
- Response Type: `AbortBatchWithdrawReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `orderIds` | `string[]` | No | When `execMode=batch`, this applies to `reviewing` and `pending`; when `execMode=single`, it applies to `reviewing`, `pending`, and `processing`. Optional. ; validation: `(validate.rules).repeated.min_items = 0,(validate.rules).repeated.max_items = 500` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `status` | `string` | No | If the list below is empty, the entire batch order was canceled successfully. |
| `canceledOrderIds` | `string[]` | No | Canceled sub-order IDs |
| `ignoredOrderIds` | `string[]` | No | Ignored sequence IDs that were already completed or already submitted to the fund service (`Successful|Processing`). |

### GetBatchWithdrawOrder

- HTTP: `POST /getBatchWithdrawOrder`
- Request Type: `GetBatchWithdrawOrderReq`
- Response Type: `BatchWithdrawOrder`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `verbose` | `uint32` | No | validation: `(validate.rules).uint32 = {ignore_empty: true, gte: 0, lte:3}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | No |  |
| `taskName` | `string` | No |  |
| `billId` | `string` | No |  |
| `coin` | `Coin` | No |  |
| `amount` | `string` | No |  |
| `networkFee` | `string` | No |  |
| `networkFeeCoin` | `Coin` | No |  |
| `status` | `string` | No | "Init|Reviewing｜Rejected|Pending|Processing|Completed", |
| `reason` | `string` | No |  |
| `mode` | `string` | No |  |
| `stats` | `BatchWithdrawStats` | No |  |
| `createdAt` | `int64` | No |  |
| `updatedAt` | `int64` | No |  |

### GetBatchWithdrawOrderRecordList

- HTTP: `POST /getBatchWithdrawOrderRecordList`
- Request Type: `GetBatchWithdrawOrderRecordListReq`
- Response Type: `GetBatchWithdrawOrderRecordListReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `nextId` | `string` | No | Next-page cursor |
| `limit` | `uint64` | No | Next-page cursor ; validation: `(validate.rules).uint64 = {lte: 100}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `nextId` | `string` | No | Next-page cursor |
| `records` | `BatchWithdrawTaskEntity[]` | No |  |

## Data Models

### CheckWithdrawAddressReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `addressInfoList` | `WithdrawAddress[]` | Yes | validation: `(validate.rules).repeated.min_items = 1,(validate.rules).repeated.max_items = 500` |

### WithdrawAddress

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `address` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `memo` | `string` | No |  |
| `seq` | `uint32` | Yes | validation: `(validate.rules).uint32.gte = 1` |
| `codes` | `int32[]` | No |  |

### CheckWithdrawAddressReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `addressInfoResults` | `WithdrawAddressResult[]` | No | address -- result |

### WithdrawAddressResult

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `seq` | `uint32` | No |  |
| `codes` | `int32[]` | No |  |

### ApplyBatchWithdrawReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `taskName` | `string` | No |  |
| `orders` | `BatchWithdrawTaskEntity[]` | No | validation: `(validate.rules).repeated.min_items = 0,(validate.rules).repeated.max_items = 500` |
| `mode` | `string` | Yes | `Single|Batch`; execution mode: single transaction or batched submission ; validation: `(validate.rules).string.min_len = 1` |
| `notifyUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:120, uri:true}` |

### BatchWithdrawTaskEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 1, max_len:64}` |
| `address` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `memo` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:16}` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `remark` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:64}` |
| `recordId` | `string` | No |  |
| `status` | `string` | No |  |
| `networkFee` | `string` | No |  |
| `txId` | `string` | No |  |
| `reason` | `string` | No |  |
| `createdAt` | `int64` | No |  |
| `updatedAt` | `int64` | No |  |

### ApplyBatchWithdrawReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | No |  |
| `billId` | `string` | No |  |

### AppendBatchWithdrawReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `orders` | `BatchWithdrawTaskEntity[]` | Yes | validation: `(validate.rules).repeated.min_items = 1,(validate.rules).repeated.max_items = 500` |

### AppendBatchWithdrawReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `appended` | `int32` | No |  |
| `total` | `int32` | No |  |
| `batch_order_id` | `string` | No |  |

### ConfirmBatchWithdrawReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `delaySeconds` | `int64` | No | validation: `(validate.rules).int64 = {ignore_empty: true, gte: 0, lte:3600}` |
| `confirmExecution` | `bool` | No |  |

### BatchWithdrawOrder

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | No |  |
| `taskName` | `string` | No |  |
| `billId` | `string` | No |  |
| `coin` | `Coin` | No |  |
| `amount` | `string` | No |  |
| `networkFee` | `string` | No |  |
| `networkFeeCoin` | `Coin` | No |  |
| `status` | `string` | No | "Init|Reviewing｜Rejected|Pending|Processing|Completed", |
| `reason` | `string` | No |  |
| `mode` | `string` | No |  |
| `stats` | `BatchWithdrawStats` | No |  |
| `createdAt` | `int64` | No |  |
| `updatedAt` | `int64` | No |  |

### Coin

Network token information

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coin_id` | `uint64` | No | Token ID |
| `coin_symbol` | `string` | No | Token symbol |
| `coin_price` | `string` | No |  |

### BatchWithdrawStats

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `total` | `int32` | No | Total transaction count |
| `succeeded` | `int32` | No | Succeeded count |
| `failed` | `int32` | No | Failed count |
| `canceled` | `int32` | No | Canceled count |
| `processing` | `int32` | No | In progress |
| `execOrderId` | `string` | No | Last executed sub-order ID |

### AbortBatchWithdrawReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `orderIds` | `string[]` | No | When `execMode=batch`, this applies to `reviewing` and `pending`; when `execMode=single`, it applies to `reviewing`, `pending`, and `processing`. Optional. ; validation: `(validate.rules).repeated.min_items = 0,(validate.rules).repeated.max_items = 500` |

### AbortBatchWithdrawReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `status` | `string` | No | If the list below is empty, the entire batch order was canceled successfully. |
| `canceledOrderIds` | `string[]` | No | Canceled sub-order IDs |
| `ignoredOrderIds` | `string[]` | No | Ignored sequence IDs that were already completed or already submitted to the fund service (`Successful|Processing`). |

### GetBatchWithdrawOrderReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `verbose` | `uint32` | No | validation: `(validate.rules).uint32 = {ignore_empty: true, gte: 0, lte:3}` |

### GetBatchWithdrawOrderRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `batchOrderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `nextId` | `string` | No | Next-page cursor |
| `limit` | `uint64` | No | Next-page cursor ; validation: `(validate.rules).uint64 = {lte: 100}` |

### GetBatchWithdrawOrderRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `nextId` | `string` | No | Next-page cursor |
| `records` | `BatchWithdrawTaskEntity[]` | No |  |
