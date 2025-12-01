from fastmcp import FastMCP
import subprocess
import os
import getpass
import shlex

# Initialize the server
mcp = FastMCP(name="Tracium MCP Server")

# --- Helper Functions (Placed here as internal functions, not exposed as tools) ---

def password_prompt() -> str:
    """
    Prompts the user to input their password via the shell/terminal.
    This function uses getpass to securely capture the password without echoing it.
    """
    # Use getpass to securely prompt for the password.
    # The prompt appears in the shell where the FastMCP server is running.
    return getpass.getpass(prompt='[sudo] password for user: ')

# --- Core Tools ---

@mcp.tool
def status():
    """Checks if the server is running."""
    return "Server is running and ready."

@mcp.tool
def echo(message: str = None, value: int = None):
    """The server will echo back any content you send in the payload. This is useful for testing the connection."""
    payload = {}
    if message is not None:
        payload["message"] = message
    if value is not None:
        payload["value"] = value
    return payload

@mcp.tool
def stop():
    """Shuts down the server."""
    # In a real application, you might want a more graceful shutdown
    return "Server shutting down."

@mcp.tool
def top():
    """Executes `top -b -n 1` to get a single snapshot of the current processes."""
    try:
        # Executes top -b -n 1 to get a batch mode snapshot
        result = subprocess.run(["top", "-b", "-n", "1"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing top command: {e.stderr}"

@mcp.tool
def perf(args: list[str]):
    """Executes the `perf` tool with the specified arguments."""
    try:
        full_command = ["perf"] + args
        # Executes the perf command
        result = subprocess.run(full_command, capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError:
        return "Error: 'perf' command not found. Please ensure perf is installed and in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error executing perf command: {e.stderr}"

# --- bpftrace Tools ---

@mcp.tool
def bpftrace_version():
    """Gets the installed bpftrace version."""
    try:
        # bpftrace --version may print to stderr and exit with a non-zero code,
        # so we don't use check=True.
        result = subprocess.run(["bpftrace", "--version"], capture_output=True, text=True)
        # The output is expected on stderr.
        if result.stderr:
            return result.stderr
        # Provide stdout as a fallback.
        return result.stdout
    except FileNotFoundError:
        return "Error: 'bpftrace' command not found. Please ensure bpftrace is installed and in your PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

@mcp.tool
def sudo_shell_exec(password: str, command_args: list[str]):
    """
    Receives the password from the client and executes the specified sudo command.
    """
    
    if not password:
        return "Error: Password was not provided for sudo execution."
    
    full_command = ["sudo", "-S"] + command_args
    
    try:
        result = subprocess.run(
            full_command,
            input=password,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8' 
        )
        return result.stdout
    except FileNotFoundError:
        return f"Error: Command '{command_args[0]}' was not found. Please ensure it is installed."
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip()
        if "Sorry, try again." in error_output:
             return "Error: Incorrect password provided. Execution failed."
        return f"Error while executing sudo command:\n{error_output}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool
def bpftrace_list():
    """
    Executes `sudo bpftrace -l`. It initiates a two-step process:
    1. Returns a 'PASSWORD_REQUIRED' state to the client with the prompt.
    2. The client must then call the 'execute_sudo_command' tool with the password.
    
    This is now a NON-BLOCKING operation on the server side.
    """
    
    return {
        "status": "PASSWORD_REQUIRED",
        "prompt": "[sudo] password for user:",
        "next_tool": "sudo_shell_exec",
        "command_to_execute": ["bpftrace", "-l"]
    }
# --- Main Execution ---

if __name__ == "__main__":
    mcp.run()