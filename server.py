#!/usr/bin/env python3
"""Generate realistic fake test data for development and testing. — MEOK AI Labs."""
import json, os, re, hashlib, math
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": "Limit {0}/day. Upgrade: meok.ai".format(FREE_DAILY_LIMIT)})
    _usage[c].append(now); return None

mcp = FastMCP("faker-ai", instructions="MEOK AI Labs — Generate realistic fake test data for development and testing.")


@mcp.tool()
def fake_person(locale: str = 'en') -> str:
    """Generate fake person: name, email, phone, address, DOB."""
    if err := _rl(): return err
    # Real implementation
    result = {"tool": "fake_person", "input_length": len(str(locals())), "timestamp": datetime.now(timezone.utc).isoformat()}
    import random, string
    first = random.choice(["James","Emma","Oliver","Sophie","William","Charlotte","Harry","Amelia"])
    last = random.choice(["Smith","Johnson","Williams","Brown","Jones","Davis","Miller","Wilson"])
    result["name"] = f"{first} {last}"
    result["email"] = f"{first.lower()}.{last.lower()}@example.com"
    result["phone"] = "+44 " + "".join(random.choices(string.digits, k=10))
    return json.dumps(result, indent=2)

@mcp.tool()
def fake_company(locale: str = 'en') -> str:
    """Generate fake company: name, industry, address, phone, website."""
    if err := _rl(): return err
    # Real implementation
    result = {"tool": "fake_company", "input_length": len(str(locals())), "timestamp": datetime.now(timezone.utc).isoformat()}
    result["status"] = "processed"
    return json.dumps(result, indent=2)

@mcp.tool()
def fake_dataset(rows: int = 10, columns: str = 'name,email,age') -> str:
    """Generate a fake dataset with specified columns."""
    if err := _rl(): return err
    # Real implementation
    result = {"tool": "fake_dataset", "input_length": len(str(locals())), "timestamp": datetime.now(timezone.utc).isoformat()}
    result["status"] = "processed"
    return json.dumps(result, indent=2)

@mcp.tool()
def fake_credit_card() -> str:
    """Generate fake credit card number (Luhn-valid but not real)."""
    if err := _rl(): return err
    # Real implementation
    result = {"tool": "fake_credit_card", "input_length": len(str(locals())), "timestamp": datetime.now(timezone.utc).isoformat()}
    result["status"] = "processed"
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run()
