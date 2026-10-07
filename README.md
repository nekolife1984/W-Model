# W-Model
Wモデルによる開発ワークフロー

## はじめての試行

このRepositoryには、規約・工程別スキル・統括スキルを使った小規模Featureの試行記録があります。

1. [W-Modelの共通規約](.agents/docs/w-model/00-index.md)で成果物の正本と配置を確認します。
2. [統括ワークフロー](.agents/skills/w-model-workflow/SKILL.md)を読み、開始条件・工程ゲート・停止条件を確認します。
3. [期限リマインダーFeatureの机上試行](docs/w-model-trials/task-reminder/README.md)を要件からQAまで順に読みます。各工程の入力・成果物・独立レビュー手順のシミュレーション・差し戻し記録を追い、意図的な不整合とHuman Gateの停止記録を確認できます。
4. 新しいFeatureでは、試行例をコピーせず、[Feature仕様テンプレート](.agents/templates/w-model/feature-spec.md)などを使って対象Repositoryの正本を作成します。各工程のスキルを独立して実行し、承認が必要な判断が未確定なら人間の回答まで停止します。

統括スキルの呼び出し時は、要求元、対象Repository/branch/base、Feature略号、既存仕様、要件確定者、BDD採否を入力してください。`OPEN`の事項を推測で確定せず、未実施・失敗・BLOCKEDをPASSとして扱わないでください。

規約の入口は[W-Model開発規約](.agents/docs/w-model/00-index.md)、工程スキルの一覧は[統括スキル](.agents/skills/w-model-workflow/SKILL.md)を参照してください。
