# Blind SQL Injection — Web Log Forensics

**Category:** Blue Team / DFIR / Web Log Analysis  
**Challenge:** Flagyard (authorized CTF)

## Scenario
Investigate suspicious web requests against a DVWA endpoint using Apache and ModSecurity logs. The observed User-Agent identifies sqlmap, and Boolean SQL injection conditions yield distinguishable HTML responses.

## Evidence
- `access.log`: web request chronology and User-Agent.
- `error.log`: WAF rule hits and anomaly alerts.
- `modsec_audit.log`: recorded request bodies and HTML responses.

**Evidence is not included** in this public repository.

## Scripts
| Script | Purpose |
| --- | --- |
| `01_find_probes.py` | Print example SQL predicates and corresponding HTML response classifications |
| `02_length_checks.py` | Summarize password-length tests, grouped by row and position |
| `03_character_checks.py` | Summarize individual-character comparisons without printing recovered secrets |
| `audit_parser.py` | Shared transaction extraction and URL-decoding helpers |

## Usage
Use Python 3.9+ (standard library only). Place the supplied `modsec_audit.log` on your own computer:

```bash
python3 01_find_probes.py /path/to/modsec_audit.log
python3 02_length_checks.py /path/to/modsec_audit.log
python3 03_character_checks.py /path/to/modsec_audit.log
```

## Findings
- sqlmap requests targeted `/DVWA/vulnerabilities/sqli_blind/`.
- ModSecurity detected malicious patterns, but its engine was configured in detection-only mode.
- The target page returned different text for true and false SQL conditions, allowing inference from the HTTP responses.
- Metadata and character-by-character database probes were present in the audit evidence.

## Lessons learned
HTTP 200 does not prove a request was harmless. Correlating complete HTTP requests with application responses is crucial when assessing SQL injection alerts.

## Responsible disclosure
This is an educational investigation. Avoid publishing raw logs, cookies, credentials, and challenge answers.
