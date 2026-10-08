# AI 動態雷達

每天早上精選 AI 新聞、專家解析、深度分析、我的自選股、投資觀察與 Podcast。

- 網站：https://lisaingithub.github.io/ai-radar/
- 資料由 Claude 每天台北時間 08:00 前後搜尋公開來源整理，並自動同步到 `data/` 資料夾。
- 內容僅為資訊整理，不是投資建議。重要資訊請點原始來源確認。

## 結構

- `index.html`：網頁本體
- `shim.js`：在 GitHub Pages 上改讀 `data/` 的每日快照
- `data/`：每日資料（digests、experts、predictions、calendar 等）
- `scripts/build_data.py`：把 Claude 資料庫匯出檔整理成 `data/`

## GitHub 版的限制

- 唯讀：無法上傳 Podcast 音檔，Podcast 使用裝置語音朗讀。
- 只保留最近 90 天的摘要。
