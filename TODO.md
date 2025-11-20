# TODO: TouristAlertSystem Tasks

## Remove GIS Features
- [ ] Remove 'leaflet' from INSTALLED_APPS in project/settings.py
- [ ] Remove django-leaflet from requirements.txt
- [ ] Search and remove any leaflet template tags (leaflet_js, leaflet_css, leaflet_map) from templates
- [ ] Confirm models use FloatField for lat/lng
- [ ] Ensure admin classes are normal ModelAdmin
- [ ] Ensure all templates use CDN Leaflet.js instead of django-leaflet
- [ ] Check alerts/templates/alerts/dashboard.html for leaflet tags and fix
- [ ] Verify maps work with JavaScript-only Leaflet
- [ ] Run python manage.py check
- [ ] Run python manage.py migrate
- [ ] Run python manage.py runserver
- [ ] Ensure no GDAL dependencies
- [ ] Confirm project uses only Django, Gunicorn, CDN Leaflet
- [ ] No GIS initialization during startup

## Connect Modules and Update Dashboard
- Correct app_name in authentication/urls.py from 'alerts' to 'authentication'.
- Update urlpatterns to match views.py (login_view, logout_view).
- Add path('auth/', include('authentication.urls')) to project/urls.py.
- Create users/urls.py with app_name='users' and urlpatterns for profile.
- Create users/views.py with profile_view function to display/edit user settings.
- Add path('users/', include('users.urls')) to project/urls.py.
- Add user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True) to Alert model.
- Remove or replace source CharField with user field.
- Modify alerts/views.py to set alert.user = request.user instead of source.
- Update serializers if needed.
- Execute python manage.py makemigrations and migrate for the model change.
- Add a refresh button or AJAX endpoint in dashboard/views.py to fetch new OSINT alerts.
- Modify dashboard template to include refresh functionality.
- Verify login/logout, user profile, alert creation with user link, and dashboard updates.

## Completed Steps:
- [x] Step 1: Fixed authentication URLs
- [x] Step 2: Included authentication in main URLs
- [x] Step 3: Created users URLs and views
- [x] Step 4: Included users in main URLs
- [x] Step 5: Updated Alert model with user ForeignKey
- [x] Step 6: Updated alerts views to use user field
- [x] Step 7: Ran migrations successfully
- [x] Step 8: Added refresh OSINT endpoint and button
- [x] Step 9: Ready for testing
