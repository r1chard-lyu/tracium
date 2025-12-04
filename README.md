# Systracesuite
Systracesuite is a MCP server designed to expose Linux tracing and debugging capabilities such as eBPF, bpftrace, perf, ftrace, and syscall tracing to LLMs and autonomous agents.

It provides a unified observability interface that enables AI systems to inspect, profile, and debug Linux kernel and user-space behavior through safe, structured MCP tools.

# Architecture
This project contains a simple implementation of a MCP server that communicates over STDIO using JSON-RPC.

![Architecture](assets/architecture.png)


## Files

- `mcp_server/main.py`: The main server executable.
- `mcp_server/tools`: Contains Bpftrace tools synchronized with
    the upstream repository.
    https://github.com/bpftrace/bpftrace/tree/master/tools
- `requirements.txt`: Contains the required Python packages.
- `setup.sh`: Setup systracesuite's whitelisted tools so they can run with passwordless sudo. The MCP Server cannot trigger the Gemini CLI interactive shell to prompt the user for privilege escalation.

## Installation

This server relies on the `fastmcp` library. Install all dependencies using pip and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage
Quick start

1. Clone the repository and change into the project directory:
    ```bash
    git clone git@github.com:r1chard-lyu/systracesuite.git
    cd systracesuite
    ```

2. Install Python dependencies:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3. Allow passwordless sudo for bpftrace so the server can run tools without interactive prompts. Note: use only in development — do not enable in production.
    ```bash
    sudo ./setup.sh
    ```

4. Register systracesuite as an MCP server with your Gemini CLI. Replace `<ABS_PATH_TO_SYSTRACESUITE>` with the absolute path to this repository on your machine:
    ```bash
    gemini mcp add systracesuite \
        --scope user \
        uv run --with fastmcp \
        fastmcp run <ABS_PATH_TO_systracesuite>/mcp_server/main.py
    ```

5. Verify the MCP registration:
    ```bash
    gemini mcp list
    ```

    If registration succeeded you should see an entry like:
    ```text
    Configured MCP servers:

    ✓ systracesuite: uv run --with fastmcp fastmcp run <ABS_PATH_TO_systracesuite>/mcp_server/main.py (stdio) - Connected
    ```

# Contributing
Contributions, features, issues, and discussions are all welcome.