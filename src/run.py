import sys
from pathlib import Path

import pkg.log as log
import pkg.pixivapi as pixiv_api
import pkg.cfg as cfg

def get_config_and_api():
    config = cfg.get_pixiv_config()
    api = pixiv_api.new_pixiv_api(pixiv_api.ApiMetaArgument(
        PHPSESSID=config.phpsessid,
        PROXY=config.proxy
    ))
    return config, api

def get_filepath(config, artwork_id: int, idx: int) -> Path:
    return config.file_path / f"{artwork_id}_{idx}.jpg"

def download_artwork(api, config, artwork_info):
    total_file_size = 0
    for idx, url in enumerate(artwork_info.image_download_urls):
        file_path = get_filepath(config, artwork_info.artwork_id, idx)
        if file_path.exists() and file_path.stat().st_size > 0:
            total_file_size += file_path.stat().st_size
            continue
        content = api.get_image(url)
        total_file_size += len(content)
        with file_path.open('wb+') as f:
            f.write(content)
    return total_file_size

def is_artwork_exist(config, artwork_info) -> bool:
    for idx in range(artwork_info.nums):
        file_path = get_filepath(config, artwork_info.artwork_id, idx)
        if not file_path.exists() or file_path.stat().st_size <= 0:
            return False
    return True

def crawler_by_artwork_id(artwork_id: int):
    config, api = get_config_and_api()
    options = pixiv_api.new_filter()
    artwork_info = api.get_artwork_info(artwork_id, options)
    # 校验
    invalid_reason = options.valid_by_artwork_info(artwork_info)
    if invalid_reason:
        log.info(f"artwork {artwork_info.artwork_id} is invalid, reason: {invalid_reason}")
        return
    
    # 优化输出
    artwork_url = f"https://www.pixiv.net/artworks/{artwork_info.artwork_id}"
    tags_str = ", ".join([tag.name for tag in artwork_info.tags])
    log.workInfo("---")
    log.workInfo(f"平台: Pixiv")
    log.workInfo(f"作品标题: {artwork_info.title} (链接: {artwork_url})")
    log.workInfo(f"作品ID: {artwork_info.artwork_id}")
    log.workInfo(f"画师: {artwork_info.user_name} (ID: {artwork_info.user_id})")
    log.workInfo(f"Tags: {tags_str}")
    log.workInfo("---")

    if is_artwork_exist(config, artwork_info):
        if not options.update:
            log.info(f"artwork {artwork_info.artwork_id} already exist")
            return

    total_file_size = download_artwork(api, config, artwork_info)
    log.info(
        f"save artwork {artwork_info.artwork_id} to {config.file_path}",
        title=artwork_info.title,
        tags=[tag.name for tag in artwork_info.tags],
        user=f"{artwork_info.user_name}({artwork_info.user_id})",
        file_size=total_file_size
    )

if __name__ == "__main__":
    crawler_by_artwork_id(int(sys.argv[1]))