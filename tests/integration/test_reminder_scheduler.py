import unittest
from datetime import datetime, timedelta, timezone

from task_reminder import Reminder, dispatch_due_reminders


class FakeNotifier:
    def __init__(self, fail=False):
        self.sent = []
        self.fail = fail

    def send(self, reminder_id):
        if self.fail:
            raise RuntimeError("delivery failed")
        self.sent.append(reminder_id)


class ReminderSchedulerIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.due_at = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)
        self.now = self.due_at - timedelta(hours=12)

    def test_successful_dispatch_persists_once_across_runs(self):
        """TEST-TR-INT-001: send via the port once across scheduler runs."""
        reminder = Reminder("task-1", self.due_at)
        notifier = FakeNotifier()

        first = dispatch_due_reminders([reminder], self.now, notifier)
        second = dispatch_due_reminders([reminder], self.now, notifier)

        self.assertEqual(first, ("task-1",))
        self.assertEqual(second, ())
        self.assertEqual(notifier.sent, ["task-1"])
        self.assertTrue(reminder.sent)

    def test_delivery_failure_propagates_without_marking_sent(self):
        """TEST-TR-INT-002: propagate delivery failure without state mutation."""
        reminder = Reminder("task-1", self.due_at)
        notifier = FakeNotifier(fail=True)

        with self.assertRaisesRegex(RuntimeError, "delivery failed"):
            dispatch_due_reminders([reminder], self.now, notifier)

        self.assertFalse(reminder.sent)
