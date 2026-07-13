# Merchant Assets Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/getAppCoinAssetList` -> `GetAppCoinAssetList` (All assets)
- `/getAppCoinAsset` -> `GetAppCoinAsset` (Asset balance for a single token)
- `/getAggregationFeeRecord` -> `GetAppCollectFeeRecordList` (Query consolidation fee records)

## Interface Details

### GetAppCoinAssetList

- HTTP: `POST /getAppCoinAssetList`
- Request Type: `Empty`
- Response Type: `AppCoinAssetListReply`
- Description: All assets

#### Request Parameters

No body.

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `assets` | `AssetEntity[]` | No |  |

### GetAppCoinAsset

- HTTP: `POST /getAppCoinAsset`
- Request Type: `AppCoinAssetReq`
- Response Type: `AppCoinAssetReply`
- Description: Asset balance for a single token

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `asset` | `AssetEntity` | No |  |

### GetAppCollectFeeRecordList

- HTTP: `POST /getAggregationFeeRecord`
- Request Type: `GetAppCollectFeeRecordListReq`
- Response Type: `GetAppCollectFeeRecordListReply`
- Description: Query consolidation fee records

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `startAt` | `int64` | Yes | Seconds ; validation: `(validate.rules).int64.gt = 0` |
| `endAt` | `int64` | Yes | Seconds ; validation: `(validate.rules).int64.gt = 0` |
| `nextId` | `string` | No | Pagination cursor |
| `limit` | `uint64` | No | Default: 20 ; validation: `(validate.rules).uint64 = {lte: 100}` |
| `chain` | `string` | No | An empty string means this field is not used as a filter. |
| `address` | `string` | No | An empty string means this field is not used as a filter. |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `list` | `CollectFeeRecordEntity[]` | No |  |
| `nextId` | `string` | No |  |

## Data Models

### AppCoinAssetListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `assets` | `AssetEntity[]` | No |  |

### AssetEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `available` | `string` | No |  |

### AppCoinAssetReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |

### AppCoinAssetReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `asset` | `AssetEntity` | No |  |

### GetAppCollectFeeRecordListReq

Consolidation fee records (merchant side)

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `startAt` | `int64` | Yes | Seconds ; validation: `(validate.rules).int64.gt = 0` |
| `endAt` | `int64` | Yes | Seconds ; validation: `(validate.rules).int64.gt = 0` |
| `nextId` | `string` | No | Pagination cursor |
| `limit` | `uint64` | No | Default: 20 ; validation: `(validate.rules).uint64 = {lte: 100}` |
| `chain` | `string` | No | An empty string means this field is not used as a filter. |
| `address` | `string` | No | An empty string means this field is not used as a filter. |

### GetAppCollectFeeRecordListReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `list` | `CollectFeeRecordEntity[]` | No |  |
| `nextId` | `string` | No |  |

### CollectFeeRecordEntity

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `collects` | `CollectFeeItem[]` | No |  |
| `aggregationTime` | `int64` | No |  |
| `chain` | `string` | No |  |
| `address` | `string` | No |  |

### CollectFeeItem

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `aggregationFee` | `string` | No |  |
