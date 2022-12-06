from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.views import View
import requests
from django.http import HttpResponse
from pprint import pprint as pp
# Create your views here.


class ExchangeView(View):
    session = requests.Session()
    fiat_price = {}
    data = {}
    def get(self, request, *args, **kwargs):
        parameters = {'start': '1', 'limit': '500'}
        self.headers = {'Accepts':'application/json', 'X-CMC_PRO_API_KEY': '6dc5bc0e-e0b0-462b-83db-64cfba12d0b2'}
        main_url = 'https://pro-api.coinmarketcap.com/v1/fiat/map'
        price = {}
        currency_rates = {}
        self.session.headers.update(self.headers)
        try:
            data = self.session.get(main_url).json()
            pp(data)
        except BaseException:
            return HttpResponse("Please make sure you're connected to the internet before requesting that page. <br><br> Ensure that it is a strong WIFI or data connection and try requesting the page again.")
        
        if request.session.get('fiat_price'):

            fiat_price = request.session.get('fiat_price')
            price = fiat_price
            del request.session['fiat_price']
            print('data from price_data::::', price)

        if 'currency' in request.GET:
            fiat_to_check = request.GET['currency']
            rate = requests.get('https://v6.exchangerate-api.com/v6/e1b2766c3a44281c94b7d72e/latest/' + fiat_to_check).json()
            currency_rates = rate

        return render(request, 'exchange.html', {'data': data['data'], 'price_data': price, 'currency_rates': currency_rates})

    def post(self, request, *args, **kwargs):
        from_currency = request.POST.get('fcurrency')
        to_currency = request.POST.get('to_currency')
        amount = request.POST.get('amount')
        
        fiat_price = self.session.get('https://v6.exchangerate-api.com/v6/e1b2766c3a44281c94b7d72e/latest/' + from_currency ).json()
        
        if fiat_price:
            try:
                price = fiat_price['conversion_rates'][to_currency] * int(amount)
            except BaseException:
                return redirect('/')


        request.session['fiat_price'] = [price, to_currency]

        return redirect('exchange')




class CryptoPriceView(TemplateView):
    template_name = "cryptoprice.html"
    
    parameters = {'start': '1', 'limit': '500'}
    headers = {'Accepts':'application/json', 'X-CMC_PRO_API_KEY': '6dc5bc0e-e0b0-462b-83db-64cfba12d0b2'}
    main_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    
    def get_context_data(self, **kwargs):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        price  = {}
        print(self.session)
        try:
            price = self.session.get(self.main_url, params = self.parameters).json()
       
        except BaseException:
            return {}

        context = super().get_context_data(**kwargs)
        context['price_data'] = price['data']

        return context
