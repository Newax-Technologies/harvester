from typing import Any

import httpx

from ..extractors import extract_emails, extract_page_identity, extract_phones, visible_text

_PREVIEW_URL_TEMPLATE = "https://t.me/s/{channel}"


class TelegramChannelConnector:
    """
    Fetches a Telegram channel's public HTML preview page
    (https://t.me/s/<channel>) -- the page Telegram itself serves without
    any authentication specifically for anonymous/embed viewing of public
    channels. This is a public web fetch, the same authorization basis as
    sources/web.py's crawler (see compliance/source_policy.py), not account
    automation: there is no login, no MTProto client, and no Bot API token
    involved, and it only ever reads channels a caller names explicitly --
    there is no discovery/search capability (Telegram exposes none for
    public channels), so job.yaml's `telegram_channels` list is the only
    input.

    Reuses extractors.py (the same parsing helpers sources/web.py's crawler
    uses) rather than writing bespoke Telegram-page parsing -- the preview
    page is just HTML.
    """

    def __init__(self, timeout_seconds: float = 10.0, user_agent: str = "LeadBot/1.0"):
        self.client = httpx.Client(
            timeout=timeout_seconds,
            headers={"User-Agent": user_agent},
            follow_redirects=True,
        )

    def fetch_channel(self, channel: str) -> dict[str, Any] | None:
        channel = channel.strip().lstrip("@")
        if not channel:
            return None
        url = _PREVIEW_URL_TEMPLATE.format(channel=channel)

        try:
            response = self.client.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Error fetching Telegram channel '{channel}': {e}")
            return None

        html = response.text
        text = visible_text(html)
        identity = extract_page_identity(html, url)
        # extract_page_identity's "name" key is JSON-LD Person-specific
        # (see extractors.py) and is essentially always empty for a channel
        # page -- "organization" (site_name/og:title-derived, with a
        # title-text fallback) is the field that actually carries the
        # channel's display name, matching how sources/web.py itself treats
        # an institution's name as identity["organization"], not
        # identity["name"].
        channel_name = identity["organization"]
        # A channel that doesn't exist (or was made private) still returns
        # 200 with Telegram's generic "channel preview unavailable" shell --
        # that page has neither a distinguishing name nor any body text
        # worth keeping. (extract_page_identity always falls back to the
        # URL's bare domain when even that's missing, so channel_name alone
        # is never a reliable emptiness signal on its own.)
        if not channel_name and not text:
            return None

        return {
            "channel": channel,
            "preview_url": url,
            "name": channel_name,
            "description": identity["description"],
            "all_emails": extract_emails(text, html),
            "all_phones": extract_phones(text),
        }
