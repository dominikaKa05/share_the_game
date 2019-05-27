from search_views.filters import BaseFilter
from sharing_app import models


class ProductSearchFilter(BaseFilter):
	search_fields = {
		'search_title': {'operator': '__icontains', 'fields': ['name']},
		'search_category': {'operator': '__istartswith' , 'fields': ['category']},
		'search_age_min': {'operator': '__lte', 'fields': ['min_age']},
		'search_players_min': {'operator': '__exact', 'fields': ['min_number_of_players']},
		'search_players_max': {'operator': '__gte', 'fields': ['max_number_of_players']},


	}
