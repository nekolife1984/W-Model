# Issue #25: Generator・Reviewer・Test Designer接続の試行記録

## 試行の位置付け

- Feature fixture: `SAVE10` チェックアウト割引
- 対象手順Revision: `6ea3da5b1aea2258976b3ca0c51e57c73a5ea356`（実行時remote head。試行後の文書改訂は後続Revisionで確認）
- 試行方法: 各役割を別のエージェント起動で実行。入力正本と出力要旨をIssueコメントに記録し、ここでは取得・照合に必要なIDと結果を索引化する。
- 制約: Repositoryに対象アプリケーション実装はない。試行したのは要求・契約の解釈、テスト設計・レビュー、差戻し、再確認、算術値の照合であり、実装テストではない。
- 詳細な進捗・試行結果: [Issue #25 試行コメント](https://github.com/nekolife1984/W-Model/issues/25#issuecomment-6033566145)、[独立レビュー記録](https://github.com/nekolife1984/W-Model/issues/25#issuecomment-6033630212)、[Test Executor記録](https://github.com/nekolife1984/W-Model/issues/25#issuecomment-6033552001)

## 入力正本

`SAVE10-REQ-R1` 相当のfixture要求:

> チェックアウトでプロモーションコード SAVE10 を使える。割引率は10%。注文合計に割引を適用してから税を計算し、割引額と最終金額を表示する。送料は税計算前に注文へ加算される。

検討用入力は商品小計100円、送料10円、税率10%、コード有効。v1は割引対象（商品小計のみか、送料込みか）と端数処理を定めていない。

## 別実行と判定

| 役割・実行ID | 入力 | 出力・判定 |
|---|---|---|
| Generator `EED45348-B351-4183-9D5F-777D1A6C3AC1` | 要求fixture v1 | REQ/AC案。割引対象と丸めをOPENにし、金額期待値の確定をBLOCKED。 |
| Test Designer `test-designer-issue25-20261007-01` | 要求fixture v1のみ。Generator出力は初版設計時に未提示。 | 独立ケース案。割引対象の複数解釈（割引10円または11円）と丸めOPENを記録し、金額ゲートをBLOCKED。 |
| 開発成果物Reviewer `FCR-25-20261007-01` | 要求fixture v1とREQ/AC案 | 割引対象と丸めが一意でないためBLOCKED。 |
| Test Designer照合 `test-designer-issue25-20261007-02` | 要求fixture v1、Designer初版、AC-25-2 | ACが送料を注文に加えた後に割引する解釈を含意し得る一方、初版に商品小計だけ割引する解釈例がある差を検出。要件・受入へ差戻し、正本の判断待ちでゲート保留。 |
| 修正Generator `GEN-ISSUE25-SAVE10-20261007-01` | Fixture owner判断（v2） | [`issue-25-save10-requirements-v2.md`](issue-25-save10-requirements-v2.md) に `SAVE10-REQ-R2`、REQ/AC、期待値を保存。割引10円、課税基礎100円、税10円、最終110円。 |
| Test Designer再設計 `TD-ISSUE25-SAVE10-20261007-02` | 正本 `SAVE10-REQ-R2`。Generator出力は設計入力に含めない。 | [`issue-25-save10-test-designer-r2.md`](issue-25-save10-test-designer-r2.md) に新Revisionを基にした独立ケースを保存。期待値10円/100円/10円/110円。v1判定を流用せず。 |
| 検証仕様Reviewer `RVW-ISSUE25-SAVE10-20261007-01` | `SAVE10-REQ-R2`とTest Designer再設計 | 期待値を独立計算して一致を確認。必須指摘なし、提案のみで通過。 |
| Test Executor `EXEC-ISSUE25-SAVE10-20261007-01` | `SAVE10-REQ-R2`、受入ケース、対象手順Revision `6ea3da5b1aea2258976b3ca0c51e57c73a5ea356` | 割引10円→商品小計90円→課税基礎100円→税10円→最終110円を算術照合しPASS。実装コードはなく、ソフトウェア実行ではない。 |

## 試行結果

- Generator、独立Test Designer、開発成果物Reviewer、検証仕様Reviewer、Test Executorを別起動で実施し、役割・入力正本・実行ID・出力要旨・判定を追跡できる。
- Test Designerは要求fixtureを独立解釈して複数の割引対象を示し、Generator成果物との後続照合でAC-25-2の解釈差を検出した。要件・受入へ差し戻し、fixture ownerの判断で正本をv2へ更新した。
- v2の別実行でTest Designerが再設計し、独立した検証仕様Reviewerが新Revisionで期待値を再確認した。旧Revisionの判定は引き継いでいない。
- 実装コードに対するUnit/Acceptance実行は未実施。算術照合を実装テスト完了として扱わない。

## Test Executorの再現手順

アプリケーションと実行コマンドがないため、契約式を手計算で照合した。`割引額=100×0.10=10円`; `割引後商品小計=100−10=90円`; `課税基礎=90+10=100円`; `税=round_half_up(100×0.10)=10円`; `最終額=90+10+10=110円`。期待値と全て一致。入力正本・期待値は上記のv2正本とTest Designer成果物を参照。実行ログおよびソフトウェアテスト結果は存在しない。
