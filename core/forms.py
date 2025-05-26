from django import forms
from core.models import Product_Review

class ProductReviewForms(forms.ModelForm):
    review= forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write Reviews"}))

    class Meta:
        model= Product_Review
        fields= ['review', 'rating']