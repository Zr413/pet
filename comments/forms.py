# from django import forms
# from blog.models import Comment
#
#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['text'].widget.attrs.update({'class': 'textarea', 'placeholder': 'Write your comment here...'})
