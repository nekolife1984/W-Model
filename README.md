# W-Model
Wモデルによる開発ワークフロー

## はじめての試行

このRepositoryには、規約・工程別スキル・統括スキルを使った小規模Featureの試行記録があります。

1. [W-Modelの共通規約](.agents/docs/w-model/00-index.md)で成果物の正本と配置を確認します。
2. [統括ワークフロー](.agents/skills/w-model-workflow/SKILL.md)を読み、開始条件・工程ゲート・停止条件を確認します。
3. [期限リマインダーFeatureの初回机上試行](docs/w-model-trials/task-reminder/README.md)で曖昧さ・不整合の検出と差し戻しを確認し、承認後の[Feature仕様](docs/10-features/task-reminder.md)から実装・テスト・QA成果物をたどります。
4. 新しいFeatureでは、試行例をコピーせず、[Feature仕様テンプレート](.agents/templates/w-model/feature-spec.md)などを使って対象Repositoryの正本を作成します。各工程のスキルを独立して実行し、承認が必要な判断が未確定なら人間の回答まで停止します。

統括スキルの呼び出し時は、要求元、対象Repository/branch/base、Feature略号、既存仕様、要件確定者、BDD採否を入力してください。`OPEN`の事項を推測で確定せず、未実施・失敗・BLOCKEDをPASSとして扱わないでください。

このサンプルのUnit・Integration・Acceptanceテストは標準ライブラリの`unittest`で実行できます：

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

テスト仕様は[`docs/50-test/`](docs/50-test/)、対応表は[`docs/90-traceability/task-reminder.md`](docs/90-traceability/task-reminder.md)、実行結果は[QAレポート](docs/50-test/task-reminder-qa.md)と[承認後の工程実行記録](docs/w-model-trials/task-reminder/08-approved-execution.md)を参照してください。

規約の入口は[W-Model開発規約](.agents/docs/w-model/00-index.md)、工程スキルの一覧は[統括スキル](.agents/skills/w-model-workflow/SKILL.md)を参照してください。
