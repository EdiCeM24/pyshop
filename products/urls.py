from django.urls import path
from . import views
from products.views import (
    CreateCheckoutSessionView,
    productLandingPageView,
    SuccessView,
    CancelView,
    stripe_webhook,
    stripeIntentView,
)


urlpatterns = [
    path('', views.index),
    path('new', views.new),
    path('create-payment-intent/<pk>/', stripeIntentView.as_view(), name='create-payment-intent'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
    path('', views.productLandingPageView.as_view(), name='landingpage'),
    path('create-checkout-session/<pk>/', views.CreateCheckoutSessionView.as_view()),
]
