async def describe_devices() -> str:
    return "Мои устройства: раздел в разработке."


async def intro_add_device() -> str:
    return "Выберите платформу устройства для настройки:"


async def describe_platform_mac() -> str:
    return "Mac: установите клиент WireGuard/Outline, импортируйте конфиг, включите VPN."


async def describe_platform_android() -> str:
    return "Android: установите клиент из Google Play, импортируйте конфиг, включите VPN."


async def describe_platform_windows() -> str:
    return "Windows: скачайте клиент, импортируйте конфиг, включите VPN."