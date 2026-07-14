# User Assets Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/getUserCoinAssetList` -> `GetUserCoinAssetList` (Retrieve a user's asset list)
- `/getUserCoinAsset` -> `GetUserCoinAsset` (Retrieve a user's asset balance)

## Interface Details

### GetUserCoinAssetList

- HTTP: `POST /getUserCoinAssetList`
- Request Type: `GetUserCoinAssetListReq`
- Response Type: `GetUserCoinAssetListReply`
- Description: Retrieve a user's asset list

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | No |  |
| `assets` | `UserAsset[]` | No |  |

### GetUserCoinAsset

- HTTP: `POST /getUserCoinAsset`
- Request Type: `GetUserCoinAssetReq`
- Response Type: `GetUserCoinAssetReply`
- Description: Retrieve a user's asset balance

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | No |  |
| `asset` | `UserAsset` | No |  |

## Data Models

### GetUserCoinAssetListReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |

### GetUserCoinAssetListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | No |  |
| `assets` | `UserAsset[]` | No |  |

### UserAsset

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `available` | `string` | No |  |

### GetUserCoinAssetReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 5, max_len:64}` |
| `coinId` | `uint64` | Yes | Token ID ; validation: `(validate.rules).uint64.gte = 1` |

### GetUserCoinAssetReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `userId` | `string` | No |  |
| `asset` | `UserAsset` | No |  |
