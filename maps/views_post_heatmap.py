# maps/views_post_heatmap.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wildlife.constants import CENTER_LAT, CENTER_LON, GRID_SIZE, MIN_LAT, MAX_LAT, MIN_LON, MAX_LON, HALF_LAT_SPAN, HALF_LON_SPAN


@login_required
def heatmap_dashboard(request):
    context = {
        'CENTER_LAT': CENTER_LAT,
        'CENTER_LON': CENTER_LON,
        'GRID_SIZE': GRID_SIZE,
        'MIN_LAT': MIN_LAT,
        'MAX_LAT': MAX_LAT,
        'MIN_LON': MIN_LON,
        'MAX_LON': MAX_LON,
        'HALF_LAT_SPAN': HALF_LAT_SPAN,
        'HALF_LON_SPAN': HALF_LON_SPAN,
    }
    return render(request, "maps/heatmap_dashboard.html", context)

