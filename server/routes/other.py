from fastapi import APIRouter
from fastapi.responses import JSONResponse
from server.utils.config import settings

router = APIRouter(prefix="/other")


@router.get("/splash-screen")
def get_meta_data():
    return JSONResponse(
        status_code=200,
        content={
            "privacy_policy": "https://picsy.art/privacy-policy",
            "terms_and_conditions": "https://picsy.art/terms-of-use",
            "about_us": "https://picsy.art/about-us",
            "contact_us": "https://picsy.art/contact-us",
            "pagination_count": settings.PAGINATION_SIZE,
            "native-ad-frequency": 10,
            "grid-view-image-resolution-divide-by": 4,
            "image-slider-resolution-divide-by": 2,
            "app_update": {
                "android": {
                    "version": "1.2.4",
                    "is-force-update": False,
                    "store-link": "https://play.google.com/store/apps/details?id=art.picsy.deltabits",
                },
                "iOS": {
                    "version": "1.0.0",
                    "is-force-update": False,
                    "store-link": "https:///",
                },
            },
            "admob-app-ids": {
                "android": "xxxxx",
                "iOS": "xxxxx",
            },
            "admob-ad-units": {
                "app-opener-ad": {
                    "test-ids": {
                        "android": "ca-app-pub-3940256099942544/9257395921",
                        "iOS": "ca-app-pub-3940256099942544/5575463023",
                    },
                    "production-ids": {
                        "android": "ca-app-pub-8020793389292824/5960135625",
                        "iOS": "xxxxxxx",
                    },
                },
                "native-ad": {
                    "test-ids": {
                        "android": "ca-app-pub-3940256099942544/2247696110",
                        "iOS": "ca-app-pub-3940256099942544/3986624511",
                    },
                    "production-ids": {
                        "android": "ca-app-pub-8020793389292824/8543594333",
                        "iOS": "xxxxxxx",
                    },
                },
                "interstitial-ad": {
                    "test-ids": {
                        "android": "ca-app-pub-3940256099942544/1033173712",
                        "iOS": "ca-app-pub-3940256099942544/4411468910",
                    },
                    "production-ids": {
                        "android": "ca-app-pub-8020793389292824/1343067910",
                        "iOS": "xxxxxxx",
                    },
                },
                "rewarded-ad": {
                    "test-ids": {
                        "android": "ca-app-pub-3940256099942544/5224354917",
                        "iOS": "ca-app-pub-3940256099942544/1712485313",
                    },
                    "production-ids": {
                        "android": "ca-app-pub-8020793389292824/4844022473",
                        "iOS": "xxxxxxx",
                    },
                },
            },
            "ad_units_visibility": {
                "android": {
                    "show-app-opener-ad": True,
                    "show-native-ad": True,
                    "show-interstitial-ad-onTapOfImage": False,
                    "show-interstitial-ad-whenGetBackFromImages": True,
                    "show-rewarded-ad-on-download-image": False,
                    "show-rewarded-ad-on-set-image": True,
                },
                "iOS": {
                    "show-app-opener-ad": True,
                    "show-native-ad": True,
                    "show-interstitial-ad-onTapOfImage": True,
                    "show-interstitial-ad-whenGetBackFromImages": True,
                    "show-rewarded-ad-on-download-image": True,
                    "show-rewarded-ad-on-set-image": True,
                },
            },
            "search-categories": [
                {
                    "title": "Nature",
                    "bg-image": "https://image.lexica.art/full_webp/4b660c5d-f3f7-45a1-b504-e9f3cc7aaac5",
                },
                {
                    "title": "Abstract",
                    "bg-image": "https://image.lexica.art/full_webp/b8bdcb66-3d9d-4e57-acc7-6afa88579d8e",
                },
                {
                    "title": "Space",
                    "bg-image": "https://image.lexica.art/full_webp/82495f03-0281-431c-999d-49ff26419278",
                },
                {
                    "title": "Animals",
                    "bg-image": "https://image.lexica.art/full_webp/166ecc6a-61c6-46ce-8859-caa40431a94e",
                },
                {
                    "title": "Cityscapes",
                    "bg-image": "https://image.lexica.art/full_webp/4c8a5dca-dfbc-405d-87a5-197cb8170278",
                },
                {
                    "title": "Art",
                    "bg-image": "https://image.lexica.art/full_webp/094e246c-287c-416f-9be6-09029043f07a",
                },
                {
                    "title": "Quotes",
                    "bg-image": "https://image.lexica.art/full_webp/2c024715-2a9f-44d1-a2c1-713e79bdb62e",
                },
                {
                    "title": "Technology",
                    "bg-image": "https://image.lexica.art/full_webp/641646a8-139d-42e2-a474-b6b233da1290",
                },
                {
                    "title": "season",
                    "bg-image": "https://image.lexica.art/full_webp/8996dfd5-13b0-408e-a95d-ced4639d4c2d",
                },
                {
                    "title": "Anime",
                    "bg-image": "https://image.lexica.art/full_webp/805ebd1e-8e5e-4b43-923f-efa5c2da2f1c",
                },
            ],
        },
    )
