#!/bin/bash
set -euo pipefail

# This script creates a sudoers.d entry to allow the current user
# to run bpftrace with sudo without a password.

SUDOERS_DIR="/etc/sudoers.d"

# Use whoami to get current user as requested
CURRENT_USER="${SUDO_USER:-$(whoami)}"

# If you run this script with sudo and actually want the original user,
# you can use this instead:
# CURRENT_USER="${SUDO_USER:-$(whoami)}"

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Error: please run this script as root, for example:"
    echo "  sudo $0"
    exit 1
fi

# Find bpftrace path
BPFTRACE_PATH="$(command -v bpftrace || true)"
if [ -z "$BPFTRACE_PATH" ]; then
    echo "Error: bpftrace not found in PATH."
    exit 1
fi

SUDOERS_FILE="${SUDOERS_DIR}/tracium_allow_tools"

# Sudoers rule line
RULE="${CURRENT_USER} ALL=(root) NOPASSWD: ${BPFTRACE_PATH}"

echo "Creating sudoers file: ${SUDOERS_FILE}"
echo "${RULE}" > "${SUDOERS_FILE}"

# Correct permission for sudoers.d files
chmod 440 "${SUDOERS_FILE}"

# Validate with visudo
if visudo -cf "${SUDOERS_FILE}"; then
    echo "Sudoers file is valid."
    echo "Rule added:"
    echo "  ${RULE}"
else
    echo "visudo reported an error. Removing file."
    rm -f "${SUDOERS_FILE}"
    exit 1
fi