from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView
from .models import Machine, Maintenance, Claim


# Проверки
def is_client(user):
    return user.groups.filter(name="Клиент").exists()

def is_service_company(user):
    return user.groups.filter(name="Сервисная организация").exists()


# Главная страница (гостевой доступ)
class WelcomeView(TemplateView):
    template_name = 'machines/welcome.html'


# Поиск машины по заводскому номеру без авторизации
class MachineSearchView(TemplateView):
    template_name = 'machines/machine_search_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('factory_number')
        machine = None
        if query:
            try:
                machine = Machine.objects.only(
                    'factory_number', 'model', 'engine_model', 'transmission_model',
                    'drive_axle_model', 'steer_axle_model', 'shipment_date'
                ).get(factory_number=query)
            except Machine.DoesNotExist:
                pass
        context['machine'] = machine
        context['query'] = query
        return context


@method_decorator([login_required, user_passes_test(is_client)], name='dispatch')
class MachineListView(ListView):
    model = Machine
    template_name = 'machines/machine_list.html'
    context_object_name = 'machines'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        equipment_model = self.request.GET.get('equipment_model')
        engine_model = self.request.GET.get('engine_model')
        transmission_model = self.request.GET.get('transmission_model')
        drive_axle = self.request.GET.get('drive_axle_model')
        steer_axle = self.request.GET.get('steer_axle_model')
        sort_by = self.request.GET.get('sort_by')

        if equipment_model:
            queryset = queryset.filter(model__icontains=equipment_model)
        if engine_model:
            queryset = queryset.filter(engine_model__name__icontains=engine_model)
        if transmission_model:
            queryset = queryset.filter(transmission_model__name__icontains=transmission_model)
        if drive_axle:
            queryset = queryset.filter(drive_axle_model__name__icontains=drive_axle)
        if steer_axle:
            queryset = queryset.filter(steer_axle_model__name__icontains=steer_axle)
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset


@method_decorator([login_required, user_passes_test(is_client)], name='dispatch')
class MachineDetailView(DetailView):
    model = Machine
    template_name = 'machines/machine_detail.html'
    context_object_name = 'machine'

    def get_queryset(self):
        return Machine.objects.filter(client=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        machine = self.object
        context['maintenances'] = machine.maintenance_set.all()
        context['claims'] = machine.claim_set.all()
        return context


@method_decorator([login_required, user_passes_test(is_client)], name='dispatch')
class ClientMachineListView(ListView):
    model = Machine
    template_name = 'core/client_machine_list.html'
    context_object_name = 'machines'

    def get_queryset(self):
        queryset = Machine.objects.filter(client=self.request.user).select_related(
            'manufacturer', 'engine_model', 'transmission_model',
            'drive_axle_model', 'steer_axle_model', 'exploitation_place'
        )

        model = self.request.GET.get('model')
        engine_model = self.request.GET.get('engine_model')
        transmission_model = self.request.GET.get('transmission_model')
        drive_axle = self.request.GET.get('drive_axle_model')
        steer_axle = self.request.GET.get('steer_axle_model')
        sort_by = self.request.GET.get('sort_by')

        if model:
            queryset = queryset.filter(model__icontains=model)
        if engine_model:
            queryset = queryset.filter(engine_model__name__icontains=engine_model)
        if transmission_model:
            queryset = queryset.filter(transmission_model__name__icontains=transmission_model)
        if drive_axle:
            queryset = queryset.filter(drive_axle_model__name__icontains=drive_axle)
        if steer_axle:
            queryset = queryset.filter(steer_axle_model__name__icontains=steer_axle)
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset


@method_decorator([login_required, user_passes_test(is_service_company)], name='dispatch')
class ServiceMachineListView(ListView):
    model = Machine
    template_name = 'machines/service_machine_list.html'
    context_object_name = 'machines'

    def get_queryset(self):
        user = self.request.user

        return Machine.objects.filter(
            maintenance__service_company=user
        ).union(
            Machine.objects.filter(claim__service_company=user)
        ).distinct().select_related(
            'manufacturer', 'engine_model', 'transmission_model',
            'drive_axle_model', 'steer_axle_model', 'exploitation_place'
        )


@method_decorator([login_required], name='dispatch')
class MaintenanceListView(ListView):
    model = Maintenance
    template_name = 'machines/maintenance_list.html'
    context_object_name = 'maintenances'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        machine = self.request.GET.get('machine')
        service_company = self.request.GET.get('service_company')
        maintenance_type = self.request.GET.get('maintenance_type')
        sort_by = self.request.GET.get('sort_by', '-date')

        if machine:
            qs = qs.filter(machine__factory_number__icontains=machine)
        if service_company:
            qs = qs.filter(service_company__username__icontains=service_company)
        if maintenance_type:
            qs = qs.filter(maintenance_type__icontains=maintenance_type)

        return qs.order_by(sort_by)


@method_decorator([login_required], name='dispatch')
class ClaimListView(ListView):
    model = Claim
    template_name = 'machines/claim_list.html'
    context_object_name = 'claims'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        node = self.request.GET.get('failure_node')
        repair = self.request.GET.get('repair_method')
        service_company = self.request.GET.get('service_company')
        sort_by = self.request.GET.get('sort_by', '-claim_date')

        if node:
            qs = qs.filter(failure_node__icontains=node)
        if repair:
            qs = qs.filter(repair_method__icontains=repair)
        if service_company:
            qs = qs.filter(service_company__username__icontains=service_company)

        return qs.order_by(sort_by)
