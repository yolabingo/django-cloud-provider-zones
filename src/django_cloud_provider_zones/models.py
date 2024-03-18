from django.db import models


class CloudProvider(models.Model):
    """this db data is generated by external scripts"""

    provider = models.CharField(primary_key=True, max_length=64, unique=True)

    def __str__(self):
        return self.provider.upper()

    class Meta:
        verbose_name = "Cloud Provider"


class CloudRegion(models.Model):
    """this db data is generated by external scripts"""

    region_name_with_provider = models.CharField(primary_key=True, max_length=256)
    provider = models.ForeignKey(CloudProvider, on_delete=models.CASCADE)
    record_last_synced = models.CharField(max_length=256)
    region_name = models.CharField(max_length=256)
    region_short_name = models.CharField(max_length=256)
    region_short_name_with_provider = models.CharField(max_length=256)

    def __str__(self):
        return self.region_name_with_provider

    class Meta:
        ordering = ["region_name_with_provider"]
        verbose_name = "Cloud Region"


class CloudAvailabilityZone(models.Model):
    """this db data is generated by external scripts"""

    az_name_with_provider = models.CharField(primary_key=True, max_length=256)
    provider = models.ForeignKey(CloudProvider, on_delete=models.CASCADE)
    region = models.ForeignKey(CloudRegion, on_delete=models.CASCADE)
    record_last_synced = models.CharField(max_length=256)
    az_name = models.CharField(max_length=256)
    az_short_name = models.CharField(max_length=256)
    az_id = models.CharField(max_length=256, blank=True, null=True)
    az_short_name_with_provider = models.CharField(max_length=256)

    def __str__(self):
        return self.az_name_with_provider

    class Meta:
        ordering = ["az_name_with_provider"]
        verbose_name = "Cloud Availability Zone"
