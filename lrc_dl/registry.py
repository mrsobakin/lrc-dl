from lrc_dl.core import AbstractProvider


class Registry:
    providers: dict[str, type[AbstractProvider]] = {}

    @classmethod
    def get_synced_providers(cls) -> dict[str, type[AbstractProvider]]:
        # TODO: stub
        return dict(cls.providers)

    @classmethod
    def register_provider(cls, provider_class: type[AbstractProvider]) -> None:
        cls.providers[provider_class.name] = provider_class


def lyrics_provider(cls: type[AbstractProvider]) -> type[AbstractProvider]:
    Registry.register_provider(cls)

    return cls
