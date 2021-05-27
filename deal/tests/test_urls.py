from django.test import SimpleTestCase
from django.urls import reverse, resolve
from deal.views import index,add_deal,address_asset,save_deal,view_deal_detail, deal_delete


class TestUrls(SimpleTestCase):


    def test_index_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_add_deal(self):
        url = reverse('add-deal')
        self.assertEqual(resolve(url).func, add_deal)
    
    def test_address_assets(self):
        url = reverse('address_assets')
        self.assertEqual(resolve(url).func, address_asset)
    
    def test_save_deal(self):
        url = reverse('save_deal')
        self.assertEqual(resolve(url).func, save_deal)
    
    def test_view_deal_detail_is_resolved(self):
        url = reverse('deal-detail', args=[1])
        self.assertEqual(resolve(url).func, view_deal_detail)
    
    def test_delete_deal_is_resolved(self):
        url = reverse('deal_delete', args=[1])
        self.assertEqual(resolve(url).func, deal_delete)
    
    

    