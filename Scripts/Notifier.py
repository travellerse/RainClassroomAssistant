try:
    import apprise
except ImportError:  # pragma: no cover
    apprise = None


class AppriseNotifier:
    def __init__(self, config, main_ui):
        self.config = config or {}
        self.apprise = None
        self.events = {}
        self.enabled = False
        self.main_ui = main_ui
        self._build()

    def update_config(self, config):
        self.config = config or {}
        self._build()

    def _build(self):
        apprise_config = self.config.get("apprise", {})
        urls = [url.strip() for url in apprise_config.get("urls", []) if url.strip()]
        self.events = apprise_config.get("events", {})
        if not apprise or not apprise_config.get("enabled") or not urls:
            if apprise_config.get("enabled") and not apprise:
                self.main_ui.add_message_signal.emit("Apprise 模块不可用，无法发送通知", 2)
            self.apprise = None
            self.enabled = False
            return
        self.apprise = apprise.Apprise()
        added = 0
        for url in urls:
            try:
                if self.apprise.add(url):
                    added += 1
            except Exception as e:
                self.main_ui.add_message_signal.emit(f"Apprise 添加通知地址失败：{e}", 2)
        self.enabled = added > 0
        if not self.enabled:
            self.apprise = None

    def notify(self, event, title, body):
        if not self.enabled:
            return False
        if not self.events.get(event, False):
            return False
        if not self.apprise:
            return False
        try:
            self.apprise.notify(title=str(title), body=str(body))
            return True
        except Exception as e:  # pragma: no cover
            self.main_ui.add_message_signal.emit(str(e), 2)
            return False
