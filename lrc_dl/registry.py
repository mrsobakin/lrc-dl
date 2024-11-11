from lrc_dl.core import AbstractProvider


class Registry:
    providers: dict[str, type[AbstractProvider]] = {}

    @staticmethod
    def get_synced_providers() -> dict[str, type[AbstractProvider]]:
        # TODO: stub
        return dict(Registry.providers)

    @staticmethod
    def register_provider(provider_class: type[AbstractProvider]) -> None:
        Registry.providers[provider_class.name] = provider_class


def lyrics_provider(cls: type[AbstractProvider]) -> type[AbstractProvider]:
    Registry.register_provider(cls)

    return cls
