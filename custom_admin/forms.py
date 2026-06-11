from django import forms
from .models import Product
import re
import os


class ProductForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise forms.ValidationError(
                "Product name can contain only letters and spaces."
            )

        if len(name) > 30:
            raise forms.ValidationError(
                'Name cannot be more than 30 characters'
            )

        return name

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            allowed_extensions = [".jpg", ".jpeg", ".png"]
            ext = os.path.splitext(image.name)[1].lower()

            if ext not in allowed_extensions:
                raise forms.ValidationError("Only JPG, JPEG and PNG files are allowed.")

            if image.content_type not in ["image/jpeg", "image/png"]:
                raise forms.ValidationError("Only JPG, JPEG and PNG files are allowed.")

        return image

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")

        if price >= 1000000:
            raise forms.ValidationError("Price cannot be more than 10 lakhs!")

        return price

    class Meta:
        model = Product
        fields = ["name", "image", "description", "price"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "50"
                }
            )
        }


class EditProductForm(forms.ModelForm):

    name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    image = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    description = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )

    price = forms.DecimalField(
        required=False,
        max_digits=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if name and not re.fullmatch(r"[A-Za-z ]+", name):
            raise forms.ValidationError(
                "Product name can contain only letters and spaces."
            )

        return name

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            return image

        allowed_extensions = [".jpg", ".jpeg", ".png"]
        ext = os.path.splitext(image.name)[1].lower()

        if ext not in allowed_extensions:
            raise forms.ValidationError("Only JPG, JPEG and PNG files are allowed.")

        if hasattr(image, "content_type"):
            if image.content_type not in ["image/jpeg", "image/png"]:
                raise forms.ValidationError("Only JPG, JPEG and PNG files are allowed.")

        return image

    class Meta:
        model = Product
        fields = ["name", "image", "description", "price"]
