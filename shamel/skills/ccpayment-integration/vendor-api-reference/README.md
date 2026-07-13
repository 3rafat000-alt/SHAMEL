# CCPayment API v2 Complete Documentation

Last Updated: 2026-04-07

## Overview

This directory documents the CCPayment API v2 HTTP routes and related request/response models.

**Base URL:** `https://ccpayment.com/ccpayment/v2/`

**Authentication Headers:**
- `Appid`: application identifier
- `Timestamp`: millisecond timestamp
- `Sign`: signature of the request body

**Common Response Envelope:**
```json
{
  "code": 10000,
  "msg": "success",
  "data": {}
}
```

## Module List

1. [Basic Info Module](./01-basic-info.md) - 7 HTTP route(s)
2. [Merchant Assets Module](./02-merchant-assets.md) - 3 HTTP route(s)
3. [Merchant Deposit Module](./03-merchant-deposit.md) - 4 HTTP route(s)
4. [Merchant Withdraw Module](./04-merchant-withdraw.md) - 8 HTTP route(s)
5. [Merchant Batch Withdraw Module](./05-merchant-batch-withdraw.md) - 7 HTTP route(s)
6. [User Assets Module](./06-user-assets.md) - 2 HTTP route(s)
7. [User Deposit Module](./07-user-deposit.md) - 3 HTTP route(s)
8. [User Withdraw Module](./08-user-withdraw.md) - 4 HTTP route(s)
9. [User Transfer Module](./09-user-transfer.md) - 7 HTTP route(s)
10. [Orders Module](./10-orders.md) - 3 HTTP route(s)
11. [Swap Module](./11-swap.md) - 5 HTTP route(s)
12. [User Swap Module](./12-user-swap.md) - 3 HTTP route(s)
13. [Utilities Module](./13-utilities.md) - 5 HTTP route(s)

## Notes

- The module split in this directory is documentation-oriented and optimized for SDK generation.
- If an interface changes, regenerate these files from the latest v2 API definitions before updating SDK generation rules.

## Appendix

- [Appendix](./appendix.md)

**Document Version:** v2.1
**Last Updated:** 2026-04-07
