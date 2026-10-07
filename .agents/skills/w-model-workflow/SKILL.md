---
name: w-model-workflow
description: 要求からRelease GateまでのW-Model工程を調整し、別実行のGenerator/Reviewer/Testと明示的なHuman Gateで接続する。
---

# W-Model Workflow Orchestrator

## 目的

Feature要求を正本・独立検証・ゲートに沿って工程間で引き継ぎます。工程の詳細手順は[エンドツーエンド実行フロー規約](../../docs/w-model/08-end-to-end-workflow.md)およびリンク先の工程規約・各スキルを正本とします。カスタムエージェント定義ファイルは作成せず、利用環境のサブエージェント起動機能を使います。

## 入力と初期確認

- 要求元Feature Issue/文書と要求の情報源
- 対象Repository、作業branch、base/head SHA、作業ツリー状態
- 関連仕様・成果物・安定ID、既存テストと実行方法
- 依存Task/Issue、利用可能なサブエージェント・権限・環境
- 要件・方式・PR・ReleaseのHuman Gate ownerと判断方法（未確定は未確定のまま扱う）

開始時に対象Revision、ユーザー変更、未追跡ファイル、Issue/Project状態、依存を読み戻します。依存未完了、対象不明、変更の取得元不明、権限不足がある場合は、確認可能な調査のみ行い該当工程を開始しません。ユーザーの成果物・未追跡ファイルを破棄・上書きしません。

## オーケストレーション手順

1. **工程計画**：要求を読み、必要な工程・成果物・依存順、完了条件、テスト、レビュー、Human Gateを列挙します。全工程が不要な場合は対象リスク・変更範囲から除外理由を記録します。
2. **工程実行**：対応する `w-model-requirements` → `w-model-architecture` → `w-model-task-design` → `w-model-implementation` を起動します。各工程でGeneratorを呼び、その出力を読み戻してから、別実行のReviewer/Test Designerを起動します。Taskは依存グラフの順で個別に実行します。
3. **人間判断停止**：仕様の振る舞い・方式・リスク判断がHuman Gate対象なら、選択肢・影響・根拠を人へ示して停止します。明示した承認記録とRevisionが得られるまで、依存する下流工程を開始しません。
4. **差分レビュー・修正**：独立レビューの必須指摘を対応し、差分が変わるたびに同一または別の独立Reviewerに新しいRevisionを渡して再確認します。同工程内の修正サイクルは初回生成後最大3回です。提案の採否理由も記録します。
5. **テスト・QA**：実装後にUnit → Integration → System → Acceptanceの適用テストを実行し、`w-model-traceability`と`w-model-qa`を起動して対応・証跡・判定を作成します。QA結果はPASS/FAIL/BLOCKEDの根拠を持ち、Human Gate・PR承認と分離します。
6. **最終ゲート**：すべての必須終了条件、独立レビュー、検証結果、未解決事項、トレーサビリティを対象Revisionで照合します。Human PR Review・マージ・Release承認は権限を持つ人間の判断として引き継ぎます。AIDE採用RepositoryではIssue・PR・Projectフローも確認します。
7. **状態保存**：工程、実行担当、修正サイクル、Revision、成果物、実際の検証結果、Human Gate、ブロッカー、次の作業をIssue等の共有作業記録へ記載します。中断時は規約の再開メモ形式を使用します。

## サブエージェントへの呼び出し

各サブエージェントは別の起動呼び出しで、対象に必要な最小限の情報だけを受け取ります。利用環境の起動形式に応じて、次の共通依頼を役割ごとに作ります。

```text
役割：<Generator / Reviewer / Test Designer / Test Executor>
実行スキル：<w-model-requirements / w-model-architecture / w-model-task-design /
             w-model-implementation / w-model-traceability / w-model-qa>
対象・Revision：<Feature/Task、Repository、branch、base/head SHA>
完了条件：<Issueまたは規約の参照>
入力正本：<必要な相対パス、ID、URLだけ>
範囲・対象外：<明記>
出力先・形式：<成果物正本またはレビュー/テスト記録>
制約・停止条件：<権限、OPEN判断、既存差分保護、環境制約>

観測事実と推測を分けてください。対象Revision、変更ファイル、検証コマンドと
実際の結果、必須/提案指摘、未解決事項、次工程への引き継ぎを報告してください。
未実行・失敗を成功扱いせず、成果物が別実行から取得可能か確認してください。
```

ReviewerにはGeneratorの自己評価を渡さず、正本・完了条件・レビュー対象差分を渡します。Test担当には期待結果の正本、テストID、Revision、コマンド、環境条件を渡します。単一の会話内で役割名だけを変更して独立性を主張しません。共有成果物をReviewerが取得できない場合はレビュー未完了です。

## 停止・回復

- **3回の修正上限**：3サイクル後も必須指摘・必須テスト失敗が解消しない場合は停止し、人へ対象Revision、試行結果、選択肢、影響を示します。修正回数をリセットしてループを継続しません。
- **早期Escalation**：要求/設計矛盾、権限者判断、レビューの相反、秘密情報・破壊操作の懸念、Revision/共有元不明があれば即時停止します。
- **サブエージェント失敗**：まず作業ツリーと出力先を確認します。副作用のない一時的な起動失敗のみ同一入力で1回再起動可。処理状態・副作用不明なら再実行せず、状態確認またはHuman Escalationにします。成果物欠落・権限不足・再失敗は工程を未完了として記録します。
- **中断・再開**：工程・担当・Revision・ゲート・修正回数・出力取得元・検証結果・OPEN事項を保存します。再開時にRepository/branch/base/head/作業ツリーと共有元を読み戻し、記録と一致することを確認してから再開します。不一致や所有者不明変更があれば停止し、上書きしません。

## 判定と出力

工程ごとに `通過 / 未通過 / BLOCKED` と根拠を報告します。全体完了は各必須工程が通過し、対象Revisionに対する検証・Traceability・QAが揃い、人間判断が未承認のまま完了扱いされていない場合に限ります。出力には次を含めます。

- 実行工程・担当役割・開始/終了ゲートの結果
- 成果物の正本パス、関連ID、対象Revision
- Generator/Reviewer/Testの分離と取得元
- 検証コマンド・実結果・証跡リンク、未実施と理由
- 必須/提案指摘、修正サイクル数、再レビュー結果
- Human Gate/Escalation/OPEN・未解決事項と停止範囲
- 次工程または人間へ渡す具体的な作業

PR提出・マージ・Releaseは個別の完了境界です。マージ依頼がない限りマージせず、Release承認を推定しません。

## 参照

- [エンドツーエンド実行フロー規約](../../docs/w-model/08-end-to-end-workflow.md)
- [W-Model開発規約目次](../../docs/w-model/00-index.md)
- 工程別スキル：`w-model-requirements`、`w-model-architecture`、`w-model-task-design`、`w-model-implementation`、`w-model-traceability`、`w-model-qa`
