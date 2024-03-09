from django.shortcuts import render, redirect
from usermgmt.decorators import user_has_access
from django.contrib.auth.decorators import login_required


@user_has_access
@login_required
def notification_view(request, **kwargs):
	ctx = {**kwargs}
	ctx["backlink"] = request.GET.get("backlink")
	return render(request, "dashboard/notification.html", ctx)


@user_has_access
@login_required
def mark_as_read_view(request, **kwargs):
	request.user.notifications.mark_all_as_read()
	url = "/app/notifications"
	backlink = request.GET.get("backlink")
	if backlink != "None":
		url += "?backlink=" + backlink
	return redirect(url)
