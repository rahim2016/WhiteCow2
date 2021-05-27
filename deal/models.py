from embed_video.fields import EmbedVideoField
from django.db import models
import pandas as pd
import numpy as np
import requests
from .config import *
import json
from django.contrib.auth.models import User
import logging
from django.utils.timezone import now
import json
import uuid

from django.db import models
from django.utils import timezone
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask,CrontabSchedule
from .enums import TimeInterval, SetupStatus

logger = logging.getLogger('django')

# Create your models here.
class Deals(models.Model):
    
    name = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateTimeField(default=now, blank=True, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Deals'
        ordering = ['-date']

class Setup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setups'
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    deal = models.OneToOneField(Deals, on_delete=models.CASCADE, related_name="deal_setup", blank=True, null=True)
    title = models.CharField(max_length=70, blank=False)
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    created_at = models.DateTimeField(auto_now_add=True)
    time_interval = EnumChoiceField(
        TimeInterval, default=TimeInterval.every_day)

    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.title
    

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()

        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.title,
            task='computation_heavy_task',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

    @property
    def interval_schedule(self):
        if self.time_interval == TimeInterval.one_min:
            return CrontabSchedule.objects.get( minute='1',hour='*',day_of_week='*',day_of_month='*', month_of_year='*',)
        if self.time_interval == TimeInterval.every_day:
            return CrontabSchedule.objects.get( minute='0',hour='8',day_of_week='*',day_of_month='*', month_of_year='*',)
        if self.time_interval == TimeInterval.week_ends:
            return CrontabSchedule.objects.get( minute='0',hour='8',day_of_week='6,0',day_of_month='*', month_of_year='*',)

        raise NotImplementedError(
            '''Interval Schedule for {interval} is not added.'''.format(
                interval=self.time_interval.value))



class SchedulerTime(models.Model):
    name = models.CharField(max_length=40, blank=True, null = True)

    def __str__(self):
        return self.name
    

class PropertyStatus(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = 'PropertyStatus'

class Adress(models.Model):
    """
    Addres Class contains attributes necessary for saving the Adress of a deal.
    """
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    deal = models.OneToOneField(Deals, on_delete=models.CASCADE, related_name="deal_address", blank=True, null=True)
    city = models.CharField(max_length=40)
    state_code = models.CharField(max_length=10)
    location = models.CharField(max_length=10, blank=True, default='') #postal code

    offset = models.CharField(max_length=10, default="0")
    limit = models.IntegerField(default=30)

    def __str__(self):
        return "{}, {}".format(self.city, self.state_code)

class AssetsForRent(models.Model):
    
    deal = models.ForeignKey(Deals, on_delete=models.CASCADE, related_name="deal_assets_for_rent", blank=True, null=True)
    
    sort = models.CharField(max_length=255, blank=True, null=True)
    price_min = models.IntegerField(blank=True, null=True)
    price_max = models.IntegerField(blank=True, null=True)
    beds_min = models.IntegerField(blank=True, null=True)
    beds_max = models.IntegerField(blank=True, null=True)
    baths_min = models.IntegerField(blank=True, null=True)
    baths_max = models.IntegerField(blank=True, null=True)
    property_type = models.CharField(max_length=255, blank=True, null=True)
    expand_search_radius = models.CharField(max_length=25, blank=True, null=True)
    include_nearby_areas_slug_id = models.CharField(max_length=255, blank=True, null=True)
    home_size_min = models.IntegerField(blank=True, null=True)
    home_size_max = models.IntegerField(blank=True, null=True)
    in_unit_features = models.CharField(max_length=255, blank=True, null=True)
    community_ammenities = models.CharField(max_length=255, blank=True, null=True)
    cats_ok = models.CharField(max_length=30, blank=True, null=True)
    dogs_ok = models.CharField(max_length=30, blank=True, null=True)


    def __str__(self):
        return "Assets for rent"

class Sort(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
    
class PropertyType(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
class ExpandSearchRadius(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
class HomeSize(models.Model):

    value = models.IntegerField(blank=True, null=True)

    
   
class InUnitFeatures(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class CommunityAmmenities(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
class Ok (models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

    


class AssetsForSale(models.Model):
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True) 
    deal = models.OneToOneField(Deals, on_delete=models.CASCADE, related_name="deal_assets_for_sale", blank=True, null=True)

    sort = models.CharField(max_length=255, blank=True, null=True)
    price_min = models.IntegerField(blank=True, null=True)
    price_max = models.IntegerField(blank=True, null=True)
    beds_min = models.IntegerField(blank=True, null=True)
    beds_max = models.IntegerField(blank=True, null=True)
    baths_min = models.IntegerField(blank=True, null=True)
    baths_max = models.IntegerField(blank=True, null=True)
    property_type = models.CharField(max_length=255, blank=True, null=True)
    property_type_nyc_only = models.CharField(max_length=255, blank=True, null=True)
    new_construction = models.CharField(max_length=25, blank=True, null=True)
    hide_pending_contingent = models.CharField(max_length=25, blank=True, null=True)
    has_virtual_tours = models.CharField(max_length=25, blank=True, null=True)
    has_3d_tours = models.CharField(max_length=25, blank=True, null=True)
    hide_foreclosure = models.CharField(max_length=25, blank=True, null=True)
    price_reduced = models.CharField(max_length=25, blank=True, null=True)
    open_house = models.CharField(max_length=25, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    no_hoa_fee = models.CharField(max_length=25, blank=True, null=True)
    hoa_max = models.IntegerField(blank=True, null=True)
    days_on_realtor = models.CharField(max_length=25, blank=True, null=True)
    expand_search_radius = models.CharField(max_length=25, blank=True, null=True)
    include_nearby_areas_slug_id = models.CharField(max_length=255, blank=True, null=True)
    home_size_min = models.IntegerField(blank=True, null=True)
    home_size_max = models.IntegerField(blank=True, null=True)
    lot_size_min = models.IntegerField(blank=True, null=True)
    lot_size_max = models.IntegerField(blank=True, null=True)
    stories = models.CharField(max_length=25, blank=True, null=True)
    garage = models.CharField(max_length=25, blank=True, null=True)
    heating_cooling = models.CharField(max_length=25, blank=True, null=True)
    inside_rooms = models.CharField(max_length=255, blank=True, null=True)
    outside_features = models.CharField(max_length=255, blank=True, null=True)
    lot_views = models.CharField(max_length=255, blank=True, null=True)
    community_ammenities = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "Assets for sale"

class SortSale(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class PropertyTypeSale(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
class PropertyTypeNycOnly(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name



class NoHoaFee(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class HomeSizeMinSale(models.Model):

    value = models.IntegerField(blank=True, null=True)

class HomeSizeMaxSale(models.Model):

    value = models.IntegerField(blank=True, null=True)

class LotSize(models.Model):

    value = models.IntegerField(blank=True, null=True)

class Stories(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class Garage(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class HeatingCooling(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class InsideRooms(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
class OutsideFeatures(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name
class LotViews(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class CommunityAmmenitiesSale(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

class FeaturesInNycOnly(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name


class SubscriptionDataForRent(models.Model):
    
    deal = models.ForeignKey(Deals, on_delete=models.CASCADE, related_name="deal_subscription_for_rent", blank=True, null=True)
    
    photos = models.JSONField(blank=True, null = True)
    branding = models.JSONField(blank=True, null = True)
    other_listings = models.JSONField(blank=True, null = True)
    list_price_min = models.IntegerField(blank=True, null = True)
    href = models.CharField(max_length=255,blank=True, null = True )
    when_indexed = models.DateTimeField(blank=True, null = True )
    last_sold_price = models.FloatField(blank=True, null = True )
    property_id = models.CharField(max_length=255,blank=True, null = True )
    advertisers = models.JSONField(blank=True, null = True)
    virtual_tours = models.CharField(max_length=50,blank=True, null = True )
    seller_promotion = models.CharField(max_length=50,blank=True, null = True )
    listing_id = models.CharField(max_length=50,blank=True, null = True )
    price_reduced_amount = models.CharField(max_length=50,blank=True, null = True )
    location = models.JSONField(blank=True, null = True)
    last_update_date = models.DateTimeField(blank=True, null = True )
    source = models.JSONField(blank=True, null = True)
    permalink = models.CharField(max_length=255,blank=True, null = True )
    list_date = models.DateTimeField(blank=True, null = True )
    open_houses = models.CharField(max_length=50,blank=True, null = True )
    last_sold_date = models.DateField(blank=True, null = True )
    last_price_change_date = models.DateField(blank=True, null = True )
    description = models.JSONField(blank=True, null = True)
    last_price_change_amount = models.CharField(max_length=50,blank=True, null = True )
    price_reduced_date = models.DateField(blank=True, null = True )
    property_history = models.CharField(max_length=50,blank=True, null = True )
    photo_count = models.IntegerField(blank=True, null = True)
    list_price = models.CharField(max_length=50,blank=True, null = True )
    lead_attributes = models.JSONField(blank=True, null = True)
    list_price_max = models.IntegerField(blank=True, null = True)
    tags = models.CharField(max_length=255,blank=True, null = True )
    pet_policy = models.JSONField(blank=True, null = True)
    products = models.JSONField(blank=True, null = True)
    suppression_flags = models.CharField(max_length=50,blank=True, null = True )
    status = models.CharField(max_length=10,blank=True, null = True )
    flags = models.JSONField(blank=True, null = True)
    community = models.CharField(max_length=50,blank=True, null = True )
    matterport = models.BooleanField(blank=True, null = True )
    primary_photo = models.JSONField(blank=True, null = True)


class SubscriptionDataForSale(models.Model):
    
    
    primary_photo = models.JSONField(max_length=10485760,blank=True, null = True)
    date = models.DateTimeField(default=now, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null = True )
    source = models.JSONField(max_length=10485760,blank=True, null = True)
    tags = models.CharField(max_length=10485760,blank=True, null = True )
    permalink = models.CharField(max_length=10485760,blank=True, null = True )
    status = models.CharField(max_length=10485760,blank=True, null = True )
    list_date = models.DateTimeField(blank=True, null = True )
    open_houses = models.CharField(max_length=10485760,blank=True, null = True )
    description = models.JSONField(max_length=10485760,blank=True, null = True)
    branding = models.JSONField(max_length=10485760,blank=True, null = True)
    list_price = models.IntegerField(blank=True, null = True)
    lead_attributes = models.JSONField(max_length=10485760,blank=True, null = True)
    property_id = models.CharField(max_length=10485760,blank=True, null = True )
    photos = models.JSONField(max_length=10485760,blank=True, null = True)
    flags = models.JSONField(max_length=10485760,blank=True, null = True)
    community = models.CharField(max_length=10485760,blank=True, null = True )
    products = models.JSONField(max_length=10485760,blank=True, null = True)
    virtual_tours = models.CharField(max_length=10485760,blank=True, null = True )
    other_listings = models.JSONField(max_length=100000,blank=True, null = True)
    listing_id = models.CharField(max_length=10485760,blank=True, null = True )
    price_reduced_amount = models.CharField(max_length=10485760,blank=True, null = True )
    location = models.JSONField(max_length=10485760,blank=True, null = True)
    matterport = models.CharField(max_length=10485760,blank=True, null = True )
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    deal = models.ForeignKey(Deals, on_delete=models.SET_NULL, related_name="deal_subscription_for_sale", blank=True, null=True)

    
    


    

    
    



class Item(models.Model):
    video = EmbedVideoField()  # same like models.URLField()
