from typing import Union
from pathlib import Path
from pydantic import BaseModel, Field, validator, ValidationError

from loguru import logger as log

from .operations import crawl_path, CrawlResults

valid_dir_types: list[str] = ["source", "target"]


class DirInfo(BaseModel):
    type: str | None = Field(default="source")
    name: str | None = Field(default=None)
    path: Union[str, Path] | None = Field(default=None)

    @validator("type")
    def valid_type(cls, v) -> str:
        if v not in valid_dir_types:
            raise ValidationError

        return v

    @validator("path")
    def valid_path(cls, v) -> Path:
        if isinstance(v, Path):
            return v

        else:
            try:
                _v: Path = Path(v)

                return _v
            except:
                raise ValidationError

    @property
    def exists(self) -> bool:
        return self.path.exists()

    def get_files(self) -> list[Path]:
        _crawl: CrawlResults = crawl_path(
            path=self.path, recurse=True, search_filter="*.fxp"
        )

        return _crawl.files

    def get_dirs(self) -> list[Path]:
        _crawl: CrawlResults = crawl_path(path=self.path, recurse=True)

        return _crawl.dirs
