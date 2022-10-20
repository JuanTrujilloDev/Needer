class ExtendsInnerContentMixin:
    def get_context_data(self, **kwargs):
        context = super(ExtendsInnerContentMixin, self).get_context_data(**kwargs)
        context['innercontent'] = 'main/user/content.html'
        return context