# 期限リマインダー 結合テスト仕様

## 対象・方針

- 対象契約：[`DESIGN-TR-IF-001`](../../40-design/task-reminder.md#contract-design-tr-if-001)
- 境界：dispatcher → Notifier Port、dispatcher → Reminder送信状態。
- 環境：プロセス内ReminderとFake Notifier。DB・ネットワーク配送は含まない。
- 実行：`PYTHONPATH=src python3 -m unittest discover -s tests/integration -v`

## ケース `TEST-TR-INT-001` — Port呼出しと一回性

- Given: 期限窓内・有効・未送信のReminderとFake Notifier。
- When: dispatcherを2回実行。
- Then: Fake NotifierはIDを1回だけ受け取り、Reminder.sentはtrue。
- Given: Notifierが例外を送出。
- Then: 例外は呼出し元へ伝播し、該当Reminder.sentはfalseのまま。
- 対応：`DESIGN-TR-IF-001`, `REQ-TR-001/003`, `AC-TR-004`。

## ケース `TEST-TR-INT-002` — 配送Port失敗時の状態

- Given: 対象Reminderと例外を送出するFake Notifier。
- When: dispatcherを実行する。
- Then: 例外が伝播し、Reminder.sentはfalseのまま。
- 対応：`DESIGN-TR-IF-001`のFailure契約。

## 未検証事項

複数workerの競合、プロセス再起動後の永続性、配信先の受理/重複挙動は対象外。
