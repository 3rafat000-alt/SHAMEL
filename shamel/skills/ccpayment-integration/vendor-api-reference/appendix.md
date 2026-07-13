# Appendix

Last Updated: 2026-04-07

## Authentication

- Header `Appid`: merchant application identifier
- Header `Timestamp`: current request timestamp in milliseconds
- Header `Sign`: request signature generated from the request body

## Common Conventions

- All published API v2 routes use `POST`.
- Time fields are integer timestamps unless the field comment says otherwise.
- List interfaces commonly use `nextId` as the pagination cursor.
- Amount, price and fee fields are strings in proto definitions and should be handled as decimal strings.

## Enums

### WithdrawType

| Name | Value | Notes |
| --- | --- | --- |
| `_` | `0` |  |
| `Network` | `1` |  |
| `Cwallet` | `2` |  |

### HostedStep

| Name | Value | Notes |
| --- | --- | --- |
| `HostedTag_unused` | `0` |  |
| `FirstStep` | `1` |  |
| `SecondStep` | `2` |  |

## Error Codes

The following codes are synchronized from the v2 API error definitions.

| Name | Code | Notes |
| --- | --- | --- |
| `unused` | `0` |  |
| `Success` | `10000` |  |
| `Failed` | `10001` |  |
| `InvalidArgument` | `11000` | ********** Common error codes in the 11000 range*********/ Invalid parameters |
| `HeaderInvalidArgument` | `11001` |  |
| `Internal` | `11002` | Internal error |
| `NotFound` | `11003` | Data not found |
| `RateLimit` | `11004` | Reduce request frequency |
| `VerifySignFailed` | `11005` | Signature verification failed |
| `ReqExpired` | `11006` | Request expired |
| `RepeatedSubmit` | `11007` |  |
| `QueryDurationTooMax` | `11008` | The query time range is too large |
| `ReqDailyLimit` | `11009` | Daily request limit exceeded |
| `QueryNumMax` | `11010` | Too many orders requested; the maximum is 100 |
| `OrderDuplicate` | `11011` | Duplicate merchant order ID |
| `ExpiredAtTooMax` | `11012` | Order expiration time is too long |
| `NoSupportVersion` | `11013` | This version is not supported by API v2 |
| `MaliciousReq` | `11014` | Malicious request detected; IP blocked for 5 days |
| `UserIdNotFound` | `11015` | User ID does not exist userId does not exist |
| `NotOnlineDeposit` | `11016` | Only on-chain deposits are supported |
| `CwalletClosed` | `11017` | cc wallet is closed |
| `FrequentOperation` | `11018` | Operation attempted too frequently, or lock acquisition failed. Please try again shortly. |
| `MerchantDisabled` | `12000` | Merchant is disabled |
| `MerchantNotFound` | `12001` | Merchant not found |
| `IpNotInWhitelist` | `12002` | IP address is not in the whitelist |
| `MerchantApiDisabled` | `12003` | This merchant cannot use the API until website or corporate verification is completed. |
| `InvalidCoin` | `13000` | Invalid token |
| `InvalidChain` | `13001` | Invalid chain |
| `AbnormalCoinPrice` | `13002` | Abnormal token price |
| `AbnormalCoinPriceNotSupportMode` | `13003` | Abnormal token price; merchant-paid network fee mode is not supported |
| `UnstableBlockchain` | `13004` | Unstable blockchain. Withdrawal of this coin is not available. Please try it later. |
| `AbnormalCoinStatus` | `13005` | Token status is abnormal; trading has been halted |
| `CoinStopSwap` | `13006` | This token is not available for swaps |
| `BalanceInsufficient` | `14000` | Insufficient balance |
| `WithdrawFeeTooLow` | `14001` | Withdrawal fee is too low |
| `AddressNotActive` | `14002` | Address is invalid or inactive |
| `AddressEmptyMemo` | `14003` | Memo is required for this chain |
| `ChainStopWithdraw` | `14004` | Withdrawals are disabled on this chain |
| `WithdrawValueLessThanLimit` | `14005` |  |
| `WithdrawValueMoreThanLimit` | `14006` |  |
| `WithdrawAddrFormat` | `14007` | Invalid withdrawal address format |
| `WithdrawCannotSelf` | `14008` | Cannot withdraw to your own address |
| `CoinNoSupportMemo` | `14009` | This token does not support memo |
| `NoSupportCoin` | `14010` | This merchant does not support the token |
| `WithdrawFeeBalanceNotEnough` | `14011` | Insufficient balance in the withdrawal fee account |
| `NotSupportMerchantTransfer` | `14012` | Internal transfers between merchants are not supported |
| `CoinPrecisionLimit` | `14013` | Submitted amount exceeds the token's allowed decimal precision |
| `NotFinishCollection` | `14014` | Consolidation fee has not been completed |
| `WithdrawToContractAddress` | `14015` | It’s not supported to transfer to the contract address of this token. |
| `WithdrawInvalidAddressType` | `14016` | Address type error, we only support transfer to data accounts. |
| `AddressInBlackList` | `14017` | Address is blacklisted; withdrawal rejected |
| `DisabledWithdraw` | `14018` | Withdrawals are disabled |
| `WithdrawAmountFeeTooLittle` | `14019` | Withdrawal amount minus network fee is below the minimum allowed amount |
| `NotWhitelistDisabledWithdraw` | `14020` | Withdrawals are disabled because no whitelist is configured |
| `NotWhitelistDisabledSwap` | `14021` | Swaps are disabled because no whitelist is configured |
| `TestModeLimitAmount` | `14022` | Withdrawal amount is restricted in test mode |
| `TestModeSingleLimitAmount` | `14023` | Single-withdrawal amount is limited to 10 in test mode |
| `AddressFormatErr` | `14024` | Invalid address format Address format |
| `AddressMemoFormatErr` | `14025` | Memo is required for this chain |
| `RiskAddress` | `14026` | Risky address |
| `SeqDuplicate` | `14027` | Duplicate sequence number |
| `UnableAbort` | `14028` | Unable to abort |
| `AddressBlackList` | `14029` | Address is blacklisted |
| `GenerateAddressFailed` | `15000` | Deposit 15000 Failed to generate address |
| `PaymentAddressNumTooMuch` | `15001` | The limit for requesting user payment addresses has been exceeded |
| `OrderExpired` | `15002` | Order expired |
| `ChainStopDeposit` | `15003` | Deposits are disabled |
| `OrderUrlExpired` | `15004` | Generated URL has expired |
| `CoinUnavailableForSwap` | `16001` | Swap-related error range 16000; swap operations are disabled |
| `SwapAmountInTooLow` | `16002` | Swap input amount is too small |
| `AmountOutMinimumTooHigh` | `16003` | Output amount is below the minimum allowed amount |
| `MerchantSwapLimit` | `16004` | Swap amount exceeds the daily limit |
| `DisabledSwap` | `16005` | Swaps are disabled |
| `NoSupportSwap` | `16006` | Swaps are not supported |
| `UnUsedAddressDeprecatedNotAllowed` | `17000` | Address deprecation is not allowed for unused addresses |
| `UnMatchedMerchantAddressDeprecated` | `17001` | Address deprecation failed because the merchant address does not match |
| `UnBindingMemoAddressDeprecated` | `17002` | Address deprecation is not supported for addresses with memo |
| `UnBindingAddressDeprecated` | `17003` | Address has already been deprecated |
| `UnSupportedAddressDeprecated` | `17004` | Address deprecation is only supported for deposit or user addresses |
| `UnSupportedChainAddress` | `17005` | Address and chain do not match |
| `UnbindingAddressFailed` | `17006` | Address deprecation failed |
| `AddressNotBelongCCP` | `17007` | Address does not belong to CCPayment |

## Core Models

| Model | Fields |
| --- | --- |
| `Coin` | `coin_id`, `coin_symbol`, `coin_price` |
| `BatchWithdrawStats` | `total`, `succeeded`, `failed`, `canceled`, `processing`, `execOrderId` |
