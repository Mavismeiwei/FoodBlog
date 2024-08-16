import os

if __name__ == '__main__':
    # 加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_01.settings")
    # 导入Django 并启动Django项目
    import django

    django.setup()

    from app01.models import Articles, Comment

    # 如何确认评论的层级关系？根评论是一个层级 子评论也是一个层级 但是要确认其父评论是谁 因为要@表示
    # 方案一：


    print(Articles.objects.get(nid=1))  # 通过nid找到某篇文章
    comment_query = Comment.objects.filter(article_id=1)  # 找到该篇文章中的所有评论
    print(comment_query)


