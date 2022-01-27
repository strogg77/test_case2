from rest_framework import generics
from media.models import Page, Content
from media import serializers
from django.db import transaction
from django.db.models import F
import threading

class PageList(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = serializers.PageSerializer

@transaction.atomic
def increment_counters(pk):
    counter = Content.objects.filter(page=pk).select_for_update().update(count=F('count')+1)

class PageDetail(generics.RetrieveAPIView):
    serializer_class = serializers.PageDetail
    increment_thread = None
    def get_queryset(self):
        if (self.kwargs.get('pk')):
            qs=Page.objects.filter(pk=self.kwargs.get('pk'))
        else:
            qs=super().get_queryset()
        increment_thread=threading.Thread(target=increment_counters,args=(self.kwargs.get('pk'),))
        increment_thread.start()
#        increment_counters(self.kwargs.get('pk'))
        return qs

    def __del__(self):
        if (self.increment_thread!=None):
            self.increment_thread.join()

