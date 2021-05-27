from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .view_method import *
import json,requests
from datetime import datetime
import datetime as datetime_
from django_pandas.io import read_frame
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import sys,six,json
from django.http import JsonResponse
from django.core.paginator import Paginator
import pandas as pd
from .enums import *
from django.http import JsonResponse
# Create your views here.

@login_required
def search_deals(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        deals = Deals.objects.filter(date__icontains=search_str, owner=request.user) | Deals.objects.filter(
            name__icontains=search_str, owner=request.user)
        data = deals.values()
        return JsonResponse(list(data), safe=False)

    
def index(request):
    """
    This view is to display the landing page

    """

    return render(request, 'deal/Views/index.html')

# Create your views here.
@login_required
def view_deal(request):
    """
    This view is to display the landing page

    """

    deal = Deals.objects.filter(owner =request.user)
    paginator = Paginator(deal, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {'saved_deals':deal,
                 'page_obj': page_obj}
    return render(request, 'deal/Views/dashboard.html',context)
@login_required
def dashboad(request):
    """
    This view is to display the landing page

    """

    deal = Deals.objects.filter(owner =request.user)
    paginator = Paginator(deal, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {'saved_deals':deal,
                 'page_obj': page_obj}
    return render(request, 'deal/Views/dashboad.html',context)

deal_data =None
def add_deal(request):
    """
    Form for deal name and property status
    """
    property_status = PropertyStatus.objects.all()
    context = {
        'property_status':property_status
    }

    if request.method == 'GET':

        return render(request, 'deal/Views/add-deal.html', context)
    if request.method =='POST':
        name = request.POST['name']
        scheduler_time = request.POST['time']
        print("######## Deal's name is ", name)
       # import pdb
        #pdb.set_trace()
        property_status = request.POST['property_status']
        
        global  deal_data
        def deal_data():
            return property_status, name
        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'deal/Views/add-deal.html', context)

       

        return redirect('address_assets')


def address_asset(request):
    sort  = Sort.objects.all()
    property_type = PropertyType.objects.all()
    expand_search_radius = ExpandSearchRadius.objects.all()
    home_size = HomeSize.objects.all()
    in_unit_features = InUnitFeatures.objects.all()
    community_ammenities = CommunityAmmenities.objects.all()
    ok = Ok.objects.all()

    sort_sale = SortSale.objects.all()
    property_type_sale = PropertyTypeSale.objects.all()
    property_type_nyc_only = PropertyTypeNycOnly.objects.all()
    no_hoa_fee = NoHoaFee.objects.all()
    home_size_min_sale = HomeSizeMinSale.objects.all()
    home_size_max_sale = HomeSizeMaxSale.objects.all()
    lot_size = LotSize.objects.all()
    stories = Stories.objects.all()
    garage = Garage.objects.all()
    heating_cooling = HeatingCooling.objects.all()
    inside_rooms = InsideRooms.objects.all()
    outside_features = OutsideFeatures.objects.all()
    lot_views = LotViews.objects.all()
    community_ammenities_sale = CommunityAmmenitiesSale.objects.all()
    features_in_nyc_only = FeaturesInNycOnly.objects.all()


    context = {
        'sort':sort,
        'property_types':property_type,
        'expand_search_radius':expand_search_radius,
        'home_sizes':home_size,
        'in_unit_features':in_unit_features,
        'community_ammenities':community_ammenities,
        'ok':ok,
        'sort_sales':sort_sale,
        'property_type_sales':property_type_sale,
        'property_type_nyc_only':property_type_nyc_only,
        'no_hoa_fees':no_hoa_fee,
        'home_size_min_sales':home_size_min_sale,
        'home_size_max_sales':home_size_max_sale,
        'lot_sizes':lot_size,
        'stories':stories,
        'garages':garage,
        'heating_coolings':heating_cooling,
        'inside_rooms':inside_rooms,
        'outside_features':outside_features,
        'lot_views':lot_views,
        'community_ammenities_sales':community_ammenities_sale,
        'features_in_nyc_only':features_in_nyc_only

    }
    
    if request.method == 'GET':
        
       
        
        return render(request, 'deal/Views/address_asset.html', context)
    
    if request.method == 'POST':
        city = request.POST['city']
        state_code = request.POST['state_code']
        location = request.POST['location']
        
        
        if not city:
            messages.error(request, 'City is required')
            return render(request, 'deal/Views/address_asset.html', context)
        if not state_code:
            messages.error(request, 'State code is required')
            return render(request, 'deal/Views/address_asset.html', context)
        

        query= request.POST
        query_data = query.copy()
       # print(query_data)
        query_data.pop('csrfmiddlewaretoken')
        d = {k:v.strip('[]') for k,v in query_data.items()}
        print("Data to make API call is : ", d)

       
  
    
       
        print("computing Deal......\n")
        response = property_search_query(url = url_for_sale, query_params=d)
        df = process_query_response(response=response)
            #deal_df = pd.read_csv('/Users/home/Documents/GitHub/WhiteCow2/deal/deal_df.csv')
            #df = pd.read_csv('/Users/home/Documents/GitHub/WhiteCow2/sale.csv')
        list_property_id = df['property_id'].tolist()[:3]
        deal_dict = calculate_deal(list_property_id, df)
            
        deal_df = get_deal_datafrane(deal_dict, df)
           
        deal_df = deal_df.where(deal_df.notnull(), None)

        deal_df = formatting(deal_df)
        print("Here is the Deal \n")
        print(deal_df)

        context['deals'] = deal_df
            
           
        property_type = d['property_type']
        context['property_type'] = property_type

        request.session['city'] = city
        request.session['state_code'] = state_code
        request.session['location'] = location
        request.session['d'] = d
        deal= json.loads(deal_df.to_json())
        request.session['deal_df'] = deal

      
        context['deals'] = deal_df
        return render(request, 'deal/Views/address_asset.html', context)
            




def save_deal(request):

    
    

    if request.method == 'POST':
     
        name = request.POST.get('name')
        time = request.POST.get('time')
        city = request.session['city'] 
        state_code = request.session['state_code']
        location = request.session['location']
        assets = request.session['d']
        deal= request.session['deal_df']
        deal = pd.DataFrame.from_dict(deal)

        for i in deal.itertuples():
        
            deal['last_update_date'] = datetime.fromtimestamp(i.last_update_date / 1e3) 
            deal['list_date'] = datetime.fromtimestamp(i.list_date / 1e3) 
        #deal = formatting(deal)
       
        
        Deals.objects.create(name = name,owner=request.user)
        de = Deals.objects.latest('id')
        if time != "":
            if TimeInterval(time) is TimeInterval.one_min:
                Setup.objects.create(title=name,owner=request.user,deal=de,time_interval = TimeInterval.one_min)
            if TimeInterval(time) is TimeInterval.every_day:
                Setup.objects.create(title=name,owner=request.user,deal=de,time_interval = TimeInterval.every_day)
            if TimeInterval(time) is TimeInterval.week_ends:
                Setup.objects.create(title=name,owner=request.user,deal=de,time_interval = TimeInterval.week_ends)
            

        
        deal['owner'] = request.user
        deal['deal'] = de

        assets.pop('city')
        assets.pop('state_code')
        assets.pop('location')
        assets['owner'] = request.user
        assets['deal'] =  de
        
       
        for k  in assets :
            if assets[k] == '':
                assets[k] = None
        

    
        Adress.objects.create(owner=request.user,deal=de,city=city,state_code=state_code, location=location)
        AssetsForSale.objects.create(**assets)


        entries = []       
    
        for e in deal.T.to_dict().values():

            entries.append(SubscriptionDataForSale(**e))
        
        SubscriptionDataForSale.objects.bulk_create(entries)
 
            
        
       # SubscriptionDataForSale.objects.bulk_create(entries)

        return redirect('dashboad')

    return render(request, 'deal/Views/address_asset.html')


def deal_stats(request):
    todays_date = datetime_.date.today()
    one_month_ago = todays_date - datetime_.timedelta(days=30)
    one_year_ago = todays_date - datetime_.timedelta(days=30*12)
    one_day_ago = todays_date - datetime_.timedelta(days=1)
    

    deal_stats_month= SubscriptionDataForSale.objects.filter(owner=request.user,date__gte=one_month_ago).count()
    deal_stats_year= SubscriptionDataForSale.objects.filter(owner=request.user,date__gte=one_year_ago).count()
    deal_stats_day= SubscriptionDataForSale.objects.filter(owner=request.user,date__gte=one_day_ago).count()

    deal_stats_land= SubscriptionDataForSale.objects.filter(owner=request.user,description__icontains = "land").count()
    deal_stats_multi_family= SubscriptionDataForSale.objects.filter(owner=request.user,description__icontains = "multi_family").count()
    deal_stats_single_family= SubscriptionDataForSale.objects.filter(owner=request.user,description__icontains = "single_family").count()
    deal_stats_mobile= SubscriptionDataForSale.objects.filter(owner=request.user,description__icontains = "mobile").count()
    deal_stats_farm= SubscriptionDataForSale.objects.filter(owner=request.user,description__icontains = "farm").count()
    deal_stats_2021= SubscriptionDataForSale.objects.filter(owner=request.user,date__icontains = "2021").count()
    finalrep = {'month': deal_stats_month,
                'year':deal_stats_year,
                'day': deal_stats_day,
                 'land': deal_stats_land,
                  'multi_family': deal_stats_multi_family,
                   'single_family': deal_stats_single_family,
                    'mobile': deal_stats_mobile,
                     'farm': deal_stats_farm,
                      "year_2021":deal_stats_2021}

    return JsonResponse({'deal_category_data': finalrep}, safe=False)


def view_deal_detail(request, pk):

    deal = Deals.objects.get(pk=pk)

    data = SubscriptionDataForSale.objects.filter(deal_id =pk, owner=request.user)

    deal_df = read_frame(data)
    
    context = {
        'deals':deal_df
    }
    return render(request,'deal/Views/deal-detail.html',context )



def deal_delete(request, pk):
    subscription = SubscriptionDataForSale.objects.filter(owner=request.user, deal_id = pk)
    setup = Setup.objects.filter(owner=request.user, deal_id = pk)
    asset = AssetsForSale.objects.filter(owner=request.user, deal_id = pk)
    address = Adress.objects.filter(owner=request.user, deal_id = pk)
    deal = Deals.objects.filter(owner=request.user, pk = pk)  

    
    subscription.delete()
    setup.delete()
    address.delete()
    asset.delete()
    deal.delete()
    

    return redirect('dashboad')
    
@login_required
def manage_subscriptions(request):
    """
    Thie view is to display the subcriptions(saved deals) a user has made
    """
    
    deal = Deals.objects.filter(owner = request.user)
    setup = Setup.objects.filter(owner = request.user)
    setupOne = Setup.objects.filter(owner = request.user).first()
    return render(request, 'deal/Views/subscriptions.html',{'deals':setup,'setup':setupOne})


