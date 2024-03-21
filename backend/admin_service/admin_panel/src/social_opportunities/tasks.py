# from celery import shared_task
# from social_opportunities.email import CooperationEmail

# from social_opportunities.models import Cooperation


# @shared_task
# def send_email_cooperation(cooperation_id):
#     try:
#         obj = Cooperation.objects.get(id=cooperation_id)
#     except Cooperation.DoesNotExist:
#         raise

#     context = {
#         "site": obj.site,
#         "name": obj.name,
#         "email": obj.email,
#         "phone": obj.phone,
#     }
#     # recipient = product.user

#     to = [""]
#     CooperationEmail(context=context).send(to)
