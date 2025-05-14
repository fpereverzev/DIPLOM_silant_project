from django.db import models
from django.contrib.auth.models import User


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EngineModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TransmissionModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DriveAxleModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SteerAxleModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExploitationPlace(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Machine(models.Model):
    factory_number = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    engine_model = models.ForeignKey(EngineModel, on_delete=models.CASCADE)
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.CASCADE)
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete=models.CASCADE)
    steer_axle_model = models.ForeignKey(SteerAxleModel, on_delete=models.CASCADE)
    supply_contract = models.CharField(max_length=100)
    shipment_date = models.DateField()
    consignee = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=255)
    exploitation_place = models.ForeignKey(ExploitationPlace, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Клиент'})

    def __str__(self):
        return f"{self.model} ({self.factory_number})"


class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=100)
    date = models.DateField()
    operating_hours = models.PositiveIntegerField()
    work_order_number = models.CharField(max_length=100)
    order_date = models.DateField()
    service_company = models.ForeignKey(User, on_delete=models.CASCADE,
                                        limit_choices_to={'groups__name': 'Сервисная организация'})

    def __str__(self):
        return f"ТО #{self.pk} для {self.machine}"


class Claim(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    claim_date = models.DateField()
    operating_hours = models.PositiveIntegerField()
    failure_node = models.CharField(max_length=100)
    failure_description = models.TextField()
    repair_method = models.TextField()
    used_parts = models.TextField()
    recovery_date = models.DateField()
    service_company = models.ForeignKey(User, on_delete=models.CASCADE,
                                        limit_choices_to={'groups__name': 'Сервисная организация'})

    def __str__(self):
        return f"Рекламация #{self.pk} для {self.machine}"
