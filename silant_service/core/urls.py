from django.urls import path
from .views import (
    MachineListView, MachineDetailView, ClientMachineListView, ServiceMachineListView,
    MaintenanceListView, ClaimListView, WelcomeView, MachineSearchView
)
from rest_framework.routers import DefaultRouter
from .api import MachineViewSet, MaintenanceViewSet, ClaimViewSet

router = DefaultRouter()
router.register(r'api/machines', MachineViewSet)
router.register(r'api/maintenances', MaintenanceViewSet)
router.register(r'api/claims', ClaimViewSet)

urlpatterns = [
    path('', WelcomeView.as_view(), name='home'),
    path('search/', MachineSearchView.as_view(), name='machine_search'),
    path('machines/', MachineListView.as_view(), name='machine_list'),
    path('machines/<int:pk>/', MachineDetailView.as_view(), name='machine_detail'),
    path('my-machines/', ClientMachineListView.as_view(), name='client_machine_list'),
    path('service-machines/', ServiceMachineListView.as_view(), name='service_machine_list'),
    path('maintenances/', MaintenanceListView.as_view(), name='maintenance_list'),
    path('claims/', ClaimListView.as_view(), name='claim_list'),
]

urlpatterns += router.urls
