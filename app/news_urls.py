from news_objects import fetch_epaper

urls = [
    "https://epaper.andhrajyothy.com/NTR_VIJAYAWADA_MAIN?eid=182",
    "https://epaper.eenadu.net/Home/Index?eid=2",
]


def get_all_image_urls() -> list[str]:
    all_images = []
    for url in urls:
        batch = fetch_epaper(url)
        all_images.extend(batch.image_urls)
    return all_images
