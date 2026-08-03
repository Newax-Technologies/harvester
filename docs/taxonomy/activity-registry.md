# Harvester Domain–Activity Registry Index

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This registry completes the domain-specific activity taxonomy for all **1,586 canonical domains** across all 16 broad sectors.

## Activity definitions

- [Canonical activities, part 1](activity-registry-part-1.md)
- [Canonical activities, part 2](activity-registry-part-2.md)
- [Canonical activities, part 3](activity-registry-part-3.md)

## Applicability profiles and domain assignments

- [Activity profiles, part 1](activity-profiles-part-1.md)
- [Domain assignments, part 1](domain-assignments-part-1.md)
- [Activity profiles, part 2](activity-profiles-part-2.md)
- [Domain assignments, part 2](domain-assignments-part-2.md)
- [Activity profiles, part 3](activity-profiles-part-3.md)
- [Domain assignments, part 3](domain-assignments-part-3.md)
- [Activity profiles, part 4](activity-profiles-part-4.md)
- [Domain assignments, part 4](domain-assignments-part-4.md)
- [Activity profiles, part 5](activity-profiles-part-5.md)
- [Domain assignments, part 5](domain-assignments-part-5.md)
- [Activity profiles, part 6](activity-profiles-part-6.md)
- [Domain assignments, part 6](domain-assignments-part-6.md)
- [Activity profiles, part 7](activity-profiles-part-7.md)
- [Domain assignments, part 7](domain-assignments-part-7.md)
- [Activity profiles, part 8](activity-profiles-part-8.md)
- [Domain assignments, part 8](domain-assignments-part-8.md)

## Locked rules

1. Activities are shared canonical identities.
2. Every domain is explicitly assigned to a default activity profile.
3. Selecting an activity for one domain never activates it for another domain.
4. `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence.
5. Activities absent from a profile are `NOT_APPLICABLE` by default.
6. Users approve each domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.
7. Completed harvest jobs retain the registry versions used when they ran.

## Delivery boundary

This is a controlled documentation dataset. It does not implement schema, migrations, APIs, interface controls, activity detection, evidence scoring, or releases.
