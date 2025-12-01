# Tracium
Tracium is a Model Context Protocol (MCP) server designed to expose Linux tracing and debugging capabilities such as eBPF, bpftrace, perf, ftrace, and syscall tracing to LLMs and autonomous agents.

It provides a unified observability interface that enables AI systems to inspect, profile, and debug Linux kernel and user-space behavior through safe, structured MCP tools.

# Architecture
```
        ┌─────────────┐          ┌───────────────────────┐
        │  MCP Client │   MCP    │         Tracium       │
        │ (LLM/Agent) │◀───────▶ │        MCP Server     │
        └─────────────┘          └──────────────┬────────┘
                                                │
                   ┌────────────────────────────┼──────────────────────────┐
                   │                            │                          │
            ┌───────────────┐          ┌──────────────┐           ┌─────────────────┐
            │   bpftrace    │          │     perf     │           │     ftrace      │
            ├───────────────┤          ├──────────────┤           ├─────────────────┤
            │ bpftrace      │          │ perf_events  │           │ tracepoints     │
            │ kprobe/uprobe │          │ flamegraphs  │           │ syscall trace   │
            └───────────────┘          └──────────────┘           └─────────────────┘

```

# Contributing
Contributions, Features, issues, and discussions are all welcome.