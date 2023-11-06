from pathlib import Path
from typing import Union

from pydantic import BaseModel, Field


class CrawlResults(BaseModel):
    files: list[Path] | None = Field(default=None)
    dirs: list[Path] | None = Field(default=None)


def crawl_path(
    path: Union[str, Path] = None,
    recurse: bool = True,
    type_filter: str | None = None,
    search_filter: str | None = None,
) -> CrawlResults:
    def crawl(
        path: Path = None,
        recurse: bool = recurse,
        search_filter: str | None = search_filter,
        files: list[Path] | None = None,
        dirs: list[Path] | None = None,
    ) -> CrawlResults:
        files: list[Path] = []
        dirs: list[Path] = []

        for i in path.glob(search_filter):
            if i.is_file():
                files.append(i)
            else:
                dirs.append(i)

                if recurse:
                    crawl(path=i, recurse=recurse, _files=files, _dirs=dirs)

        return_obj: CrawlResults = CrawlResults(files=files, dirs=dirs)

        return return_obj

    if path is None:
        raise ValueError("Missing path to crawl")
    if isinstance(path, str):
        path: Path = Path(path)

    if type_filter is not None:
        if type_filter not in ["files", "dirs"]:
            raise ValueError(
                f"Invalid type filter: {type_filter}. Must be one of ['files', 'dirs']."
            )

    if search_filter:
        search_str: str = f"**/{search_filter}"
    else:
        search_str: str = "**/*"

    _crawl = crawl(path=path, search_filter=search_str)

    return _crawl
