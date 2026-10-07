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

1. **工程計画**：要求を読み、必要な工程・開発成果物と対応する検証成果物、依存順、完了条件、独立確認、Human Gateを列挙します。Unit/Integration/System/Acceptance各レベルの適用性を責務・境界・リスクから判断し、N/Aの場合は根拠、残余リスク、代替検証、再評価条件、独立確認者を計画に含めます。環境・権限不足はN/Aにせず未実施/BLOCKEDとして扱います。エンドツーエンド規約の工程状態と記録テンプレートを工程ごとに適用し、全工程が不要な場合は対象リスク・変更範囲から除外理由を記録します。
2. **工程実行**：対応する `w-model-requirements` → `w-model-architecture` → `w-model-task-design` → `w-model-implementation` を起動します。各工程で、まず独立Test Designerが上流正本から検証仕様を先行導出して固定し、次にGeneratorが開発成果物を作成・固定します。その後、開発成果物Reviewerと検証仕様Reviewerがそれぞれ別実行で確認し、Orchestratorが両成果物を照合します。実装段階では、Test Designerが契約に基づくUnit期待結果を先に固定し、実装Generatorは承認済み仕様に基づいてUnitテストコードを実装します。Taskは依存グラフの順で個別に実行します。既存実装の検証などでTest Designerの先行設計を適用できない場合は、入力の受領順と独立性への影響を記録し、影響を評価するまでゲートを通しません。環境が別実行を提供できない場合、Orchestratorは代行せず独立性未達で停止します。
3. **対ゲート**：両成果物の存在・取得可能性・ID/リンク・入力と出力のRevisionを読み戻し、独立確認の判定と必須指摘の状態を記録します。N/A判断は対象責務・リスク、代替検証、再評価条件と独立確認を照合します。どちらか一方の欠落、確認未実施、必須指摘未解決、テスト失敗・判定不能なら当該工程を`差し戻し`または`検証中`のまま停止し、次工程を起動しません。必須テストが環境不足等で未実施ならQAは`BLOCKED`であり、N/Aとして通過させません。通過時は受け入れた入力、開始許可者・日時、次工程へ渡す制約を記録します。開始許可でHuman Gateを代替しません。
4. **開始条件・引き継ぎ**：後続工程の開始前に前工程の対ゲート記録と入力正本を再取得し、対象Revision・承認状態・保留範囲の一致を確認します。通過後に関係Revisionが変わっていたら旧判定を継承せず`変更により再確認待ち`へ戻します。対の片方が欠けた試行（受入仕様なしのFeature仕様、Integration仕様なしの詳細設計など）は、開発成果物が完成していても停止し、欠落を補って独立確認を終えるまで再開しません。
5. **人間判断停止**：仕様の振る舞い・方式・リスク判断がHuman Gate対象なら、選択肢・影響・根拠を人へ示して`承認待ち`で停止します。明示した承認記録と対象仕様Revisionが得られるまで、依存する下流工程を開始しません。承認後に仕様Revisionが変わった場合は旧承認を新Revisionへ適用せず、再承認の要否・根拠・判断者を記録します。
6. **差分レビュー・修正**：開発成果物・検証仕様それぞれの独立レビューを完了し、その後にID・契約・観測値・期待結果を照合します。必須指摘や異なる契約解釈があれば該当成果物へ差し戻し、必要に応じて人間判断へエスカレーションします。差分が変わるたびに同一または別の独立Reviewer/Test Designerに新しいRevisionを渡して再確認し、照合もやり直します。同工程内の修正サイクルは初回生成後最大3回です。提案の採否理由も記録します。
7. **テスト・QA**：実装後にUnit → Integration → System → Acceptanceの適用テストを実行し、`w-model-traceability`と`w-model-qa`を起動して対応・証跡・判定を作成します。QA結果はPASS/FAIL/BLOCKEDの根拠を持ち、Human Gate・PR承認と分離します。
8. **最終ゲート**：すべての必須終了条件、独立レビュー、検証結果、未解決事項、トレーサビリティを対象Revisionで照合します。Human PR Review・マージ・Release承認は権限を持つ人間の判断として引き継ぎます。対象リポジトリに固有の変更管理手順がある場合は、別途その手順も確認します。
9. **状態保存**：工程状態、入力/出力Revision、実行担当・実行ID、検証結果・証跡、テストレベル別の適用性/N/A根拠・代替検証・再評価条件・独立確認、Human Gate、未解決事項、次工程開始可否を規約の工程記録テンプレートで共有作業記録へ記載します。作業項目全体の進捗状態は工程判定と区別して記録します。中断時は規約の再開メモ形式を使用します。

## サブエージェントへの呼び出し

