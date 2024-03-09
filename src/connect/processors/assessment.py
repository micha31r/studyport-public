import uuid, base64
from standards.models import Assessment

# https://directoryservices.kamar.nz/?listening-service/Messages/assessments

def run(data):
	success = True
	assessments = data["assessments"]["data"]

	for i in range(len(assessments)-1, -1, -1):
		item = assessments[i]

		if item["type"] in ["A", "U", "G"]:
			number 				= item["number"]
			type_ 				= item["type"]
			title 				= item["title"]
			description 		= item["description"]
			subfield 			= item["subfield"]
			credits 			= item["credits"]
			level 				= item["level"]
			internalexternal 	= item["internalexternal"].lower()
			
			if not (number and type_ and title and subfield and credits and level and internalexternal):
				success = False
				continue
				
			obj = Assessment.objects.filter(assessment_code=number).first()
			if not obj:
				obj = Assessment.objects.create(
					assessment_code = number,
					result_type 	= type_,
					title 			= title,
					description 	= description,
					subfield 		= subfield,
					credits 		= credits,
					level 			= level,
					assessment_type = internalexternal,
				)
			else:
				obj.assessment_code = number
				obj.result_type 	= type_
				obj.title 			= title
				obj.description 	= description
				obj.subfield 		= subfield
				obj.credits 		= credits
				obj.level 			= level
				obj.assessment_type = internalexternal
				obj.save()

			assessments.pop(i)

	data["assessments"]["count"] = len(assessments)
	data["assessments"]["data"] = assessments
	return success, data["assessments"]


