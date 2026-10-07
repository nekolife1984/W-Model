---
name: w-model-architecture
description: 確定範囲の要件をシステム構成・制約へ落とし込み、Architecture判断と対応するシステムテストを設計する。
---

# W-Model Architecture

Feature要求をシステム全体の構成・責務・制約へ展開し、Architectureに対応するシステムテスト観点を同時に作成します。適用規約は[Architectureとシステムテスト設計](../../docs/w-model/03-architecture-and-system-test.md)、共通ルールは[W-Model開発規約](../../docs/w-model/00-index.md)と[共通原則](../../docs/w-model/01-common-principles.md)です。

## 入力

- Feature仕様のREQ・AC、関連受入仕様と承認・保留状態。
- 現行Architecture、用語、既存ADR、外部システム・運用条件と各情報源。
- Feature略号・既存識別子、成果物配置、Architecture判断の決定者・承認方法。
- システムテストを実行する環境、データ、外部連携の利用可能性（不明なら質問）。

振る舞い・合否・構成に影響する入力が未確定なら、推測で確定させず、影響ID、質問、必要な決定者をOPEN事項にします。影響する設計・テストや次工程を保留し、利用可能な承認済み範囲だけを明示します。

## 手順

1. 共通規約、Feature要件、既存Architecture・ADR・用語を確認し、出典と正本を列挙する。未確認の情報を事実として補わない。
2. REQ/ACの確定・保留状態と、システム境界・利用者・外部依存・運用上の制約を整理する。不明点、矛盾、影響するIDと確認先を記録する。
3. `.agents/templates/w-model/architecture-spec.md`を使い、主要構成、責務、境界、データ・制御の関係、品質属性、外部依存、運用・障害制約をREQ/AC IDへ対応付ける。Architectureの要素は見出し・相対リンクで参照し、詳細設計要素ID（DESIGN）は詳細設計に用いる。詳細な内部実装の説明を避ける。
4. 重要な選択ごとに影響・制約・代替案・トレードオフを整理する。`.agents/templates/w-model/adr.md`に`Proposed` ADRを作成し、承認者が不明なら未確定として提示する。承認なしに`Accepted`へ変更しない。
5. `.agents/templates/w-model/system-test-spec.md`を使い、Architecture・REQ・ACに対応するシステムテスト方針と観点を作成する。正常・境界・外部連携・障害・復旧・該当するセキュリティ/性能/可用性/運用条件を検討し、非該当理由も記録する。
6. 各テストに安定した`TEST-<FEATURE>-SYS-NNN`を付け、前提、刺激・負荷・環境、観測点、期待結果、計測・合否方法と必要なデータを具体化する。非機能指標・閾値の情報源を示し、未承認の候補値はOPENとし合否基準にしない。
7. Architecture制約・重要判断・REQ/AC・TEST IDの参照を相互に確認する。実行可能テストを作る場合は`tests/system/`に置き、Markdownと同一ケースを二重管理しない。
8. 作成者とは別の担当者へ要件・Architecture・ADR案・システムテスト成果物を渡して独立レビューを依頼する。対象Revision、判定、必須・提案指摘と状態を記録し、必須指摘を解消した後に影響箇所を再レビューする。
9. 重要判断、承認待ち、未確定事項を人間へ提示する。承認者・日付・対象Revisionと、決定事項・保留範囲を記録し、Architecture・テストに反映する。
10. 次工程へ、承認済みのArchitecture制約・ADR、関連REQ/AC/DESIGN/TEST ID、テスト環境・データ、未解決事項と進行禁止範囲を引き継ぐ。

## 完了ゲート

- 境界、構成要素、責務、外部依存、制約が根拠付きで説明でき、REQ/ACと結び付いている。
- 該当する非機能要求に測定条件・期待結果・合否基準があり、システムテストから追跡できる。未確定の指標や閾値はOPENで、合否判定に使っていない。
- 重要判断はADRに背景・代替案・影響があり、未承認なら`Proposed`のままである。
- 独立レビューが実施され、必須指摘が解消されている。レビュー未実施を完了扱いにしない。
- 構成・合否に影響するOPEN事項がある場合、その影響範囲と人間の判断待ちを示し、該当する確定・後続工程を保留している。
- ID・相対リンクが有効で、成果物の正本と実行可能テストの配置が明確である。

## 出力

- Architecture：`docs/30-architecture/<feature>.md`
- システムテスト方針・観点：`docs/50-test/system/<feature>.md`
- 重要な設計判断：`docs/60-adr/ADR-NNN-<short-title>.md`
- 実行可能システムテスト（採用する場合）：`tests/system/`
- 独立レビュー記録：対象Revision、担当、判定、指摘と状態
- Human Gate・次工程引き継ぎ：承認者、日付、対象Revision、決定・保留事項、関連IDと進行可能範囲

成果物の実ファイル名や既存配置がRepositoryで確立している場合は、それを正本として使用し、二重管理しません。
