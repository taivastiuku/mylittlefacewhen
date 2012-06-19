from django import forms
import base64
#from resizor import models
#import re

class CreateTask(forms.Form):
    image = forms.CharField(max_length=10000000, required=True)
    format = forms.CharField(max_length=4, required=False)
    sizes = forms.CharField(max_length=32, required=False)
    write_gif = forms.BooleanField(required=False)

    def clean(self):
	cleaned_data = self.cleaned_data

        sizes = []
            
        for size in cleaned_data.get("sizes", "").split(","):
            try:
                sizes.append(int(size))
            except:
                pass
        if not sizes:
            sizes = [120,]

        if cleaned_data.get("format"):
            if cleaned_data["format"].lower() not in ("png", "jpg"):
                raise forms.ValidationError("Invalid format selected")
            cleaned_data["format"] = cleaned_data["format"].lower()

        cleaned_data["sizes"] = sizes

        cleaned_data["image"] = base64.b64decode(cleaned_data["image"])

        return cleaned_data

