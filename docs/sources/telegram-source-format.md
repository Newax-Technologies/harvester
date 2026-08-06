# Harvester Telegram Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Existing runtime source type exists; governed adapter format is not implemented**

## 1. Purpose

This document defines how customer-authorized bots, customer-owned channels and groups, licensed imports, public channel references, and manual operator assertions may enter Harvester.

Harvester must not use stolen sessions, personal account automation, phone-number enumeration, unauthorized group access, or bulk extraction from channels and users outside an approved permission basis.

## 2. Source modes

```text
TELEGRAM_BOT_AUTHORIZED
TELEGRAM_CHANNEL_AUTHORIZED
TELEGRAM_GROUP_AUTHORIZED
TELEGRAM_AUTHORIZED_IMPORT
TELEGRAM_OPERATOR_REFERENCE
```

## 3. User configuration

```text
mode
bot_credential_reference_id
connection_reference_id
chat_ids
channel_ids
approved_update_types
webhook_secret_reference
polling_policy
message_window
language_filters
keyword_profile_version
attachment_policy
retention_policy_version
deletion_policy_version
operator_reference_urls
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Chat or channel | Chat ID | Customer-authorized communication space |
| User | User ID | Participant reference only where permitted |
| Message | Chat ID plus message ID | Announcement, request or operational evidence |
| Update | Update ID | Delivery and refresh event |
| File | File ID or unique file ID | Attachment reference |
| Authorized import row | Customer external ID | Customer-owned historical record |
| Operator reference | Telegram URL | Manual navigation and bounded assertion |

## 5. Canonical formatting

```text
source.code = TELEGRAM
source.mode = selected Telegram mode
native.object_type = chat | channel | message | update | file
native.object_id = provider ID
native.parent_id = chat or channel ID
native.url = public message URL only when available and permitted
entity_hints.organization_names = customer-authorized channel title when organization mapping is approved
entity_hints.person_names = participant name only under an approved purpose
entity_hints.provider_identifiers = chat, channel, user and message IDs
content.summary = permitted message text or bounded excerpt
content.published_at = message date
signals.keyword_matches = approved profile matches
signals.event_types = request, announcement, hiring, outage, event or operational update hypotheses
policy.authorization_basis = CUSTOMER_AUTHORIZED_CONNECTION | CUSTOMER_AUTHORIZED_IMPORT | MANUAL_OPERATOR_REFERENCE
```

## 6. Example message observation

```json
{
  "schema_version": "1.0",
  "source": {"code": "TELEGRAM", "mode": "TELEGRAM_CHANNEL_AUTHORIZED"},
  "native": {"object_type": "message", "object_id": "-100123:456", "parent_id": "-100123", "url": "https://t.me/example/456"},
  "entity_hints": {
    "organization_names": ["Example Trade Association"],
    "provider_identifiers": [{"type": "TELEGRAM_CHAT_ID", "value": "-100123"}]
  },
  "content": {
    "summary": "Customer-authorized channel message announced a procurement event.",
    "language": "en",
    "published_at": "2026-08-01T11:00:00Z",
    "content_type": "message"
  },
  "signals": {"event_types": ["PROCUREMENT_ANNOUNCEMENT"]},
  "policy": {
    "authorization_basis": "CUSTOMER_AUTHORIZED_CONNECTION",
    "retention_policy": "TELEGRAM_CONNECTION_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
TELEGRAM_SUCCESS
TELEGRAM_WEBHOOK_SIGNATURE_INVALID
TELEGRAM_DUPLICATE_UPDATE
TELEGRAM_BOT_REMOVED
TELEGRAM_CHAT_NOT_AUTHORIZED
TELEGRAM_MESSAGE_DELETED
TELEGRAM_RATE_LIMITED
TELEGRAM_FILE_UNAVAILABLE
TELEGRAM_IMPORT_AUTHORIZATION_MISSING
TELEGRAM_PRIVACY_BLOCKED
TELEGRAM_POLICY_BLOCKED
```

## 8. Privacy and retention

- Store the minimum participant data required for the approved use case.
- Private chat and group content is never a general prospecting source.
- Webhook and polling updates must be deduplicated by update ID and message identity.
- Deletion, bot removal, customer revocation, and retention expiry must propagate to observations where required.
- Attachments require content-type, malware, size, retention and access controls.

## 9. Evidence boundaries

Telegram may support customer-authorized announcements, community events, requests, operational updates and contact-path evidence.

It cannot independently prove legal identity, buying authority, budget, service absence, consent to other communication channels or a qualified opportunity.

## 10. Delivery boundary

This document does not implement Telegram bots, webhooks, polling, imports, file handling, privacy controls, parsing or scoring.