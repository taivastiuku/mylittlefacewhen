from django.forms import ModelForm
from django.forms.models import model_to_dict
from tastypie.validation import Validation

from viewer import forms


class FaceValidation(Validation):
    update_form = forms.PublicUpdateFace
    create_form = forms.NewCreateFace

    def form_args(self, bundle, form):
        data = bundle.data

        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}

        kwargs = {'data': {}}

        if hasattr(bundle.obj, 'pk'):
            if issubclass(form, ModelForm):
                kwargs['instance'] = bundle.obj

            kwargs['data'] = model_to_dict(bundle.obj)

        kwargs['data'].update(data)
        return kwargs

    def is_valid(self, bundle, request):
        print "is_valid"
        if request.method == 'POST':
            form = self.create_form(**self.form_args(bundle, self.create_form))
        else:
            form = self.update_form(**self.form_args(bundle, self.update_form))
        print "form valid", form.is_valid()
        if form.is_valid():
            bundle.data = form.cleaned_data
            return {}
        else:
            return form.errors
