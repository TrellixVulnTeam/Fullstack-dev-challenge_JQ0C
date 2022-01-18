
class TopAppsCategory():

    TOP_FREE_APPS = 'TOP_FREE_APPS'
    TOP_FREE_GAMES = 'TOP_FREE_GAMES'
    TOP_PAID_APPS = 'TOP_PAID_APPS'
    TOP_PAID_GAMES = 'TOP_PAID_GAMES'
    TOP_GROSSING_APPS = 'TOP_GROSSING_APPS'
    TOP_GROSSING_GAMES = 'TOP_GROSSING_GAMES'

    @classmethod
    def GetCategory(cls, category):
        switcher = {
            'top free apps': cls.TOP_FREE_APPS,
            'top free games': cls.TOP_FREE_GAMES,
            'top grossing apps': cls.TOP_GROSSING_APPS,
            'top grossing games': cls.TOP_GROSSING_GAMES,
            'top paid apps': cls.TOP_PAID_APPS,
            'top paid games': cls.TOP_PAID_GAMES
        }
        return switcher.get(category.lower())

    @classmethod
    def GetAllCategories(cls):
        return [cls.TOP_FREE_APPS , cls.TOP_FREE_GAMES , cls.TOP_PAID_APPS , cls.TOP_PAID_GAMES , cls.TOP_GROSSING_APPS , cls.TOP_GROSSING_GAMES]