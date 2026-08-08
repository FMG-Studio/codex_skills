---
name: game-devops-operator
description: "Build, review, automate, secure, operate, or troubleshoot delivery platforms for games. Use for game CI/CD, engine build farms, artifact and patch pipelines, dedicated-server fleets, backend deployment, infrastructure as code, environments, observability, capacity, load testing, incidents, rollback, disaster recovery, and live-service release readiness. Do not use as the primary skill for gameplay implementation, game-design ideation, content creation, client frame-rate optimization, generic workstation setup, or backend feature coding without an operations outcome."
---

# Game DevOps Operator

Deliver reproducible game builds and observable, recoverable game services. Optimize for the project's actual game type, platforms, engine, release model, player regions, scale, compliance boundary, and budget rather than assuming every game needs cloud-native infrastructure.

Read [references/game-delivery-and-live-operations.md](references/game-delivery-and-live-operations.md) when designing or reviewing a release pipeline, online-service topology, production-readiness gate, incident process, or disaster-recovery plan.

## Establish The Operations Contract

Inspect current evidence before proposing or changing infrastructure:

- repositories, engine and build metadata, package manifests, CI configuration, scripts, artifact stores, and signing steps;
- client, dedicated-server, backend, database, cache, queue, matchmaking, identity, commerce, telemetry, and platform-service boundaries that actually exist;
- environments, regions, DNS, certificates, secrets, cloud accounts, infrastructure as code, deployment manifests, runbooks, dashboards, alerts, backups, and restore evidence;
- supported stores and platforms, release channels, version policy, maintenance windows, player geography, expected concurrency, and cost constraints;
- recent pipeline runs, deployments, incidents, capacity measurements, load tests, and production read-backs.

Resolve the requested outcome and the smallest topology that can achieve it. Distinguish:

- offline or peer-hosted games, where build, signing, packaging, crash reporting, and store delivery may be the main operations surface;
- session-based online games, where allocation, matchmaking, compatibility, regional capacity, and session draining matter;
- persistent live services, where migrations, state durability, SLOs, incident response, abuse controls, and disaster recovery are first-class.

Ask a focused question only when an unresolved platform, scale, data-loss tolerance, cost, release authority, or destructive production action would materially change the result. Otherwise state a conservative assumption and continue.

## Define Measurable Acceptance

Before implementation, record only the targets relevant to the request:

- supported client and server platforms, engine version, build configurations, and release channels;
- reproducibility, duration, queue-time, cache, artifact-retention, provenance, and signing expectations for builds;
- availability, matchmaking and allocation success, latency, disconnect, crash-free session, tick health, recovery-time, and recovery-point objectives;
- expected and burst concurrent users, sessions, regions, server density, scaling limits, and cost guardrails;
- deployment, compatibility, migration, rollback, backup, restore, and incident-response criteria;
- evidence that will prove each target after the change.

Do not invent an SLO, player count, hardware profile, region, RTO, RPO, or budget. Label proposed values `candidate` until accepted by the user or authoritative project evidence.

## Build A Reproducible Delivery Path

Trace the real dependency graph from source revision to installable client and runnable server. Preserve required engine tools, SDKs, platform credentials, plugins, submodules, large-file assets, generated content, localization, symbols, and version metadata.

- Pin or record toolchain versions where drift can change the artifact.
- Keep secrets out of repositories, logs, caches, artifacts, and untrusted pull-request jobs.
- Separate compile, cook or content processing, test, package, sign, publish, and deploy stages when their permissions or failure boundaries differ.
- Reuse caches only with keys that include every input capable of invalidating the result.
- Give artifacts immutable identities tied to source revision, configuration, target, and build provenance.
- Retain symbols and mappings required to diagnose released crashes.
- Verify the exact artifact promoted between environments; do not silently rebuild for production.
- Treat signing, notarization, console certification, store review, and staged store rollout as external gates when they apply.

Optimize build time only after measuring queue, checkout, dependency, compile, cook, package, upload, and test durations separately. Faster pipelines must not weaken correctness, isolation, provenance, or secret boundaries.

## Choose Infrastructure Proportionally

Prefer the least complex design that meets accepted reliability and scale targets. A small game may need one or several well-managed hosts, containers, backups, and monitoring rather than Kubernetes. Add orchestration, multi-region routing, service meshes, or custom platform layers only when measured scale, isolation, recovery, or team-operability requirements justify them.

Manage durable infrastructure through the project's established infrastructure-as-code and configuration workflow. Before mutation:

1. Resolve the exact account, project, environment, region, cluster, host, namespace, service, and data store.
2. Inspect the current plan or diff and unrelated changes.
3. Identify stateful dependencies, player impact, compatibility risks, rollback limits, and required backups.
4. Use least privilege and the approved secret store.
5. Apply the narrow change through the established deployment path.
6. Read back live state and service behavior.

Never copy a destructive production command from a proposed plan into execution without resolving its exact target and recovery boundary. Stop before an unapproved paid resource, force update, irreversible migration, data deletion, certificate or DNS cutover, or player-visible production rollout.

## Release Clients And Services Safely

Treat a game release as a compatibility matrix, not one deploy event. Consider the released client versions, dedicated-server versions, backend API and schema versions, saved data, protocol, configuration, content manifests, and platform branches that coexist during rollout.

