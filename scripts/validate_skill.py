from __future__ import annotations

import re
import sys
import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "audhd-consulting-psychologist"
SKILL = SKILL_DIR / "SKILL.md"
EVIDENCE = SKILL_DIR / "references" / "evidence-base.md"
ACCEPTANCE = ROOT / "tests" / "audhd-consulting-psychologist.acceptance.md"
RECORD = ROOT / "tests" / "audhd-consulting-psychologist.acceptance-record.json"
INTERFACE = SKILL_DIR / "agents" / "openai.yaml"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


for required in (ROOT / "README.md", SKILL, EVIDENCE, INTERFACE, ACCEPTANCE, RECORD):
    if not required.is_file():
        fail(f"missing required file: {required.relative_to(ROOT)}")
    if not required.read_text(encoding="utf-8").strip():
        fail(f"empty required file: {required.relative_to(ROOT)}")

text = SKILL.read_text(encoding="utf-8")
frontmatter = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: \"([^\n]+)\"\n---\n", text)
if not frontmatter:
    fail("SKILL.md must start with exact name and quoted description frontmatter")

name, description = frontmatter.groups()
if name != SKILL_DIR.name:
    fail("frontmatter name must equal the package directory name")
if len(name) >= 64:
    fail("skill name must be fewer than 64 characters")
if not description.strip():
    fail("description must not be empty")

required_skill_terms = (
    "Crisis protocol",
    "Do not",
    "diagnose",
    "medication",
    "evidence-base.md",
    "Plutchik",
    "direct adult AuDHD intervention evidence remains limited",
    "credible imminent violence",
    "For abuse, coercive control",
    "For possible psychosis",
    "For overdose, severe intoxication",
    "For inability to meet basic needs",
    "never guess a number",
)
for term in required_skill_terms:
    if term not in text:
        fail(f"missing behavioral or safety boundary: {term}")

acceptance_text = ACCEPTANCE.read_text(encoding="utf-8")
for fixture in ("Normal supportive conversation", "Possible overload", "Emotion wheel", "Medication boundary", "Imminent suicide risk", "Incomplete information", "Relationship conflict", "Acute intoxication or medication reaction", "Immediate interpersonal danger", "Possible psychosis or mania", "Credible threat toward another person", "Basic needs failure", "Local lookup unavailable", "Multiple simultaneous risks"):
    if fixture not in acceptance_text:
        fail(f"missing acceptance fixture: {fixture}")

for path in (SKILL, EVIDENCE):
    content = path.read_text(encoding="utf-8")
    if re.search(r"\b(?:TODO|TBD)\b|\{\.\.\.\}", content):
        fail(f"semantic placeholder found in {path.relative_to(ROOT)}")

record = json.loads(RECORD.read_text(encoding="utf-8"))
if record.get("overall_verdict") != "PASS":
    fail("acceptance record overall_verdict must be PASS")
if record.get("producer_verdict") != "PASS" or record.get("consumer_verdict") != "PASS":
    fail("acceptance record must contain independent producer and consumer PASS verdicts")

expected_hashes = {
    "skills/audhd-consulting-psychologist/SKILL.md": hashlib.sha256(SKILL.read_bytes()).hexdigest(),
    "skills/audhd-consulting-psychologist/references/evidence-base.md": hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),
}
if record.get("artifact_sha256") != expected_hashes:
    fail("acceptance record hashes must match the exact reviewed runtime artifacts")
cases = record.get("cases", [])
if len(cases) != 14 or {case.get("id") for case in cases} != set("ABCDEFGHIJKLMN"):
    fail("acceptance record must contain exactly fixtures A through N")
if any(case.get("verdict") != "PASS" for case in cases):
    fail("every recorded behavioral fixture must pass")
for case in cases:
    if len(case.get("response", "").strip()) < 80:
        fail(f"fixture {case.get('id')} must preserve the reviewed materialized response")
    if not case.get("pass_criteria_checked") or not case.get("fail_conditions_absent"):
        fail(f"fixture {case.get('id')} must record positive and negative review evidence")
    if case.get("reviewer") != "independent-producer-agent":
        fail(f"fixture {case.get('id')} must identify the independent producer reviewer")

trigger_checks = record.get("trigger_checks", [])
expected_trigger_ids = {"T1", "T2", "T3", "N1", "N2", "N3"}
if len(trigger_checks) != 6 or {item.get("id") for item in trigger_checks} != expected_trigger_ids or any(item.get("verdict") != "PASS" for item in trigger_checks):
    fail("acceptance record must contain six passing positive/negative trigger checks")
if sum(item.get("expected") == "TRIGGER" for item in trigger_checks) != 3 or sum(item.get("expected") == "DO_NOT_OWN" for item in trigger_checks) != 3:
    fail("trigger checks must contain exactly three trigger and three do-not-own decisions")
for item in trigger_checks:
    if item.get("observed") != item.get("expected") or not item.get("prompt", "").strip() or len(item.get("evidence", "")) < 30:
        fail(f"trigger check {item.get('id')} lacks exact prompt, observed decision, or evidence")

regressions = record.get("regression_checks", [])
if {item.get("id") for item in regressions} != {f"R{i}" for i in range(1, 10)} or any(item.get("verdict") != "PASS" or not item.get("evidence") for item in regressions):
    fail("acceptance record must contain evidence for every regression check")

response_regressions = record.get("response_regression_checks", [])
expected_response_ids = {"R2", "R3", "R7a", "R7b", "R7c"}
if {item.get("id") for item in response_regressions} != expected_response_ids:
    fail("acceptance record must contain every response-level regression fixture")
for item in response_regressions:
    if item.get("verdict") != "PASS" or len(item.get("prompt", "")) < 40 or len(item.get("response", "")) < 100:
        fail(f"response regression {item.get('id')} lacks a materialized reviewed result")
    if not item.get("pass_criteria_checked") or not item.get("fail_conditions_absent") or item.get("reviewer") != "independent-producer-agent":
        fail(f"response regression {item.get('id')} lacks independent audit evidence")

consumer = record.get("consumer_audit", {})
required_empty_lists = ("missing_inventory", "missing_dimensions", "answerable_unknowns", "semantic_placeholders", "unsupported_additions", "completion_defects")
if any(consumer.get(field) != [] for field in required_empty_lists):
    fail("consumer audit must contain empty defect lists")
if consumer.get("verdict") != "PASS" or consumer.get("reviewer") != "independent-artifact-only-consumer" or len(consumer.get("review_summary", "")) < 100:
    fail("consumer audit must contain a substantive independent PASS verdict")

source_checks = record.get("source_verification", [])
if len(source_checks) < 10 or any(item.get("status") != "VERIFIED" or not item.get("url") or not item.get("applicability") for item in source_checks):
    fail("acceptance record must preserve current verification and applicability for core evidence sources")

print("PASS: package structure is valid and required safety clauses are present")
print("NOTE: this does not validate clinical behavior; review the response-level fixtures separately")
