# AIDEの利用案内

ルールの正本は[開発ルール目次](.agents/docs/aide/00_index.md)配下の文書です。

- 開発作業では、[ブランチ](.agents/docs/aide/01-branches.md)・[情報保護](.agents/docs/aide/06-security.md)・[コミット](.agents/docs/aide/08-commit-messages.md)の共通ルールを確認してください。
- Issueの起票・対応、開発変更、レビュー、作業の再開・中断では、[aide-workflowスキル](.agents/skills/aide-workflow/SKILL.md)を読み、該当工程の文書・節を確認してから操作してください。工程別の参照は、共通ルールを省略するためのものではありません。

## GitHub Project

- GitHub Project情報は `.agents/project.json` を参照
- ファイルがないか `project` が `null` の場合は、[aide-initスキル](.agents/skills/aide-init/SKILL.md)でセットアップ
# W-Model 開発規約

Wモデル開発では、成果物と対応する検証を同時に設計します。共通原則、成果物の正本・配置、識別子、AIDEとの責務分担は[W-Model開発規約](.agents/docs/w-model/00-index.md)を参照してください。
