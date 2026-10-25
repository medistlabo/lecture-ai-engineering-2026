# 第1回 解答

## 演習

- 講座に固有の質問（宿題の3レベル）へのモデルの回答（要約でよい）：
- 用語集の正しい意味と比べて気づいたこと：
- 表示できたトークン数（入力 / 出力）：

## 宿題

- 取り組んだレベル：基礎
- やったこと：モデルを変えて出力の確認を行った。
- 結果：
[model] gemini-3.5-flash-lite
[usage] input tokens: 7, output tokens: 600
[usage] input tokens: 7, output tokens: 619
[usage] input tokens: 7, output tokens: 619
[model] gemini-3.5-flash
[usage] input tokens: 7, output tokens: 764
[usage] input tokens: 7, output tokens: 708
[usage] input tokens: 7, output tokens: 820

- 気づき・疑問：どちらのモデルもインプットで認識するトークン数は同じだが、アウトプットでのトークン数が異なり、性能の高いモデルを用いると出力トークン数が増加し変動幅も大きくなった。

- 取り組んだレベル：実装
- やったこと：github copilotを利用して会話履歴を保持したまま質問できるようにした。
- 結果：会話を続けて質問できるようになった。
- 気づき・疑問：はじめて使用したが、非常に簡単に実装ができるということが分かった。

- 取り組んだレベル：発展
- やったこと：応答時間を計測できるようにした。
- 結果：[metrics] response time: 0.79s, input tokens: 1041, output tokens: 22として結果が出力されるようになった。
- 気づき・疑問：”現在の内閣総理大臣は誰ですか”という全く同じ質問をすると”現在の内閣総理大臣は**石破 茂**（いしば しげる）氏です。”という全く同じの誤った回答が出力された。ただし、出力の形は全く同じWord、トークンであったが、応答時間には最大で0.3秒ほどブレがあった。
