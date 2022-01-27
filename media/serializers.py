from rest_framework import serializers
from django.contrib.auth.models import User
from media.models import Content, Page, Video, Audio, Text

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'file', 'subs']

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ['id', 'file', 'bitrate']

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'text']

#class ContentSerializer(serializers.HyperlinkedModelSerializer):
#    """
#    For every conent row use only one of underlyng serializers
#    """
#    video = VideoSerializer(many=False, read_only=True, required=False)
#    audio = AudioSerializer(many=False, read_only=True, required=False)
#    text = TextSerializer(many=False, read_only=True, required=False)
#
#    def to_representation(self,instance):
#        """
#        Remove unused fields of serializer
#        """
#        ret = super().to_representation(instance)
#        if ret['video']==None:
#            del ret['video']
#        if ret['audio']==None:
#            del ret['audio']
#        if ret['text']==None:
#            del ret['text']
#        return ret
#
#    def to_internal_value(self, data):
#        """
#        This is for POST queries. Not reilized now
#        """
#        ret=super().to_internal_value(data)
#        return ret
#
#    class Meta:
#        model = Content
#        fields = ['url', 'id', 'title', 'order', 'count', 'video', 'audio', 'text']


class ContentDetail(serializers.HyperlinkedModelSerializer):
    """
    For every conent row use only one of underlyng serializers
    """
    video = VideoSerializer(many=False, read_only=True, required=False)
    audio = AudioSerializer(many=False, read_only=True, required=False)
    text = TextSerializer(many=False, read_only=True, required=False)
    
    def to_representation(self,instance):
        """
        Remove unused fields of serializer
        """
        ret = super().to_representation(instance)
        if ret['video']==None:
            del ret['video']
        if ret['audio']==None:
            del ret['audio']
        if ret['text']==None:
            del ret['text']
        return ret
    
    class Meta:
        model = Content
        fields = ['id', 'title', 'order', 'count', 'video', 'audio', 'text']

class PageDetail(serializers.HyperlinkedModelSerializer):
    """
    For whole of page detail view
    """
    contents = serializers.SerializerMethodField('paginated_contents')
    
    def paginated_contents(self, obj):
        contents=Content.objects.filter(page=obj)
        paginator = self.context.get('view').pagination_class() #may be use pagination.PageNumberPagination
        page = paginator.paginate_queryset(contents, self.context['request'])
        count = paginator.page.paginator.count
        next_link = paginator.get_next_link()
        prev_link = paginator.get_previous_link()
        serializer = ContentDetail(page, many=True, context={'request': self.context['request']})
        ret = {'count': count, 'next': next_link, 'previous': prev_link, 'data': serializer.data}
        return ret

    class Meta:
        model = Page
        fields = ['id', 'title', 'creation', 'contents']

class PageSerializer(serializers.ModelSerializer):
    """
    Page list serializer
    """
    content = serializers.HyperlinkedIdentityField(view_name='page_detail',format='html')

    class Meta:
        model = Page
        fields = ['id', 'title', 'creation', 'content']

