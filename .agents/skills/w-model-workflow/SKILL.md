---
name: w-model-workflow
description: 要求からRelease GateまでのW-Model工程を調整し、別実行のGenerator/Reviewer/Testと明示的なHuman Gateで接続する。
---

# W-Model Workflow Orchestrator

## 目的

Feature要求を正本・独立検証・ゲートに沿って工程間で引き継ぎます。開始前に[エンドツーエンド実行フロー規約](../../docs/w-model/08-end-to-end-workflow.md)を読み、順序・役割分離・記録・停止条件に従います。工程内の作業はリンク先の工程規約・スキルに従います。

## 入力と初期確認

- 要求元Feature Issue/文書と要求の情報源
- 対象Repository、作業branch、base/head SHA、作業ツリー状態
- 関連仕様・成果物・安定ID、既存テストと実行方法
- 依存Task/Issue、利用可能なサブエージェント・権限・環境
- 要件・方式・PR・ReleaseのHuman Gate ownerと判断方法（未確定は未確定のまま扱う）

開始時に対象Revision、ユーザー変更、未追跡ファイル、Issue/Project状態、依存を読み戻します。依存未完了、対象不明、変更の取得元不明、権限不足がある場合は、確認可能な調査のみ行い該当工程を開始しません。ユーザーの成果物・未追跡ファイルを破棄・上書きしません。

## オーケストレーション手順

1. **工程計画**：必要な工程、成果物と検証の対、依存順、完了条件、独立担当、Human Gateを決めます。テストレベルの適用性・N/A判断は[Architecture規約](../../docs/w-model/03-architecture-and-system-test.md#テストレベル適用性の判断)に従い、除外する工程は対象リスク・変更範囲から理由を記録します。
2. **工程実行**：`w-model-requirements` → `w-model-architecture` → `w-model-task-design` → `w-model-implementation`を依存順に起動します。[工程ごとの実行順序](../../docs/w-model/08-end-to-end-workflow.md#工程ごとのgeneratorreviewertest-designer接続)に従い、独立Test Designerの先行設計・固定、生成、両成果物の独立レビュー、照合を行います。Unit仕様は実装前にレビューします。先行設計できない場合は受領順と独立性への影響を評価するまでゲートを保留します。
3. **対ゲート**：[工程ゲート](../../docs/w-model/08-end-to-end-workflow.md#成果物と検証の対による工程ゲート)で両成果物・Revision・独立確認・指摘状態を照合します。片方の欠落・取得不能、確認未実施、必須指摘未解決、失敗・判定不能なら次工程を起動しません。必須テストの環境不足は未実施/BLOCKEDとし、N/Aにしません。
4. **変更と修正**：新Revisionには旧PASS・承認を流用せず、[変更起点別の影響評価](../../docs/w-model/08-end-to-end-workflow.md#変更起点別の影響評価)を行います。影響なしも根拠・比較Revision・確認者を記録し、不明なら停止します。修正後は独立再レビュー・成果物/仕様の再照合を行い、提案の採否理由も残します。
5. **人間判断**：振る舞い・方式・リスク判断は選択肢・影響・根拠を示し、対象仕様Revisionへの明示承認まで依存工程を停止します。変更後の再承認要否は権限者が判断します。
6. **テスト・QA**：Unit → Integration → System → Acceptanceの適用テストを実行し、`w-model-traceability`と`w-model-qa`を起動します。QA判定とHuman Gate・PR承認は分離します。
7. **最終ゲート**：対象Revisionの終了条件、独立レビュー、検証、未解決事項、Traceabilityを照合し、Human PR Review・マージ・Release承認を権限者へ引き継ぎます。リポジトリ固有の変更管理手順も確認します。

## サブエージェントへの呼び出し

利用環境のサブエージェント機能を使い、カスタムエージェント定義ファイルは作成しません。[呼び出し・引き継ぎ仕様](../../docs/w-model/08-end-to-end-workflow.md#サブエージェント呼び出し引き継ぎ仕様)の依頼形式と[役割の兼務](../../docs/w-model/08-end-to-end-workflow.md#役割の兼務)を適用します。

- Test Designerには要求・契約正本を先に渡し、開発成果物は検証仕様固定後の照合用とします。検証仕様Reviewerは別担当・別実行にします。
- ReviewerにはGeneratorの自己評価を渡さず、正本・完了条件・差分を渡します。
- 別起動の実行IDと共有成果物の取得元を記録します。同じ会話内の役割変更や自己レビューを独立確認とせず、別実行・取得可能性が成立しなければ代行せず停止します。
- 契約解釈が相反する場合は双方の引用・解釈・影響を記録して差し戻し、正本が曖昧ならOPENとしてHuman Gate ownerへ提示します。

## 停止・回復

- **修正上限・早期Escalation**：初回生成後は最大3サイクルとし、回数をリセットしません。要求/設計矛盾、権限者判断、レビュー相反、情報保護・破壊操作の懸念、Revision/共有元不明は上限を待たず停止します。提示内容は[Human Escalation](../../docs/w-model/08-end-to-end-workflow.md#指摘修正回数とhuman-escalation)に従います。
- **失敗・中断・再開**：[回復手順と再開メモ](../../docs/w-model/08-end-to-end-workflow.md#サブエージェント失敗中断再開)を使います。作業ツリー・出力先を確認し、副作用のない一時的な起動失敗のみ同一入力で1回再起動できます。処理状態・副作用不明なら再実行しません。

## 判定と出力

工程ごとに`通過 / 未通過 / BLOCKED`と根拠を報告し、[工程記録テンプレート](../../docs/w-model/08-end-to-end-workflow.md#工程記録テンプレート)へ担当・Revision・証跡・承認・未解決事項・次工程開始可否を保存します。変更時は[変更影響・再確認記録](../../docs/w-model/08-end-to-end-workflow.md#変更影響再確認記録)も残し、修正サイクル数と再レビュー結果を追跡します。作業項目全体の進捗と工程判定は区別します。

全体完了は、対象Revisionの必須工程・検証・Traceability・QA・人間判断が揃った場合に限ります。詳細は[完了判定](../../docs/w-model/08-end-to-end-workflow.md#完了判定)に従います。

PR提出・マージ・Releaseは個別の完了境界です。マージ依頼がない限りマージせず、Release承認を推定しません。

## 参照

- [エンドツーエンド実行フロー規約](../../docs/w-model/08-end-to-end-workflow.md)
- [W-Model開発規約目次](../../docs/w-model/00-index.md)
- 工程別スキル：`w-model-requirements`、`w-model-architecture`、`w-model-task-design`、`w-model-implementation`、`w-model-traceability`、`w-model-qa`
