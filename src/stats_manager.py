import utils.requester as tools


class BaseQuery:
    def get(self, modifier: str) -> str:
        if hasattr(self, modifer):
            return getattr(self, modifier)
        print(f"{self.__class__.__name__} has no {modifier} modifier")
        raise KeyError


class Teams(BaseQuery):
    url_suffix = "teams/"


class Team(BaseQuery):
    url_suffix = Teams.url_suffix
    player_names = "?expand=person.names"
    roster = "?expand=team.roster"
    next_game = "?expand=team.schedule.next"
    last_game = "?expand=team.schedule.previous"
    stats = "?expand=team.stats"
    multiple_teams = "?teamId="  # Needs teamId's appended comma seperated
    specific_stats = "?stats=stats"  # Needs phrase appended

    def __init__(self, team_name: str):
        self.team_id = tools.team_dict.get(team_name, 0)

    def get_multiple_teams(self, team_ids: list) -> str:
        return f"{self.multiple_teams}{(',').join(team_ids)}"

    def get_stat(self, stat: str) -> str:
        return f"{self.specific_stats}{stat}"

    def team(self, modifier: str = "") -> str:
        return f"{self.url_suffix}{self.team_id}{modifier}"


class NHL(BaseQuery):
    """Class containing all nhl teams with easy to use url suffixes and modifiers

    Args:
        BaseQuery: Basic class for stats api queries
    """

    def __init__(self):
        [
            setattr(self, ("_").join(team.split(" ")).lower(), Team(team))
            for team in tools.team_dict
        ]


if __name__ == "__main__":
    nhl = NHL()
    print(nhl.toronto_maple_leafs.team())
    toronto_maple_leafs = Team("Toronto Maple Leafs")
    print(toronto_maple_leafs.team())
    result = tools.get_request(nhl.toronto_maple_leafs.team())
    print(result)
    result = tools.get_request(nhl.vegas_golden_knights.team())
    print(result)
