class NextUrlMixin:
    """Mixin to handle the 'next' parameter for redirecting after a successful form submission."""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_url'] = self.request.POST.get('next') or self.request.GET.get('next') or self.request.META.get('HTTP_REFERER', '')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        return super().get_success_url()
