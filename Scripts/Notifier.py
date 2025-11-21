import logging

try:
    import apprise
except ImportError:  # pragma: no cover
    apprise = None


class AppriseNotifier:
    def __init__(self, config):
        self.config = config or {}
        self.apprise = None
        self.events = {}
        self.enabled = False
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
                logging.warning("Apprise 模块不可用，无法发送通知")
            self.apprise = None
            self.enabled = False
            return
        self.apprise = apprise.Apprise()
        added = 0
        for url in urls:
            try:
                if self.apprise.add(url):
                    added += 1
            except Exception:  # pragma: no cover
                logging.exception("Apprise 添加通知地址失败：%s", url)
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
        except Exception:  # pragma: no cover
            logging.exception("Apprise 通知发送失败")
            return False
