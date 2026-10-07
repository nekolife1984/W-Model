# 期限リマインダー Traceability

| REQ | AC | Design | Unit | Integration | Acceptance | System |
|---|---|---|---|---|---|---|
| `REQ-TR-001` | `AC-TR-001` | `DESIGN-TR-IF-001` | `TEST-TR-UNIT-001/002/007/008/009` | `TEST-TR-INT-001` | `TEST-TR-ACC-001` | N/A* |
| `REQ-TR-002` | `AC-TR-002` | `DESIGN-TR-IF-001` | `TEST-TR-UNIT-005` | `TEST-TR-INT-001` | `TEST-TR-ACC-002` | N/A* |
| `REQ-TR-003` | `AC-TR-002/004` | `DESIGN-TR-IF-001` | `TEST-TR-UNIT-005` | `TEST-TR-INT-001` | `TEST-TR-ACC-003` | N/A* |
| `REQ-TR-004` | `AC-TR-003` | `DESIGN-TR-IF-001` | `TEST-TR-UNIT-003/004` | `TEST-TR-INT-001` | `TEST-TR-ACC-002` | N/A* |

`*` System Test N/Aの理由は[Architecture仕様](../30-architecture/task-reminder.md#system-test適用性)。

配送Port failure時の状態は`TEST-TR-INT-002`で検証する（再試行・配送保証自体は対象外）。入力検証は`TEST-TR-UNIT-006`で検証する。

## 確認結果

- 全REQにACと実行可能検証IDを対応付けた。
- 全テストIDはそれぞれUnit/Integration/Acceptance仕様または対応するテストコードに存在する。
- 初回試行の意図的なTraceability欠落は[試行記録](../w-model-trials/task-reminder/06-traceability-qa.md)で検出シミュレーションを保持。本実行版の対応表では解消済み。
