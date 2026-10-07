# W-Model

開発成果物と対応する検証を対にし、独立レビューと人間の判断で工程をつなぐ開発ワークフローです。

- [W-Model開発規約](.agents/docs/w-model/00-index.md)：工程別の規約・スキル・テンプレートの入口。
- [統括スキル](.agents/skills/w-model-workflow/SKILL.md)：要求からRelease Gateまでの進め方。
- [セットアップスキル](.agents/skills/w-model-init/SKILL.md)：利用先の`AGENTS.md`へ開発案内を追加。

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
