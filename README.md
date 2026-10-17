# BB 捲動彈跳過濾

一款輕巧的 Windows 工具, 過濾滑鼠滾輪意外捲動抖動問題

MeteAvci/WheelScrollFixer 的BB修改版本  
基本上就是移除了BB用不到的功能+少量修改  

- 過濾滑鼠滾輪捲動抖動
- 調整 阻擋間隔, 方向切換門檻, 最短反轉時間
- 應用程式黑名單
- 開機啟動
- 監看程序, 程式意外結束時可由監看程序重新啟動

### 截圖

![截圖](./assets/screenshot.png)

# 下載

### 到 Releases 下載最新版

- [BB Wheel Scroll Fixer.exe](https://github.com/BeefBB/bb-wheel-scroll-fixer/releases)

然後放到一個你不會移動的地方, 再執行它  

## 備註

如果開機啟動失效了, 那通常是因為你移動了這個程式,  
請重新執行一次並再次選擇 開機自動執行  

本程式需要安裝低階滑鼠掛鉤, 因此必須以系統管理員權限執行  

# 想自己編譯?

## 執行

```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
pyinstaller --noconfirm --onefile --noconsole --icon=bb-wheel-scroll-fixer.ico --name="BB Wheel Scroll Fixer" --add-data "bb-wheel-scroll-fixer.ico;."  "bb-wheel-scroll-fixer.py"
```

打包後會在 `./dist`  

# 命令列參數

- `--no-watchdog`: 不啟動監看程序, 此參數適合開發與除錯, 可避免程式結束後被監看程序重新啟動

# 致謝

部分程式碼最初基於以下項目:  

- [MeteAvci/WheelScrollFixer (MIT license)](https://github.com/MeteAvci/WheelScrollFixer)

第三方授權文件請見 `THIRD_PARTY_LICENSES/` .

# 版權

MIT License  