# User Withdraw Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/applyUserWithdrawToNetwork` -> `ApplyUserWithdrawToNetwork` (User withdrawal to an external network)
- `/applyUserWithdrawToCwallet` -> `ApplyUserWithdrawToCwallet` (User withdrawal to CWallet)
- `/getUserWithdrawRecord` -> `GetUserWithdrawRecord` (Query a user withdrawal record)
- `/getUserWithdrawRecordList` -> `GetUserWithdrawRecordList` (Query user withdrawal history)

## Interface Details

### ApplyUserWithdrawToNetwork

- HTTP: `POST /applyUserWithdrawToNetwork`
- Request Type: `ApplyUserWithdrawToNetworkReq`
- Response Type: `ApplyUserWithdrawToNetworkReply`
- Description: User withdrawal to an external network

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `address` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `memo` | `string` | No |  |
| `networkFeeInquiryID` | `string` | No |  |
| `notifyUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### ApplyUserWithdrawToCwallet

- HTTP: `POST /applyUserWithdrawToCwallet`
- Request Type: `ApplyUserWithdrawToCwalletReq`
- Response Type: `ApplyUserWithdrawToCwalletReply`
- Description: User withdrawal to CWallet

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `cwalletUser` | `string` | Yes | Email address or ID ; validation: `(validate.rules).string.min_len = 1` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### GetUserWithdrawRecord

- HTTP: `POST /getUserWithdrawRecord`
- Request Type: `GetUserWithdrawRecordReq`
- Response Type: `GetUserWithdrawRecordReply`
- Description: Query a user withdrawal record

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `UserWithdrawRecord` | No |  |

### GetUserWithdrawRecordList

- HTTP: `POST /getUserWithdrawRecordList`
- Request Type: `GetUserWithdrawRecordListReq`
- Response Type: `GetUserWithdrawRecordListReply`
- Description: Query user withdrawal history

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `orderIds` | `string[]` | No |  |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `toAddress` | `string` | No |  |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserWithdrawRecord[]` | No |  |
| `nextId` | `string` | No |  |

## Data Models

### ApplyUserWithdrawToNetworkReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `address` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `memo` | `string` | No |  |
| `networkFeeInquiryID` | `string` | No |  |
| `notifyUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |

### ApplyUserWithdrawToNetworkReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### ApplyUserWithdrawToCwalletReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `cwalletUser` | `string` | Yes | Email address or ID ; validation: `(validate.rules).string.min_len = 1` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### ApplyUserWithdrawToCwalletReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### GetUserWithdrawRecordReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `orderId` | `string` | No |  |

### GetUserWithdrawRecordReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `UserWithdrawRecord` | No |  |

### UserWithdrawRecord

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | No |  |
| `recordId` | `string` | No |  |
| `withdrawType` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `chain` | `string` | No |  |
| `orderId` | `string` | No |  |
| `txId` | `string` | No |  |
| `coinSymbol` | `string` | No |  |
| `fromAddress` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `cwalletUser` | `string` | No |  |
| `toMemo` | `string` | No |  |
| `amount` | `string` | No |  |
| `status` | `string` | No |  |
| `fee` | `WithdrawFee` | No |  |
| `coinUSDPrice` | `string` | No |  |

### WithdrawFee

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `amount` | `string` | No |  |

### GetUserWithdrawRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `orderIds` | `string[]` | No |  |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `toAddress` | `string` | No |  |
| `nextId` | `string` | No |  |

### GetUserWithdrawRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `UserWithdrawRecord[]` | No |  |
| `nextId` | `string` | No |  |
