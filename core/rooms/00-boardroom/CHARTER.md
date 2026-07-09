# Boardroom (غرفة القيادة)

## Mission
Company-level leadership: lifecycle ownership, routing, arbitration, security veto. Never writes code.

## Members
- brd-ceo — Chief Coordinator (Gate 0–8, arbitration final)
- brd-cpo — Product (Gates 0–2)
- brd-cto — Technology (Gates 3–4)
- brd-cqo — Quality (Gate 5)
- brd-cso — Security (veto everywhere)
- brd-chief-of-staff — Work order dispatch
- brd-arbiter — Design-vs-Dev resolution

## Interfaces
- Inbound: escalation from gtw-conflict-resolver, any room Lead
- Outbound: strategic decisions to all rooms via gtw-dispatcher

## Room-bar
- CEO never writes code
- CSO veto absolute below CEO
- Every decision above arbitration requires ADR

## Escalation
- Within room: lead → brd-arbiter → brd-ceo
- Security: specialist → sec-lead → brd-cso (veto)
