---
name: w-model-requirements
description: Feature要求をREQ・AC・業務ルール・受入仕様へ整理し、独立レビューとHuman Gateのための成果物を作る。
---

# W-Model Requirements

Feature要求を、追跡可能で受入検証できる仕様へ整理します。適用規約は[要件定義と受入テスト設計](../../docs/w-model/02-requirements-and-acceptance.md)、共通ルールは[W-Model開発規約](../../docs/w-model/00-index.md)と[共通原則](../../docs/w-model/01-common-principles.md)です。成果物の配置はこれらの正本に従います。

## 入力

- Feature要求またはIssueとその背景・情報源
- 関連するFeature仕様、共通仕様、用語集、適用可能な制約
- RepositoryのFeature ID略号・既存ID
- BDD採用の有無（未決なら人間へ確認し、勝手に決めない）
- 人間の要件確定者と承認方法（分からなければ未確定として記録）

入力にない業務判断を事実として作らず、必要な情報が不足していても、確認事項と影響を明記したドラフトを作成します。

## 手順

1. 既存仕様・共通ルール・識別子を確認し、正本と関連情報源を列挙する。Feature略号の重複があれば新規IDを発行せず解決を依頼する。
2. 要求を目的、利用者、スコープ、制約、業務ルール、例外、非機能要求に整理する。重複・矛盾・曖昧さ・情報不足を明示し、要求の出典へつなぐ。
3. 各要求に一意な `REQ-<FEATURE>-NNN` を割り当て、利用者の目的と観測可能な振る舞いで記述する。実装方法を要求として固定しない。
4. 各REQに一つ以上の `AC-<FEATURE>-NNN` を作り、前提・操作・期待結果と境界・失敗時の結果を具体化する。各ACが対応するREQを明記する。
5. 業務ルールをFeature固有の仕様と共通仕様に分ける。共通仕様の正本へ相対リンクし、参照先がない、または記載が矛盾する場合はOPENで記録する。
6. ACごとに受入観点を作り、ケースへ落とす。BDD採用時は `tests/acceptance/<feature>.feature` を実行可能仕様とし、非採用時は `docs/50-test/acceptance/<feature>.md` を仕様とする。TEST IDとREQ/AC IDを相互に追跡可能にする。
7. `.agents/templates/w-model/feature-spec.md`を基に `docs/10-features/<feature>.md` を作成または更新する。BDD採用時は必要に応じて`acceptance.feature`テンプレート、非採用時は`acceptance-spec.md`テンプレートを使う。同じScenarioを複数の正本へ複製しない。
8. 別の担当者・サブエージェントに、要求原文・参照仕様・Feature仕様・受入仕様だけを渡して独立レビューを依頼する。曖昧さ、矛盾、欠落、受入観点の実施可能性、未確定事項の隠れを確認してもらう。
9. レビュー指摘を必須・提案に分けて記録し、必須指摘を解消する。指摘対応によりREQ/ACが変われば対応する受入ケースと相互参照を更新し、影響箇所を再レビューする。
10. 未確定事項をOPENのまま一覧化し、影響範囲・質問・判断者を人間へ提示する。仕様のHuman Gateでは人間の決定と承認対象Revisionを記録する。

## 後続工程へのゲート

- 同一RevisionのFeature仕様と受入仕様を独立Reviewerが確認し、REQ→AC→受入ケース・期待結果を有効なID・リンクで追跡できることを確認します。
- 成果物の欠落・取得不能、独立レビュー未実施、受入判定不能、対応漏れ・参照切れ、必須指摘未解決なら停止し、Architecture工程を開始しません。
- 振る舞い・制約・受入判定に影響するOPEN事項は人間の判断を待ち、承認範囲と進行禁止範囲を分けます。
- 通過・承認・引き継ぎの記録は[要件・受入ゲート](../../docs/w-model/02-requirements-and-acceptance.md#要件受入ゲート)に従います。

## 出力と引き継ぎ

- Feature仕様: `docs/10-features/<feature>.md`
- 受入仕様: BDDなら `tests/acceptance/<feature>.feature`、非BDDなら `docs/50-test/acceptance/<feature>.md`
- 実施可能なテストコード: `tests/acceptance/`（プロジェクトのテスト構成に従う）
- 仕様レビュー結果: 対象Revision、担当、判定、必須・提案指摘と状態
- Human Gate記録: 承認者、日付、承認対象Revision、決定済み・保留の事項
- 次工程への引き継ぎ: 確定済みREQ/AC ID、制約・参照、関連受入テスト、残る判断事項

## 呼び出し例

```text
次のFeature要求を w-model-requirements スキルに従って整理してください。
要求元: <Issue URLまたは要求文>
Feature略号: <Repository内で一意な略号>
BDD: <採用／非採用／未決>
参照仕様: <関連リンク、または未確認>
要件確定者: <担当者、または未確定>

BDDや要件が未決の場合は推測で選ばず、確認事項として提示してください。
振る舞いに影響する未確定事項が残る場合は、Human Gateで停止してください。
```

詳細なREQ/AC例、レビュー観点、BDDと非BDDの仕様例は[要件定義規約](../../docs/w-model/02-requirements-and-acceptance.md)を参照してください。
