import sys

sys.path.append(".")

from pathlib import Path

from red_utils.ext.loguru_utils import init_logger, LoguruSinkStdOut, LoguruSinkAppFile
from loguru import logger as log

from dynaconf import settings

from splice_serum_copy.domain.directory import DirInfo, crawl_path, CrawlResults
from splice_serum_copy.domain.sync import DirSyncHandler
from splice_serum_copy.utils.path_utils import sync_files

sinks = [
    LoguruSinkStdOut(level=settings.LOG_LEVEL).as_dict(),
    LoguruSinkAppFile().as_dict(),
]


def run_sync(sync_handler: DirSyncHandler = None) -> list[Path]:
    if sync_handler is None:
        raise ValueError("Missing DirSyncHandler object")

    merge_sync_lists: list[list[Path]] = []
    seen_paths = set()
    copied_files: list[Path] = []

    for d in sync_handler.tars:
        sync: list[Path] | None = sync_files(src_dir=sync_handler.src, tar_dir=d)
        merge_sync_lists.append(sync)

    for path_list in merge_sync_lists:
        for p in path_list:
            if p not in seen_paths:
                copied_files.append(p)
                seen_paths.add(p)

    return copied_files


if __name__ == "__main__":
    init_logger(sinks=sinks)

    log.info(f"[env:{settings.ENV}|container:{settings.CONTAINER_ENV}] Starting app")
    log.debug(f"Source dir: {settings.SRC_DIR}")
    log.debug(f"Target dirs: {settings.TAR_DIRS}")

    src_dir: DirInfo = DirInfo.model_validate(settings.SRC_DIR)
    log.debug(f"Source dir: {src_dir}")

    tar_dirs: list[DirInfo] = []

    for _d in settings.TAR_DIRS:
        d: DirInfo = DirInfo.model_validate(_d)
        tar_dirs.append(d)

    log.debug(f"[{len(tar_dirs)}] target dir(s)")
    log.debug(tar_dirs)

    log.debug(f"Source dir [{src_dir.path}] exists: {src_dir.exists}")
    for _d in tar_dirs:
        log.debug(f"Target dir [{_d.path}] exists: {_d.exists}")

    sync_handler: DirSyncHandler = DirSyncHandler(src=src_dir, tars=tar_dirs)
    sync_handler.src_info
    sync_handler.tar_info

    res: list[Path] = run_sync(sync_handler=sync_handler)

    if res is not None:
        log.debug(f"[{len(res)}] file(s) copied.")
