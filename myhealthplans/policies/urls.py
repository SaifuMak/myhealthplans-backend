from django.urls import path
from .views import PolicyActions,PolicyDetailView

urlpatterns = [
    path('actions/', PolicyActions.as_view(), name='policy-actions'),
     path('actions/<int:pk>/', PolicyDetailView.as_view(), name='policy-detail'),

]