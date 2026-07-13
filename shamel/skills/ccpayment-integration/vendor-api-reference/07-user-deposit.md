# User Deposit Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/getOrCreateUserDepositAddress` -> `GetOrCreateUserDepositAddress` (Get or create a user deposit address)
- `/getUserDepositRecord` -> `GetUserDepositRecord` (Retrieve a user deposit record)
- `/getUserDepositRecordList` -> `GetUserDepositRecordList` (Query user deposit history)

## Interface Details

### GetOrCreateUserDepositAddress

- HTTP: `POST /getOrCreateUserDepositAddress`
- Request Type: `GetOrCreateUserDepositAddressReq`
- Response Type: `GetOrCreateUserDepositAddressReply`
- Description: Get or create a user deposit address

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | Cannot start with `sys`; length must be 5 to 64 characters. ; validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `address` | `string` | No |  |
| `memo` | `string` | No |  |

### GetUserDepositRecord

- HTTP: `POST /getUserDepositRecord`
- Request Type: `GetUserDepositRecordReq`
- Response Type: `GetUserDepositRecordReply`
- Description: Retrieve a user deposit record

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `UserDepositRecord` | No |  |

### GetUserDepositRecordList

- HTTP: `POST /getUserDepositRecordList`
- Request Type: `GetUserDepositRecordListReq`
- Response Type: `GetUserDepositRecordListReply`
- Description: Query user deposit history

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `toAddress` | `string` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserDepositRecord[]` | No |  |
| `nextId` | `string` | No |  |

## Data Models

### GetOrCreateUserDepositAddressReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | Cannot start with `sys`; length must be 5 to 64 characters. ; validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### GetOrCreateUserDepositAddressReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `address` | `string` | No |  |
| `memo` | `string` | No |  |

### GetUserDepositRecordReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |

### GetUserDepositRecordReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `UserDepositRecord` | No |  |

### UserDepositRecord

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | No |  |
| `recordId` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `chain` | `string` | No |  |
| `contract` | `string` | No |  |
| `coinSymbol` | `string` | No |  |
| `txId` | `string` | No |  |
| `coinUSDPrice` | `string` | No |  |
| `fromAddress` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `toMemo` | `string` | No |  |
| `amount` | `string` | No |  |
| `serviceFee` | `string` | No |  |
| `status` | `string` | No |  |
| `arrivedAt` | `int64` | No |  |
| `isFlaggedAsRisky` | `bool` | No |  |

### GetUserDepositRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `toAddress` | `string` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `nextId` | `string` | No |  |

### GetUserDepositRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserDepositRecord[]` | No |  |
| `nextId` | `string` | No |  |
