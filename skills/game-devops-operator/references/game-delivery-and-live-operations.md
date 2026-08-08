# Game Delivery And Live Operations Review

Use this reference as a review surface, not as a mandatory architecture. Select only the sections that apply to the user's game type, platforms, topology, and requested outcome.

## Release Inventory

Record the exact identities that can coexist during rollout:

| Surface | Identity | Compatibility boundary | Promotion evidence | Rollback boundary |
| --- | --- | --- | --- | --- |
| Client | platform, channel, version, source revision | server, API, schema, content, save | store or channel read-back | store delay and old clients |
| Dedicated server | image or package digest, build ID | client protocol, backend, content | allocation and join smoke | session draining |
| Backend | deployment and config revision | clients, schema, dependencies | player-journey check | data compatibility |
| Data | migration and schema version | old and new binaries | migration and read/write checks | restore or forward fix |
| Content/config | manifest and feature-state revision | clients and servers | resolved runtime value | cache and propagation delay |

Omit nonexistent surfaces. Add project-specific ones rather than forcing them into these rows.

## Production-Readiness Questions

### Build and supply chain

- Can an authorized clean runner produce the same required outputs from the recorded revision and inputs?
- Are engine, SDK, plugin, dependency, signing, and content-processing versions controlled?
- Are artifacts immutable, checksummed, attributable, scanned where required, and promoted without rebuilding?
- Are symbols, mappings, manifests, licenses, and provenance retained for the release lifetime?
- Can untrusted changes access release credentials or poison a shared cache?

### Compatibility and rollout

- Which old clients and active sessions remain during rollout?
- What prevents an incompatible client, server, backend, schema, content, or save combination?
- Can the rollout pause, drain, canary, phase, or disable the risky behavior?
- Which changes are reversible, forward-fix only, store-gated, or data-destructive?
- Has the actual recovery path been exercised on the intended artifact and environment?

### Online session lifecycle

- What creates, registers, declares ready, allocates, drains, terminates, and cleans a game server?
- How are abandoned allocations, duplicate ownership, stuck sessions, and orphaned resources reconciled?
- Which signal predicts demand early enough to satisfy the accepted player join time?
- What happens when a region, allocator, matchmaker, host, or dependency is unavailable?

### State and recovery

- Which state is authoritative, cached, eventually consistent, reconstructable, or disposable?
- What are the accepted data-loss and recovery-time limits?
- Are backups isolated from the primary failure domain and protected from accidental deletion?
- Has a representative restore been timed and validated at the application level?
- Who owns migration failure, partial writes, reconciliation, and player compensation decisions?

### Observability and response

- Can operators follow the affected player journey across client, edge, service, and game server?
- Are metrics tied to a build, environment, region, platform, and mode without unbounded labels?
- Do alerts describe player impact, urgency, owner, dashboard, runbook, and escalation?
- Can deployment, configuration, infrastructure, and feature-state changes be placed on the incident timeline?
- Does recovery verification cover the failed player journey rather than process health alone?

## Verification Ladder

Use the highest rung required by the claim:

1. **Static** — configuration parses, policy or manifest is structurally valid.
2. **Build** — the intended artifact is created and identified.
3. **Component** — one service or server starts and passes its scoped checks.
4. **Integration** — required dependencies and compatibility paths work together.
5. **Player journey** — a representative user can complete the affected flow.
6. **Capacity or resilience** — the accepted workload or failure is exercised within budgets.
7. **Recovery** — rollback, restore, or reconstruction meets the accepted boundary.

Never use a lower rung as proof of a higher-rung claim.

## Minimum Release Evidence

For the surfaces in scope, retain:

- source revision, artifact digest or build ID, engine and toolchain versions;
- CI run and promotion record;
- environment, region, configuration, schema, and feature-state revision;
- compatibility cases exercised and results;
- player-journey, capacity, observability, and recovery evidence required by the accepted claim;
- known risks, untested surfaces, rollback limits, owner, and decision.

The record may live in the project's established release system. Do not create a new document merely to satisfy this reference when durable equivalent evidence already exists.
