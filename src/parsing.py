"""Parsing: read JSON-with-comments config into a validated Config."""
import json

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
    ValidationInfo
)

COMMENT_PREFIXES = ("#", "//", "/*")

DEFAULTS = {
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
}


class Level(BaseModel):
    """Represents a maze level with width and height."""
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class Config(BaseModel):
    """Game configuration with validation and defaults."""
    lives: int = DEFAULTS["lives"]
    pacgum: int = DEFAULTS["pacgum"]
    points_per_pacgum: int = DEFAULTS["points_per_pacgum"]
    points_per_super_pacgum: int = DEFAULTS["points_per_super_pacgum"]
    points_per_ghost: int = DEFAULTS["points_per_ghost"]
    seed: int = DEFAULTS["seed"]
    level_max_time: int = DEFAULTS["level_max_time"]
    levels: list[Level] = [Level(width=15, height=15)]

    @field_validator(
        "lives",
        "level_max_time",
        "pacgum",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        mode="before"
    )
    @classmethod
    def must_be_positive(cls, v: int, info: ValidationInfo) -> int:
        if v <= 0:
            name = info.field_name
            assert name is not None
            default = DEFAULTS[name]
            print(f"Warning: {name}={v} invalid, using {default}")
            return default
        return v


class ParsingError(Exception):
    """Raised when config parsing fails."""


class Parsing:
    """Parses config files and returns validated Config."""

    def __init__(self, file: str) -> None:
        """Initialize parser with config file path."""
        self.file = file

    @staticmethod
    def strip_comments(text: str) -> str:
        """Remove comment lines from raw text."""
        lines = []
        for i in text.splitlines():
            stripped = i.lstrip()
            if stripped.startswith(COMMENT_PREFIXES):
                continue
            lines.append(i)
        return "\n".join(lines)

    def open_file(self) -> Config:
        """Read config file and return validated Config."""
        try:
            with open(self.file, encoding="utf-8") as f:
                raw = f.read()
                clean = self.strip_comments(raw)
                data_file = json.loads(clean)
        except FileNotFoundError:
            raise ParsingError(f"Config file not found: {self.file}")
        except json.JSONDecodeError as e:
            raise ParsingError(f"Invalid JSON: {e}")
        except OSError as e:
            raise ParsingError(f"Cannot read file: {e}")
        try:
            return Config(**data_file)
        except ValidationError as e:
            raise ParsingError(f"Config schema invalid: {e}")
