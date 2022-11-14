from django import forms
from .models import monitoringStock
from bootstrap_modal_forms.forms import BSModalModelForm


class StockForm(forms.ModelForm):
    class Meta:
        model = monitoringStock
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        value_max = cleaned_data.get("value_max")
        value_min = cleaned_data.get("value_min")

        if value_max and value_min and value_min >= value_max:
            raise forms.ValidationError(
                'Valor máximo deve ser maior que valor mínimo.')
