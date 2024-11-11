from dataclasses import dataclass, field
from pathlib import Path
from typing import Self
import os
import tomllib

from lrc_dl.logger import DefaultLogger


def _get_config_file() -> Path | None:
    config_dir = os.environ.get("XDG_CONFIG_HOME")

    if config_dir is None:
        return None

    return Path(config_dir) / "lrc-dl" / "config.toml"


CONFIG_PATH = _get_config_file()


@dataclass
class LyricsDlConfig:
    order: list[str] = field(default_factory=lambda: ["kugou", "youtube"])
    delay: float | None = 10
    prepend_header: bool = True
    providers_configs: dict[str, dict] = field(default_factory=lambda: {})

    @classmethod
    def from_file(cls, path: Path) -> Self:
        with open(path, "rb") as f:
            config = tomllib.load(f)

        return cls(
            order=config["providers"].pop("order"),
            providers_configs=config["providers"],
        )

    @classmethod
    def default(cls) -> Self:
        try:
            if CONFIG_PATH is not None:
                return cls.from_file(CONFIG_PATH)
        except FileNotFoundError:
            DefaultLogger().warning(
                f"Warning: Missing config file ({CONFIG_PATH})."
                " Falling back to default parameters."
            )

        return cls()
