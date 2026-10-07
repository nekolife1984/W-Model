---
name: w-model-qa
description: W-Modelのテスト実行、証跡整理、失敗原因の切り分け、QA/PR・Releaseゲート判定を行う。Human Gate判断は人間へ分離して引き継ぐ。
---

# W-Model QA・テスト運用

## 目的

Feature仕様・テスト設計・実行証跡を照合し、対象Revisionに対するQA判定と残リスクを報告する。QA PASSとHuman Gateの承認を混同せず、判断権限のない未確定事項を推測で承認しない。

## 必須入力

- 対象Repository、Feature/PR、対象Revision（完全なcommit SHA）と比較対象
- 変更範囲、関連REQ/AC、Architecture・詳細設計・Task契約
- テスト方針、各レベルのテスト設計、必須CI・品質ゲート
- 実行可能なテスト、テスト環境・データ・外部依存に関する制約
- トレーサビリティ対応表と過去の失敗・未解決事項

不足が判定を妨げる場合は、確認可能な範囲を先に調査し、不足・影響・必要な判断をBLOCKEDとして示す。対象Revisionが確定しない結果を当該Revisionの成功証跡として扱わない。

## 手順

1. **範囲を固定する**：Repository、対象Revision、変更ファイル、関連REQ/AC、除外範囲を読み戻す。仕様・設計・テストの正本を特定する。
2. **ゲートを特定する**：Feature/Repositoryで定義された必須チェックと適用テストレベルを列挙する。未定義の品質閾値を勝手に追加せず、必要なら未確定事項として提示する。
3. **適用性・設計を照合する**：Unit/Integration/System/Acceptanceの目的、期待結果、環境、データ、Mock/Stub境界を確認する。全REQへの全レベル適用を機械的に要求せず、各レベルの責務・リスク根拠、N/Aの独立確認、代替検証、再評価条件を確認する。小規模・費用・時間・環境不足をN/Aの根拠として認めない。
4. **実行順に検証する**：Unit → Integration → System → Acceptanceの順で、対象変更に適用されるテストを実行する。構成上順序を変えた場合は理由を記録する。既存環境の変更や外部サービスへの操作が必要なら、権限・影響を先に確認する。
5. **結果を分類する**：適用性（適用/N/A）と実行結果（成功/失敗/未実施）を別々に記録する。N/Aは対象固有の責務・リスク根拠、代替検証、再評価条件、独立Reviewerの判定を記録する。未実施は環境・データ等の理由と影響、解消担当または次の行動を記録し、必須テスト未実施ならQAをBLOCKEDにする。環境不足をN/Aにしない。
6. **失敗を診断する**：観測事実、原因仮説、根拠を分けて記録する。要件、Architecture/System、詳細設計/Integration、実装/Unit、テスト欠陥、環境、トレーサビリティ/証跡、セキュリティ/運用の分類から戻り先を示す。不明なら未分類として追加調査を提案する。
7. **証跡を結ぶ**：各結果にテストID/コマンド、対象Revision、実行日時またはCI run ID、環境、結果リンクを付ける。ログをIssue・QAレポートへ丸ごと複製しない。
8. **トレーサビリティを確認する**：REQ/ACとテスト設計・実行結果・適用外理由の対応を確認する。対応表と実行証跡は [Traceability](../../docs/w-model/06-traceability.md) に従う。
9. **ゲートを判定する**：QAレポートを作成し、必須ゲートの失敗・不明なRevision・未解決ブロッカーがあればFAILまたはBLOCKEDとする。PASSでもマージ・リリースやHuman Gateの承認を意味しない。
10. **人間へ引き継ぐ**：Human Gateがあれば、選択肢、影響、根拠、QA判定、対象Revision、保留範囲を提示し、承認者・判断・日時を別記録する。判断を推測しない。

## 出力

規約の [`QAレポート形式`](../../docs/w-model/07-test-operations-and-qa.md#qaレポート形式)に従い、次を報告する。

- 対象Revision・範囲・適用ゲート
- テストレベル別状態と証跡
- 失敗原因・根拠・差し戻し先
- トレーサビリティ結果、適用外と未実行の理由
- N/Aごとの対象Revision、根拠、代替検証、再評価条件、独立確認結果
- QA判定（PASS / FAIL / BLOCKED）と根拠
- Human Gateの判断事項と状態（QA判定と別項目）
- 未解決リスク、担当または次の具体的作業

## 判定規則

- **PASS**：対象範囲が明確で、必須ゲートが成功し、必要な証跡と対応関係が確認でき、未解決ブロッカーがない。
- **FAIL**：実行結果が必須期待値に不適合、または必須ゲートを満たさない。
- **BLOCKED**：必要なテスト・証跡・対象Revision・環境・判断が不足し、合否を確定できない。
- 必須テストの環境・データ不足はテスト状態を未実施、QA判定をBLOCKEDとする。未実施をN/Aと扱わない。
- N/Aの独立確認・代替検証・再評価条件のいずれかが欠ける場合は根拠不足としてFAILまたはBLOCKEDとする。
- 任意検証の未実行を許容する場合は、非必須である根拠、影響、リスク受容者、対応計画を明記する。状態は未実行のまま保つ。
- Human Gateは承認／却下／保留として独立記録する。QA PASSだけでHuman Gateを通過させない。

## 参照

- [テスト運用とQAゲート規約](../../docs/w-model/07-test-operations-and-qa.md)
- [共通原則](../../docs/w-model/01-common-principles.md)
- [要件定義と受入テスト設計](../../docs/w-model/02-requirements-and-acceptance.md)
- [Architectureとシステムテスト設計](../../docs/w-model/03-architecture-and-system-test.md)
- [Task分解と詳細設計・結合テスト](../../docs/w-model/04-task-decomposition-and-detailed-design.md)
- [実装と単体テスト](../../docs/w-model/05-implementation-and-unit-testing.md)
- [トレーサビリティ検証](../../docs/w-model/06-traceability.md)
