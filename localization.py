# localization.py
# -*- coding: utf-8 -*-

TRANSLATIONS = {
    "zh_TW": {
        "window_title": "BB 捲動彈跳過濾",
        "grp_blocking": "阻擋邏輯",
        "grp_app_control": "應用程式控制",
        "grp_system": "系統",
        "chk_start_boot": "開機自動執行",
        "tip_start_boot": "勾選後, Windows 啟動時會自動啟動本程式",
        "chk_enable": "啟用捲動阻擋",
        "tip_enable": "控制是否啟用捲動阻擋功能的總開關",
        "lbl_interval": "阻擋間隔(s) :",
        "tip_interval": "在此時間內檢查反向事件; 若要使用方向切換門檻, 必須大於最短反轉時間",
        "lbl_threshold": "方向切換門檻 :",
        "tip_threshold": "確認為新方向所需的反向連續捲動次數; 只計算最短反轉時間之後, 阻擋間隔到期之前的事件",
        "lbl_min_reversal": "最短反轉時間(s) :",
        "tip_min_reversal": "物理檢查: 比此時間更快的反轉會立即被阻擋",
        "lbl_blacklist": "黑名單(不套用阻擋) :",
        "btn_add_current": "新增目前應用程式",
        "btn_remove_selected": "移除選取項目",
        "btn_clear_all": "全部清除",
        "btn_defaults": "還原預設值",
        "btn_help": "說明",
        "btn_about": "關於",
        "btn_save": "儲存變更",
        "status_saved": "設定已成功儲存",
        "status_restored": "已成功還原為預設值",
        "msg_startup_failed_title": "無法設定開機啟動",
        "msg_startup_failed_text": "建立或移除高權限工作排程失敗, 請確認程式以系統管理員權限執行",
        "msg_reset_title": "確認重設",
        "msg_reset_text": "確定要還原預設設定嗎？",
        "msg_reset_yes": "是",
        "msg_reset_cancel": "取消",
        "msg_threshold_unreachable_title": "方向切換門檻無法生效",
        "msg_threshold_unreachable_text": "方向切換門檻大於 1 時, 阻擋間隔必須大於最短反轉時間, 否則沒有可累計反向事件的時間範圍. 請調高阻擋間隔或調低最短反轉時間後再儲存",
        "tray_settings": "設定",
        "tray_toggle": "啟用",
        "tray_exit": "結束",
        "tray_msg_title": "捲動彈跳過濾",
        "tray_enabled": "已啟用",
        "tray_disabled": "已停用",
        "help_window_title": "BB 捲動彈跳過濾 - 說明",
        "help_content": """
        <h1>BB 捲動彈跳過濾 - 說明</h1>
        <p>本程式會過濾短時間內快速反轉方向的滑鼠滾輪事件, 以減少意外捲動. 設定視窗分為"阻擋邏輯", "應用程式控制"及"系統"三個區塊.</p>
        <h2>阻擋邏輯</h2>
        <ul>
          <li><b>阻擋間隔(s): </b>在最近一次通過的滾輪事件後, 於此時間範圍內檢查方向反轉. 超過此間隔後, 程式會重新判斷捲動方向. 若使用大於 1 的方向切換門檻, 此值必須大於最短反轉時間.</li>
          <li><b>方向切換門檻: </b>最短反轉時間之後, 阻擋間隔到期之前, 反方向的連續滾輪事件需達到此次數, 才會被視為有意切換方向並通過; 未達門檻的反向事件會被阻擋.</li>
          <li><b>最短反轉時間(s): </b>若方向反轉發生得比此時間更快, 該事件會立即被阻擋.</li>
        </ul>
        <h2>應用程式控制</h2>
        <ul>
          <li><b>黑名單(不套用阻擋): </b>清單內的應用程式不會套用滾輪阻擋, 例如 <code>chrome.exe</code>. 比對的是執行檔名稱, 不區分大小寫.</li>
          <li><b>新增目前應用程式: </b>暫時隱藏設定視窗, 並將當時的前景應用程式加入黑名單.</li>
          <li><b>移除選取項目 / 全部清除: </b>從黑名單移除選取的應用程式, 或清空整份清單.</li>
        </ul>
        <h2>系統</h2>
        <ul>
          <li><b>啟用捲動阻擋: </b>控制是否套用阻擋邏輯. 也可以從系統匣選單立即切換.</li>
          <li><b>開機自動執行: </b>登入 Windows 時透過工作排程器啟動本程式, 並在系統匣背景執行.</li>
        </ul>
        <h2>儲存與其他選項</h2>
        <ul>
          <li><b>儲存變更: </b>套用並儲存設定視窗中的變更. 尚未儲存的調整不會套用.</li>
          <li><b>還原預設值: </b>確認後還原阻擋參數與啟用狀態, 並立即儲存; 黑名單及開機啟動設定不會因此清除.</li>
          <li><b>說明 / 關於: </b>可從設定視窗底部「還原預設值」旁的按鈕開啟.</li>
          <li>在系統匣圖示的選單中, 可開啟設定, 切換捲動阻擋, 或結束程式.</li>
        </ul>
        <p>本程式使用 Windows 低階滑鼠掛鉤; 若無法正常攔截滾輪事件, 請確認程式以系統管理員權限執行.</p>
        """,
        "btn_close": "關閉",
        "about_qlabel": "<b>BB 捲動彈跳過濾</b>",
        "about_window_title": "關於 BB 捲動彈跳過濾 - 關於",
        "about_version": "版本: 1.2.1",
        "about_author": "作者: BeefBB",
        "about_description": "MeteAvci/WheelScrollFixer 的BB修改版本",
    }
}

class Translator:
    def tr(self, key, **kwargs):
        """Returns the Traditional Chinese translation for a key."""
        return TRANSLATIONS["zh_TW"].get(key, key).format(**kwargs)

translator = Translator()
