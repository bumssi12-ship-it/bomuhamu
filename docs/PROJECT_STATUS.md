# Bomuhamu / BomBom Threads Manager — Verified Project Status

**Last updated:** 2026-10-13 (JST)
**Purpose:** Preserve a reproducible handoff without implying that local Windows or Meta App Review steps have been completed.

## Canonical public policy repository

- GitHub repository: `bumssi12-ship-it/bomuhamu` (public, default branch `main`)
- Website: https://bumssi12-ship-it.github.io/bomuhamu/
- Privacy: https://bumssi12-ship-it.github.io/bomuhamu/privacy-policy/
- Data deletion: https://bumssi12-ship-it.github.io/bomuhamu/data-deletion/
- Terms: https://bumssi12-ship-it.github.io/bomuhamu/terms/
- App Review Guide: https://bumssi12-ship-it.github.io/bomuhamu/review-guide/

## Live evidence, not assumptions

| Gate | State | Evidence / caveat |
|---|---|---|
| Public policy pages | **PASS, exact HTML parity 5/5** | [GitHub Actions 38394160858](https://github.com/bumssi12-ship-it/bomuhamu/actions/runs/38394160858): all 5 publicly served pages returned HTTP 200 and SHA256 matched checked-out source on 2026-10-13 |
| GitHub Pages deployment | **PASS** | [GitHub Actions 38374289896](https://github.com/bumssi12-ship-it/bomuhamu/actions/runs/38374289896), success on 2026-10-13 |
| Daily page monitoring | **CONFIGURED AND OBSERVED RUNNING** | `.github/workflows/meta-pages-health.yml`: daily and on-change checks now compare content SHA256 against the exact repository revision; push checks retry while Pages propagates |
| Meta App Review submission | **NOT VERIFIED** | Static pages do not indicate submission or approval |
| `threads_keyword_search` public search access | **NOT VERIFIED** | Prior local testing showed own-account-only / LIMITED discovery |
| `threads_profile_discovery` approval | **NOT VERIFIED** | Limited historical local evidence does not prove current App Review grant |
| Windows app installation | **NOT VERIFIED FOR LATEST BUILD** | A 2026-10-12 v3.4 install attempt failed in pytest temporary-directory setup due to Windows `WinError 5` and rolled back; subsequent installation evidence not available |
| Windows scheduled candidate collection | **NOT VERIFIED** | Check installed task/action/last run from user's PC |
| Windows SQLite/OAuth state | **DO NOT ASSUME** | Read-only PC diagnostic required to establish current condition |

## Immediate next actions — no reinstallation unless evidence requires it

1. Obtain the latest **read-only SAFE VERIFY R3** report from the Windows computer: `Downloads\BomBom_Threads_Reports\BOMBOM_VERIFY_LATEST.txt`. It must not contain tokens, app secrets or full private configuration.
2. Classify actual installed app, SQLite read-only integrity, scheduled task enabled/disabled status, task action path, last run result and candidate collection status. Repair only a confirmed defect.
3. In the Meta App Dashboard, inspect the **actual** App Review status for `threads_keyword_search` and `threads_profile_discovery` and the reviewer feedback. Do not infer approval from the policy website.
4. If submission is pending, use the public [App Review Guide](https://bumssi12-ship-it.github.io/bomuhamu/review-guide/) to prepare OAuth and per-permission in-app screencasts, without exposing any token or app secret.
5. Reauthorize Threads **only when the required permission is actually granted or when a separate verified token/authentication problem necessitates it**; do not repeatedly renew OAuth in hope of bypassing App Review restrictions.

## Safety constraints

- Scheduled collection may discover, score, de-duplicate and queue; **no scheduled Like, Follow, Repost or Reply**.
- External write actions must remain explicitly user-initiated with applicable local safeguards.
- Preserve user records, backups, OAuth credentials and disabled task settings during any repair.
- Do not claim the Windows environment is fully operational until real-device evidence exists.
- Do not add login tokens, secrets or private Windows logs to this **public** repository.

## Source-of-truth hierarchy

- GitHub Actions logs are the source of truth for public pages and CI runs.
- The user's sanitized Windows diagnostic is the source of truth for Windows runtime state.
- The Meta App Dashboard is the source of truth for permission approval.
- Static app review documentation is descriptive and cannot replace these runtime records.
