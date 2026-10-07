# 期限リマインダー Unit Test仕様

- 対象：`src/task_reminder.py` の時間窓判定、入力検証、順序と状態更新。
- 実行：`PYTHONPATH=src python3 -m unittest discover -s tests/unit -v`

| Case | 入力 | 期待結果 | Trace |
|---|---|---|---|
| `TEST-TR-UNIT-001` | `now = due_at - 24h` | 送信対象 | `REQ-TR-001`, `AC-TR-001` |
| `TEST-TR-UNIT-002` | `due_at - 24h < now < due_at` | 送信対象 | `REQ-TR-001`, `AC-TR-001` |
| `TEST-TR-UNIT-003` | `now < due_at - 24h` | 対象外 | `REQ-TR-004`, `AC-TR-003` |
| `TEST-TR-UNIT-004` | `now >= due_at` | 対象外 | `REQ-TR-004`, `AC-TR-003` |
| `TEST-TR-UNIT-005` | 無効、送信済み、期限なし | 対象外 | `REQ-TR-002/003/004`, `AC-TR-002/003` |
| `TEST-TR-UNIT-006` | naive `now`または`due_at` | `ValueError` | `DESIGN-TR-IF-001` |
| `TEST-TR-UNIT-007` | 異なるoffsetだが同じinstant | 期限窓内として対象 | `BR-TR-001` |
| `TEST-TR-UNIT-008` | DST移行をまたぐ期限24時間前 | 経過時間24hの境界として対象 | `BR-TR-001` |
| `TEST-TR-UNIT-009` | 複数対象を入力 | 入力順を保ってdispatch | `DESIGN-TR-IF-001` |

タイムゾーンが異なっても同じinstantを表すaware datetimeは等価に扱う。夏時間を含む暦日計算はしない。
