from lead_harvester.intelligence.detection_status import (
    compute_lms_detection_status,
    compute_website_detection_status,
)
from lead_harvester.models.profile import DetectionStatus
from lead_harvester.models.signal import Signal, SignalType
from lead_harvester.models.source import RawPageSnapshot


def _successful_snapshot(html: str = "<html>hi</html>") -> RawPageSnapshot:
    return RawPageSnapshot(url="https://x.edu", html=html, fetch_error="")


def _failed_snapshot() -> RawPageSnapshot:
    return RawPageSnapshot(url="https://x.edu", html=None, fetch_error="http_error: 500")


def _lms_signal() -> Signal:
    return Signal(signal_type=SignalType.TECHNOLOGY_PRESENT, signal_text="Has a parent portal.")


class TestWebsiteDetectionStatus:
    def test_no_website_is_unknown_not_absent_confirmed(self):
        # Correction: this system has no source that exhaustively confirms
        # a genuine absence of any website -- a blank field means "we
        # don't know," never "confirmed missing."
        assert compute_website_detection_status(None, []) == DetectionStatus.UNKNOWN
        assert compute_website_detection_status("", []) == DetectionStatus.UNKNOWN

    def test_website_known_but_never_crawled(self):
        assert compute_website_detection_status("https://x.edu", []) == DetectionStatus.NOT_CRAWLED

    def test_website_known_with_successful_snapshot_is_present(self):
        assert (
            compute_website_detection_status("https://x.edu", [_successful_snapshot()])
            == DetectionStatus.PRESENT
        )

    def test_website_known_but_every_fetch_failed(self):
        assert (
            compute_website_detection_status("https://x.edu", [_failed_snapshot()])
            == DetectionStatus.CRAWL_FAILED
        )

    def test_one_successful_snapshot_among_failures_is_present(self):
        assert (
            compute_website_detection_status(
                "https://x.edu", [_failed_snapshot(), _successful_snapshot()]
            )
            == DetectionStatus.PRESENT
        )

    def test_never_returns_absent_confirmed(self):
        # [Certain]: a static crawler can never confirm absence on its
        # own -- no combination of inputs to this function should produce
        # ABSENT_CONFIRMED.
        for website in (None, "", "https://x.edu"):
            for snapshots in ([], [_failed_snapshot()], [_successful_snapshot()]):
                assert (
                    compute_website_detection_status(website, snapshots)
                    != DetectionStatus.ABSENT_CONFIRMED
                )


class TestLmsDetectionStatus:
    def test_lms_signal_present_is_present(self):
        assert (
            compute_lms_detection_status("https://x.edu", [_successful_snapshot()], [_lms_signal()])
            == DetectionStatus.PRESENT
        )

    def test_lms_signal_wins_even_without_a_website_on_file(self):
        # A researcher-sourced signal (e.g. LinkedIn) could exist even
        # when no website was ever discovered for this institution.
        assert compute_lms_detection_status(None, [], [_lms_signal()]) == DetectionStatus.PRESENT

    def test_no_website_and_no_signal_is_not_crawled(self):
        assert compute_lms_detection_status(None, [], []) == DetectionStatus.NOT_CRAWLED

    def test_website_known_but_never_crawled_is_not_crawled(self):
        assert compute_lms_detection_status("https://x.edu", [], []) == DetectionStatus.NOT_CRAWLED

    def test_every_fetch_failed_is_crawl_failed(self):
        assert (
            compute_lms_detection_status("https://x.edu", [_failed_snapshot()], [])
            == DetectionStatus.CRAWL_FAILED
        )

    def test_real_crawl_with_no_lms_mention_is_not_detected_not_absent(self):
        # [Certain]: this is the core case the correction targets -- a
        # genuine, successful crawl that found nothing must NOT be
        # confused with a confirmed absence (an authenticated student
        # portal or JS-rendered dashboard is invisible to this crawler).
        assert (
            compute_lms_detection_status("https://x.edu", [_successful_snapshot()], [])
            == DetectionStatus.NOT_DETECTED
        )

    def test_non_lms_technology_signal_does_not_count_as_present(self):
        other_signal = Signal(
            signal_type=SignalType.TECHNOLOGY_PRESENT, signal_text="Uses some unrelated widget."
        )
        assert (
            compute_lms_detection_status("https://x.edu", [_successful_snapshot()], [other_signal])
            == DetectionStatus.NOT_DETECTED
        )

    def test_never_returns_absent_confirmed(self):
        # [Certain]: same guarantee as the website function -- no crawler-
        # only evidence combination should ever produce ABSENT_CONFIRMED.
        for website in (None, "", "https://x.edu"):
            for snapshots in ([], [_failed_snapshot()], [_successful_snapshot()]):
                assert (
                    compute_lms_detection_status(website, snapshots, [])
                    != DetectionStatus.ABSENT_CONFIRMED
                )

    def test_historical_snapshot_with_lms_html_but_no_signal_row_is_present(self):
        # Correction: a snapshot crawled BEFORE Module 20's
        # TECHNOLOGY_PRESENT signal detection existed has no Signal row
        # even when its stored HTML plainly shows an LMS -- an empty
        # signal list there means "this detection rule never ran," not
        # "it ran and found nothing." Recomputation must re-derive
        # PRESENT from the HTML itself, not mistake the missing Signal
        # row for a genuine non-detection.
        snapshot = _successful_snapshot(html="<html><body>Login to Moodle here</body></html>")
        assert (
            compute_lms_detection_status("https://x.edu", [snapshot], []) == DetectionStatus.PRESENT
        )

    def test_historical_snapshot_with_no_lms_html_stays_not_detected(self):
        # The re-scan must not turn every historical crawl into PRESENT --
        # only ones whose stored HTML actually contains LMS evidence.
        snapshot = _successful_snapshot(html="<html><body>Welcome to our school</body></html>")
        assert (
            compute_lms_detection_status("https://x.edu", [snapshot], [])
            == DetectionStatus.NOT_DETECTED
        )
