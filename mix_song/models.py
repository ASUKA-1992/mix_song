from django.db import models

class Songs(models.Model):
    '''曲モデル'''
    artist = models.CharField(verbose_name='アーティスト名', max_length=50)
    lyricist = models.CharField(verbose_name='作詞家', max_length=50, blank=True, null=True)
    composer = models.CharField(verbose_name='作曲家', max_length=50, blank=True, null=True)
    title = models.CharField(verbose_name='タイトル', max_length=50)
    lyrics = models.TextField(verbose_name='歌詞', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Songs'

    def __str__(self):
        return self.title

class Artists(models.Model):
    '''アーティストモデル'''
    artist = models.CharField(verbose_name='アーティスト名', max_length=50, unique=True)
    page_index = models.IntegerField(verbose_name='ページ番号')
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Artists'

    def __str__(self):
        return self.artist