"""Small, deterministic deadline-reminder dispatch example for the W-Model trial."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable, Protocol


REMINDER_LEAD_TIME = timedelta(hours=24)


@dataclass
class Reminder:
    """One reminder and the in-memory state needed for sequential dispatch."""

    reminder_id: str
    due_at: datetime | None
    enabled: bool = True
    sent: bool = False


class Notifier(Protocol):
    """Boundary for delivering a reminder."""

    def send(self, reminder_id: str) -> None:
        """Deliver the reminder or raise an exception on failure."""


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


def dispatch_due_reminders(
    reminders: Iterable[Reminder], now: datetime, notifier: Notifier
) -> tuple[str, ...]:
    """Dispatch eligible reminders once, in input order.

    The eligible interval is inclusive at ``due_at - 24 hours`` and exclusive
    at ``due_at``. State is marked sent only after the notifier succeeds.
    Persistence, parallel workers, and delivery retry policy belong to callers.
    """

    _require_aware(now, "now")
    now_utc = now.astimezone(timezone.utc)
    sent_ids: list[str] = []

    for reminder in reminders:
        if reminder.due_at is not None:
            _require_aware(reminder.due_at, "due_at")

        if not reminder.enabled or reminder.sent or reminder.due_at is None:
            continue
        due_at_utc = reminder.due_at.astimezone(timezone.utc)
        if now_utc < due_at_utc - REMINDER_LEAD_TIME or now_utc >= due_at_utc:
            continue

        notifier.send(reminder.reminder_id)
        reminder.sent = True
        sent_ids.append(reminder.reminder_id)

    return tuple(sent_ids)
