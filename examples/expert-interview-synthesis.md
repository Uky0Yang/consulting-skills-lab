# Expert Interview Synthesis: ticket-triage rollout

All participants and excerpts below are fictional training material, not interviews conducted with real people. This worked example is not a recorded forward-test.

## Request and raw material

> Use $expert-interview-synthesis to decide whether our eight-week triage pilot supports rolling out to all sites. Prepare next-round questions and synthesize the supplied notes without claiming representative market demand.

All four source records refer to the same pilot period. Recording/publication consent is not supplied; use anonymized IDs and do not initiate outreach.

- I1, site operations lead, transcript paragraph 4: “The routing queue was shorter on most mornings, but we still checked the sensitive tickets manually.” Firsthand experience; no queue measurements supplied.
- I1, paragraph 7: “The vendor slide says each site saves twenty hours a week.” Repetition of a vendor claim, not a measured result.
- I2, finance analyst, transcript paragraph 3: “Paid overtime was unchanged in the pilot. We have not separated triage time from other support work.” Firsthand access to payroll; underlying records not attached.
- I3, second-site team lead, notes section B: a supervisor reports that the tool missed exceptions twice in week six. The note summarizes this statement; no exact wording or incident log is available.
- I4, reseller, transcript paragraph 2: “The vendor slide says each site saves twenty hours a week.” Same underlying slide as I1; no pilot data or independent test.

## Next-round guide

Ask the operations lead to walk through one recent ticket and show queue timestamps, including manual checks. Ask finance which costs or hours could actually be avoided and which were redeployed. Ask the second-site supervisor to describe the two exceptions and the impact of the manual fallback. Ask for a contrary case: when was routing slower or less reliable than before?

Confirm consent, confidentiality and access to permissible records before interviews or recording. These are proposed questions, not sent invitations.

## Evidence ledger

| ID | Provenance | Extract | Type and interpretation | Confidence |
| --- | --- | --- | --- | --- |
| E1 | I1 ¶4 | “The routing queue was shorter on most mornings, but we still checked the sensitive tickets manually.” | Scoped firsthand perception of speed; manual control remains necessary | Directional |
| E2 | I1 ¶7 and I4 ¶2 | “The vendor slide says each site saves twenty hours a week.” | One underlying vendor claim repeated by two people; not two independent confirmations | Unverified |
| E3 | I2 ¶3 | “Paid overtime was unchanged in the pilot. We have not separated triage time from other support work.” | Attributed cost observation requiring payroll corroboration; not proof of zero operational benefit | Directional |
| E4 | I3 notes B | Paraphrase: two missed exceptions in week six | Secondhand summary; original wording and incidence denominator unknown | Unverified |

## Conflict register and findings

**Speed is promising but not quantified.** E1 suggests a shorter perceived queue in one site, not measured throughput gains across all sites. E4 points to a quality risk that may differ by ticket type; retain it even though it is a minority account.

**Twenty hours of savings is not corroborated.** E2 has one commercial source and no period-matched measurement. E3 concerns paid overtime, which differs from time released or redeployed. The apparent disagreement may be about definitions; do not average “twenty” and “zero.”

The sample contains four participant roles, but two repeat one claim and one record is paraphrased hearsay. It cannot estimate population prevalence, rollout adoption or the percentage of sites that will benefit.

## Decision and next verification

Do not recommend an unrestricted rollout or book cash savings from this evidence. Propose a staged pilot extension with baseline/post queue logs, time-on-task sampling, exception denominators and incident severity. Operations owns speed/quality measurement; finance validates avoided versus redeployed cost; the pilot sponsor approves the gate before expanding.

A gate cannot be invented from missing business tolerances. Ask the sponsor to agree quality and contribution thresholds. If critical exception controls cannot be demonstrated, pause expansion and retain manual checks. Handoff E1–E4 with their provenance and unresolved status to the transformation plan or decision memo.

Editable files: [interview guide](../skills/expert-interview-synthesis/assets/interview-guide.md) and [evidence ledger](../skills/expert-interview-synthesis/assets/interview-evidence.csv).
