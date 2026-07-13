# User Transfer Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/userTransfer` -> `UserTransfer` (Create a user transfer)
- `/getUserTransferRecord` -> `GetUserTransferRecord` (Query a user transfer record)
- `/getUserTransferRecordList` -> `GetUserTransferRecordList` (Query user transfer history)
- `/userBatchTransfer` -> `UserBatchTransfer` (Create a batch user transfer)
- `/getUserBatchTransferRecord` -> `GetUserBatchTransferRecord` (Query a batch user transfer record)
- `/getUserBatchTransferRecordList` -> `GetUserBatchTransferRecordList` (Query batch user transfer history)
- `/getUserBatchTransferRecordDetail` -> `GetUserBatchTransferRecordDetail` (Query detailed records for a batch user transfer)

## Interface Details

### UserTransfer

- HTTP: `POST /userTransfer`
- Request Type: `UserTransferReq`
- Response Type: `UserTransferReply`
- Description: Create a user transfer

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `fromUserId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `toUserId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `remark` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### GetUserTransferRecord

- HTTP: `POST /getUserTransferRecord`
- Request Type: `GetUserTransferRecordReq`
- Response Type: `GetUserTransferRecordReply`
- Description: Query a user transfer record

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `UserTransferRecord` | No |  |

### GetUserTransferRecordList

- HTTP: `POST /getUserTransferRecordList`
- Request Type: `GetUserTransferRecordListReq`
- Response Type: `GetUserTransferRecordListReply`
- Description: Query user transfer history

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderIds` | `string[]` | No |  |
| `fromUserId` | `string` | No |  |
| `toUserId` | `string` | No |  |
| `coinId` | `uint64` | No | Token ID |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserTransferRecord[]` | No |  |
| `nextId` | `string` | No |  |

### UserBatchTransfer

- HTTP: `POST /userBatchTransfer`
- Request Type: `UserBatchTransferReq`
- Response Type: `UserBatchTransferReply`
- Description: Create a batch user transfer

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `toUsers` | `ToUser[]` | Yes | validation: `(validate.rules).repeated.min_items = 1` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `remark` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### GetUserBatchTransferRecord

- HTTP: `POST /getUserBatchTransferRecord`
- Request Type: `GetUserBatchTransferRecordReq`
- Response Type: `GetUserBatchTransferRecordReply`
- Description: Query a batch user transfer record

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `UserBatchTransferRecord` | No |  |

### GetUserBatchTransferRecordList

- HTTP: `POST /getUserBatchTransferRecordList`
- Request Type: `GetUserBatchTransferRecordListReq`
- Response Type: `GetUserBatchTransferRecordListReply`
- Description: Query batch user transfer history

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderIds` | `string[]` | No |  |
| `userId` | `string` | No |  |
| `coinId` | `uint64` | No | Token ID |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserBatchTransferRecord[]` | No |  |
| `nextId` | `string` | No |  |

### GetUserBatchTransferRecordDetail

- HTTP: `POST /getUserBatchTransferRecordDetail`
- Request Type: `GetUserBatchTransferRecordDetailReq`
- Response Type: `GetUserBatchTransferRecordDetailReply`
- Description: Query detailed records for a batch user transfer

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserTransferRecord[]` | No |  |
| `nextId` | `string` | No |  |

## Data Models

### UserTransferReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `fromUserId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `toUserId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `remark` | `string` | No |  |

### UserTransferReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### GetUserTransferRecordReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |

### GetUserTransferRecordReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `UserTransferRecord` | No |  |

### UserTransferRecord

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `orderId` | `string` | No |  |
| `fromUserId` | `string` | No |  |
| `toUserId` | `string` | No |  |
| `amount` | `string` | No |  |
| `status` | `string` | No |  |
| `remark` | `string` | No |  |
| `coinUSDPrice` | `string` | No |  |

### GetUserTransferRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderIds` | `string[]` | No |  |
| `fromUserId` | `string` | No |  |
| `toUserId` | `string` | No |  |
| `coinId` | `uint64` | No | Token ID |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |

### GetUserTransferRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserTransferRecord[]` | No |  |
| `nextId` | `string` | No |  |

### UserBatchTransferReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `toUsers` | `ToUser[]` | Yes | validation: `(validate.rules).repeated.min_items = 1` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `remark` | `string` | No |  |

### ToUser

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `amount` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |

### UserBatchTransferReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### GetUserBatchTransferRecordReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |

### GetUserBatchTransferRecordReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `UserBatchTransferRecord` | No |  |

### UserBatchTransferRecord

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `userId` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `orderId` | `string` | No |  |
| `toUsers` | `ToUser[]` | No |  |
| `status` | `string` | No |  |
| `remark` | `string` | No |  |
| `coinUSDPrice` | `string` | No |  |

### GetUserBatchTransferRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderIds` | `string[]` | No |  |
| `userId` | `string` | No |  |
| `coinId` | `uint64` | No | Token ID |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |

### GetUserBatchTransferRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserBatchTransferRecord[]` | No |  |
| `nextId` | `string` | No |  |

### GetUserBatchTransferRecordDetailReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `nextId` | `string` | No |  |

### GetUserBatchTransferRecordDetailReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserTransferRecord[]` | No |  |
| `nextId` | `string` | No |  |
