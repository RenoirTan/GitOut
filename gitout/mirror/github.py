import typing as t

from github import Github as _Github # prevent confusion

from .service import Settings, Service

class GithubService(Service):
    def __init__(self, settings: Settings, *args, **kwargs) -> None:
        super().__init__(settings, *args, **kwargs)
    
    def setup(self) -> None:
        self.validate()
        self.g = _Github(login_or_token=self.settings.token)
    
    def validate(self) -> None:
        if self.settings.token is None:
            raise ValueError("Github requires a token for accessing the API")
    
    def request(self) -> None:
        self.repos = self.g.get_user().get_repos()
    
    def get_clone_urls(self) -> t.Optional[t.Iterable[str]]:
        return map(lambda r: r.clone_url, self.repos)