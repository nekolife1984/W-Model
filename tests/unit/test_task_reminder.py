import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from task_reminder import Reminder, dispatch_due_reminders


class RecordingNotifier:
    def __init__(self):
        self.sent = []

    def send(self, reminder_id):
        self.sent.append(reminder_id)


class DispatchDueRemindersTests(unittest.TestCase):
    def setUp(self):
        self.due_at = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)
        self.notifier = RecordingNotifier()

    def dispatch(self, now, reminder=None):
        reminder = reminder or Reminder("task-1", self.due_at)
        result = dispatch_due_reminders([reminder], now, self.notifier)
        return reminder, result

    def test_includes_exactly_24_hours_before_due(self):
        """TEST-TR-UNIT-001: include the lower bound of the eligibility window."""
        reminder, result = self.dispatch(self.due_at - timedelta(hours=24))
        self.assertEqual(result, ("task-1",))
        self.assertTrue(reminder.sent)

    def test_includes_first_run_after_window_opens(self):
        """TEST-TR-UNIT-002: include a scheduler run inside the window."""
        _, result = self.dispatch(self.due_at - timedelta(hours=23, minutes=59))
        self.assertEqual(result, ("task-1",))

    def test_excludes_time_before_window(self):
        """TEST-TR-UNIT-003: exclude a run before the window opens."""
        _, result = self.dispatch(self.due_at - timedelta(hours=24, seconds=1))
        self.assertEqual(result, ())
        self.assertEqual(self.notifier.sent, [])

    def test_excludes_due_instant_and_later(self):
        """TEST-TR-UNIT-004: exclude the due instant and expired reminders."""
        for now in (self.due_at, self.due_at + timedelta(seconds=1)):
            with self.subTest(now=now):
                self.notifier.sent.clear()
                _, result = self.dispatch(now)
                self.assertEqual(result, ())

    def test_excludes_disabled_sent_and_missing_due_reminders(self):
        """TEST-TR-UNIT-005: exclude disabled, sent, and undated reminders."""
        reminders = [
            Reminder("disabled", self.due_at, enabled=False),
            Reminder("sent", self.due_at, sent=True),
            Reminder("missing", None),
        ]
        result = dispatch_due_reminders(
            reminders, self.due_at - timedelta(hours=1), self.notifier
        )
        self.assertEqual(result, ())
        self.assertEqual(self.notifier.sent, [])

    def test_compares_instants_across_timezones(self):
        """TEST-TR-UNIT-007: compare aware timestamps by instant."""
        equivalent_due = self.due_at.astimezone(timezone(timedelta(hours=9)))
        reminder = Reminder("task-1", equivalent_due)
        _, result = self.dispatch(self.due_at - timedelta(hours=24), reminder)
        self.assertEqual(result, ("task-1",))

    def test_uses_elapsed_hours_across_daylight_saving_transition(self):
        """TEST-TR-UNIT-008: treat 24 hours as elapsed time across DST."""
        new_york = ZoneInfo("America/New_York")
        due_at = datetime(2026, 3, 9, 2, 30, tzinfo=new_york)
        exactly_24_hours_before = datetime(2026, 3, 8, 1, 30, tzinfo=new_york)
        reminder = Reminder("dst-task", due_at)

        result = dispatch_due_reminders(
            [reminder], exactly_24_hours_before, self.notifier
        )

        self.assertEqual(result, ("dst-task",))

    def test_preserves_input_order_for_multiple_eligible_reminders(self):
        """TEST-TR-UNIT-009: return dispatched IDs in input order."""
        reminders = [
            Reminder("task-b", self.due_at),
            Reminder("task-a", self.due_at),
        ]

        result = dispatch_due_reminders(
            reminders, self.due_at - timedelta(hours=12), self.notifier
        )

        self.assertEqual(result, ("task-b", "task-a"))
        self.assertEqual(self.notifier.sent, ["task-b", "task-a"])

    def test_rejects_naive_now(self):
        """TEST-TR-UNIT-006: reject naive scheduler and deadline timestamps."""
        cases = (
            ([Reminder("task-1", self.due_at)], datetime(2026, 10, 9, 12), "now"),
            ([Reminder("task-1", datetime(2026, 10, 10, 12))], self.due_at, "due_at"),
        )
        for reminders, now, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    dispatch_due_reminders(reminders, now, self.notifier)

if __name__ == "__main__":
    unittest.main()
