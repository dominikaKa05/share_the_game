from search_views.filters import BaseFilter
from sharing_app import models


class ProductSearchFilter(BaseFilter):
    search_fields = {
        'search_title' : ['name'],
        'search_category': ['category'],
        'search_age_min' : { 'operator' : '__gte', 'fields' : ['min_age'] },
        # 'search_players' : { 'operator' : '__range(min_number_of_players, max_number_of_players)', 'fields' : ['min_number_of_players','max_number_of_players'] },
		'search_players': { 'operator' :'__gte',' fields' : ['min_number_of_players'] }, {'operator':'__lte', 'fields': ['max_number_of_players']}:
    }