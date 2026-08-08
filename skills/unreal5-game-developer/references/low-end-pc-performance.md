# Low-End PC Performance

Use this reference to turn "runs on weak PCs" into a measurable Unreal Engine 5 acceptance contract. Re-check official documentation for the project's exact engine version before changing version-sensitive settings.

## Evidence Priority

Prefer, in order:

1. measurements from the minimum supported PC;
2. measurements from a documented conservative proxy with comparable CPU, GPU, RAM, VRAM, storage, resolution, and drivers;
3. current project budgets and prior traces from the same representative scenario;
4. official Unreal Engine documentation;
5. hypotheses that still require measurement.

Editor FPS, a developer's workstation, code inspection, asset counts, or a single average-FPS number do not prove low-end readiness.

## Target Profile

Materialize these fields before accepting a performance claim:

- CPU, GPU, RAM, VRAM, storage type, OS, driver;
- screen resolution, window mode, upscaler, screen percentage;
- scalability preset and project-specific overrides;
- build configuration and exact commit;
- representative map, route, camera, player count, AI count, effects load, and test duration;
- FPS target and frame-time budget;
- maximum game-thread, render-thread, GPU, RAM, VRAM, loading, and hitch values;
- allowed quality or density fallbacks.

If a field is unknown, keep it `pending` or explicitly `candidate`; do not silently substitute the development machine.

## Measurement Ladder

1. Reproduce the target scenario in a packaged Development or Test build when practical.
2. Warm up caches and streaming consistently.
3. Use `stat unit` to identify whether Game, Draw, or GPU is the current limiter.
4. Capture Unreal Insights for CPU scheduling, tasks, asset loading, and hitches when required.
5. Use `stat gpu` or GPU Visualizer for render-pass cost.
6. Use memory reports, Low-Level Memory Tracker, platform tools, or project-established capture methods for RAM and VRAM.
7. Measure loading and traversal hitches, not only steady-state frames.
8. Repeat the same capture after one targeted change.
9. Compare correctness, frame-time distribution, tail latency, memory, loading, and visual impact.

Keep raw trace or report paths when the repository's evidence policy allows them. Otherwise record a reproducible command and summarized measurements without committing machine-private data.

## CPU And Gameplay Review

Inspect measured hot paths for:

- always-enabled Actor or component Tick;
- work repeated for inactive, hidden, distant, or irrelevant objects;
- broad world searches or repeated component discovery;
- excessive Blueprint-to-C++ boundary calls in hot loops;
- allocations, temporary strings, container growth, or logging per frame;
- unbounded loops, fan-out events, AI perception, pathfinding, EQS, or Behavior Tree services;
- high-frequency spawn/destroy, garbage collection pressure, and UObject count;
- unnecessary collision pairs, complex traces, substepping, skeletal bodies, or destruction;
- over-replication, overly frequent RPCs, or unchanged properties sent repeatedly;
- blocking I/O, save, asset, network, generation, or decompression work on the game thread.

Do not replace a measured problem with a more complex system unless the repeated capture improves the accepted budget.

## GPU And Content Review

Inspect:

- screen percentage and anti-aliasing/upscaling cost;
- dynamic light and shadow count, range, overlap, and resolution;
- Lumen, Nanite, Virtual Shadow Maps, reflections, translucency, post-processing, fog, particles, decals, and overdraw;
- material instructions, texture sizes, sampler use, shader permutations, and PSO hitches;
- skeletal meshes, morph targets, cloth, groom, animation update rate, and skinning;
- foliage density, view distance, HLOD, occlusion, world partition, and streaming boundaries;
- draw calls, primitive/component count, instancing, LODs, and impostors;
- render targets, UI redraw, scene captures, and cameras.

Provide a coherent Low preset. Test feature fallbacks in motion and gameplay; disabling a renderer feature is not acceptable if it breaks navigation, readability, combat feedback, or the core fantasy.

## Asset Loading And Memory

- Use hard references only when the dependency must be resident with the owner.
- Use `TSoftObjectPtr` or `TSoftClassPtr` for optional or deferred content and load asynchronously when latency is acceptable.
- Treat blocking asset loads as hitch risks.
- Define load ownership, preload window, cancellation, failure behavior, and unload lifecycle.
- Verify that caches and pools have bounded memory and a demonstrated reuse benefit.
- Check peak memory during map transition, streaming, combat spikes, and return-to-menu flows.

## Useful Official Documentation

- Performance profiling overview: https://dev.epicgames.com/documentation/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine
- Unreal Insights: https://dev.epicgames.com/documentation/unreal-engine/unreal-insights-in-unreal-engine
- Stat commands: https://dev.epicgames.com/documentation/unreal-engine/stat-commands-in-unreal-engine
- Scalability reference: https://dev.epicgames.com/documentation/unreal-engine/scalability-reference-for-unreal-engine
- Testing and optimizing content: https://dev.epicgames.com/documentation/unreal-engine/testing-and-optimizing-your-content
- Object pointers and soft references: https://dev.epicgames.com/documentation/unreal-engine/object-pointers-in-unreal-engine

## Acceptance Report

Report:

- target and proxy status;
- exact build and scenario;
- baseline and candidate measurements;
- identified bottleneck and changed files or assets;
- correctness and visual regression result;
- passed and failed budgets;
- variance, caveats, and remaining untested scenarios.

Verdict is `verified` only when the accepted low-end target or approved proxy satisfies every required budget in the representative build. Otherwise report `candidate`, `failed`, or `externally blocked` with the exact missing evidence.
