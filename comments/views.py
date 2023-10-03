# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.utils.decorators import method_decorator
# from django.views import View
# from django.views.generic.edit import CreateView
#
# from blog.models import News
# from blog.models import Comment
# from comments.forms import CommentForm
#
#
# @method_decorator(login_required, name='dispatch')
# class CommentCreateView(CreateView):
#     model = Comment
#     fields = ['text']
#     form_class = CommentForm
#     template_name = 'comments.html'
#     context_object_name = 'comment'
#
#     def create_news(request):
#         form = CommentForm()
#         if request.method == 'POST':
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect('/comments/')
#
#         return render(request, 'comments.html', {'form': form})
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.instance.news_id = self.kwargs['pk']
#         return super().form_valid(form) and HttpResponseRedirect('/comments/')
#
#
# class LikeView(View):
#     def get(self, request, *args, **kwargs):
#         news = get_object_or_404(News, id=self.kwargs['pk'])
#         news.like()
#         return HttpResponseRedirect(reverse('news-details', args=[str(news.id)]))
#
#
# class DislikeView(View):
#     def get(self, request, *args, **kwargs):
#         news = get_object_or_404(News, id=self.kwargs['pk'])
#         news.dislike()
#         return HttpResponseRedirect(reverse('news-details', args=[str(news.id)]))
#
# # Create your views here.
