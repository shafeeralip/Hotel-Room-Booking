from django.http import HttpResponseRedirect



def custom_decorator(function):
    def _function(request,*args, **kwargs):
        

        if request.session.get('hotel') is None:
        # if empty means, empty string
        # if request.session.get('order_reference') is not None\
        # and not request.session.get('order_reference'):
            return HttpResponseRedirect('/hotel')
        return function(request, *args, **kwargs)
    return _function