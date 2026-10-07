import unittest
from datetime import datetime, timedelta, timezone

from task_reminder import Reminder, dispatch_due_reminders


class FakeNotifier:
    def __init__(self):
        self.sent = []

    def send(self, reminder_id):
        self.sent.append(reminder_id)


class TaskReminderAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.due_at = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)
        self.notifier = FakeNotifier()

    def test_enabled_task_is_sent_on_first_scheduler_run_in_window(self):
        """TEST-TR-ACC-001: send at the lower bound and at a later first run."""
        for reminder_id, first_run in (
            ("at-boundary", self.due_at - timedelta(hours=24)),
            ("inside-window", self.due_at - timedelta(hours=12)),
        ):
            with self.subTest(reminder=reminder_id):
                reminder = Reminder(reminder_id, self.due_at)
                sent = dispatch_due_reminders([reminder], first_run, self.notifier)
                self.assertEqual(sent, (reminder_id,))
                self.assertTrue(reminder.sent)
        self.assertEqual(self.notifier.sent, ["at-boundary", "inside-window"])

    def test_disabled_already_sent_and_outside_window_tasks_are_not_sent(self):
        """TEST-TR-ACC-002: do not send disabled, sent, or out-of-window reminders."""
        reminders = [
            Reminder("disabled", self.due_at, enabled=False),
            Reminder("already-sent", self.due_at, sent=True),
            Reminder("too-early", self.due_at),
            Reminder("expired", self.due_at),
            Reminder("undated", None),
        ]
        now_by_id = {
            "disabled": self.due_at - timedelta(hours=12),
            "already-sent": self.due_at - timedelta(hours=12),
            "too-early": self.due_at - timedelta(hours=25),
            "expired": self.due_at,
            "undated": self.due_at - timedelta(hours=12),
        }

        for reminder in reminders:
            with self.subTest(reminder=reminder.reminder_id):
                result = dispatch_due_reminders(
                    [reminder], now_by_id[reminder.reminder_id], self.notifier
                )
                self.assertEqual(result, ())

        self.assertEqual(self.notifier.sent, [])

    def test_second_run_does_not_send_duplicate(self):
        """TEST-TR-ACC-003: repeated scheduler runs do not duplicate delivery."""
        reminder = Reminder("task-1", self.due_at)
        now = self.due_at - timedelta(hours=12)

        dispatch_due_reminders([reminder], now, self.notifier)
        dispatch_due_reminders([reminder], now, self.notifier)

        self.assertEqual(self.notifier.sent, ["task-1"])


if __name__ == "__main__":
    unittest.main()
