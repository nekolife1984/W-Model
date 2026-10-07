---
name: w-model-task-design
description: Featureを依存関係の明確なTaskへ分解し、実装と結合テストが共有する薄い詳細設計契約を作成する。
---

# W-Model Task Design

確定済みのFeature・Architectureを、1 PRで実行・検証できるTaskへ分解し、Taskごとに詳細設計と結合テスト観点を作成します。適用規約は[Task分解と詳細設計・結合テスト](../../docs/w-model/04-task-decomposition-and-detailed-design.md)、共通ルールは[W-Model開発規約](../../docs/w-model/00-index.md)と[共通原則](../../docs/w-model/01-common-principles.md)です。

## 入力

- 確定済みFeature仕様、REQ・AC、関連受入仕様とその承認・保留状態。
- Architecture、外部IF・共通仕様・用語、関連ADRと未確定事項。
- 既存のTask・Story、Feature略号・識別子、Issueの親子・依存関係、成果物配置。
- 実装と結合検証に必要な既存コード・IF情報、テスト環境・データの入手可能性。
- レビュー担当と、未確定事項の判断者。分からない場合は質問として記録します。

必要な要件・IF・状態・データ整合性が未確定で、Taskの完了条件や結合テストを左右する場合は推測で補わずOPENとします。影響ID、質問、必要な決定者を示し、影響を受けるTask・実装・テストの確定を保留します。

## 手順

1. Feature仕様、Architecture、共通規約、既存Issue・設計・テストの正本を確認し、確定範囲、既存ID、制約、未解決事項を列挙します。
2. FeatureをStoryと実装可能な作業候補へ分け、各候補の利用価値・変更境界・REQ/AC・検証方法を対応付けます。独立して1 PRにできない場合は、分割理由、暫定状態、後続統合条件を明記します。
3. `.agents/templates/w-model/task-issue.md`を使い、目的、対象外、完了条件、検証方法、変更範囲、依存先と理由、関連IDを記述します。依存がない場合は明記し、依存グラフの循環と未解決の外部条件を確認します。
4. Taskごとに`.agents/templates/w-model/detailed-design.md`を使い、必要なDESIGN IDを割り当てます。責務・IF・データ・状態・処理順・トランザクション・例外から必要な契約だけを記録し、根拠をREQ/AC・Architecture・共通仕様へリンクします。決定やコードの逐語説明は重複させません。
5. 対応する`.agents/templates/w-model/integration-test-spec.md`を使い、境界と失敗モードからテスト観点を先に作成します。`TEST-<FEATURE>-INT-NNN`、前提、入力・操作、観測点、期待結果、環境・データ・判定方法を定義し、適用しない観点には理由を付けます。
6. Task完了条件から設計・テストへ、またREQ/ACから実装Task・設計・テストへ参照をたどり、IDの重複、参照切れ、検証のない条件、依存漏れを確認します。
7. 作成者とは独立した担当者に、入力文書とTask・設計・テストの同一Revisionを渡してレビューを依頼します。対象Revision、判定、必須・提案指摘と状態を記録し、必須指摘の解消後に影響箇所を再レビューします。
8. 未確定の判断、保留範囲、実装・結合検証の開始可能条件を明記し、関連REQ/AC/DESIGN/TEST ID、依存関係、既知の制約とともに後続担当へ引き継ぎます。

## 完了ゲート

- Task Issue・詳細設計契約と対応するIntegration仕様が同一Revisionで揃い、独立ReviewerがTask完了条件・契約と結合仕様の対応を確認している。
- Integration仕様が欠ける、取得できない、レビュー未実施、契約とテストが不一致、必須指摘未解決の場合はTaskを未完了として実装を開始しない。欠落を補って再レビューする。
- 通過時は成果物パス・DESIGN/TEST ID・Revision、依存、レビュー判定・指摘状態、実装担当へ渡す入力・保留範囲、開始許可者・日時を記録する。必要なHuman Gateは別途確認する。
- Featureの対象範囲がStory / Taskに分かれ、各Taskは限定した変更・1 PR・検証可能な完了条件を持つ。
- 各TaskにREQ/ACとの対応と依存関係があり、依存グラフに循環がない。
- 詳細設計は実装・結合テストで共有する契約を含み、実装の逐語的説明を複製しない。
- 各設計境界に適切な結合テスト観点があり、前提から期待結果と合否を判定できる。
- 独立レビューが実施され、必須指摘が解消されている。レビュー未実施は完了扱いにしない。
- 契約や合否に影響するOPEN事項の影響範囲と進行禁止範囲が明示されている。
- ID、相対リンク、Issue依存、成果物の正本と配置が整合している。

## 出力

- 親Feature / Storyに関連付けたTask Issue（対象RepositoryのIssue運用を使用）。
- 詳細設計契約：`docs/40-design/<feature>/`。
- 結合テスト方針・観点：`docs/50-test/integration/`。
- 実行可能結合テスト（作成対象の場合）：`tests/integration/`。
- 独立レビュー記録：対象Revision、担当、判定、指摘と状態。
- 引き継ぎ情報：関連REQ/AC/DESIGN/TEST ID、依存、OPEN事項、実装・検証の開始可能範囲。

Repositoryに既存の正本やIssue階層がある場合はそれを使用し、同じ契約・シナリオを重複管理しません。
