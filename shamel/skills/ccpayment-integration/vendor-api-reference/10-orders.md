# Orders Module

Last Updated: 2026-04-07

All HTTP interfaces in this file are synchronized from the CCPayment API v2 definitions. Every route uses `POST` and the base URL is `https://ccpayment.com/ccpayment/v2/`.

## Endpoint List

- `/getAppOrderInfo` -> `GetAppOrderInfo` (Retrieve order details)
- `/createInvoiceUrl` -> `CreateInvoiceUrl` (CreateInvoiceUrl)
- `/getInvoiceOrderInfo` -> `GetInvoiceOrderInfo` (Retrieve invoice order details)

## Interface Details

### GetAppOrderInfo

- HTTP: `POST /getAppOrderInfo`
- Request Type: `GetAppOrderInfoReq`
- Response Type: `GetAppOrderInfoReply`
- Description: Retrieve order details

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `amountToPay` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `chain` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `toMemo` | `string` | No |  |
| `createAt` | `int64` | No |  |
| `rate` | `string` | No |  |
| `fiatId` | `uint64` | No |  |
| `fiatSymbol` | `string` | No |  |
| `expiredAt` | `int64` | No |  |
| `checkoutUrl` | `string` | No |  |
| `buyerEmail` | `string` | No |  |
| `paidList` | `PayInfo[]` | No |  |

### CreateInvoiceUrl

- HTTP: `POST /createInvoiceUrl`
- Request Type: `CreateInvoiceUrlReq`
- Response Type: `CreateInvoiceUrlReply`
- Description: CreateInvoiceUrl

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `product` | `string` | No | [(validate.rules).string={ignore_empty: true, gte: 1}] ; validation: `(validate.rules).string = {ignore_empty: true,min_len: 1, max_len:128}` |
| `priceFiatId` | `uint64` | No |  |
| `priceCoinId` | `uint64` | No |  |
| `price` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `buyerEmail` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:120, email:true}` |
| `returnUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |
| `expiredAt` | `int64` | No | Order expiration time. Defaults to 24 hours if omitted. ; validation: `(validate.rules).int64 = {ignore_empty: true, gte: 1}` |
| `closeUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |
| `notifyUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `invoiceUrl` | `string` | No |  |

### GetInvoiceOrderInfo

- HTTP: `POST /getInvoiceOrderInfo`
- Request Type: `GetInvoiceOrderInfoReq`
- Response Type: `GetInvoiceOrderInfoReply`
- Description: Retrieve invoice order details

#### Request Parameters

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

#### Response Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | No |  |
| `createAt` | `int64` | No |  |
| `product` | `string` | No |  |
| `price` | `string` | No |  |
| `priceCoinId` | `uint64` | No | Returned when the invoice is priced in tokens. |
| `priceFiatId` | `uint64` | No | Returned when the invoice is priced in fiat currency. |
| `priceSymbol` | `string` | No |  |
| `invoiceUrl` | `string` | No | Checkout page URL |
| `buyerEmail` | `string` | No | Buyer email; returned only when provided. |
| `expiredAt` | `int64` | No | Order expiration time. Defaults to 24 hours if not provided. |
| `totalPaidValue` | `string` | No | Total paid value, in the pricing currency. |
| `paidList` | `GetInvoiceOrderInfoReply.PayInfo[]` | No | Only paid transaction entries are returned. |

## Data Models

### GetAppOrderInfoReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### GetAppOrderInfoReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `amountToPay` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `chain` | `string` | No |  |
| `toAddress` | `string` | No |  |
| `toMemo` | `string` | No |  |
| `createAt` | `int64` | No |  |
| `rate` | `string` | No |  |
| `fiatId` | `uint64` | No |  |
| `fiatSymbol` | `string` | No |  |
| `expiredAt` | `int64` | No |  |
| `checkoutUrl` | `string` | No |  |
| `buyerEmail` | `string` | No |  |
| `paidList` | `PayInfo[]` | No |  |

### PayInfo

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `fromAddress` | `string` | No |  |
| `amount` | `string` | No |  |
| `serviceFee` | `string` | No |  |
| `txid` | `string` | No |  |
| `status` | `string` | No |  |
| `arrivedAt` | `int64` | No |  |
| `rate` | `string` | No |  |
| `isFlaggedAsRisky` | `bool` | No |  |

### CreateInvoiceUrlReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string = {min_len: 3, max_len:64}` |
| `product` | `string` | No | [(validate.rules).string={ignore_empty: true, gte: 1}] ; validation: `(validate.rules).string = {ignore_empty: true,min_len: 1, max_len:128}` |
| `priceFiatId` | `uint64` | No |  |
| `priceCoinId` | `uint64` | No |  |
| `price` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |
| `buyerEmail` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:120, email:true}` |
| `returnUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |
| `expiredAt` | `int64` | No | Order expiration time. Defaults to 24 hours if omitted. ; validation: `(validate.rules).int64 = {ignore_empty: true, gte: 1}` |
| `closeUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |
| `notifyUrl` | `string` | No | validation: `(validate.rules).string = {ignore_empty: true, max_len:150, uri:true}` |

### CreateInvoiceUrlReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `invoiceUrl` | `string` | No |  |

### GetInvoiceOrderInfoReq

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | Yes | validation: `(validate.rules).string.min_len = 1` |

### GetInvoiceOrderInfoReply

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `orderId` | `string` | No |  |
| `createAt` | `int64` | No |  |
| `product` | `string` | No |  |
| `price` | `string` | No |  |
| `priceCoinId` | `uint64` | No | Returned when the invoice is priced in tokens. |
| `priceFiatId` | `uint64` | No | Returned when the invoice is priced in fiat currency. |
| `priceSymbol` | `string` | No |  |
| `invoiceUrl` | `string` | No | Checkout page URL |
| `buyerEmail` | `string` | No | Buyer email; returned only when provided. |
| `expiredAt` | `int64` | No | Order expiration time. Defaults to 24 hours if not provided. |
| `totalPaidValue` | `string` | No | Total paid value, in the pricing currency. |
| `paidList` | `GetInvoiceOrderInfoReply.PayInfo[]` | No | Only paid transaction entries are returned. |

### GetInvoiceOrderInfoReply.PayInfo

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recordId` | `string` | No |  |
| `coinId` | `uint64` | No |  |
| `coinSymbol` | `string` | No |  |
| `chain` | `string` | No |  |
| `fromAddress` | `string` | No | Source address |
| `toAddress` | `string` | No | Receiving address |
| `toMemo` | `string` | No |  |
| `paidAmount` | `string` | No | Amount paid in the settlement token |
| `serviceFee` | `string` | No | Service fee |
| `txid` | `string` | No |  |
| `status` | `string` | No |  |
| `arrivedAt` | `int64` | No | Arrival time |
| `rate` | `string` | No | USD price of the paid token divided by the USD price of the pricing currency |
| `paidValue` | `string` | No | Paid value, in the pricing currency. |
| `isFlaggedAsRisky` | `bool` | No |  |
