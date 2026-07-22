# Lead Harvester

A Python MVP for finding and ranking business leads from:

1. Search queries through the Brave Search API.
2. Public websites that permit crawling.
3. Authorized social-media exports in CSV format.

It extracts contact details, organization identity, social links, evidence text, target keywords, locations, and buying-intent phrases. It then scores and deduplicates leads in SQLite and exports CSV or JSON.

## Why it does not blindly scrape social networks

Most social platforms restrict automated collection, reuse, and commercial exploitation of user data. This project deliberately uses official APIs or exports you are authorized to process. Adding a login-cookie scraper would be easy engineering and terrible product judgment: it would be fragile, legally risky, and likely to get accounts blocked.

## Features

- Async website crawler using HTTPX.
- `robots.txt` checks using Python's standard library.
- Per-domain rate limiting, response-size limits, timeouts, and concurrency controls.
- Same-domain crawling with priority for contact/about/team pages.
- Email, phone, organization, location, social-profile, and evidence extraction.
- Brave Search query discovery when an API key is configured.
- Social CSV ingestion with flexible column aliases.
- Lead scoring from contactability, ICP keyword fit, location fit, and intent signals.
- SQLite persistence, fingerprint deduplication, CSV/JSON export.
- Unit tests and Docker support.

## Installation

```bash
cd lead-harvester
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
```

Optional environment variables:

```bash
cp .env.example .env
export BRAVE_SEARCH_API_KEY="your-key"
export LEAD_HARVESTER_USER_AGENT="YourCompanyLeadBot/1.0 (+https://yourdomain.com/contact)"
```

The CLI reads environment variables from the shell. It intentionally does not silently load `.env`; production systems should use a proper secret manager, because apparently committing API keys remains a popular human hobby.

## Run with seed websites

```bash
lead-harvester run \
  --seeds-file examples/seeds.txt \
  --keywords "clinic,hospital,orthotics,prosthetics" \
  --locations "Islamabad,Rawalpindi" \
  --minimum-score 35 \
  --export output/leads.csv
```

## Run with search queries

```bash
export BRAVE_SEARCH_API_KEY="your-key"

lead-harvester run \
  --query 'private clinics Islamabad "contact"' \
  --query 'orthopedic rehabilitation Rawalpindi' \
  --keywords "clinic,rehabilitation,orthopedic" \
  --locations "Islamabad,Rawalpindi" \
  --count-per-query 10 \
  --export output/web-leads.csv
```

## Import authorized social-media data

Your CSV may use aliases such as `platform`, `profile_url`, `display_name`, `company`, `job_title`, `bio`, `caption`, or `post_text`.

```bash
lead-harvester run \
  --social-csv examples/social_export.csv \
  --keywords "automation,website,CRM,patient management" \
  --locations "Islamabad,Rawalpindi" \
  --minimum-score 40 \
  --export output/social-leads.csv
```

## Combine all sources

```bash
lead-harvester run \
  --query 'schools Islamabad need LMS' \
  --seed https://example.edu.pk \
  --social-csv licensed-social-export.csv \
  --keywords "school,LMS,learning management system" \
  --locations "Islamabad,Rawalpindi" \
  --database output/leads.sqlite3 \
  --export output/leads.json \
  --format json
```

## Expected social CSV fields

The importer accepts common aliases. A useful canonical shape is:

```csv
platform,profile_url,display_name,company,job_title,email,phone,website,location,bio
```

Only process data that you own, have licensed, received through an official API, or have another lawful basis to use. Keep evidence and source URLs so every lead remains auditable.

## Scoring model

- Email: +22; named email: +5.
- Phone: +18.
- Website: +8.
- Social profiles: up to +8.
- Keyword matches: up to +30.
- Target location: +10.
- Buying intent: up to +24.
- Named contact: +4.
- No email and no phone: -15.
- Final score is capped at 100.

Edit `src/lead_harvester/scoring.py` to match your actual ICP. A universal lead score is marketing astrology wearing a spreadsheet costume.

## Tests

```bash
pytest -q
ruff check .
```

## Production roadmap

1. Add official platform connectors behind a shared adapter interface.
2. Add domain/email verification through a licensed provider.
3. Add entity resolution across domains, company names, and social profiles.
4. Add CRM synchronization and human review before outreach.
5. Add consent, suppression, retention, and deletion controls.
6. Add a FastAPI service and dashboard only after the data pipeline proves useful.

## Compliance guardrails

- Respect `robots.txt`, site terms, API terms, and applicable privacy/marketing laws.
- Do not bypass authentication, CAPTCHAs, rate limits, or access controls.
- Do not collect sensitive personal data.
- Do not auto-message scraped profiles.
- Keep a suppression list and honor deletion/opt-out requests.
- Use official APIs or authorized exports for social platforms.
