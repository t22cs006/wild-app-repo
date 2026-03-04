import csv
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import DangerGrid

@staff_member_required
def batch_danger_post(request):
    if request.method == "POST":
        file = request.FILES["csv"]
        reader = csv.reader(file.read().decode("utf-8").splitlines())

        created = 0
        for row in reader:
            gx, gy, *reason = row
            reason = reason[0] if reason else ""

            obj, is_created = DangerGrid.objects.get_or_create(
                gx=int(gx),
                gy=int(gy),
                defaults={"reason": reason}
            )
            if is_created:
                created += 1

        return redirect("dangergrid:result")

    return render(request, "dangergrid/batch_danger_post.html")


@staff_member_required
def batch_danger_result(request):
    return render(request, "dangergrid/danger_result.html")

def danger_grid_api(request):
    """collectionmap で使う JSON API"""
    grids = DangerGrid.objects.all()
    data = {f"{g.gx},{g.gy}": g.reason for g in grids}
    return JsonResponse(data)
