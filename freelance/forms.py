from django import forms
from .models import Category, Tag

black_list = [
    "phone",
    "номер",
    "телефон",
]

class PostForm(forms.Form):
    title = forms.CharField(max_length=50, min_length=3)
    description = forms.CharField(max_length=1000)
    photo = forms.ImageField(required=False)

    def clean_title(self):
        title = self.cleaned_data.get("title")
        for word in black_list:
            if word in title.lower():
                raise forms.ValidationError("Запрещённое слово в названии")
        return title

class SearchForm(forms.Form):
    ordering = [
        ("created_at", "Created At"),
        ("updated_at", "Updated At"),
        ("title", "Title"),
        ("-created_at", "Created At(desc)"),
        ("-updated_at", "Updated At(desc)"),
    ]

    search =  forms.CharField(max_length=100, required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), 
        required=False
    )
    ordering = forms.ChoiceField(
        choices=ordering, 
        required=False
    )
