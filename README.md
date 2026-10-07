# W-Model

W-Modelは、開発成果物と対応する検証を各工程で対にして作成し、独立レビューと人間の判断で工程をつなぐ開発ワークフローです。このRepositoryでは、W-Modelを既存の開発Repositoryへ導入するための規約・スキル・テンプレートを提供します。

## 目的

要件や設計を先に作り、テストを後から補うのではなく、各開発成果物を作る段階で対応する検証方法と期待結果も設計します。これにより、何を満たすための実装か、どの検証で確認するかを追跡しやすくし、変更時の影響範囲や未確認事項を明確にします。

W-Modelが扱うのは、要件から実装・検証までの開発成果物とその対応です。Issue、PR、ブランチ、コミットなどの作業管理は別の運用ルールで扱います。

## Wモデルの概要

左側で要求を具体化して設計へ落とし込み、実装後、右側で対応する検証を行います。各検証は対応する成果物に照らして設計されます。

| 開発成果物 | 対応する検証 |
|---|---|
| 要件定義（REQ・受入条件） | 受入テスト設計 |
| Architecture（構成・責務・制約） | システムテスト設計 |
| Task分解・詳細設計契約 | 結合テスト設計 |
| 実装 | 単体テスト |

検証結果と成果物間の参照をトレーサビリティで確認し、QAゲートで証跡や未解決事項を整理します。各工程では独立したレビュー・検証を行い、必要な人間の承認（Human Gate）を得てから後続工程へ進みます。要件や設計が変更された場合は影響範囲を評価し、必要なレビュー・検証・承認をやり直します。

## このRepositoryに含まれるもの

- [W-Model開発規約](.agents/docs/w-model/00-index.md)：工程ごとの成果物、検証、ゲート、共通ルール。
- [統括スキル](.agents/skills/w-model-workflow/SKILL.md)：要求からRelease Gateまでの進め方と工程間の引き継ぎ。
- 工程別スキル：要件定義、Architecture、Task設計、実装、QA、トレーサビリティなど。
- テンプレートと導入スクリプト：既存Repositoryへ必要なW-Model関連ファイルを導入。
- [セットアップスキル](.agents/skills/w-model-init/SKILL.md)：利用先の`AGENTS.md`へW-Modelの案内を追加。

## 既存Repositoryへ導入する

Node.js 18以降とPython 3.9以降が必要です。まずdry-runで導入予定と競合を確認します。dry-runは導入先を変更しません。

```sh
npx --yes --package=github:nekolife1984/W-Model w-model-install /path/to/existing-repository --dry-run
```

計画に問題がなければ、`--apply`を指定して適用します。

```sh
npx --yes --package=github:nekolife1984/W-Model w-model-install /path/to/existing-repository --apply
```

導入対象は`scripts/w_model_install_manifest.json`に列挙されたW-Model規約・スキル・テンプレートに限定されます。既存ファイルと内容が異なる場合は全体の書き込みを停止し、差分を表示します。同一ファイルは保持され、再実行できます。`AGENTS.md`と`.agents/project.json`は変更しません。`AGENTS.md`への案内追加は、導入後に`w-model-init`スキルを実行してください。

W-Model Repositoryをclone済みの場合は、次の方法でも実行できます。

```sh
python3 scripts/w_model_install.py /path/to/existing-repository --dry-run
python3 scripts/w_model_install.py /path/to/existing-repository --apply
```

インストーラーのテストはRepositoryルートで実行します。

```sh
python3 -m unittest discover -s scripts/tests -v
```
