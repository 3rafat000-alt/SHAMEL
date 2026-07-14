# Utilities Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/webhook/resend` -> `WebhookResend` (Resend webhook notifications)
- `/getPaymentBlockHeight` -> `GetTradeBlockHeight` (No proto comment.)
- `/checkWithdrawalAddressValidity` -> `CheckWithdrawalAddressValidity` (No proto comment.)
- `/addressUnbinding` -> `DeprecatedAddress` (No proto comment.)
- `/rescanLostTransaction` -> `RescanLostTransaction` (No proto comment.)

## Interface Details

### WebhookResend

- HTTP: `POST /webhook/resend`
- Request Type: `WebhookResendReq`
- Response Type: `WebhookResendReply`
- Description: Resend webhook notifications

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `startTimestamp` | `int64` | No | [(validate.rules).string={ignore_empty: true, gte: 1}] Start timestamp |
| `endTimestamp` | `int64` | No |  |
| `webhookResult` | `string` | No |  |
| `transactionType` | `string` | No |  |
| `recordIds` | `string[]` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `resendCount` | `int64` | No |  |

### GetTradeBlockHeight

- HTTP: `POST /getPaymentBlockHeight`
- Request Type: `GetTradeBlockHeightReq`
- Response Type: `GetTradeBlockHeightResp`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record_id` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `txBlockHeight` | `int64` | No |  |
| `currBlockHeight` | `int64` | No |  |
| `reqConfirmations` | `int64` | No |  |

### CheckWithdrawalAddressValidity

- HTTP: `POST /checkWithdrawalAddressValidity`
- Request Type: `CheckWithdrawalAddressValidityReq`
- Response Type: `CheckWithdrawalAddressValidityResp`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `address` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `addrIsValid` | `bool` | No |  |

### DeprecatedAddress

- HTTP: `POST /addressUnbinding`
- Request Type: `UnboundAddressReq`
- Response Type: `UnboundAddressResp`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `address` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `unbound` | `UnBoundAddressDetail[]` | No |  |
| `unboundAt` | `int64` | No |  |
| `userID` | `string` | No |  |
| `referenceID` | `string` | No |  |

### RescanLostTransaction

- HTTP: `POST /rescanLostTransaction`
- Request Type: `RescanLostTransactionReq`
- Response Type: `RescanLostTransactionReply`

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `toAddress` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `txId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `memo` | `string` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `description` | `string` | No |  |

## Data Models

### WebhookResendReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `startTimestamp` | `int64` | No | [(validate.rules).string={ignore_empty: true, gte: 1}] Start timestamp |
| `endTimestamp` | `int64` | No |  |
| `webhookResult` | `string` | No |  |
| `transactionType` | `string` | No |  |
| `recordIds` | `string[]` | No |  |

### WebhookResendReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `resendCount` | `int64` | No |  |

### GetTradeBlockHeightReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `record_id` | `string` | No |  |

### GetTradeBlockHeightResp

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `txBlockHeight` | `int64` | No |  |
| `currBlockHeight` | `int64` | No |  |
| `reqConfirmations` | `int64` | No |  |

### CheckWithdrawalAddressValidityReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `address` | `string` | No |  |

### CheckWithdrawalAddressValidityResp

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `addrIsValid` | `bool` | No |  |

### UnboundAddressReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `address` | `string` | No |  |

### UnboundAddressResp

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `unbound` | `UnBoundAddressDetail[]` | No |  |
| `unboundAt` | `int64` | No |  |
| `userID` | `string` | No |  |
| `referenceID` | `string` | No |  |

### UnBoundAddressDetail

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | No |  |
| `address` | `string` | No |  |

### RescanLostTransactionReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `chain` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `toAddress` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `txId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `memo` | `string` | No |  |

### RescanLostTransactionReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `description` | `string` | No |  |
