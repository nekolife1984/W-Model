# 期限リマインダー 詳細設計・契約

## Task

- `TASK-TR-01`：期限・通知可否・送信済み状態から対象を選び、Notifier Portへdispatchする。
- 依存：`TASK-TR-01`はFeature仕様 `REQ-TR-001`〜`REQ-TR-004`、`ADR-TR-001`に依存。
- 完了条件：時間窓の端点、無効/送信済み/期限なしの除外、送信後の一回性、naive datetime拒否をUnit・Integrationで検証。

## Contract `DESIGN-TR-IF-001`

```python
dispatch_due_reminders(
    reminders: Iterable[Reminder],
    now: datetime,
    notifier: Notifier,
) -> tuple[str, ...]
```

- `Reminder`: `reminder_id: str`, `due_at: datetime | None`, `enabled: bool`, `sent: bool`。
- Preconditions：`now`と期限設定値はtimezone-aware。naive `now`は`ValueError`。期限なしは有効入力だが非対象。
- 対象条件：`enabled and not sent and due_at is not None and due_at - 24h <= now < due_at`。
- 順序：入力順を維持する。
- Side effect：各対象に `notifier.send(reminder_id)` を一度呼び、成功後に `sent=True`。返値は送信したIDのtuple。
- Failure：Notifier例外を伝播し、その対象の`sent`は更新しない。例外後の再試行・部分成功の回復・永続性は呼び出し元の責任。
- Concurrency：非並列。複数プロセス間のexactly-once保証なし。

## Integration Test契約

`TEST-TR-INT-001`はFake Notifierと同じReminder状態を使い、窓内の1件を送信後、次回実行では再送しないことを確認する。送信Portが例外を返す場合に状態を誤って送信済みにしないことも確認する。
