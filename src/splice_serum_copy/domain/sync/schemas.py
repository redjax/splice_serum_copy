from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union
from pathlib import Path

from loguru import logger as log

from splice_serum_copy.domain.directory import DirInfo


class DirSyncHandler(BaseModel):
    src: DirInfo = Field(default=None)
    tars: list[DirInfo] = Field(default=None)

    @property
    def src_info(self) -> None:
        log.debug(f"[exists: {self.src.exists}] Source: {self.src.path}")

    @property
    def tar_info(self) -> None:
        for _t in self.tars:
            log.debug(f"[exists: {_t.exists}] Target: {_t.path}")
