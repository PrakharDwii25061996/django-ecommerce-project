from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
	ProductListCreateAPIView, ProductUpdateRetrieveDestroyAPIView,
	PaymentCreateAPIView, PaymentSuccessAPIView, PaymentCancelAPIView,
	CategoryAPIView, SubCategoryAPIView
)


urlpatterns = [
	path('product/create/', ProductListCreateAPIView.as_view(), name='product'),
	path('product/<int:id>/', ProductUpdateRetrieveDestroyAPIView.as_view(), name='product_update'),
	path('api/create-payment/', PaymentCreateAPIView.as_view(), name='payment_gateway'),
	path('success/', PaymentSuccessAPIView.as_view(), name='payment_success'),
	path('cancel/', PaymentCancelAPIView.as_view(), name='payment_failed'),

	path('category/', CategoryAPIView.as_view(), name='category'),
	path('sub/category/', SubCategoryAPIView.as_view(), name='sub_category')

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
