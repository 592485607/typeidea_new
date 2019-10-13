from django import forms

"""
    自定义Form，对展示层的定义
"""
class PsotAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea,label='摘要',required=False)