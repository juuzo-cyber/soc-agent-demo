#!/usr/bin/env python3
"""
SOC alert triage — the "brain" node your audience builds.

Everything here runs locally with zero setup: no API keys, no network calls,
no external services. It takes a mock security alert and returns a structured
triage decision — exactly the shape that would feed a downstream system like
Microsoft Sentinel or ServiceNow.

Run it:   python triage.py
"""

import json
from dataclasses import dataclass, asdict


@dataclass
class Triage:
    """The structured output. In a real pipeline this JSON is what gets handed
    to the next system (a Sentinel incident, a ServiceNow case, etc.)."""
    alert_id: str
    severity: str            # Low | Medium | High | Critical
    mitre_technique: str
    summary: str
    recommended_action: str


def triage_alert(alert: dict) -> Triage:
    # ========================================================================
    #  THIS IS THE PART THE AUDIENCE BUILDS.
    #  Edit any of it live and re-run — it's completely safe, nothing external.
    # ========================================================================

    # --- Severity: how worried should we be? ---
    # Impossible travel is suspicious, but if MFA was satisfied and there were
    # no failed logins it's more likely a VPN / legitimate-travel false positive.
    if not alert["mfa_satisfied"] or alert["failed_logins"] > 0:
        severity = "High"
    else:
        severity = "Medium"

    # --- Map the behaviour to a MITRE ATT&CK technique ---
    mitre_technique = "T1078 - Valid Accounts"

    # --- Plain-English summary for the analyst ---
    summary = (
        f"Impossible travel for {alert['user']}: {alert['location']}. "
        f"MFA satisfied = {alert['mfa_satisfied']}, "
        f"failed logins = {alert['failed_logins']}."
    )

    # --- What should happen next? ---
    if severity == "High":
        recommended_action = (
            "Disable the account, revoke active sessions, and contact the user."
        )
    else:
        recommended_action = (
            "Confirm the travel with the user and monitor for follow-on activity."
        )

    # ========================================================================
    #  END of the build-along section.
    # ========================================================================

    return Triage(
        alert_id=alert["alert_id"],
        severity=severity,
        mitre_technique=mitre_technique,
        summary=summary,
        recommended_action=recommended_action,
    )


def print_card(t: Triage) -> None:
    """Pretty-print the triage as a card so it reads well in a demo."""
    line = "=" * 62
    print(line)
    print(f"  SOC TRIAGE  .  {t.alert_id}")
    print(line)
    print(f"  Severity   : {t.severity.upper()}")
    print(f"  MITRE      : {t.mitre_technique}")
    print(f"  Summary    : {t.summary}")
    print(f"  Action     : {t.recommended_action}")
    print(line)


if __name__ == "__main__":
    with open("mock_alert.json") as f:
        alert = json.load(f)

    result = triage_alert(alert)

    # 1) The human-friendly view
    print_card(result)

    # 2) The structured output — THIS is what flows to Sentinel / ServiceNow
    print("\nStructured output (what the next system receives):")
    print(json.dumps(asdict(result), indent=2))
