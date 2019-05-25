from search_views.filters import BaseFilter
from sharing_app import models


class ProductSearchFilter(BaseFilter):
    search_fields = {
        'search_title' : { 'operator' : '__icontains', 'fields' : ['name'] },
        'search_category': { 'operator' : '__icontains', 'fields' : ['category'] },
        'search_age_min' : { 'operator' : '__lte', 'fields' : ['min_age'] },
        'search_players_min': {'operator': '__lte', 'fields': ['min_number_of_players']},
        'search_players_max': {'operator': '__lte', 'fields': ['max_number_of_players']},

		# 'search_players':{ 'operator' :'__filter(search_players__range=(min_number_of_players, max_number_of_players))',' fields' : ['min_number_of_players','max_number_of_players']},
    }