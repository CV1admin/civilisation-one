from __future__ import annotations

from dataclasses import dataclass


@dataclass
class APIMessage:
    route: str
    payload: dict


class VireaxAPILayer:
    """REST-style transformation bus for subsystem communication."""

    def route(self, message: APIMessage) -> dict:
        if message.route == "/configure":
            return {"status": "updated", "config": message.payload}
        if message.route == "/state":
            return {"status": "ok", "state": message.payload}
        return {"status": "unknown_route", "route": message.route}