- Prefer backward- and forward-compatible transitions across the required overlap window.
- Use expand-and-contract migrations when old and new binaries must run concurrently.
- Define whether sessions can drain, reconnect, migrate, or must be terminated.
- Keep kill switches or feature flags for operational risk when the project supports them.
- Separate rollback of stateless services from rollback of data, save formats, economy changes, and store-published clients.
- Validate a rollback before relying on it; a deployment tool's rollback button is not evidence of recoverability.
- Prevent incompatible clients from joining servers with an explicit version or protocol policy and a player-safe message.

For desktop and console releases, account for patch size, download and install behavior, delta-generation rules, depot or branch configuration, signing, entitlements, and certification gates. For mobile releases, account for store review delay, phased rollout, platform delivery rules, and long-lived old clients. Use current official platform and engine documentation for version-sensitive requirements.

## Operate Dedicated-Server Fleets

When dedicated servers are in scope, define and verify:

- immutable server build identity and runtime configuration;
- readiness, liveness, registration, allocation, session lifecycle, graceful drain, termination, and cleanup behavior;
- placement by region, mode, map, capacity class, latency, and failure domain;
- warm-pool or startup-time requirements and autoscaling signals;
- CPU, memory, network, disk, process, tick, player-slot, and per-session limits;
- matchmaking-to-allocation timeout and failure handling;
- log, crash, replay, and forensic artifact collection;
- recovery from host, region, control-plane, and dependency failures.

Scale on a signal that leads player demand early enough to satisfy allocation time. Raw CPU alone may miss queue growth, reserved-but-not-started sessions, slow startup, or region-specific shortages. Prevent both uncontrolled scale-up and scale-to-zero behavior that violates accepted join-time targets.

## Make Production Observable

Instrument the player journey and the infrastructure beneath it. Use stable build, environment, region, platform, mode, and service dimensions while controlling cardinality. Never attach player secrets or unnecessary personal data to telemetry.

Cover the relevant path:

```text
launch -> authenticate -> patch or config -> queue -> match -> allocate -> connect -> play -> persist -> reward -> exit
```

Correlate service logs, metrics, traces, deployment events, server build IDs, client crash versions, and session identifiers permitted by the privacy model. Useful signals may include:

- crash-free users and sessions, startup and patch failures;
- authentication, queue, matchmaking, allocation, connection, reconnect, and persistence success;
- latency, jitter, packet loss, disconnect reason, tick health, and session duration;
- request rate, errors, saturation, dependency health, queue depth, database health, and regional capacity;
- cost per concurrent player, session, or region when cost is in scope.

Alert on symptoms that require action and link alerts to an owner, dashboard, runbook, and escalation route. A dashboard with no decision or response path is not production readiness.

## Prove Capacity And Recovery

Model load from player behavior rather than multiplying one HTTP request. Include login bursts, queueing, matchmaking, server allocation, reconnect storms, gameplay traffic, persistence, rewards, commerce where authorized, telemetry, and dependency limits that affect the requested scenario.

- Use isolated test identities and synthetic data.
- Protect production and third-party services with explicit authorization and rate limits.
- Run ramp, spike, soak, failover, and recovery scenarios only when they answer an accepted risk.
- Record workload model, environment, build, data shape, regions, duration, bottleneck, saturation point, error behavior, and cleanup.
- Test backup restoration and service reconstruction; successful backup creation alone does not prove recovery.

Do not call a system ready for the expected concurrency from a smoke test, average utilization, or an unrepresentative empty-server benchmark.

## Diagnose Incidents From Evidence

During an incident:

1. Establish severity, affected player journey, start time, regions, platforms, builds, scope, and safety or data risks.
2. Preserve evidence and compare changes around the onset.
3. Mitigate player impact with the smallest reversible action.
4. Verify recovery using player-facing and system signals.
5. Communicate confirmed facts, uncertainty, impact, mitigation, and next update time.
6. After stabilization, reconstruct the timeline and create owned corrective actions that prevent recurrence or reduce impact.

Do not make speculative root cause the basis for a destructive mitigation. Do not declare recovery because a process restarted; verify the affected player journey and agreed service indicators.

## Validate The Requested Outcome

Match the evidence to the claim:

- pipeline: a clean or controlled run produces the intended immutable artifact with recorded provenance;
- infrastructure: plan or diff review, successful apply, and live read-back of the exact targets;
- deployment: health plus representative player-journey checks on the promoted artifact;
- compatibility: exercised supported client, server, backend, schema, and save-data combinations;
- observability: injected or historical signal reaches the correct dashboard and alert route without leaking sensitive data;
- capacity: representative load reaches the accepted target within SLO and resource or cost guardrails;
- rollback: rehearsed rollback or recovery procedure with measured outcome and known data boundary;
- disaster recovery: restored state and reconstructed service meet accepted RTO and RPO;
- repository delivery: intended files only are committed, pushed without force, and the remote branch contains the local commit.

Classify evidence as `verified`, `candidate`, `not exercised`, or `externally blocked`. A config parse, CI syntax check, container start, health endpoint, or deployment command proves only that layer. Continue independently actionable work when another required layer is blocked.

## Done Criteria

Finish only when every requested build, artifact, infrastructure, deployment, compatibility, observability, capacity, recovery, operational, and repository outcome is verified or explicitly blocked by a genuinely unavailable capable source or environment. Report the exact environments, builds, commands or runs, read-backs, measurements, remaining risks, and rollback boundary. Never describe a proposed architecture, green syntax check, successful command, or healthy process as a production-ready game service without the player-facing evidence required by the claim.
