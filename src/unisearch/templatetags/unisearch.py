from django import template
from unisearch.mappings import MAPPINGS

register = template.Library()

@register.filter
def get_search_mappings(value):
	results = []
	for item in MAPPINGS["views"]:
		results.append({
			"name": item["name"],
			"description": item["description"],
			"url": item["url"],
		})
		if item.get("components"):
			for component in item["components"]:
				results.append({
					"name": f"{item['name']} / {component['name']}",
					"description": component["description"],
					"url": item["url"] + component["url"],
				})
	return results