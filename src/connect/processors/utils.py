from group.models import School

ALLOWED_TYPES = [40]

def get_school(schools, schoolindex):
	for school in schools:
		# Type 40 is for secondary schools (year 9-13)
		if schoolindex == school["schoolindex"] and school["type"] in ALLOWED_TYPES:
			return School.objects.get(moe_code=school["moeCode"])
	return None