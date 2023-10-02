# from django.shortcuts import redirect, render
#
# common_timezones = {
#     'London': 'Europe/London',
#     'Paris': 'Europe/Paris',
#     'New York': 'America/New_York',
# }
#
#
# def set_timezone(request):
#     if request.method == 'POST':
#         request.session['django_timezone'] = request.POST['timezone']
#         return redirect('/')
#     else:
#         return render(request, 'flatpages/default.html', {'timezones': common_timezones})
