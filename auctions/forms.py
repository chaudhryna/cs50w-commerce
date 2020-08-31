from django.forms import ModelForm, Textarea, TextInput, Select, NumberInput, FileInput
from .models import Comment, Listing, Bid

class ListingForm(ModelForm):

    class Meta:
        model = Listing 
        fields = ('title', 'description', 'category', 'price', 'picture')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 3}),
            'category': Select(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'picture': FileInput(attrs={'class': 'form-control'})
        }

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)

        widgets = {
            'comment': Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 3})
        }

class BidForm(ModelForm):

    class Meta:
        model = Bid
        fields = ('bid_price',)

        widgets = {
            'bid_price': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bid'})} 