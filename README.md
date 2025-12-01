# Tracium
Tracium is a Model Context Protocol (MCP) server designed to expose Linux tracing and debugging capabilities such as eBPF, bpftrace, perf, ftrace, and syscall tracing to LLMs and autonomous agents.

It provides a unified observability interface that enables AI systems to inspect, profile, and debug Linux kernel and user-space behavior through safe, structured MCP tools.

# Architecture
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
            │ bpftrace      │          │ perf_events  │          │ tracepoints     │
            │ kprobe/uprobe │          │ flamegraphs  │           │ syscall trace   │
            └───────────────┘          └──────────────┘           └─────────────────┘

# Contributing
Contributions, Features, issues, and discussions are all welcome.

# Python MCP Server (via stdio)

This project contains a simple implementation of a "fastmcp" style server that communicates over standard input (stdin) and standard output (stdout) using JSON-RPC.

## Files

- `mcp_server/main.py`: The main server executable.
- `requirements.txt`: Contains the required Python packages.

## Installation

This server relies on the `fastmcp` library. Install all dependencies using pip and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## How to Start

Execute the `main.py` file directly using Python 3.

```bash
python3 mcp_server/main.py
```

After the server starts, it will wait for JSON-RPC commands from standard input.

## How to Communicate
All communication must follow the JSON-RPC 2.0 specification. Each JSON object must end with a newline character `\n`.

### Initialization
Before you can call any tools, you must first send an `initialize` request to the server.

```json
{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "1.0", "capabilities": {}, "clientInfo": {"name": "Terminal Client", "version": "1.0.0"}}, "id": 0}
```

### Tool Call Format
To execute a command, you must use the `tools/call` method. The tool's name is specified in `params.name`, and its arguments are passed in `params.arguments`.

```json
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "<tool_name>", "arguments": { ... }}, "id": 1}
```

### Response Format

The server will return a JSON-RPC 2.0 response object.

```json
// Success
{"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": "<tool_output>"}], "isError": false}}
```

## Available Tools

### 1. status

Checks if the server is running.

**Command:**
```json
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "status", "arguments": {}}, "id": 1}
```

**Successful Response Snippet:**
```json
{"result": {"content": [{"type": "text", "text": "Server is running and ready."}]}}
```

### 2. echo

The server will echo back any content you send in the `arguments`. This is useful for testing the connection.

**Command:**
```json
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "echo", "arguments": {"message": "hello world", "value": 123}}, "id": 2}
```

**Successful Response Snippet:**
```json
{"result": {"content": [{"type": "text", "text": "{\"message\": \"hello world\", \"value\": 123}"}]}}
```

### 3. stop

Shuts down the server.

**Command:**
```json
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "stop", "arguments": {}}, "id": 3}
```

**Successful Response Snippet:**
```json
{"result": {"content": [{"type": "text", "text": "Server shutting down."}]}}
```
The server will terminate after sending this response.

### 4. top

Executes `top -b -n 1` to get a single snapshot of the current processes.

**Command:**
```json
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "top", "arguments": {}}, "id": 4}
```

**Successful Response Snippet:**
```json
{"result": {"content": [{"type": "text", "text": "<output of the top command>"}]}}
```

### 5. perf

Executes the `perf` tool with the specified arguments. The `arguments` must contain an `args` key with a list of strings.

**Command (Example with `perf stat`):**
```json
{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "perf", "arguments": {"args": ["stat", "-e", "cycles", "sleep", "1"]}}, "id": 5}
```

**Successful Response Snippet:**
```json
{"result": {"content": [{"type": "text", "text": "<output of the perf command>"}]}}
```