各サブエージェントは別の起動呼び出しで、対象に必要な最小限の情報だけを受け取ります。利用環境の起動形式に応じて、次の共通依頼を役割ごとに作ります。

| 工程 | Test Designerの先行する独立入力・成果 | Generator | Reviewer |
|---|---|---|---|
| 要件・受入 | 要求原文・確定ルール・BDD採否から受入ケースと期待結果を導出 | `w-model-requirements` | 要求原文とFeature仕様 |
| Architecture・System | REQ/AC・非機能要求からSystem Test観点・期待結果を導出 | `w-model-architecture` | REQ/AC・制約とArchitecture |
| Task・詳細設計・Integration | 承認済み上流正本からIntegration境界・前提・期待結果を導出。実装者と分離 | `w-model-task-design` | 要件・ArchitectureとTask契約 |
| 実装・Unit | 承認済み契約からUnitケース・期待結果を導出。実装前に設計を固定 | `w-model-implementation` | 契約と実装差分 |
| 統合・回帰 | 承認済みIntegration/System/Acceptance仕様から適用ケースを選定し、不足仕様を設計。Test Executorは別実行で実行し証跡を記録 | 既存成果物の対象Revisionを固定 | 必要なテスト仕様・差分 |

Test Designerには、期待結果の根拠となる要求・契約正本、ID、Revision、対象範囲を渡します。開発成果物は設計後の照合対象とし、テスト仕様をそのコピーにしません。検証仕様ReviewerはTest Designerとは別実行で、正本から期待結果を再解釈し、曖昧さ・境界値・異常系・矛盾を確認します。Orchestratorは両独立確認の後にのみ開発成果物と検証仕様を照合します。

```text
役割：<Generator / Reviewer / Test Designer / 検証仕様Reviewer / Test Executor>
実行スキル：<w-model-requirements / w-model-architecture / w-model-task-design /
             w-model-implementation / w-model-traceability / w-model-qa>
対象・Revision：<Feature/Task、Repository、branch、base/head SHA>
実行担当・実行ID：<人/エージェント識別子、別起動呼び出しの一意ID>
完了条件：<Issueまたは規約の参照>
入力正本・Revision・受領順：<必要な相対パス、ID、完全なSHAまたはDraft識別子、受領順>
範囲・対象外：<明記>
期待結果の根拠：<Test Designer/Executorは要求・契約正本とID。該当なしは理由>
出力先・形式・Revision：<成果物正本またはレビュー/テスト記録>
取得元・環境：<remote/refまたは共有成果物、環境・バージョン>
制約・停止条件：<権限、OPEN判断、既存差分保護、環境制約>

観測事実と推測を分けてください。対象Revision、変更ファイル、検証コマンドと
実際の結果、必須/提案指摘、未解決事項、次工程への引き継ぎを報告してください。
未実行・失敗を成功扱いせず、成果物が別実行から取得可能か確認してください。
```

ReviewerにはGeneratorの自己評価を渡さず、正本・完了条件・レビュー対象差分を渡します。Test担当には期待結果の正本、テストID、Revision、コマンド、環境条件を渡します。単一の会話内で役割名だけを変更して独立性を主張しません。共有成果物をReviewerが取得できない場合はレビュー未完了です。

各呼び出しの記録には、役割、担当識別子、実行ID（または環境で取得可能な一意の呼び出し識別子）、入力正本・ID・Revision、受領順、出力正本・Revision、期待結果の根拠、検証コマンド・実結果、証跡取得元を含めます。未コミット差分の場合はbase SHA・対象ファイル・diff SHA-256・取得方法も残します。異なる契約解釈を発見した場合は双方の引用箇所・解釈・影響を記録して差し戻し、正本が曖昧ならOPENとしてHuman Gate ownerへ停止します。修正後は新RevisionでTest DesignerまたはGeneratorの再実行、独立レビュー、成果物/仕様の再照合を行い、旧判定を流用しません。

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
- 各役割の実行ID、入力正本・Revision、出力正本・Revision、期待結果根拠と照合結果
- 検証コマンド・実結果・証跡リンク、未実施と理由
- 必須/提案指摘、修正サイクル数、再レビュー結果
- Human Gate/Escalation/OPEN・未解決事項と停止範囲
- 次工程または人間へ渡す具体的な作業

PR提出・マージ・Releaseは個別の完了境界です。マージ依頼がない限りマージせず、Release承認を推定しません。

## 参照

- [エンドツーエンド実行フロー規約](../../docs/w-model/08-end-to-end-workflow.md)
- [W-Model開発規約目次](../../docs/w-model/00-index.md)
- 工程別スキル：`w-model-requirements`、`w-model-architecture`、`w-model-task-design`、`w-model-implementation`、`w-model-traceability`、`w-model-qa`
