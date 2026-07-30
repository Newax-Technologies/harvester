"""
Research Brain
==============
Uses an AI model (OpenAI-compatible) to analyse a LinkedIn profile
and produce structured intelligence:
  - Lead quality score (1–10)
  - Pain points detected
  - Buying signals
  - Best outreach angle
  - Suggested subject line
  - Personalised email / connection note draft

Results are saved to the database as ResearchFinding + AccountBrief records.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from lead_harvester.database import get_session
from lead_harvester.models import (
    AccountBrief,
    BriefStatus,
    CanonicalInstitution,
    FindingType,
    JobStatus,
    OperatingStatus,
    ResearchFinding,
    ResearchJob,
)
from lead_harvester.models.source import RawSourceRecord, SourceType

SYSTEM_PROMPT = """You are an elite B2B sales intelligence analyst.
You receive raw LinkedIn profile data and return a structured JSON analysis.
Be specific. Ground every insight in the actual profile text — do not invent facts.
Return ONLY valid JSON with no markdown fences."""

ANALYSIS_PROMPT = """Analyse this LinkedIn profile for B2B outreach:

PROFILE URL: {url}
NAME: {name}
HEADLINE: {headline}
COMPANY: {company}
LOCATION: {location}
ABOUT: {about}
EXPERIENCE: {experience}
EDUCATION: {education}
RECENT ACTIVITY: {activity}

