from django.test import TestCase, Client
from django.urls import reverse
from deal.models import Deals, Adress,AssetsForSale,PropertyStatus
import json
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.add_deal_url = reverse('add-deal')
        self.address_assets_url = reverse('address_assets')
        self.save_deal_url = reverse('save_deal')

        self.address1 = Adress.objects.create(city="New York City", state_code="NY", location="")
        self.asset1 = AssetsForSale.objects.create()
        
        self.user = User.objects.create_user(username='testuser', email='test@company.com', password='12345')
        self.deal1 = Deals.objects.create(owner=self.user, name='deal1', property_status='Sale')
        
        self.pk = self.deal1.pk

        self.deal_detail_url = reverse('deal-detail', args=[self.pk])
        self.delete_url = reverse('deal_delete', args = [self.pk])
        self.query_data = {'csrfmiddlewaretoken': ['mjPODcrEb4GpyCPWr3uDP0MjDRjqwON45j3oRmDaAaU0g5AYRLCmc575wChNiTQp'], 'city': ['New York City'], 'state_code': ['NY'], 'location': [''], 'sort': ['frehsnest'], 'price_min': [''], 'price_max': [''], 'beds_min': [''], 'beds_max': [''], 'baths_min': [''], 'baths_max': [''], 'property_type': [''], 'property_type_nyc_only': [''], 'new_construction': [''], 'hide_pending_contingent': [''], 'has_virtual_tours': [''], 'has_3d_tours': [''], 'hide_foreclosure': [''], 'price_reduced': [''], 'open_house': [''], 'keywords': [''], 'no_hoa_fee': [''], 'hoa_max': [''], 'expand_search_radius': [''], 'home_size_min': ['', ''], 'lot_size_min': [''], 'lot_size_max': [''], 'stories': [''], 'garage': [''], 'heating_cooling': [''], 'inside_rooms': [''], 'outside_features': [''], 'lot_views': [''], 'community_ammenities': ['']}

     

    def test_index_GET(self):

        
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/Views/index.html')

    def test_add_deal_GET(self):
        login = self.client.login(username='testuser', password='12345')

        response = self.client.get(self.add_deal_url)
        

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/Views/add-deal.html')

        
    def test_add_deal_POST(self):
        login = self.client.login(username='testuser', password='12345')

        property_status = "Sale"
        context = {
        'property_status':property_status,
        'name':'deal'
        
        }
        
        response = self.client.post(self.add_deal_url, context)

        self.assertEquals(response.status_code, 302)
        #self.assertEquals(self.deal1.name, 'deal1')



    def test_address_assets_GET(self):
        login = self.client.login(username='testuser', password='12345')

        response = self.client.get(self.address_assets_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/Views/address_asset.html')

    
    def test_address_assets_POST(self):
        login = self.client.login(username='testuser', password='12345')

        context = {
            'city':'New York City',
            'state_code': 'NY',
            'location':'',
            'property_status':'Sale',
            'csrfmiddlewaretoken':'csrfmiddlewaretoken',
            'property_type':'land'
        }


        response = self.client.post(self.address_assets_url, context)
        self.assertEquals(response.status_code, 200)


    def test_save_deal_GET(self):
        login = self.client.login(username='testuser', password='12345')

        deal2 = Deals(owner=self.user, name="deal2", property_status="Sale")
        deal2.save()
        deal_get = Deals.objects.get(pk=2)

        self.assertEquals(deal_get.name, "deal2")
        

    def test_deal_detail_GET(self):
        
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(self.deal_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/Views/deal-detail.html')
    

    
 

    
    