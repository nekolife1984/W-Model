# 期限リマインダー Architecture

## 対象・制約

- 対応：`REQ-TR-001`〜`REQ-TR-004`
- 制約：標準ライブラリのみのサンプル。永続DB、外部通知サービス、実時間スケジューラは含めない。
- 時刻：aware datetimeの瞬間として比較。タイムゾーン付き入力はPythonのdatetime比較で同一時点に正規化される。
- 非機能・運用：単一プロセス、逐次呼び出し、プロセス内状態のみ。並列実行・耐障害性・配送SLAは保証しない。

## 構成・責務

| 要素 | 責務 | 検証 |
|---|---|---|
| `Reminder` | ID、期限、通知可否、送信済み状態を保持 | Unit |
| `dispatch_due_reminders` | 期限窓・有効性・送信済み状態を評価し、Port呼び出しと状態更新を調整 | Unit / Integration |
| `Notifier` Port | 通知送信境界。サンプル実行ではFakeを利用 | Integration / Acceptance |
| 呼び出し元 | 実スケジュール、永続化、再試行を担当（本例では未実装） | 対象外 |

## 設計判断

- `ADR-TR-001`：小規模試行のため、純粋な期限判定とPort注入による逐次dispatchに限定する。永続化や実配信を入れず、境界条件を決定的に検証可能にする。
- 判定状態：このFeatureでは承認済み。承認記録は[Feature仕様](../10-features/task-reminder.md)を参照。

## System Test適用性

System Testは非適用。実行プロセス、外部連携、運用環境を構成せず、対象は単一ライブラリとFake Portで閉じる。期限判定の境界はAcceptance、コンポーネント境界はIntegrationで検証する。実スケジューラ・DB・配信基盤を追加する場合は再評価する。
