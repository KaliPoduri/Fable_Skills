# STRIDE (distilled)

Sources: Microsoft Threat Modeling Tool — Threats
(https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
and "Uncover Security Design Flaws Using The STRIDE Approach", MSDN
Magazine, Nov 2006
(https://learn.microsoft.com/en-us/archive/msdn-magazine/2006/november/uncover-security-design-flaws-using-the-stride-approach).
Both verified 2026-07-06.

## The six categories and the property each violates

| Letter | Threat | Violated security property | Definition (Microsoft) |
|---|---|---|---|
| S | Spoofing | Authentication | Illegally accessing and then using another user's authentication information (username, password, token) or posing as another system/service. |
| T | Tampering | Integrity | Malicious modification of data — persistent data in a store, or data in transit between two machines. |
| R | Repudiation | Non-repudiation | A user denies performing an action and the system cannot prove otherwise (no trustworthy trace/audit). |
| I | Information Disclosure | Confidentiality | Exposure of information to individuals not supposed to have access — files, data in transit, memory contents, error internals. |
| D | Denial of Service | Availability | Denying or degrading service to valid users (exhaustion, crash, resource fill-up). |
| E | Elevation of Privilege | Authorization | An unprivileged user gains privileged access sufficient to compromise the system; attacker becomes part of the trusted base. |

## DFD element types

| Element type | Meaning | Examples |
|---|---|---|
| External entity (interactor) | People/systems outside your control that interact with the system | End user, third-party API, partner service, admin human |
| Process | Code the system runs | API service, worker, function, gateway, cron job |
| Data store | Data at rest | Database, file storage, cache, queue contents, registry/config, logs |
| Data flow | Data in motion between elements | HTTP call, queue publish, DB connection, file transfer |
| Trust boundary | Line where trust level changes | Internet→edge, service→DB, user↔admin plane, tenant↔tenant, process↔third party |

## STRIDE-per-element applicability (MSDN Figure 5)

Apply ONLY the marked categories to each element type:

| Element type | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| External entity | X |  | X |  |  |  |
| Process | X | X | X | X | X | X |
| Data store |  | X |  | X | X |  |
| Data flow |  | X |  | X | X |  |

Notes:
- Processes get all six — they are where code runs and privileges live.
- Data stores and flows cannot "act", so no spoofing/repudiation/EoP on
  them (repudiation concerns around stores are usually about the LOGS they
  hold — model log tampering as T on the log store).
- Elements touching a trust boundary deserve the deepest analysis; a flow
  crossing a boundary is the classic highest-exposure case.
- Threats chain: spoofing an admin enables denial of service; a tampering
  path may yield elevation of privilege. Record the threat where it starts;
  do not chase every downstream consequence into separate entries.

## Writing a concrete threat statement

Formula: **[actor] does [action] to [element] causing [consequence]**.

- Weak: "Tampering may occur on the data flow."
- Strong: "An on-path attacker modifies sales records in transit between
  the client and the collection API, corrupting weekly revenue reports."

## Mitigation classes per category

Match the mitigation to the violated property; name a concrete control in
the model, not just the class.

| Category | Defense class | Typical controls |
|---|---|---|
| Spoofing | Authentication | Strong authN (MFA, mutual TLS), signed tokens with expiry, certificate pinning between services, anti-CSRF |
| Tampering | Integrity | TLS in transit, signatures/MACs/hashes, input validation at trust boundaries, integrity-checked storage, anti-replay (nonces, timestamps, counters) |
| Repudiation | Non-repudiation | Append-only audit logs with actor+time+action, log integrity protection, clock sync, signed receipts |
| Information Disclosure | Confidentiality | Encryption in transit and at rest, least-privilege access to data, generic error messages externally, secret management, data minimization |
| Denial of Service | Availability | Rate limiting and quotas, input size limits, timeouts and circuit breakers, autoscaling/redundancy, backpressure on queues |
| Elevation of Privilege | Authorization | Least privilege for every identity, authorization checks on every request at the server, sandboxing/isolation, separation of admin plane, secure defaults |

Response types for the register (OWASP): **Mitigate** (add a control),
**Eliminate** (remove the feature/flow/data), **Transfer** (move the risk
to a component or party better placed to handle it), **Accept** (documented
decision to do nothing — Low risk only).
