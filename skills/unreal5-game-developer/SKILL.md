---
name: unreal5-game-developer
description: "Implement, debug, migrate, build, profile, optimize, test, or review gameplay and tooling in Unreal Engine 5 projects. Use for UE5 C++, Blueprints, modules, plugins, Enhanced Input, animation, AI, physics, networking, asset loading, packaging, and performance work. Always treat smooth execution on the project's defined low-end PC target as a first-class acceptance constraint. Do not use as the primary skill for game-design ideation, balance-only work, final art creation, product UI, or non-Unreal development."
---

# Unreal 5 Game Developer

Deliver verified Unreal Engine behavior within an explicit low-end PC budget. Read [references/low-end-pc-performance.md](references/low-end-pc-performance.md) whenever implementation, review, rendering, streaming, AI, physics, memory, loading, packaging, or performance is in scope.

## Orient To The Project

Before editing:

1. Locate the authoritative repository root and `.uproject`.
2. Read the descriptor, engine association, module and target rules, plugins, relevant `Source/`, `Config/`, tests, maps, Blueprints, data assets, and project documentation.
3. Determine the actual engine version, compiler, SDK, target platform, build configuration, branch, remote, and unrelated worktree changes.
4. Trace the real execution path through C++, Blueprints, assets, subsystems, delegates, async work, networking, animation, and configuration that can affect the request.
5. Resolve the minimum supported PC, resolution, quality preset, FPS target, and memory limits from current project evidence.

If the hardware profile or budgets are absent, propose a measurable candidate profile and label it `candidate`. Do not claim low-end readiness until the user or project accepts a target and a representative build is measured on it.

Use current official Unreal documentation for version-sensitive APIs, build settings, plugins, rendering features, and profiling tools.

## Define The Performance Contract

Before a performance-sensitive implementation, record:

- target hardware and OS;
- resolution, quality preset, window mode, and representative map or scenario;
- FPS target and corresponding frame-time budget;
- game-thread, render-thread, GPU, RAM, VRAM, load-time, and hitch limits that apply;
- baseline build, measurement command or trace, and sample duration;
- independently variable quality or density fallbacks.

Use `16.67 ms` only as the mathematical frame budget for 60 FPS and `33.33 ms` for 30 FPS, never as an invented product target.

## Choose The Implementation Boundary

Follow established project ownership. When no contract exists, default to:

- C++ for durable systems, hot paths, reusable contracts, and automation;
- Blueprints for content wiring, presentation, rapid experiments, and designer tuning;
- data assets, curves, tables, tags, or configuration for values that must change without recompilation.

This is a fallback, not a mandatory architecture. Keep a narrow fix narrow. Do not introduce a framework, subsystem, plugin, pooling layer, or rewrite until current evidence shows it is required.

Expose the smallest stable Blueprint surface needed by designers. Avoid hard-coded asset paths when project-established assignable or data-driven references exist.

## Implement With A Low-End Bias

- Prefer events, delegates, timers, state changes, and bounded work over unconditional per-frame polling. Use Tick only when the behavior requires it, with an appropriate interval, tick group, enablement lifecycle, and measured cost.
- Keep work proportional to visible or active gameplay. Cull, sleep, deactivate, or reduce update frequency for distant and irrelevant actors.
- Avoid repeated world searches, reflection-heavy calls, string formatting, allocations, container growth, and synchronous asset loads in hot paths.
- Use soft references and asynchronous loading where delayed availability is acceptable. Define ownership, cancellation, failure, and unload behavior.
- Control Actor, UObject, component, material, collision, physics, animation, AI, navigation, audio, particle, and replication counts. Optimize the measured bottleneck rather than applying folklore.
- Reserve container capacity when the bound is known. Prefer stable ownership and clear lifetime rules; do not create unsafe caches to save a lookup.
- Consider pooling only for measured high-frequency spawn/destroy churn. A pool with no evidence is extra memory and complexity, not an optimization.
- Preserve scalable fallbacks for expensive lighting, shadows, effects, post-processing, foliage, view distance, resolution, and simulation density.
- Avoid blocking the game thread with file, asset, save-game, network, or expensive generation work when an asynchronous project-supported path exists.
- Keep generated folders and credentials out of Git. Treat `.uasset` and `.umap` as binary and do not invent merges.

## Build And Diagnose

Generate project files only when IDE metadata is missing or stale. Build the exact Editor, Game, Client, Server, or packaged target required by the request.

Diagnose the first authoritative failure and keep evidence classes separate:

- engine discovery and launcher state;
- compiler, SDK, and target-rule compatibility;
- C++ compile and link;
- module and plugin loading;
- Blueprint and asset compilation;
- gameplay runtime;
- CPU, GPU, memory, streaming, and hitch behavior;
- packaging and target-machine launch.

Do not describe generated project files, a successful compile, or an Editor launch as proof that a mechanic works or that a build meets the low-end budget.

## Profile Before And After

Use a representative packaged Development or Test build when practical. Start with `stat unit` to identify Game, Draw, or GPU pressure, then use Unreal Insights, `stat gpu`, GPU Visualizer, memory tools, load-time traces, or subsystem-specific stats as required by the bottleneck.

Keep the scene, route, camera, build configuration, scalability preset, warm-up, sample duration, and hardware constant across baseline and candidate. Report frame times and tail behavior, not average FPS alone.

Optimize one evidenced bottleneck at a time. Repeat the same capture after the change and check for regressions in correctness, visual behavior, memory, load time, and other threads.

## Verify The Full Claim

Match verification to the requested outcome:

- descriptor or config: parse and read back the final file;
- C++: compile the affected target and run relevant automated tests;
- Blueprint or asset: compile and load it in the target engine version;
- gameplay: run the representative map in PIE or the required packaged build;
- low-end performance: capture the accepted scenario on target hardware or a documented proxy and compare every agreed budget;
- packaging: produce and launch the requested package on the target PC;
- GitHub delivery: commit intended files, push without force, and compare local HEAD with the remote branch.

Record the engine version, hardware, build, map/scenario, scalability, commands or trace files, sample window, baseline, result, variance, and untested surfaces. Do not hide a failed budget behind improved average FPS.

## Done Criteria

Finish only when every requested code, Blueprint, content, build, runtime, performance, packaging, and delivery outcome is verified or explicitly blocked by an unavailable capable source or environment. Continue all independently actionable work when one outcome is blocked. Never call code optimized for weak PCs without a reproducible before/after measurement against an accepted target profile.
