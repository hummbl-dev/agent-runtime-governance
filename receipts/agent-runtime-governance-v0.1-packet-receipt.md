# Packet Receipt — Agent Runtime Governance v0.1

This is a candidate receipt template for recording that a v0.1 governance packet
was reviewed. It is non-canon and exploratory.

## Packet under review

- **Packet ID:** _<fill in from governanceManifest.id>_
- **Packet version:** _<fill in from governanceManifest.version>_
- **Schema version:** v0.1
- **Packet status:** _<fill in from packetStatus>_
- **Scope:** _<fill in from governanceManifest.scope>_

## Review

- **Reviewer:** _<name or role>_
- **Reviewed at:** _<ISO-8601 timestamp>_
- **Decision:** _<one of: accepted, rejected, changes-requested, deferred>_
- **Review basis:** _<short statement of why the decision was made>_

## Authority

- **Authority granted by:** _<from authority.grantedBy>_
- **Authority basis:** _<from authority.basis>_
- **Note:** v0.1 only records the authority claim; it does not verify it.

## Governance contract summary

- **Policy engine:** _<kind, ref>_
- **Enforcement points:** _<list of name / stage / failMode>_
- **Guardrails:** _<list of id / effect>_
- **Kill switch policy:** _<effect, trigger count>_
- **Circuit breaker policy:** _<metric, limit, effect>_
- **Audit requirements:** _<recorded fields, retention>_

## Receipt requirements check

Confirm the receipt contains every field listed in the packet's
`receiptRequirements.fields` and is attested by `receiptRequirements.signedBy`:

- [ ] All required receipt fields present.
- [ ] Receipt attested by the declared signer.
- [ ] No private, internal, or secret content included.

## Non-canon note

This receipt records that a review occurred. It does not certify adoption, does
not bind future versions, and does not assert authority beyond what the packet
itself claims. Adoption requires a separate, reviewed governance path that does
not yet exist in this repository.
