from django.urls import path
from . import views

urlpatterns = [
    # Assignment CRUD
    path('assignments/',                        views.assignment_list,          name='assignment-list'),
    path('assignments/<int:pk>/',               views.assignment_detail,        name='assignment-detail'),
    path('assignments/<int:pk>/publish/',       views.publish_assignment,       name='assignment-publish'),

    # Student flow
    path('assignments/<int:pk>/start/',         views.start_submission,         name='assignment-start'),
    path('assignments/<int:pk>/save/',          views.save_responses,           name='assignment-save'),
    path('assignments/<int:pk>/submit/',        views.submit_assignment,        name='assignment-submit'),
    path('assignments/<int:pk>/my-submission/', views.my_submission,            name='assignment-my-submission'),

    # Teacher flow
    path('assignments/<int:pk>/submissions/',   views.submission_list,          name='submission-list'),
    path('submissions/<int:sub_id>/',           views.submission_detail,        name='submission-detail'),
    path('submissions/<int:sub_id>/grade/',     views.grade_submission_view,    name='submission-grade'),
]
