from django.views.generic import TemplateView


#--- TemplateView
class HomeView(TemplateView):
    """
    HomeView는 특별한 처리 로직 없이 단순히 템플릿만 보여주는 로직.
    """
    template_name = 'home.html'
