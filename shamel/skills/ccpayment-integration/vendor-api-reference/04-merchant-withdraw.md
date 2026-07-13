# Merchant Withdraw Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/getCwalletUserId` -> `GetCwalletUserId` (Retrieve a CWallet user)
- `/getWithdrawFee` -> `GetWithdrawFee` (Withdrawal fee)
- `/applyAppWithdrawToNetwork` -> `ApplyAppWithdrawToNetwork` (Withdraw to an external network)
- `/applyAppWithdrawToCwallet` -> `ApplyAppWithdrawToCwallet` (Withdraw to CWallet)
- `/getAppWithdrawRecord` -> `GetAppWithdrawRecord` (Query a withdrawal record)
- `/getAppWithdrawRecordList` -> `GetAppWithdrawRecordList` (Query withdrawal history)
- `/getAutoWithdrawRecordList` -> `GetAutoWithdrawRecordList` (No proto comment.)
- `/getRiskyRefundRecordList` -> `GetRiskRefundRecords` (No proto comment.)

## Interface Details

### GetCwalletUserId

- HTTP: `POST /getCwalletUserId`
- Request Type: `GetCwalletUserIdReq`
- Response Type: `GetCwalletUserIdReply`
- Description: Retrieve a CWallet user

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `cwalletUserId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `cwalletUserId` | `string` | No |  |
| `cwalletUserName` | `string` | No |  |

### GetWithdrawFee

- HTTP: `POST /getWithdrawFee`
- Request Type: `GetWithdrawFeeReq`
- Response Type: `GetWithdrawFeeReply`
- Description: Withdrawal fee

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `fee` | `WithdrawFee` | No |  |
| `networkFeeInquiryID` | `string` | No |  |

### ApplyAppWithdrawToNetwork

- HTTP: `POST /applyAppWithdrawToNetwork`
- Request Type: `ApplyAppWithdrawToNetworkReq`
- Response Type: `ApplyAppWithdrawReply`
- Description: Withdraw to an external network

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `address` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `memo` | `string` | No |  |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `merchantPayNetworkFee` | `bool` | No |  |
| `networkFeeInquiryID` | `string` | No |  |
| `notifyUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### ApplyAppWithdrawToCwallet

- HTTP: `POST /applyAppWithdrawToCwallet`
- Request Type: `ApplyAppWithdrawToCwalletReq`
- Response Type: `ApplyAppWithdrawReply`
- Description: Withdraw to CWallet

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `cwalletUser` | `string` | Yes | Email address / CWallet ID ; validation: `(validate.rules).string.min_len = 1` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### GetAppWithdrawRecord

- HTTP: `POST /getAppWithdrawRecord`
- Request Type: `GetAppWithdrawRecordReq`
- Response Type: `GetAppWithdrawRecordReply`
- Description: Query a withdrawal record

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | No |  |
| `recordId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `AppWithdrawRecordEntity` | No |  |

### GetAppWithdrawRecordList

- HTTP: `POST /getAppWithdrawRecordList`
- Request Type: `GetAppWithdrawRecordListReq`
- Response Type: `GetAppWithdrawRecordListReply`
- Description: Query withdrawal history

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `orderIds` | `string[]` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `toAddress` | `string` | No |  |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `AppWithdrawRecordEntity[]` | No |  |
| `nextId` | `string` | No |  |

### GetAutoWithdrawRecordList

- HTTP: `POST /getAutoWithdrawRecordList`
- Request Type: `GetAutoWithdrawRecordListReq`
- Response Type: `GetAutoWithdrawRecordListReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `recordIds` | `string[]` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `toAddress` | `string` | No |  |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `AutoWithdrawRecordEntity[]` | No |  |
| `nextId` | `string` | No |  |

### GetRiskRefundRecords

- HTTP: `POST /getRiskyRefundRecordList`
- Request Type: `GetAutoWithdrawRecordListReq`
- Response Type: `GetRiskWithdrawRecordListReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `recordIds` | `string[]` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `toAddress` | `string` | No |  |
| `nextId` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `RiskWithdrawRecordEntity[]` | No |  |
| `nextId` | `string` | No |  |

## Data Models

### GetCwalletUserIdReq

Check or retrieve a CWallet user

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `cwalletUserId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### GetCwalletUserIdReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `cwalletUserId` | `string` | No |  |
| `cwalletUserName` | `string` | No |  |

### GetWithdrawFeeReq

Retrieve the network fee

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### GetWithdrawFeeReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `fee` | `WithdrawFee` | No |  |
| `networkFeeInquiryID` | `string` | No |  |

### WithdrawFee

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `amount` | `string` | No |  |

### ApplyAppWithdrawToNetworkReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `address` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `memo` | `string` | No |  |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `merchantPayNetworkFee` | `bool` | No |  |
| `networkFeeInquiryID` | `string` | No |  |
| `notifyUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |

### ApplyAppWithdrawReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |

### ApplyAppWithdrawToCwalletReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |
| `cwalletUser` | `string` | Yes | Email address / CWallet ID ; validation: `(validate.rules).string.min_len = 1` |
| `amount` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### GetAppWithdrawRecordReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | No |  |
| `recordId` | `string` | No |  |

### GetAppWithdrawRecordReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record` | `AppWithdrawRecordEntity` | No |  |

### AppWithdrawRecordEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `withdrawType` | `string` | No |  |
| `appId` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `chain` | `string` | No |  |
| `fromAddress` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `cwalletUser` | `string` | No |  |
| `orderId` | `string` | No |  |
| `txId` | `string` | No |  |
| `toMemo` | `string` | No |  |
| `status` | `string` | No |  |
| `amount` | `string` | No |  |
| `fee` | `WithdrawFee` | No |  |
| `reason` | `string` | No |  |
| `coinUSDPrice` | `string` | No |  |

### GetAppWithdrawRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `orderIds` | `string[]` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `toAddress` | `string` | No |  |
| `nextId` | `string` | No |  |

### GetAppWithdrawRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `AppWithdrawRecordEntity[]` | No |  |
| `nextId` | `string` | No |  |

### GetAutoWithdrawRecordListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `recordIds` | `string[]` | No |  |
| `startAt` | `int64` | No | Defaults to the last 90 days |
| `endAt` | `int64` | No |  |
| `toAddress` | `string` | No |  |
| `nextId` | `string` | No |  |

### GetAutoWithdrawRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `AutoWithdrawRecordEntity[]` | No |  |
| `nextId` | `string` | No |  |

### AutoWithdrawRecordEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `chain` | `string` | No |  |
| `orderId` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `toMemo` | `string` | No |  |
| `amount` | `string` | No |  |
| `txId` | `string` | No |  |
| `status` | `string` | No |  |
| `fee` | `WithdrawFee` | No |  |
| `nextId` | `string` | No |  |
| `serviceFee` | `string` | No |  |
| `createdAt` | `int64` | No |  |

### GetRiskWithdrawRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `records` | `RiskWithdrawRecordEntity[]` | No |  |
| `nextId` | `string` | No |  |

### RiskWithdrawRecordEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `chain` | `string` | No |  |
| `orderId` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `toMemo` | `string` | No |  |
| `amount` | `string` | No |  |
| `txId` | `string` | No |  |
| `status` | `string` | No |  |
| `fee` | `WithdrawFee` | No |  |
| `nextId` | `string` | No |  |
| `createdAt` | `int64` | No |  |
| `fromDeposit` | `FromDeposit[]` | No |  |

### FromDeposit

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
