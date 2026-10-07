# 6. Traceability・QA

## トレーサビリティ表（試行時の欠落を含む）

| 要求 | 受入条件 | 設計 | テスト | 実行証跡 | 状態 |
|---|---|---|---|---|---|
| `REQ-TR-001` | `AC-TR-001` | `DESIGN-TR-001` | `TEST-TR-ACC-001`, `TEST-TR-SYS-001` | なし | BLOCKED（OPEN要件） |
| `REQ-TR-001` | `AC-TR-002` | `DESIGN-TR-001` | `TEST-TR-ACC-002`, `TEST-TR-SYS-002` | なし | BLOCKED（未実行） |
| `REQ-TR-001` | `AC-TR-001` | `DESIGN-TR-IF-001` | 契約 `DESIGN-TR-IF-001` → `TEST-TR-INT-001` の参照が**欠落** | なし | FAIL（意図的欠落） |

## 独立Traceability照合

- 対象：上表とFeature内のID参照。
- 検出 `TRACE-R-01`：`AC-TR-001`から契約 `DESIGN-TR-IF-001` への参照はあるが、契約からIntegration Test `TEST-TR-INT-001` への参照が表にない。
- 判定：**FAIL**。必要なリンクが存在しないため、トレーサビリティ完了と主張できない。
- 戻り先：Traceability工程で対応表を修正し、契約承認後に独立再照合。契約の単位不整合は詳細設計工程、受入期待値は要件工程へ別途差し戻す。

## QA判定

- 対象Revision：この文書試行。製品コードRevisionなし。
- 結果：**BLOCKED**。
- 根拠：要件OPEN、契約FAIL/再レビュー待ち、Traceabilityの欠落、Unit/Integration/System/Acceptanceの実行証跡なし。
- 未実施：実行可能テスト、CI、環境・データ検証。
- QA PASS、PR承認、Release承認はいずれも未取得。QAゲートを通過したとは扱わない。
