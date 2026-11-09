# 第3回 解答

## 演習

- 質問：AIE2026の講座の宿題にある「3レベル」とは何ですか？
- 素のLLMとエージェントを今回同じモデルで実行した。素のLLMは一般論として「基礎・応用・発展／チャレンジ」を説明した。エージェントは用語集を検索し「基礎・実装・発展」、どれか1つを選ぶ仕組みを説明した。
- 呼ばれたツール：search_glossary(query="3レベル")、1回。LLM呼び出しはrequests=2。
- 回答の「原則として採点は行われません」という記述も用語集に由来する。検索結果自体の更新も重要であり、最新の提出案内を別に確認する必要がある。
- LoRAとQLoRAの違いを質問すると、search_glossary(query="LoRA")、search_glossary(query="QLoRA")を呼んだ。ツール2回に対してrequests=2だった。検索2件が同じモデル応答から要求されるため、ツール数とLLM呼び出し数は一致しない。
- 追加したツール：make_quiz(lecture: int) -> str。指定回の用語を用語集から抽出し、random.choiceで1つ選び、questionとanswerをJSONで返す。該当回がなければerrorを含むJSONを返す。
- docstring：「指定した回の用語集から、確認問題を1問とその答えを作る」「復習用の問題を求められたときに使う」。引数lectureと、questionを出題、answerを答え合わせに使うことも記載した。
- agent.tool_plain(tools.make_quiz)で登録。「第2回の内容から確認問題を1問出して」に対し、make_quiz(lecture=2)が1回呼ばれ、requests=2だった。ツール一覧でも登録と説明を確認した。

原文：[素のLLM](results/plain.txt)、[講座固有の質問](results/agent_course.txt)、[出題](results/quiz.txt)、[ツール一覧](results/tools.txt)

## 宿題

取り組んだレベル：**基礎**

### やったこと

INSTRUCTIONSの1行だけを以下のように変更した。

変更前：回答の最後に、関係する回（第N回）を示す。

変更後：回答の最後に「理解チェック：」という見出しと確認問題を1問示す。確認問題の答えは書かない。

両条件で「LoRAとQLoRAの違いは？」を--trace付きで実行した。モデル、質問、用語集、登録した3つのツールとdocstring、ほかの指示は同じ。各条件は独立したプロセスで1回ずつ実行した。

### 結果

| 観点 | 変更前 | 変更後 |
|---|---|---|
| search_glossaryの引数 | LoRA、QLoRA | LoRA、QLoRA |
| 検索回数 | 2回 | 2回 |
| make_quiz | 呼ばれなかった | lecture=2、1回 |
| ツール呼び出し合計 | 2回 | 3回 |
| LLM呼び出しrequests | 2回 | 3回 |
| 回答末尾 | 関係する回：第2回 | 理解チェックとSFTの確認問題 |
| コマンド全体の実行時間 | 8.208秒 | 28.675秒 |

両方とも、LoRAが少数の追加パラメータを学習し、QLoRAはベースモデルを量子化してメモリを節約することを説明した。変更後は「『教師ありファインチューニング（SFT）』の意味は？」と出題し、答えは表示しなかった。

原文：[変更前](results/before.txt)、[変更後](results/after.txt)

### 気づき・疑問

- 指示文1行の変更で、回答形式に加えてツール選択とLLM呼び出し回数も変わった。変更後は検索の後に出題ツールを使う段階が加わった。
- 必ず用語集を検索する指示は共通なので、変更後もLoRAとQLoRAを別々に検索した。
- 確認問題は同じ第2回のSFTで、LoRAとQLoRAの比較そのものを問う問題ではなかった。講義回だけでランダムに選ぶため、直前の説明との関連を強めるには、対象用語などの引数も必要だと思う。
- ツールは答えも返すが、モデルが利用者に見せる情報は別である。
- 各条件1回ずつなので、常に同じ経路・時間になるとは言えない。実行時間には通信とモデル応答の揺らぎも含まれる。
- APIなしのテストは配線や関数の動作確認。実LLMのツール選択はAPIでのtraceを別に確認する必要がある。

## 実行条件と検証

- 2026年11月9日、自分のforkのGitHub Codespacesで実行。
- 開始時main：bc41dfac203acff0706b7da10d09339d91830bfe
- モデル：gemini-3.5-flash-lite
- Python 3.12.16、pydantic-ai-slim 2.57.0、google-genai 2.31.0。講座のuv.lockを使用。
- uv run pytest -q：**21 passed**。出題内容が指定回の用語・定義に一致する3ケースと、存在しない回0・-1・99を指定する3ケースを追加。
- APIでの5つの実行はすべて終了コード0。

[実行条件と時間](results/metadata.json)、[テスト結果](results/pytest.txt)、[変更前コード](results/agent_before.py.txt)

再実行：リポジトリ直下でGEMINI_API_KEYを環境変数に設定し、uv run python lectures/03/run_experiments.py を実行する。結果ファイルは上書きされ、回答や出題は変わり得る。APIキーは提出ファイルに含めていない。

## AI利用

ChatGPTによるコード実装、Codespaces操作、実験実行、集計、文章作成支援を利用した。記載した回答・数値・traceは実際に自分のCodespacesでGemini APIを呼んで得た記録である。TestModelの出力を実LLMの実験結果として扱っていない。
