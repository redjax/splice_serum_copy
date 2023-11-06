import shutil
from pathlib import Path

from loguru import logger as log

from splice_serum_copy.domain.directory import DirInfo, crawl_path
from splice_serum_copy.domain.sync import DirSyncHandler


def sync_files(
    src_dir: DirInfo = None, tar_dir: DirInfo = None, dry_run: bool = False
) -> list[Path]:
    if src_dir is None:
        raise ValueError("Missing source directory")
    if tar_dir is None:
        raise ValueError("Missing target directory")

    src_files: list[Path] = crawl_path(path=src_dir.path, search_filter="*.fxp").files
    tar_files: list[Path] = crawl_path(path=tar_dir.path).files

    if src_files is not None:
        log.debug(f"Found [{len(src_files)}] file(s) in source dir")
    if tar_files is not None:
        log.debug(f"Found [{len(tar_files)}] file(s) in target dir")

    src_filenames: list[str] = []
    tar_filenames: list[str] = []

    for f in src_files:
        src_filenames.append(f.name)

    for f in tar_files:
        tar_filenames.append(f.name)

    copy_files: list[Path] = [n for n in src_filenames if n not in tar_filenames]
    copied_files: list[Path] = []

    if copy_files is not None:
        log.debug(f"[{len(copy_files)}] file(s) to copy")

        for f_name in copy_files:
            src_path: Path = Path(f"{src_dir.path}/{f_name}")
            tar_path: Path = Path(f"{tar_dir.path}/{f_name}")
            if dry_run:
                log.debug(f"Would copy [{src_path}] -to-> [{tar_path}]")
            else:
                log.info(f"Copying [{src_path}] -> [{tar_path}]")

                try:
                    shutil.copy(src=src_path, dst=tar_path)
                    copied_files.append(src_path)
                except FileNotFoundError as fnf:
                    raise FileNotFoundError(fnf)
                except PermissionError as perm:
                    raise PermissionError(perm)
                except Exception as exc:
                    raise Exception(
                        f"Unhandled exception copying file [{src_path}] --> [{tar_path}]. Details: {exc}"
                    )

        return copied_files

    else:
        log.warning(
            f"Did not find any files in source [{src_dir.path}] that do not exist in target [{tar_dir.path}]"
        )

        return None


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
