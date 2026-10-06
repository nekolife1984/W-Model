# 共通原則と成果物管理

## Wモデルと検証の対応

開発成果物を作成するときに、その成果物を確認する検証観点・期待結果も設計します。テストレベルは対象に応じて選び、各Featureの仕様で具体化します。

| 開発成果物 | 主な検証 | 主な確認内容 | 規定・成果物の配置 |
|---|---|---|---|
| 機能仕様・REQ・AC | 受入テスト | 利用者の要求、業務ルール、受入条件を満たすか | `docs/10-features/`、対応する受入仕様は`docs/50-test/acceptance/` |
| Architecture・システム要件 | システムテスト | システム全体、外部連携、非機能要件を満たすか | `docs/30-architecture/`、`docs/50-test/system/` |
| 詳細設計・コンポーネント契約 | 結合テスト | コンポーネント間の契約、境界、相互作用が正しいか | `docs/40-design/<feature>/`、`docs/50-test/integration/` |
| 実装コード | 単体テスト | 局所ロジックと境界条件が正しく動くか | 実装は`src/`、実行可能テストは`tests/unit/` |

テスト方針・データは`docs/50-test/`、重要な設計判断は`docs/60-adr/`、成果物間の対応表は`docs/90-traceability/`に置きます。必要なディレクトリやファイルがまだない場合は、変更に必要な範囲で作成します。受入・システム・結合テストの実行可能なコードはそれぞれ`tests/acceptance/`、`tests/system/`、`tests/integration/`に置きます。

## 正本（SSOT）と配置

| 情報 | 正本 | ルール |
|---|---|---|
| 共通開発規約 | `.agents/docs/w-model/` | 適用範囲を横断する規則を置く。 |
| 機能仕様、REQ、AC、業務ルール | `docs/10-features/<feature>.md` | Featureの期待動作の正。共通仕様は`docs/20-common/`に置き、Featureから参照する。 |
| Architectureとシステム制約 | `docs/30-architecture/` | システム構成、責務、外部連携、非機能上の制約を記録する。 |
| 詳細設計・コンポーネント契約 | `docs/40-design/<feature>/` | 実装・結合テストに必要なIF、状態、シーケンス、エラーなどを記録する。コードの逐語的な説明は重複して書かない。 |
| 重要な設計判断と理由 | `docs/60-adr/` | Architecture Decision Recordとして記録する。 |
| テスト方針・検証観点 | `docs/50-test/` | 検証の設計と期待結果を記録する。 |
| 詳細実装と実行可能な検証 | `src/`、`tests/` | コードとテストを実行時の振る舞いの正とする。文書に実装を複製しない。 |
| 成果物間の対応 | `docs/90-traceability/` | REQからAC・設計・テストへの参照と状態を示す。 |
| Issueの作業範囲・進捗、PRの変更・レビュー | GitHub Issue・Pull Request | 作業単位、承認、レビューと進捗の記録に使う。仕様の正本にはしない。 |

ディレクトリ名は標準配置です。既存Repositoryに確立した配置がある場合は同じ情報の二重管理をせず、規約と対応表で既存の正本を明示します。変更内容と決定理由は必要に応じてADRやIssueへ記録します。

## 識別子と参照

識別子は成果物の内容から独立した安定IDとし、文書を移動・改題しても再利用・改名しません。Feature略号はRepository内で一意に定め、文書名や相互参照にも同じ略号を使います。

| 種別 | 形式 | 例 |
|---|---|---|
| 要件 | `REQ-<FEATURE>-NNN` | `REQ-CI-001` |
| 受入条件 | `AC-<FEATURE>-NNN` | `AC-CI-001` |
| 詳細設計要素 | `DESIGN-<FEATURE>-NNN` | `DESIGN-CI-001` |
| テストケース | `TEST-<FEATURE>-<LEVEL>-NNN` | `TEST-CI-ACC-001`、`TEST-CI-INT-001`、`TEST-CI-SYS-001`、`TEST-CI-UNIT-001` |

`<FEATURE>`は大文字英数字のFeature略号、`NNN`は種別・Feature内で重複しない3桁以上の連番です。テストレベルは`ACC`（受入）、`SYS`（システム）、`INT`（結合）、`UNIT`（単体）を使います。既存テストランナーの命名制約がある場合、テスト名・メタデータからこのIDを追跡可能にします。

識別子は正本に一度だけ定義し、参照先ではIDと相対リンクを併記します。各REQには検証可能なACを、各ACには一つ以上の受入検証を対応させます。設計要素・他のテストレベルが必要なREQには対応するDESIGN・TEST IDを記録し、`docs/90-traceability/`で関係と未対応状態を確認できるようにします。削除・廃止したIDは再利用せず、正本に廃止を記録します。

## AIDEとの責務分担

| 管理対象 | 正本・責務 |
|---|---|
| Wモデルの原則、成果物の検証対応、仕様・設計・テストの内容 | この規約と`docs/`。各成果物の内容と技術的な正しさを扱う。 |
| 作業範囲、担当、依存、進捗、ブランチ、コミット、レビュー、PR、Project Status | AIDEのIssue・Pull Request・Projectと開発ルール。変更の進め方・承認・追跡を扱う。 |
| 実装と実行可能な検証 | `src/`と`tests/`。実際の振る舞いの正本を保つ。 |

IssueやPRは作業・レビューを管理し、仕様の代わりにはしません。Issue・PRから対象のREQ・AC・DESIGN・TEST IDと文書へリンクし、文書側にも変更理由を追跡するためのIssue・PR参照を必要に応じて記録します。レビューの記録・Status遷移は[AIDE開発ルール](../aide/00_index.md)に従います。

## 参考レポートとの対応

| レポート | 本規約 |
|---|---|
| [第1章 Wモデルの基本](../../../AI_WModel_Development_Report.md#1-wモデルの基本) | 「Wモデルと検証の対応」 |
| [第4章 仕様書ファイルの分割方針](../../../AI_WModel_Development_Report.md#4-仕様書ファイルの分割方針) | 「正本（SSOT）と配置」「識別子と参照」 |
| [第6章 推奨ドキュメント構成](../../../AI_WModel_Development_Report.md#6-推奨ドキュメント構成) | 「正本（SSOT）と配置」 |
| [第12章 推奨Repository構成](../../../AI_WModel_Development_Report.md#12-推奨repository構成) | 「正本（SSOT）と配置」 |
| [第13章 最終的な設計原則](../../../AI_WModel_Development_Report.md#13-最終的な設計原則) | 「変更時の原則」「AIDEとの責務分担」 |

レポートは設計背景の参考資料です。運用時の規則は本規約を正本とします。
