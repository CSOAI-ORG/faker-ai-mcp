#!/usr/bin/env python3
"""Generate realistic fake test data for development and testing. — MEOK AI Labs."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, random, string, hashlib
from datetime import datetime, timezone, timedelta
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

FIRST_NAMES = {
    "en": ["James", "Emma", "Oliver", "Sophie", "William", "Charlotte", "Harry", "Amelia", "Thomas", "Isabella",
           "George", "Mia", "Alexander", "Ella", "Daniel", "Grace", "Matthew", "Chloe", "Samuel", "Lily"],
    "de": ["Lukas", "Anna", "Felix", "Marie", "Paul", "Sophie", "Leon", "Emilia", "Maximilian", "Hannah"],
    "fr": ["Lucas", "Emma", "Louis", "Jade", "Gabriel", "Louise", "Raphael", "Alice", "Arthur", "Chloe"],
    "es": ["Hugo", "Lucia", "Martin", "Sofia", "Carlos", "Maria", "Pablo", "Valeria", "Daniel", "Carmen"],
}
LAST_NAMES = {
    "en": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Davis", "Miller", "Wilson", "Moore", "Taylor",
           "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Robinson", "Clark"],
    "de": ["Mueller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"],
    "fr": ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Petit", "Richard", "Durand", "Leroy", "Moreau"],
    "es": ["Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez", "Hernandez", "Perez", "Sanchez", "Ramirez", "Torres"],
}
STREETS = ["High Street", "Main Street", "Oak Avenue", "Park Lane", "Church Road", "Mill Lane",
           "Station Road", "Victoria Street", "Queen Street", "King Street", "Elm Drive", "Cedar Court"]
CITIES = {"en": ["London", "Manchester", "Birmingham", "Leeds", "Bristol", "Edinburgh", "Glasgow", "Liverpool"],
           "us": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio"],
           "de": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Stuttgart"],
           "fr": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes"]}
DOMAINS = ["example.com", "test.org", "sample.net", "demo.io", "fakeco.com", "testmail.dev"]
INDUSTRIES = ["Technology", "Healthcare", "Finance", "Education", "Retail", "Manufacturing",
              "Consulting", "Energy", "Media", "Transportation", "Real Estate", "Legal"]
COMPANY_SUFFIXES = ["Ltd", "Inc", "Corp", "Group", "Solutions", "Technologies", "Partners", "Global", "Labs"]


def _random_date(start_year: int = 1960, end_year: int = 2005) -> str:
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = (end - start).days
    rand_date = start + timedelta(days=random.randint(0, delta))
    return rand_date.strftime("%Y-%m-%d")


def _luhn_checksum(partial: str) -> str:
    digits = [int(d) for d in partial]
    odd_sum = sum(digits[-1::-2])
    even_sum = sum(sum(divmod(2 * d, 10)) for d in digits[-2::-2])
    check = (10 - (odd_sum + even_sum) % 10) % 10
    return partial + str(check)


@mcp.tool()
def generate_fake_data(data_type: str = "person", count: int = 1, locale: str = "en",
                       api_key: str = "") -> str:
    """Generate fake data of a specified type (person, company, address, email, phone). Returns 1-50 records."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    count = max(1, min(count, 50))
    results = []
    for _ in range(count):
        if data_type == "person":
            first = random.choice(FIRST_NAMES.get(locale, FIRST_NAMES["en"]))
            last = random.choice(LAST_NAMES.get(locale, LAST_NAMES["en"]))
            results.append({"name": f"{first} {last}", "email": f"{first.lower()}.{last.lower()}@{random.choice(DOMAINS)}",
                            "phone": f"+44 {''.join(random.choices(string.digits, k=10))}",
                            "dob": _random_date(), "gender": random.choice(["male", "female"])})
        elif data_type == "email":
            first = random.choice(FIRST_NAMES.get(locale, FIRST_NAMES["en"])).lower()
            last = random.choice(LAST_NAMES.get(locale, LAST_NAMES["en"])).lower()
            results.append({"email": f"{first}.{last}{random.randint(1,99)}@{random.choice(DOMAINS)}"})
        elif data_type == "phone":
            code = random.choice(["+44", "+1", "+49", "+33", "+34"])
            results.append({"phone": f"{code} {''.join(random.choices(string.digits, k=10))}"})
        elif data_type == "address":
            city_pool = CITIES.get(locale, CITIES["en"])
            results.append({"street": f"{random.randint(1,200)} {random.choice(STREETS)}",
                            "city": random.choice(city_pool), "postcode": "".join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(1,20)) + " " + str(random.randint(1,9)) + "".join(random.choices(string.ascii_uppercase, k=2))})
        else:
            results.append({"type": data_type, "value": "".join(random.choices(string.ascii_letters + string.digits, k=16))})

    return {"data_type": data_type, "locale": locale, "count": len(results), "data": results,
            "timestamp": datetime.now(timezone.utc).isoformat()}


