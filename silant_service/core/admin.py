from django.contrib import admin
from .models import (
    Machine, Maintenance, Claim,
    EngineModel, TransmissionModel,
    DriveAxleModel, SteerAxleModel, Manufacturer, ExploitationPlace
)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        'factory_number', 'model', 'manufacturer', 'engine_model',
        'transmission_model', 'drive_axle_model', 'steer_axle_model',
        'supply_contract', 'shipment_date', 'consignee',
        'delivery_address', 'exploitation_place', 'client'
    )
    list_filter = ('model', 'shipment_date', 'client')  # Убрал service_company
    search_fields = ('factory_number', 'supply_contract', 'client__username')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'manufacturer', 'engine_model', 'transmission_model',
            'drive_axle_model', 'steer_axle_model', 'exploitation_place', 'client'
        )


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        'machine', 'maintenance_type', 'date', 'operating_hours',
        'work_order_number', 'order_date', 'service_company'
    )
    list_filter = ('maintenance_type', 'service_company', 'date')
    search_fields = ('machine__factory_number', 'work_order_number')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('machine', 'service_company')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        'machine', 'claim_date', 'operating_hours', 'failure_node',
        'failure_description', 'repair_method', 'used_parts',
        'recovery_date', 'service_company'
    )
    list_filter = ('failure_node', 'service_company', 'claim_date')
    search_fields = ('machine__factory_number', 'failure_description', 'used_parts')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('machine', 'service_company')


# Регистрация простых моделей
admin.site.register(EngineModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteerAxleModel)
admin.site.register(Manufacturer)
admin.site.register(ExploitationPlace)
