<!--
source_url: https://github.com/RHEcosystemAppEng/mcp-validation
title: mcp-validation (Red Hat Ecosystem MCP validation tool)
fetched: 2026-07-05
source_type: github
rights_status: open
dimension: testing
license: MIT. note: combined README.md + USER_GUIDE.md + prompts/ + sample output report
-->

# mcp-validation (Red Hat Ecosystem MCP validation tool)

Combined prose documentation from the mcp-validation repository (github.com/RHEcosystemAppEng/mcp-validation). LICENSE: MIT -> open. Source code omitted.


---

## From `README.md` — mcp-validation overview

# MCP Validation Tool

A comprehensive validation tool for [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers to ensure protocol compliance, security, and proper implementation.

## Goal

This tool validates MCP servers by:

- **Protocol Compliance**: Tests the complete MCP initialization handshake
- **Standard Conformance**: Validates JSON-RPC 2.0 format and required fields  
- **Capability Testing**: Verifies advertised capabilities (resources, tools, prompts)
- **Security Analysis**: Integrates with [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) for vulnerability detection
- **Registry Validation**: Ensures servers match their registry schema definitions
- **Detailed Reporting**: Exports comprehensive JSON reports with validation checklists
- **Automated Testing**: Provides programmatic validation for CI/CD pipelines

## Features

- ✅ **Protocol Validation**: Complete MCP handshake and capability testing
- ✅ **Multi-Transport Support**: stdio, HTTP, and SSE transports with full OAuth 2.0 support
- ✅ **OAuth 2.0 Authentication**: Full OAuth 2.0 Dynamic Client Registration (RFC 7591)
- ✅ **Automatic Browser Opening**: Seamless OAuth authentication flow
- ✅ **Security Scanning**: Integrated mcp-scan vulnerability analysis
- ✅ **JSON Reports**: Comprehensive validation reports with linked security scans
- ✅ **Step-by-Step Logging**: Real-time validation progress with detailed feedback
- ✅ **Tool Discovery**: Lists all available tools, prompts, and resources
- ✅ **Environment Variables**: Configurable environment setup
- ✅ **Timeout Handling**: Configurable validation timeouts
- ✅ **Exit Codes**: Proper exit codes for automation
- ✅ **Verbose Mode**: Optional detailed output

## Installation

```bash
# Clone and install
git clone https://github.com/modelcontextprotocol/mcp-validation
cd mcp-validation
uv sync
```

Or install directly:
```bash
pip install mcp-validation
```

## Usage

### Basic Validation

```bash
# Validate a Python MCP server (stdio transport)
mcp-validate -- python server.py

# Validate a Node.js MCP server (stdio transport)
mcp-validate -- node server.js

# Validate npx packages (use -- separator for flags)
mcp-validate -- npx -y kubernetes-mcp-server@latest

# Validate servers via container runtime (podman/docker)
mcp-validate -- podman run -i --rm hashicorp/terraform-mcp-server
```

### HTTP Transport Validation

```bash
# Validate HTTP MCP servers with OAuth 2.0 Dynamic Client Registration
mcp-validate --transport http --endpoint https://example.com/api/mcp

# With pre-registered OAuth credentials
mcp-validate --transport http --endpoint https://gitlab.com/api/v4/mcp \
  --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET

# With personal access token
mcp-validate --transport http --endpoint https://api.example.com/mcp \
  --auth-token YOUR_ACCESS_TOKEN

# Local HTTP server
mcp-validate --transport http --endpoint http://localhost:3000/mcp
```

### SSE Transport Validation

```bash
# Validate SSE endpoints with Bearer token authentication
mcp-validate --transport sse --endpoint https://mcp.example.com/sse --auth-token YOUR_TOKEN

# SSE endpoint without authentication
mcp-validate --transport sse --endpoint https://public.mcp.example.com/sse
```

### Authentication

The tool supports different authentication methods depending on the transport:

**SSE Transport**: Simple Bearer token authentication
**HTTP Transport**: Full OAuth 2.0 support with three authentication methods:

#### 1. Dynamic Client Registration (Automatic)
```bash
# No credentials needed - automatic registration with the OAuth server
mcp-validate --transport http --endpoint https://gitlab.com/api/v4/mcp

# The tool will:
# - Automatically register a new OAuth client with the server
# - Open your browser for authorization
# - Handle the OAuth callback automatically
# - Continue with MCP validation
```

#### 2. Pre-registered OAuth Application
```bash
# Use your existing OAuth application credentials
mcp-validate --transport http --endpoint https://api.example.com/mcp \
  --client-id "your_oauth_app_client_id" \
  --client-secret "your_oauth_app_secret"

# For GitLab, create an application at:
# https://gitlab.com/-/profile/applications
# - Scopes: api, read_user
# - Redirect URI: http://localhost:3333/callback
```

#### 3. Personal Access Token
```bash
# Use a personal access token for direct authentication
mcp-validate --transport http --endpoint https://api.example.com/mcp \
  --auth-token "your_personal_access_token"

# Note: Token must have appropriate scopes for MCP access
```

**Authentication Process:**
- **Browser opens automatically** for OAuth flows
- **Callback server** starts on localhost:3333 to handle OAuth redirects
- **Secure token exchange** using PKCE (Proof Key for Code Exchange)
- **5-minute timeout** for user authentication

### With Profiles and Advanced Features

```bash
# Use specific validation profile
mcp-validate --profile security_focused -- python server.py

# List available profiles and validators
mcp-validate --list-profiles
mcp-validate --list-validators

# Custom configuration with selective validators
mcp-validate --config ./custom-config.json --enable ping --disable security -- node server.js

# Repository validation for OSS compliance
mcp-validate --repo-url https://github.com/user/mcp-server -- python server.py
```

### With Environment Variables

```bash
# IoTDB MCP server example
mcp-validate \
  --env IOTDB_HOST=127.0.0.1 \
  --env IOTDB_PORT=6667 \
  --env IOTDB_USER=root \
  --env IOTDB_PASSWORD=root \
  python src/iotdb_mcp_server/server.py
```

### JSON Report Generation

```bash
# Generate comprehensive JSON report
mcp-validate --json-report validation-report.json python server.py

# With security analysis and custom timeout
mcp-validate \
  --timeout 60 \
  --json-report full-report.json \
  --env API_KEY=secret \
  -- npx -y some-mcp-server@latest
```

### Advanced Debugging and Analysis

```bash
# Enable detailed debug output for troubleshooting
mcp-validate --debug -- python server.py

# Skip mcp-scan for faster validation
mcp-validate --skip-mcp-scan python server.py

# Full validation with security scan and detailed reporting
mcp-validate --debug --timeout 120 --json-report report.json python server.py
```

### Programmatic Usage

```python
import asyncio
from mcp_validation import validate_mcp_server_command

async def test_server():
    result = await validate_mcp_server_command(
        command_args=["python", "server.py"],
        env_vars={"API_KEY": "secret"},
        timeout=30.0,
        use_mcp_scan=True
    )
    
    if result.is_valid:
        print(f"✓ Server is MCP compliant!")
        print(f"Tools: {result.tools}")
        print(f"Capabilities: {list(result.capabilities.keys())}")
        if result.mcp_scan_results:
            print(f"Security scan: {result.mcp_scan_file}")
    else:
        print("✗ Validation failed:")
        for error in result.errors:
            print(f"  - {error}")

asyncio.run(test_server())
```

## CLI Options

| Option | Description | Example |
|--------|-------------|---------|
| `command` | Command and arguments to run the MCP server (stdio) | `-- python server.py` |
| `--transport TYPE` | Transport type: `stdio` (default), `http`, or `sse` | `--transport sse` |
| `--endpoint URL` | HTTP/SSE endpoint URL (required for http/sse transports) | `--endpoint https://api.example.com/mcp` |
| `--auth-token TOKEN` | OAuth Bearer token for HTTP/SSE authentication | `--auth-token your_token` |
| `--client-id ID` | OAuth client ID for pre-registered applications | `--client-id your_client_id` |
| `--client-secret SECRET` | OAuth client secret (used with --client-id) | `--client-secret your_secret` |
| `--config FILE` | Configuration file path | `--config ./my-config.json` |
| `--profile NAME` | Validation profile to use | `--profile security_focused` |
| `--env KEY=VALUE` | Set environment variables (repeatable) | `--env HOST=localhost` |
| `--enable VALIDATOR` | Enable specific validator | `--enable ping` |
| `--disable VALIDATOR` | Disable specific validator | `--disable security` |
| `--list-profiles` | List available validation profiles | `--list-profiles` |
| `--list-validators` | List available validators | `--list-validators` |
| `--timeout SECONDS` | Global timeout override in seconds | `--timeout 60` |
| `--verbose` | Show detailed output including warnings | `--verbose` |
| `--debug` | Enable detailed debug output with execution tracking | `--debug` |
| `--skip-mcp-scan` | Skip mcp-scan security analysis | `--skip-mcp-scan` |
| `--json-report FILE` | Export detailed JSON report to file | `--json-report report.json` |
| `--repo-url URL` | Repository URL to validate for OSS compliance | `--repo-url https://github.com/user/repo` |
| `--runtime-command CMD` | Runtime command to validate (auto-detected if not specified) | `--runtime-command uv` |

## Validation Process

The tool performs these validation steps:

1. **Process Execution**: Starts the server with provided arguments and environment
2. **Initialize Handshake**: Sends MCP `initialize` request with protocol version
3. **Protocol Compliance**: Validates JSON-RPC 2.0 format and required response fields
4. **Capability Discovery**: Tests advertised capabilities (resources, tools, prompts)
5. **Security Analysis**: Runs mcp-scan vulnerability detection (optional)
6. **Report Generation**: Creates detailed JSON reports with validation checklist

## Output Format

```
Testing MCP server: npx -y kubernetes-mcp-server@latest

🔄 Step 1: Sending initialize request...
✅ Initialize request successful
🔄 Step 2: Sending initialized notification...
✅ Initialized notification sent
🔄 Step 3: Testing capabilities...
  🔄 Testing tools...
    ✅ Found 18 tools
    📋 Names: configuration_view, events_list, helm_install, helm_list, helm_uninstall (and 13 more)
  🔄 Testing prompts...
    ✅ Found 0 prompts
  🔄 Testing resources...
    ✅ Found 0 resources
✅ Capability testing complete
🔄 Step 4: Running mcp-scan security analysis...
    🔍 Running: uvx mcp-scan@latest --json...
    📊 Scanned 18 tools
    ✅ No security issues detected
    💾 Scan results saved to: mcp-scan-results_20250730_120203.json
✅ mcp-scan analysis complete

✓ Valid: True
⏱ Execution time: 10.49s
🖥 Server: kubernetes-mcp-server vv0.0.46
🔧 Capabilities: logging, prompts, resources, tools
🔨 Tools (18): configuration_view, events_list, helm_install, helm_list, helm_uninstall, namespaces_list, pods_delete, pods_exec, pods_get, pods_list, pods_list_in_namespace, pods_log, pods_run, pods_top, resources_create_or_update, resources_delete, resources_get, resources_list
🔍 Security Scan: No issues found in 18 tools
📋 JSON report saved to: validation-report.json
```

## JSON Report Structure

The `--json-report` option generates comprehensive validation reports:

```json
{
  "report_metadata": {
    "generated_at": "2025-07-30T12:02:03.456789",
    "validator_version": "0.1.0",
    "command": "npx -y kubernetes-mcp-server@latest",
    "environment_variables": {}
  },
  "validation_summary": {
    "is_valid": true,
    "execution_time_seconds": 10.49,
    "total_errors": 0,
    "total_warnings": 0
  },
  "validation_checklist": {
    "protocol_validation": {
      "initialize_request": {"status": "passed", "details": "..."},
      "initialize_response": {"status": "passed", "details": "..."},
      "protocol_version": {"status": "passed", "details": "..."}
    },
    "capability_testing": {
      "tools_capability": {"status": "passed", "details": "..."},
      "resources_capability": {"status": "skipped", "details": "..."}
    },
    "security_analysis": {
      "mcp_scan_execution": {"status": "passed", "details": "..."}
    }
  },
  "server_information": {
    "server_info": {"name": "kubernetes-mcp-server", "version": "v0.0.46"},
    "capabilities": {"logging": {}, "tools": {"listChanged": true}},
    "discovered_items": {
      "tools": {"count": 18, "names": ["configuration_view", "..."]}
    }
  },
  "security_analysis": {
    "mcp_scan_executed": true,
    "mcp_scan_file": "mcp-scan-results_20250730_120203.json",
    "summary": {
      "tools_scanned": 18,
      "vulnerabilities_found": 0,
      "vulnerability_types": [],
      "risk_levels": []
    }
  },
  "issues": {
    "errors": [],
    "warnings": []
  }
}
```

## Exit Codes

- `0`: Server is MCP compliant
- `1`: Validation failed or server is non-compliant

## MCP Registry Validation

For servers listed in the [MCP Registry](https://github.com/modelcontextprotocol/registry), this tool can validate:

- Package installation requirements
- Environment variable specifications
- Argument format compliance
- Protocol implementation correctness

## Development

### Prerequisites

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and development workflows.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/modelcontextprotocol/mcp-validation
cd mcp-validation
```

### Quick Start with Makefile

For convenience, this project includes a Makefile with common development tasks:

```bash
# Setup development environment
make install

# Run the full pre-commit workflow (format, lint, test)
make pre-commit

# Run tests
make test

# Format code
make format

# See all available commands
make help
```

### Manual Setup

```bash
# Install all dependencies including dev extras
uv sync --extra dev

# Alternatively, install the package in development mode
uv pip install -e ".[dev]"
```

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install dependencies with dev extras |
| `make dev-setup` | Complete development environment setup |
| `make test` | Run all tests (excluding partner repos) |
| `make test-cov` | Run tests with coverage report |
| `make test-fast` | Run tests with fail-fast (-x flag) |
| `make debug-test` | Run tests with debug output and registry logging |
| `make format` | Format code with Black |
| `make check` | Check formatting without making changes |
| `make lint` | Check code with Ruff (no fixes) |
| `make lint-fix` | Check and fix code issues with Ruff |
| `make pre-commit` | Run full pre-commit workflow (format, lint, test) |
| `make ci` | Run CI-like checks (no automatic fixes) |
| `make clean` | Clean up cache and temporary files |

### Manual Testing Commands

```bash
# Run all tests
make test
# OR manually:
uv run --extra dev pytest tests/ -v

# Run tests with coverage
make test-cov
# OR manually:
uv run --extra dev pytest tests/ --cov=mcp_validation --cov-report=term-missing

# Run specific test file
uv run --extra dev pytest tests/test_enhanced_registry.py -v

# Run tests and stop on first failure
make test-fast
# OR manually:
uv run --extra dev pytest tests/ -x
```

### Code Formatting and Linting

```bash
# Format code with Black
make format
# OR manually:
uv run --extra dev black mcp_validation/

# Check code formatting (without making changes)
make check
# OR manually:
uv run --extra dev black --check mcp_validation/

# Lint with Ruff (with fixes)
make lint-fix
# OR manually:
uv run --extra dev ruff check --fix mcp_validation/

# Lint with Ruff (check only)
make lint
# OR manually:
uv run --extra dev ruff check mcp_validation/

# Type checking with mypy
uv run --extra dev mypy mcp_validation/
```

### Workflows

```bash
# Pre-commit workflow (format, lint, test)
make pre-commit

# CI-style checks (no automatic fixes)
make ci

# Manual pre-commit workflow
uv run --extra dev black mcp_validation/ && \
uv run --extra dev ruff check --fix mcp_validation/ && \
uv run --extra dev pytest tests/ -v
```

### Development Guidelines

1. **Testing**: All new features must include tests
2. **Code Style**: Use Black for formatting and Ruff for linting
3. **Type Hints**: Add type hints for all public APIs
4. **Documentation**: Update README and docstrings for new features

### Test Configuration

The project uses pytest with the following configuration in `pyproject.toml`:

- **Test Discovery**: Looks for tests in the `tests/` directory
- **Async Support**: Configured for async/await testing
- **Exclusions**: Automatically excludes partner repositories and build directories
- **Markers**: Strict marker checking enabled

### Debugging Tests

```bash
# Run tests with debug output and registry logging
make debug-test

# Run tests with verbose output and debug information
uv run --extra dev pytest -v -s

# Run specific test with debugging
uv run --extra dev pytest tests/test_enhanced_registry.py::test_enhanced_registry_validator -v -s

# Run registry tests with debug output
mcp-validate --debug -- npm test
```

### Debugging MCP Validation

The tool provides comprehensive debug output to track server execution progress:

```bash
# Enable debug output for detailed execution tracking
mcp-validate --debug -- python server.py
```

**Debug output includes:**
- **Execution Context**: Working directory, Python version, platform, user, shell
- **Command Details**: Full command, arguments, executable path
- **Environment Variables**: Custom variables (with sensitive value masking)
- **Process Information**: PID, process lifecycle events
- **Validator Progress**: Individual validator execution with timing and results
- **Validation Summary**: Overall statistics and execution time

**Example debug output:**
```
[10:19:29.872] [EXEC-INFO] 🚀 Starting MCP Server Process
[10:19:29.872] [EXEC-INFO] 📁 Working Directory: /path/to/project
[10:19:29.872] [EXEC-INFO] 🐍 Python: /usr/bin/python3 (v3.11.0)
[10:19:29.872] [EXEC-INFO] 🔧 Command: npx @dynatrace-oss/dynatrace-mcp-server
[10:19:29.872] [EXEC-INFO] 🌍 Environment Variables:
[10:19:29.872] [EXEC-INFO]    API_KEY=ab*****ef
[10:19:29.877] [VALIDATOR-INFO] 🔍 [registry] STARTING: (1/6)
[10:19:30.727] [VALIDATOR-INFO] 🔍 [registry] PASSED: Time: 0.85s
```

## Examples

### Validate Registry Server

```bash
# Apache IoTDB MCP Server from registry
mcp-validate \
  --env IOTDB_HOST=127.0.0.1 \
  --env IOTDB_PORT=6667 \
  --env IOTDB_USER=root \
  --env IOTDB_PASSWORD=root \
  --env IOTDB_DATABASE=test \
  --env IOTDB_SQL_DIALECT=table \
  python src/iotdb_mcp_server/server.py
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Validate MCP Server
  run: |
    mcp-validate --json-report validation-report.json python server.py
  env:
    DATABASE_URL: sqlite:///test.db

- name: Upload validation report
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: mcp-validation-report
    path: |
      validation-report.json
      mcp-scan-results_*.json
```

### Security Analysis

The tool integrates with [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) for comprehensive security analysis:

- **Automatic Detection**: Checks for `uvx` or `mcp-scan` availability
- **Vulnerability Scanning**: Analyzes tools for potential security issues
- **Separate Reports**: Security results saved to timestamped JSON files
- **Linked Reports**: Main validation report references security scan files
- **Skip Option**: Use `--skip-mcp-scan` for faster validation without security analysis

## Contributing

Contributions are welcome! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Related Projects

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Registry](https://github.com/modelcontextprotocol/registry)
- [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) - Security vulnerability scanner for MCP servers
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)


---

## From `USER_GUIDE.md` — User guide

# MCP Validation Framework - User Guide

A modern, plugin-based validation framework for MCP (Model Context Protocol) servers. Provides comprehensive testing of protocol compliance, capabilities, and security.

## Features

### 🏗️ Modular Architecture
- **Plugin-based validators**: Each validation type is a separate, configurable plugin
- **Flexible configuration**: Multiple validation profiles with customizable parameters
- **Dependency management**: Validators can depend on each other and run in optimal order
- **Transport abstraction**: Clean separation between communication and validation logic

### ⚙️ Configuration System
- **Validation profiles**: Pre-configured validation suites for different use cases
- **Runtime configuration**: Override settings via CLI, environment, or config files
- **Extensible validators**: Easy to add custom validation logic

### 📊 Enhanced Reporting
- **Structured results**: Clear separation of different validation aspects
- **Multiple output formats**: Console and JSON reporting with detailed breakdown
- **Progress tracking**: Real-time feedback during validation execution

## Quick Start

### Basic Usage

```bash
# Validate an MCP server
mcp-validate -- npx @dynatrace-oss/dynatrace-mcp-server

# With environment variables
mcp-validate --env DT_ENVIRONMENT=https://example.apps.dynatrace.com -- npx server

# With custom timeout
mcp-validate --timeout 60 -- python my_server.py
```

### Validation Profiles

```bash
# Use a specific validation profile
mcp-validate --profile basic -- python server.py
mcp-validate --profile security_focused -- node server.js
mcp-validate --profile comprehensive -- ./my-server
```

### Validator Control

```bash
# Enable/disable specific validators
mcp-validate --enable ping --disable security -- python server.py
mcp-validate --disable errors -- ./server  # Skip error compliance testing
```

### Configuration Files

```bash
# Use a custom configuration file
mcp-validate --config ./my-validation-config.json -- python server.py

# Set config via environment
export MCP_VALIDATION_CONFIG=./config.json
export MCP_VALIDATION_PROFILE=development
mcp-validate -- python server.py
```

### Information Commands

```bash
# List available profiles
mcp-validate --list-profiles

# List available validators
mcp-validate --list-validators
```

## Built-in Validation Profiles

### `basic`
- **Purpose**: Quick protocol compliance check
- **Validators**: protocol, capabilities
- **Use case**: Development and CI/CD pipelines

### `comprehensive` (default)
- **Purpose**: Complete validation with all features
- **Validators**: protocol, capabilities, ping, errors, security
- **Use case**: Thorough testing before release

### `security_focused`
- **Purpose**: Security-first validation
- **Validators**: protocol, errors (strict), security (required)
- **Use case**: Security audits and compliance

### `development`
- **Purpose**: Developer-friendly validation
- **Validators**: protocol, capabilities, ping, errors
- **Features**: Detailed feedback, continues on failure
- **Use case**: Local development and debugging

## Built-in Validators

### `protocol` (Required)
- **Purpose**: Basic MCP protocol compliance
- **Tests**: Initialize handshake, protocol version, server info
- **Dependencies**: None (foundation validator)

### `capabilities`
- **Purpose**: Test advertised server capabilities
- **Tests**: tools/list, prompts/list, resources/list
- **Dependencies**: protocol

### `ping`
- **Purpose**: Test optional ping functionality
- **Tests**: Ping request/response, response time measurement
- **Dependencies**: protocol

### `errors`
- **Purpose**: JSON-RPC error compliance testing
- **Tests**: Invalid method handling, malformed request handling
- **Dependencies**: protocol

### `security`
- **Purpose**: Security analysis using mcp-scan
- **Tests**: Vulnerability scanning, tool analysis
- **Dependencies**: protocol

## Configuration

### Configuration File Format

Create a `.mcp-validation.json` file:

```json
{
  "active_profile": "custom",
  "profiles": {
    "custom": {
      "description": "My custom validation profile",
      "global_timeout": 30.0,
      "continue_on_failure": true,
      "validators": {
        "protocol": {
          "enabled": true,
          "required": true
        },
        "ping": {
          "enabled": true,
          "required": false,
          "parameters": {
            "max_response_time_ms": 500
          }
        },
        "security": {
          "enabled": true,
          "required": false,
          "parameters": {
            "run_mcp_scan": true,
            "vulnerability_threshold": "medium",
            "save_scan_results": true
          }
        }
      }
    }
  }
}
```

### Environment Variables

```bash
export MCP_VALIDATION_CONFIG=./config.json    # Path to configuration file
export MCP_VALIDATION_PROFILE=development     # Active profile name
```

### Validator Parameters

Each validator supports custom parameters:

#### Protocol Validator
- `strict_version_check`: Enforce exact protocol version match
- `validate_client_info`: Validate client information format

#### Capabilities Validator
- `max_items_to_list`: Limit number of items to retrieve in list operations
- `test_all_capabilities`: Test all advertised capabilities

#### Ping Validator
- `max_response_time_ms`: Maximum acceptable response time

#### Error Validator
- `test_malformed_requests`: Test malformed JSON handling
- `test_invalid_methods`: Test invalid method handling
- `strict_error_codes`: Require exact JSON-RPC error codes

#### Security Validator
- `run_mcp_scan`: Enable mcp-scan analysis
- `vulnerability_threshold`: Minimum severity level to report
- `save_scan_results`: Save detailed scan results to file

## Programmatic API

### Simple Validation

```python
from mcp_validation import validate_server

async def main():
    session = await validate_server(["python", "my_server.py"])
    
    if session.overall_success:
        print("✅ Server is MCP compliant!")
    else:
        print("❌ Validation failed:")
        for error in session.errors:
            print(f"  - {error}")

import asyncio
asyncio.run(main())
```

### Advanced Usage

```python
from mcp_validation import (
    MCPValidationOrchestrator, 
    ConfigurationManager,
    ConsoleReporter,
    JSONReporter
)

async def advanced_validation():
    # Load custom configuration
    config_manager = ConfigurationManager("./config.json")
    config_manager.set_active_profile("development")
    
    # Create orchestrator
    orchestrator = MCPValidationOrchestrator(config_manager)
    
    # Run validation
    session = await orchestrator.validate_server(
        ["python", "server.py"],
        env_vars={"DEBUG": "1"}
    )
    
    # Generate reports
    console_reporter = ConsoleReporter(verbose=True)
    console_reporter.report_session(session)
    
    json_reporter = JSONReporter()
    json_reporter.save_report(session, "report.json", ["python", "server.py"])

asyncio.run(advanced_validation())
```

### Custom Validators

```python
from mcp_validation import BaseValidator, ValidationContext, ValidatorResult
from mcp_validation import MCPValidationOrchestrator, ConfigurationManager

class PerformanceValidator(BaseValidator):
    @property
    def name(self) -> str:
        return "performance"
    
    @property  
    def description(self) -> str:
        return "Test MCP server performance characteristics"
    
    @property
    def dependencies(self) -> List[str]:
        return ["protocol"]
    
    async def validate(self, context: ValidationContext) -> ValidatorResult:
        # Your custom validation logic here
        start_time = time.time()
        
        # Test response times, concurrent requests, etc.
        
        return ValidatorResult(
            validator_name=self.name,
            passed=True,
            errors=[],
            warnings=[],
            data={"response_time": 0.1},
            execution_time=time.time() - start_time
        )

# Register and use
config_manager = ConfigurationManager()
orchestrator = MCPValidationOrchestrator(config_manager)
orchestrator.register_validator(PerformanceValidator)
```

## Examples

See the `examples/` directory for:
- `sample-config.json` - Complete configuration example
- `custom_validator.py` - How to create custom validators
- `validation-config.json` - Advanced configuration scenarios

## Command Line Reference

```bash
mcp-validate [OPTIONS] [--] COMMAND [ARGS...]

Options:
  --config FILE              Configuration file path
  --profile NAME             Validation profile to use
  --env KEY=VALUE            Set environment variable (repeatable)
  --enable VALIDATOR         Enable specific validator
  --disable VALIDATOR        Disable specific validator
  --timeout SECONDS          Global timeout override
  --skip-mcp-scan           Skip mcp-scan security analysis
  --json-report FILENAME     Export JSON report
  --verbose                  Show detailed output
  --list-profiles           List available profiles
  --list-validators         List available validators
  -h, --help                Show help message
```

## Troubleshooting

### Common Issues

1. **Command not found**: Ensure the MCP server command is in your PATH
2. **Timeout errors**: Increase timeout with `--timeout` or in config
3. **Permission issues**: Check environment variables and file permissions
4. **mcp-scan not found**: Install with `uvx install mcp-scan` or disable security validator

### Debug Mode

```bash
# Enable verbose output
mcp-validate --verbose -- python server.py

# Generate detailed JSON report
mcp-validate --json-report debug-report.json -- python server.py
```

### Environment Variables for Debugging

```bash
export MCP_VALIDATION_PROFILE=development  # Use dev-friendly profile
export DEBUG=1                            # Enable debug logging in your server
```


---

## From `prompts/validate.md` — Validation prompt (what is checked)

CONTEXT
You are an expert of the MCP protocol and your main goal is to validate servers defined in an MCP registry.
Registry is provided as a JSON document matching the MCP registry OpenAPI schema.

You can use the the mcp-validate tool according to the provided instructions in the project README file to validate each server.
You are given a list of servers generated using the registry prompt.

REQUEST:
Validate all the servers and generate an aggregated report of the errors and warnings computed by the tool.

PHASE 1: COMMAND DEFINITION
For each server, define the validation tool command using the following rules:
- use 'uv' to run it inside the dedicated venv
- use the '--env' for each environment variable defined in the registry
  - use the default value, if provided, otherwise try to guess a reasonable default according to the variable type.
  - the type is also guessed from the variable name, since there is no indication of the type in the registry schema.
  - IMPORTANT: For server-specific environment variables, follow these patterns:
    * Dynatrace: Use "https://test.apps.dynatrace.com" format (NOT .live.dynatrace.com classic URLs)
    * Database URLs: Use localhost with appropriate ports (Redis: 6379, MySQL: 3306, PostgreSQL: 5432, etc.)
    * API endpoints: Use "https://test.example.com" or similar test domains
    * Usernames: Use "test-user" or "test-username"
    * Passwords/Secrets: Use "test-password", "test-secret", "test-api-key" as appropriate
    * Tokens: Use "test-token" format
  - TRANSPORT PROTOCOL RESTRICTION: Do NOT set environment variables related to non-stdio transport protocols:
    * Do NOT set TRANSPORT_HOST, TRANSPORT_PORT, or HOST/PORT variables for stdio-based MCP servers
    * Do NOT set HTTP/TCP transport variables unless the server explicitly requires non-stdio transport
    * Most containerized MCP servers use stdio transport and don't need HOST/PORT configuration
    * Only set transport-related variables if the server documentation explicitly requires them for non-stdio transport
- use 'podman' as the runtime tool instead of 'docker'
- use '-i --rm' followed by the container name and version
- the values of additional 'package_arguments' are prepended after the container name
- use '--json-report' to generate a report named as the MCP server, with .json suffix, under new a folder named output

Command example:
uv run mcp-validate --json-report terraform-mcp-server.json -- podman run -i --rm quay.io/ecosystem-appeng/mcpserver-importer:0.1.0

PHASE 2: VALIDATION
Run the generated command and extract the relevant data from the generated report.

PHASE 3: REPORT GENERATION:
The aggregataed report includes the following fields for each server:
- Name: same as the JSON input
- Command: the command used to validate with mcp-validate tool
- Status: either Failed or Succeeded
- Errors: the computed number of validation errors
- Warnings: the computed number of validation warnings
- Report: the name of the generated JSON report

CONSTRAINTS:
- In case of error, add an Error_Message field with the brief description of the error
- The generated report is named servers_validation.json, under the output folder
- Generate an additional report in markdown format with a summary table with the validation status and errors/warnings for each server. 
  Include information on the execution timestamp.

REFERENCES:
Registry prompt: prompts/registry.md (from the project root)
Registry JSON document: output/registry.json (from the project root)
MCP protocol: https://modelcontextprotocol.io/specification/2025-06-18
MCP registry OpenAPI schema: https://github.com/modelcontextprotocol/registry/blob/main/docs/server-registry-api/openapi.yaml, 
MCP registry seed file: https://github.com/modelcontextprotocol/registry/blob/main/data/seed.json


---

## From `prompts/registry.md` — Registry validation prompt

CONTEXT:
You are an expert of the MCP protocol and your main goal is to register servers in the MCP registry.
Servers are defined in JSON document including:
- the logical name
- the URL of the code repository
- the URL of the container image
- the MCP transport protocol:
  - one or more of stdio, http, sse (separated by /)
  - N/A if no protocol information is available

REQUEST:
Given the description of the servers according to the provided schema, generate a registry configuration for an
MCP registry, according to the MCP registry OpenAPI schema, for each server in the provided list.

PHASE 1: CLONE SERVER REPO
Clone the server in a temporary folder 'tmp_servers' at the root of the project.

PHASE 2: EXTRACT SERVER METADATA:
Retrieve relevant information from the cloned repository README file to define the server metadata:
- id: generate a random ID in uuid format
- name: same as the original name in the input document
- description: a short description from the README
- repository: 
  - url: the original repo URL
  - source: set to "github"
  - id: the GitHub repository ID using the id field from 'https://api.github.com/repos/<ORGANIZATION>/<REPO>'
- version_detail: 
  - version: parse the Repo field of the input JSON and extract the version after the last ':'. E.g., for 
  'quay.io/validated-mcp-servers/elasticsearch:20250809-5014d91', version is '20250809-5014d91'
  - release_date: set it to today's date for now
  - is_latest: alwasy set to 'true'

PHASE 3: EXTRACT PACKAGES DATA
The packages data must include a single entry of type "docker", with the following details:
- registry_name: set to 'docker'
- name: name of the container image from the input JSON, without the version tag.
- version: the version tag from the container image in the input JSON
- environment_variables: extract environment variables that can configure the behavior of the MCP server. Follow these guidelines:
  * CRITICAL: Extract exact variable names as documented in the README file - do NOT assume standard naming conventions
  * Look for variables in configuration examples, command line examples, and environment variable sections
  * Verify variable names against code examples, Docker commands, and configuration samples in the README
  * If the README shows `-e VARIABLE_NAME` in Docker commands, use exactly that variable name
  * Do NOT invent or standardize variable names - use only what is explicitly documented
  For each documented environment variable add an entry with:
  - name: exact variable name as documented (respect exact case and spelling from README)
  - description: short description based on documentation
  - is_required: whether it's a mandatory variable or not. In case of uncertainty, omit this field
  - default: possible default value if explicitly stated. In case of uncertainty, omit this field
  - is_secret: use 'true' if the variable seems to define a sensitive secret. Include variables defining a username. In case of uncertainty, omit this field
  - choices: list of possible values for the input if explicitly documented. If no choices are given, omit this field
- package_arguments: if any additional argument needs to be executed (e.g., in `docker run docker.elastic.co/mcp/elasticsearch stdio`, 'stdio' is the package argument)
  add one entry for each of them with:
    - description: short description based on documentation
    - is_required: whether it's a mandatory variable or not. In case of uncertainty, omit this field
    - format: set to "string"
    - value: the desired value from the documentatino (e.g. "stdio")
    - type: "named" or "positional", according to the documentation. For "named" arguments, the "name" field is also needed.
    - name: optional argument name (only for "named" arguments)

PHASE 4: GENERATE REGISTRY DEFINITION
Assemble all the information collected and store the definition in a registry.json file at the root of the project.
Always use this name to store the configuration.

CONSTRAINTS:
- The generated file must match the MCP registry OpenAPI schema
- If no container image has been defined (e.g., the Repo field in the JSON input does not link to a container image):
  - Set 'N/A' in the version field of version_details
  - Set an empty the packages definition

REFERENCES:
MCP protocol: https://modelcontextprotocol.io/specification/2025-06-18
MCP registry OpenAPI schema: https://github.com/modelcontextprotocol/registry/blob/main/docs/server-registry-api/openapi.yaml, 
MCP registry seed file: https://github.com/modelcontextprotocol/registry/blob/main/data/seed.json


---

## From `output/servers_validation_summary.md` — Sample validation report (example output)

# MCP Servers Validation Summary

**Execution Timestamp:** 2025-08-12T17:56:00Z  
**Validation Tool:** mcp-validate v2.0.0  
**Profile Used:** comprehensive  
**Container Runtime:** podman 5.5.2  

## Summary Statistics

- **Total Servers Validated:** 7
- **Successful Validations:** 7 (100%)
- **Failed Validations:** 0 (0%)
- **Total Errors:** 0
- **Total Warnings:** 21

## Validation Results

| Server Name | Status | Errors | Warnings | Report File |
|-------------|---------|---------|----------|-------------|
| hashicorp | ✅ Succeeded | 0 | 2 | [terraform-mcp-server.json](terraform-mcp-server.json) |
| dynatrace-oss | ✅ Succeeded | 0 | 3 | [dynatrace.json](dynatrace.json) |
| redis | ✅ Succeeded | 0 | 3 | [redis.json](redis.json) |
| redis-cloud | ✅ Succeeded | 0 | 3 | [redis-cloud.json](redis-cloud.json) |
| Couchbase-Ecosystem | ✅ Succeeded | 0 | 3 | [mcp-server-couchbase.json](mcp-server-couchbase.json) |
| elastic | ✅ Succeeded | 0 | 4 | [elasticsearch.json](elasticsearch.json) |
| jfrog | ✅ Succeeded | 0 | 3 | [jfrog.json](jfrog.json) |

## Failed Validations Details

None - All validations succeeded!

## Common Warning Patterns

1. **Container UBI Compliance (7 instances):** All container images are not based on UBI (Universal Base Image)
2. **Security Analysis Issues (7 instances):** Security analysis failed with 'NoneType' object errors
3. **Error Compliance Issues (6 instances):** Invalid method or malformed request handling issues

## Successful Server Details

### hashicorp (Terraform MCP Server)
- **Version:** 0.3.0
- **Tools:** 8 tools including terraform registry integration
- **Resources:** 2 resources (development guides)

### dynatrace-oss (Dynatrace MCP Server) 
- **Version:** 0.5.0-rc.2
- **Tools:** 0 tools discovered
- **Capabilities:** Basic MCP protocol support

### redis (Redis MCP Server)
- **Version:** 1.9.4
- **Tools:** 0 tools discovered (database connectivity required)
- **Capabilities:** experimental, prompts, resources, tools

### redis-cloud (Redis Cloud MCP Server)
- **Version:** 1.0.0
- **Tools:** 0 tools discovered (Redis Cloud API connectivity required)
- **Capabilities:** tools

### Couchbase-Ecosystem (Couchbase MCP Server)
- **Version:** 1.12.0
- **Tools:** 8 tools for database operations
- **Capabilities:** experimental, prompts, resources, tools

### elastic (Elasticsearch MCP Server)
- **Version:** 0.2.1 (server name: rmcp)
- **Tools:** 0 tools discovered
- **Capabilities:** tools (requires Elasticsearch connection for full functionality)

### jfrog (JFrog MCP Server)
- **Version:** 0.0.1
- **Tools:** 0 tools discovered
- **Capabilities:** Basic MCP protocol support

## Recommendations

1. **Improve UBI Compliance:** Consider migrating to UBI-based container images for better security
2. **Fix Security Analysis:** Resolve the 'NoneType' errors in security validation
3. **Handle Error Compliance Issues:** Improve invalid method and malformed request handling
4. **Optimize Container Loading:** Some servers (redis-cloud) took significant time to pull and start

## Notes

- Servers without Docker packages (mulesoft, snyk, Unstructured-IO, IBM) were not validated as they lack containerized distributions
- Test environment variables were used for all validations (no real service connections)
- All validations used stdio transport mode where applicable
- The elasticsearch server validation was successfully fixed by adding the required "stdio" package argument
- The redis-cloud server validation was successfully fixed by correcting the container image reference in the input JSON
