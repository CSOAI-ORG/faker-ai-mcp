<div align="center">

# Faker Ai MCP

**MCP server for faker ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-faker-ai-mcp)](https://pypi.org/project/meok-faker-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Faker Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `generate_fake_data` | Generate fake data of a specified type (person, company, address, email, phone). |
| `generate_profile` | Generate a complete fake user profile with name, contact, address, employment, a |
| `generate_address` | Generate realistic fake addresses with street, city, postcode, and country. |
| `generate_company` | Generate a fake company with name, industry, address, registration, and financia |
| `generate_dataset` | Generate a tabular fake dataset with specified columns. Supports: name, email, a |

## Installation

```bash
pip install meok-faker-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "faker-ai": {
      "command": "python",
      "args": ["-m", "meok_faker_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
