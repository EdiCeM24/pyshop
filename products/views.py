from itertools import product
import stripe
import os
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelView(TemplateView):
    template_name = 'cancel.html'



def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def new(request):
    products = new.objects.filter()
    return render(request, 'trend.html', {'products': products})

class productLandingPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        Products = product.objects.get(name="Test product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "Products": product,
        })
        return context

class CreateCheckoutSessionView(View):
   def post(self, request, *args, **kwargs):
           product_id = self.kwargs["pk"]
           products = product.objects.get(id=product_id)

           # ! /usr/bin/env python3.6
           # This is your test secret API key.
           stripe.api_key = settings.STRIPE_SECRET_KEY

           app = Django(__name__,
                    static_url_path='',
                    static_folder='public')

           YOUR_DOMAIN = 'http://localhost:127.0.0.1:8000'

           @app.route('/create-checkout-session', methods=['POST'])
           def create_checkout_session():
             try:
                  checkout_session = stripe.checkout.Session.create(
                      line_items=[
                          {
                             'prce_data': {
                                  'currency': 'usd',
                                  'unit_amount': product.price,
                                  'product_data': {
                                      'name': product.name,
                                      # 'images': ['https://i.imgur.com/EHyR2np.png'],
                                  },
                             },
                             # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                             'price': '{{PRICE_ID}}',
                             'quantity': 1,
                          },
                     ],
                    metadata={
                          "product_id": product.id,
                          },
                    mode='payment',
                    success_url=YOUR_DOMAIN + '/success/',
                    cancel_url=YOUR_DOMAIN + '/cancel/',
                       )
                  return JsonResponse({
                      'id': checkout_session.id
                  })
             except Exception as e:
                   return str(e)

             return redirect(checkout_session.url, code=303)

             if __name__ == '__main__':
                   app.run(port=4242)
# once this is installed or paste here from stripe, we use at top: from django.views.decorators.csrf import csrf_exempt.
# Using Django
@csrf_exempt
def stripe_webhook(request):            # change it from my_webhook_view to stripe_webhook.
      payload = request.body

      # For now, you only need to print out the webhook payload so you can see
      # the structure.
      #print(payload)
      sig_header = request.META['HTTP_STRIPE_SIGNATURE']
      event = None

      try:
          event = stripe.Webhook.construct_event(
              payload, sig_header, settings.STRIPE_WEBHOOK_SECRET  # endpoint_secret IT WAS THE DEFAULT ONE FROM STRIPE.
          )
      except ValueError as e:
          # Invalid payload
          return HttpResponse(status=400)
      except stripe.error.SignatureVerificationError as e:
          # Invalid signature
          return HttpResponse(status=400)

          # Handle the checkout.session.completed event
      if event['type'] == 'checkout.session.completed':
          session = event['data']['object']

          customer_email = session["customer_details"]["email"]
          product_id = session["metadata"]["product_id"]

          products = product.objects.get(id=product_id)

          send_mail(
              subject= "Here is your product",
              message="Thanks for your purchase. Here is the you ordered",
              recipient_list=[customer_email],
              from_email="sefiok24@gmail.com",
              url ="",
          )
          return HttpResponse(status=200)


      app = Django(__name__, static_folder='public',
                   static_url_path='', template_folder='public')

      def calculate_order_amount(items):
          # Replace this constant with a calculation of the order's amount
          # Calculate the order total on the server to prevent
          # people from directly manipulating the amount on the client
          return 1400

class stripeIntentView(View):
          def post(self, request, *args, **kwargs):
              @app.route('/create-payment-intent', methods=['POST'])
              def create_payment():
                  try:
                      product_id = self.kwargs["pk"]
                      products = product.objects.get(id=product_id)
                      data = json.loads(request.data)
                      # Create a PaymentIntent with the order amount and currency
                      intent = stripe.PaymentIntent.create(
                          amount=product.price,
                         # amount=calculate_order_amount(data['items']),
                          currency='usd',
                          automatic_payment_methods={
                              'enabled': True,
                          },
                      )
                      return JsonResponse({
                          'clientSecret': intent['client_secret']
                      })
                  except Exception as e:
                      return JsonResponse({ "error": str(e) }), 403

              if __name__ == '__main__':
                  app.run(port=4242)