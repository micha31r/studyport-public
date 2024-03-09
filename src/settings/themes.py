from project import utils

# Ordered
# CHART_PALETTE = [
#     "#6EB1FF", # Light blue
#     "#00C2FF", # Blue
#     "#004EE4", # Dark blue
#     "#C387FF", # Light purple
#     "#8032E2", # Purple
#     "#FDA9BD", # Pink
#     "#CC38AB", # Bright pink
#     "#CF192F", # Red
#     "#F6A87C", # Light orange
#     "#DF6F07", # Orange
#     "#FDCC21", # Light yellow
#     "#D2B100", # Yellow
#     "#98DF00", # Light green
#     "#00862E", # Dark green
#     "#13C2A3", # Turquoise
# ]


CHART_PALETTE = [
    "#6EB1FF", # Light blue
    "#004EE4", # Dark blue
    "#FDA9BD", # Pink
    "#C387FF", # Light purple
    "#13C2A3", # Turquoise
    "#CC38AB", # Bright pink
    "#DF6F07", # Orange
    "#F6A87C", # Light orange
    "#D2B100", # Yellow
    "#00862E", # Dark green
    "#00C2FF", # Blue
    "#FDCC21", # Light yellow
    "#CF192F", # Red
    "#8032E2", # Purple
    "#98DF00", # Light green
]


def get_theme(user):
    ctx = {}
    profile = getattr(user, "student", None) or getattr(user, "staff", None)
    ctx["chart_palette"] = CHART_PALETTE
    ctx["chart_color_data"] = utils.deep_serialize(profile.color_settings)
    return ctx