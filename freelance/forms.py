from django import forms

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

