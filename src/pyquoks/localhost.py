from __future__ import annotations
import waitress, flask


class ILocalhostFlask(flask.Flask):
    _RULES: dict[str, function]

    def __init__(self):
        super().__init__(import_name="osu!parser")

        for k, v in self._RULES.items():
            self.add_url_rule(rule=k, view_func=v)

    def serve(self):
        waitress.serve(app=self, host="127.0.0.1", port=727)
