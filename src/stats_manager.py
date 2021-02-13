import utils.requester as tools


class BaseQuery:
    def get(self, modifier: str) -> str:
        if hasattr(self, modifer):
            return getattr(self, modifier)
        print(f"{self.__class__.__name__} has no {modifier} modifier")
        raise KeyError


class Teams(BaseQuery):
    url_suffix = "teams/"


def with_modifier(func):
    def wrapper(*args):
        if len(args) > 1:
            if args[1] != "" and hasattr(args[0].Modifiers, args[1]):
                new_args = [args[0], getattr(args[0].Modifiers, args[1])]
                if len(args) > 2:
                    new_args.append(args[2])
                return func(*new_args)
            else:
                print(
                    f"Sorry no modifier found for {args[1]}, running without modifier"
                )
                return func(args[0])
        else:
            return func(args[0])

    return wrapper


class Team(BaseQuery):
    url_suffix = Teams.url_suffix

    class Modifiers:
        roster = "?expand=team.roster"
        next_game = "?expand=team.schedule.next"
        last_game = "?expand=team.schedule.previous"
        stats = "?expand=team.stats"
        multiple_teams = "?teamId="  # Needs teamId's appended comma seperated
        single_season_stats = "?stats=statsSingleSeason&season="

    def __init__(self, team_name: str):
        self.team_id = tools.team_dict.get(team_name, 0)

    def get_multiple_teams(self, team_ids: list) -> str:
        return f"{self.multiple_teams}{(',').join(team_ids)}"

    @with_modifier
    def team_info(self, modifier: str = "") -> str:
        return f"{self.url_suffix}{self.team_id}{modifier}"

    def roster(self, modifier: str = "") -> str:
        return f"{self.url_suffix}{self.team_id}/roster"

    @with_modifier
    def stats(self, modifier: str = "", year: str = "") -> str:
        return f"{self.url_suffix}{self.team_id}/stats{modifier}{year}"


class NHL(BaseQuery):
    """Class containing all nhl teams with easy to use url suffixes and modifiers
     Once Instantiated team url's are accessible via lower_case_underscore separated team names

    Example:
        (Toronto Maple Leafs) nhl.toronto_maple_leafs
        (Team Info) nhl.toronto_maple_leafs.team_info(optiona_modifier = str)
        ^^ A modifer can be provided and if applicable it will be used
        (Roster) nhl.toronto_maple_leafs.roster()

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
    print(nhl.toronto_maple_leafs.team_info())
    # result = tools.get_request(nhl.toronto_maple_leafs.roster())
    # print(result)
    result = tools.get_request(nhl.vegas_golden_knights.team_info("stats"))
    print(result)
    result = tools.get_request(
        nhl.vegas_golden_knights.stats("single_season_stats", "20192020")
    )
    print(result)
