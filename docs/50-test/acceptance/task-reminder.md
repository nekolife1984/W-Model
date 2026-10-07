# 期限リマインダー 受入仕様

## テスト方針・環境

- 正本：[`docs/10-features/task-reminder.md`](../../10-features/task-reminder.md)
- 実行：`PYTHONPATH=src python3 -m unittest discover -s tests/acceptance -v`
- 固定時刻：`2026-10-10T12:00:00+00:00`。全ケースでaware UTCを使用。
- 外部配送はFake Portに置き換え、呼出しID列を検査する。

## 観点

| 観点 | 対応条件 |
|---|---|
| 最早境界 | `due_at - 24h`ちょうどを含む |
| 遅延実行 | 境界より後〜due直前の最初の実行を含む |
| 最遅境界 | `due_at`ちょうどは含まない |
| 無効・重複 | enabled=falseまたはsent=trueを除外 |
| 期限なし | due_at=Noneを除外 |
| 反復実行 | 成功後の再実行で二重送信しない |

## 受入シナリオ

### `TEST-TR-ACC-001` — 期限窓内で一度通知する

- Given: 有効・未送信の期限付きReminderがある。
- When: 期限24時間前ちょうど、または窓内の後刻にschedulerを実行する。
- Then: IDが1回Notifierへ渡され、送信済みになる。
- 対応：`REQ-TR-001`, `AC-TR-001`, `AC-TR-004`。

### `TEST-TR-ACC-002` — 対象外Reminderを通知しない

- Given: 期限窓外、期限なし、通知無効、送信済みの各状態。
- When: schedulerを実行する。
- Then: Notifier呼出しはなく、除外対象の状態は変化しない。
- 対応：`REQ-TR-002`〜`REQ-TR-004`, `AC-TR-002/003`。

### `TEST-TR-ACC-003` — 再実行で重複通知しない

- Given: `TEST-TR-ACC-001`が送信済み状態を残したReminder。
- When: 同じ時間窓でschedulerを再実行する。
- Then: Notifier呼出しは増えない。
- 対応：`REQ-TR-003`, `AC-TR-004`。