@mcp.tool()
def generate_profile(locale: str = "en", include_avatar: bool = False, api_key: str = "") -> str:
    """Generate a complete fake user profile with name, contact, address, employment, and bio."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    first = random.choice(FIRST_NAMES.get(locale, FIRST_NAMES["en"]))
    last = random.choice(LAST_NAMES.get(locale, LAST_NAMES["en"]))
    city_pool = CITIES.get(locale, CITIES["en"])
    uid = hashlib.md5(f"{first}{last}{random.random()}".encode()).hexdigest()[:8]

    profile = {
        "uid": uid,
        "name": {"first": first, "last": last, "full": f"{first} {last}"},
        "email": f"{first.lower()}.{last.lower()}@{random.choice(DOMAINS)}",
        "phone": f"+44 {''.join(random.choices(string.digits, k=10))}",
        "dob": _random_date(),
        "gender": random.choice(["male", "female"]),
        "address": {"street": f"{random.randint(1,200)} {random.choice(STREETS)}",
                     "city": random.choice(city_pool), "country": locale.upper()},
        "employment": {"company": f"{random.choice(LAST_NAMES['en'])} {random.choice(COMPANY_SUFFIXES)}",
                        "title": random.choice(["Engineer", "Manager", "Analyst", "Designer", "Developer", "Director"]),
                        "industry": random.choice(INDUSTRIES)},
        "bio": f"{first} is a professional based in {random.choice(city_pool)}.",
    }
    if include_avatar:
        profile["avatar_url"] = f"https://api.dicebear.com/7.x/personas/svg?seed={uid}"
    profile["timestamp"] = datetime.now(timezone.utc).isoformat()
    return profile


@mcp.tool()
def generate_address(locale: str = "en", count: int = 1, api_key: str = "") -> str:
    """Generate realistic fake addresses with street, city, postcode, and country."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    count = max(1, min(count, 50))
    city_pool = CITIES.get(locale, CITIES["en"])
    country_map = {"en": "United Kingdom", "us": "United States", "de": "Germany", "fr": "France", "es": "Spain"}
    addresses = []
    for _ in range(count):
        addresses.append({
            "street": f"{random.randint(1, 300)} {random.choice(STREETS)}",
            "city": random.choice(city_pool),
            "postcode": "".join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(1, 20)) + " " + str(random.randint(1, 9)) + "".join(random.choices(string.ascii_uppercase, k=2)),
            "country": country_map.get(locale, "Unknown"),
            "latitude": round(random.uniform(49.0, 58.0), 6),
            "longitude": round(random.uniform(-6.0, 2.0), 6),
        })
    return {"locale": locale, "count": len(addresses), "addresses": addresses,
            "timestamp": datetime.now(timezone.utc).isoformat()}


@mcp.tool()
def generate_company(locale: str = "en", api_key: str = "") -> str:
    """Generate a fake company with name, industry, address, registration, and financial details."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    name = f"{random.choice(LAST_NAMES.get(locale, LAST_NAMES['en']))} {random.choice(COMPANY_SUFFIXES)}"
    city_pool = CITIES.get(locale, CITIES["en"])
    reg_number = "".join(random.choices(string.digits, k=8))
    employees = random.choice([5, 10, 25, 50, 100, 250, 500, 1000, 5000])

    return {
        "name": name,
        "registration_number": reg_number,
        "industry": random.choice(INDUSTRIES),
        "founded": random.randint(1970, 2024),
        "employees": employees,
        "revenue_estimate": f"${employees * random.randint(50, 200)}k",
        "address": {"street": f"{random.randint(1, 100)} {random.choice(STREETS)}",
                     "city": random.choice(city_pool)},
        "website": f"https://www.{name.lower().replace(' ', '')}.com",
        "phone": f"+44 {''.join(random.choices(string.digits, k=10))}",
        "email": f"info@{name.lower().replace(' ', '')}.com",
        "vat_number": f"GB{''.join(random.choices(string.digits, k=9))}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def generate_dataset(rows: int = 10, columns: str = "name,email,age", locale: str = "en",
                     api_key: str = "") -> str:
    """Generate a tabular fake dataset with specified columns. Supports: name, email, age, phone, city, company, date, amount."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    rows = max(1, min(rows, 100))
    cols = [c.strip().lower() for c in columns.split(",") if c.strip()]
    city_pool = CITIES.get(locale, CITIES["en"])
    data = []

    for _ in range(rows):
        row = {}
        for col in cols:
            if col == "name":
                first = random.choice(FIRST_NAMES.get(locale, FIRST_NAMES["en"]))
                last = random.choice(LAST_NAMES.get(locale, LAST_NAMES["en"]))
                row["name"] = f"{first} {last}"
            elif col == "email":
                row["email"] = f"{''.join(random.choices(string.ascii_lowercase, k=6))}@{random.choice(DOMAINS)}"
            elif col == "age":
                row["age"] = random.randint(18, 85)
            elif col == "phone":
                row["phone"] = f"+44 {''.join(random.choices(string.digits, k=10))}"
            elif col == "city":
                row["city"] = random.choice(city_pool)
            elif col == "company":
                row["company"] = f"{random.choice(LAST_NAMES['en'])} {random.choice(COMPANY_SUFFIXES)}"
            elif col == "date":
                row["date"] = _random_date(2020, 2026)
            elif col == "amount":
                row["amount"] = round(random.uniform(10.0, 10000.0), 2)
            elif col == "id":
                row["id"] = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            elif col == "boolean":
                row["boolean"] = random.choice([True, False])
            else:
                row[col] = "".join(random.choices(string.ascii_letters, k=10))
        data.append(row)

    return {"columns": cols, "rows": len(data), "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()}


if __name__ == "__main__":
    mcp.run()
