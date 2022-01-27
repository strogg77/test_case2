from django.db import models

class Page(models.Model):
    """
    Main Page model. Contains common attributes of project
    pages.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['creation'] 

class Content(models.Model):
    """
    Content model for storing common attributes of media content
    on page (such as title, ordering etc)
    """
    id = models.AutoField(primary_key=True)
    """
    Since this 'id' field is referenced by 3 tables (Video, Audio and
    Text), uniqueness control must be implemented on the application side
    """
    title = models.CharField(max_length=100)
    order = models.IntegerField()
    count = models.IntegerField()
    page = models.ForeignKey(Page, related_name='contents', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['order']

class Video(models.Model):
    """
    Model for storing attributes unique for video content.
    """
    id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=100)
    subs = models.CharField(max_length=100)
    content = models.OneToOneField(Content, related_name='video', on_delete=models.CASCADE)

class Audio(models.Model):
    """
    Model for storing attributes unique for audio content.
    """
    id = models.AutoField(primary_key=True)
    file = models.CharField(max_length=100)
    bitrate = models.IntegerField()
    content = models.OneToOneField(Content, related_name='audio', on_delete=models.CASCADE)

class Text(models.Model):
    """
    Model for storing attributes unique for text content.
    """
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    content = models.OneToOneField(Content, related_name='text', on_delete=models.CASCADE)

