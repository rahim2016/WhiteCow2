from celery import shared_task
from .models import Deals
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Setup, Deals,Adress,AssetsForSale,SubscriptionDataForSale
from .view_method import *
from .config import *
from django_celery_beat.models import IntervalSchedule, PeriodicTask,CrontabSchedule


@shared_task(name="computation_heavy_task", bind=True)
def computation_heavy_task(self):
    users = User.objects.all()
    deals = Deals.objects.all()
    deal_ids = [deal.pk for deal in deal_ids]
    user_emails = [user.email for user in users]

    periodic_task_name = PeriodicTask.objects.get(
        task=self.name  # notice PeriodicTask.name and self.name are different things
    ).name


    setups_all = Setup.objects.all()
    setups = []
    for set_ in setups_all:
        if set_.status.value =='Active':
            setups.append(set_)
    
    # setup_deal_ids = [(setup.deal_id, setup.owner) for setup in setups]
    #setup[0].status.value=='Active'

    for setup in setups:
        if periodic_task_name == setup.time_interval.value:
            user_email = [setup.owner.email]
            address = Adress.objects.filter(deal_id = setup.deal_id, owner= setup.owner).first()
            assets = AssetsForSale.objects.filter(deal_id = setup.deal_id, owner= setup.owner).first() 
            query_params = get_query_params(address=address, assets=assets)
            response = property_search_query(url = url_for_sale, query_params=query_params)
            df = process_query_response(response=response)
            print("df....\n")
            print(df.head())
            list_property_id = df['property_id'].tolist()[:3]
            print("List property id.....\n")
            print(list_property_id)
            deal_dict = calculate_deal(list_property_id, df)
            print("Deal dict.....\n")
            print(deal_dict)
            deal_df = get_deal_datafrane(deal_dict, df)
            print("deal_df.....\n")
            print(deal_df)
            deal_df = deal_df.where(deal_df.notnull(), None)
            print("deal df.....\n")
            print(deal_df)
            deal_df = formatting(deal_df)
            print("deal df.....\n")
            print(deal_df)

            deal_links = ["https://www.realtor.com/realestateandhomes-detail/"+deal.permalink for deal in deal_df.itertuples()]
            
            email(deal_list=deal_links, email_list=user_email)


            deal=deal_df 
            deal['owner'] = setup.owner
            deal['deal'] = de

            entries = []       
    
            for e in deal.T.to_dict().values():

                entries.append(SubscriptionDataForSale(**e))
            
            SubscriptionDataForSale.objects.bulk_create(entries)
        
   
    
    
    
    



def email(deal_list, email_list):
    subject = 'Thank you for registering to our site'
    message = " it  means a world to us  Here is you Deals \n "+deal_list[0]+"\n"+deal_list[1]+"\n"+deal_list[2]+"\n"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = email_list
    send_mail( subject, message, email_from, recipient_list )
    