from django.urls import path
from .views import *


app_name = "store"
urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    # path("groceries/",GroceryView.as_view(),name="groceries"),
    path("groceries.html", GroceryView.as_view(), name="groceries_html"),
    path("snacks.html", SnacksView.as_view(), name="snacks_html"),
    path("beverages.html", BeveragesView.as_view(), name="beverages_html"),
    path("personalandhomecare.html", HomecareView.as_view(), name="care_html"),
    path("packagedfoods.html", PackagedfoodsView.as_view(), name="packagedfoods_html"),
    path("stationaries.html", StationariesView.as_view(), name="stationaries_html"),
    path("others.html", OthersView.as_view(), name="others_html"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),


    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),

    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    
    path("checkout/", CheckoutView.as_view(), name="checkout"),


    path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),

    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("order-detail/<int:cp_id>/", CustomerOrderDetailView.as_view(), name="orderdetail"),

    path("cancel-order/<int:cp_id>/", CancelOrderView.as_view(), name="cancelorder"),

    path("search/", SearchView.as_view(), name="search"),

    
    
   




    
    

]