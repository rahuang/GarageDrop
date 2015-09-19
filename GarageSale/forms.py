from django import forms 

class DeliveryQuoteForm(forms.Form):
    start_addr = forms.CharField(label='Start Address', max_length=50)
    start_state = forms.CharField(label='Start State', max_length=50)
    start_city = forms.CharField(label='Start City', max_length=50)
    start_zip = forms.CharField(label='Start Zip', max_length=5)

    end_addr = forms.CharField(label='End Address', max_length=50)
    end_state = forms.CharField(label='End State', max_length=50)
    end_city = forms.CharField(label='End City', max_length=50)
    end_zip = forms.CharField(label='End Zip', max_length=5)