Return a JSON object with exactly these keys:
{{
  "lead_score": <integer 1-10>,
  "decision_maker": <true|false>,
  "pain_points": [<list of specific pain points inferred from profile>],
  "buying_signals": [<list of signals suggesting they may buy>],
  "best_angle": "<one sentence — the most compelling reason to reach out>",
  "suggested_subject": "<email subject line>",
  "email_draft": "<personalized cold email, 3 short paragraphs, under 150 words>",
  "linkedin_note": "<connection request note, under 300 characters>",
  "summary": "<2-3 sentence executive summary of why this lead matters>"
}}"""


class ResearchBrain:
    """
    AI-powered researcher that turns raw LinkedIn profile data into
    actionable outreach intelligence.

    Parameters
    ----------
    api_key : str
        OpenAI (or compatible) API key.
    model : str
        Model name (default: gpt-4o-mini — cheap and fast for this task).
    base_url : str | None
        Override for OpenAI-compatible endpoints (e.g. local Ollama).
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model
        self.base_url = base_url

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY is required for the Research Brain. "
                "Set it in your .env file or environment variables."
            )

    # ------------------------------------------------------------------
    # Public entry — process a list of raw LinkedIn records
    # ------------------------------------------------------------------

    async def process_all_pending(self) -> None:
        """Pull all unprocessed LinkedIn records and research each one."""
        from sqlalchemy import select

        async with get_session() as session:
            records = await session.scalars(
                select(RawSourceRecord)
                .where(RawSourceRecord.source_type == SourceType.LINKEDIN)
                .where(RawSourceRecord.normalized_name.isnot(None))
                # Only records not yet linked to a research job
                # (simplified — full implementation would use a processed flag)
                .limit(50)
            )
            for record in records:
                await self._research_record(session, record)

    async def research_profile(
        self,
        session: AsyncSession,
        profile_data: dict[str, Any],
        institution_id: uuid.UUID | None = None,
    ) -> dict[str, Any]:
        """
        Research a single profile dict and persist findings.
        Returns the raw AI analysis dict.
        """
        analysis = await self._call_ai(profile_data)

        if institution_id:
            await self._persist_findings(session, institution_id, profile_data, analysis)

        return analysis

    # ------------------------------------------------------------------
    # AI call
    # ------------------------------------------------------------------

    async def _call_ai(self, profile: dict[str, Any]) -> dict[str, Any]:
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url,  # None → uses OpenAI default
            )

            prompt = ANALYSIS_PROMPT.format(
                url=profile.get("profile_url", ""),
                name=profile.get("full_name", ""),
                headline=profile.get("headline", ""),
                company=profile.get("company", ""),
                location=profile.get("location", ""),
                about=profile.get("about", "")[:500],
                experience=json.dumps(profile.get("experience", [])[:3]),
                education=json.dumps(profile.get("education", [])[:2]),
                activity="\n".join(profile.get("recent_activity", [])[:2]),
            )

            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=800,
                response_format={"type": "json_object"},
            )

            raw = response.choices[0].message.content or "{}"
            return json.loads(raw)

        except Exception as e:
            print(f"[ResearchBrain] AI call failed: {e}")
            return {
                "lead_score": 0,
                "summary": f"AI analysis failed: {e}",
                "email_draft": "",
                "linkedin_note": "",
                "best_angle": "",
                "pain_points": [],
                "buying_signals": [],
                "decision_maker": False,
                "suggested_subject": "",
            }

    # ------------------------------------------------------------------
    # Persist to database
    # ------------------------------------------------------------------

    async def _persist_findings(
        self,
        session: AsyncSession,
        institution_id: uuid.UUID,
        profile: dict[str, Any],
        analysis: dict[str, Any],
    ) -> None:

        # Create a ResearchJob record
        job = ResearchJob(
            institution_id=institution_id,
            status=JobStatus.COMPLETED,
            objectives=["linkedin_profile_analysis"],
            execution_logs=[f"Analysed profile: {profile.get('profile_url', '')}"],
        )
        job.completed_at = datetime.now(UTC)
        session.add(job)
        await session.flush()

        # Key findings
        findings_to_save = {
            "lead_score": (analysis.get("lead_score", 0), FindingType.INFERENCE),
            "decision_maker": (analysis.get("decision_maker", False), FindingType.INFERENCE),
            "pain_points": (analysis.get("pain_points", []), FindingType.INFERENCE),
            "buying_signals": (analysis.get("buying_signals", []), FindingType.INFERENCE),
            "best_angle": (analysis.get("best_angle", ""), FindingType.INFERENCE),
            "email_draft": (analysis.get("email_draft", ""), FindingType.INFERENCE),
            "linkedin_note": (analysis.get("linkedin_note", ""), FindingType.INFERENCE),
            "summary": (analysis.get("summary", ""), FindingType.INFERENCE),
            "full_name": (profile.get("full_name", ""), FindingType.FACT),
            "headline": (profile.get("headline", ""), FindingType.FACT),
            "company": (profile.get("company", ""), FindingType.FACT),
            "profile_url": (profile.get("profile_url", ""), FindingType.FACT),
        }

        for key, (value, ftype) in findings_to_save.items():
            finding = ResearchFinding(
                institution_id=institution_id,
                job_id=job.id,
                finding_type=ftype,
                finding_key=key,
                finding_value=value,
                evidence=profile.get("profile_url", ""),
                confidence_score=0.85,
            )
            session.add(finding)

        # Create / update AccountBrief
        brief = AccountBrief(
            institution_id=institution_id,
            status=BriefStatus.READY_FOR_REVIEW,
            executive_summary=analysis.get("summary", ""),
            value_hypotheses=analysis.get("pain_points", []),
            stakeholder_ranking=[
                {
                    "name": profile.get("full_name", ""),
                    "role": profile.get("headline", ""),
                    "score": analysis.get("lead_score", 0),
                }
            ],
        )
        session.add(brief)

        print(
            f"[ResearchBrain] ✓ Saved findings for {profile.get('full_name', '?')} "
            f"(score: {analysis.get('lead_score', 0)}/10)"
        )

    async def _research_record(
        self,
        session: AsyncSession,
        record: RawSourceRecord,
    ) -> None:
        payload = record.raw_payload
        # Upsert a minimal CanonicalInstitution if one doesn't exist
        institution = CanonicalInstitution(
            canonical_name=payload.get("full_name", "Unknown"),
            status=OperatingStatus.OPERATIONAL,
        )
        session.add(institution)
        await session.flush()
        await self.research_profile(session, payload, institution.id)
