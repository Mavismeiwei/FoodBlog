from app01.models import Comment

# 方案一： 根据根评论去递归查找它下面的所有子评论 要把它放入到根评论的一个空间中
def find_root_sub_comment(root_comment, sub_comment_list):
    for sub_comment in root_comment.comment_set.all():
        # 找根评论的子评论
        sub_comment_list.append(sub_comment)
        find_root_sub_comment(sub_comment, sub_comment_list)

def sub_comment_list(nid):
    # 找到某个文章的所有评论
    comment_query = Comment.objects.filter(article_id=nid).order_by('-create_time')  # 最新发布的评论在上
    comment_list = []  # 把评论储存到列表

    for comment in comment_query:
        # 如果它的父级是None 说明当前评论是根评论
        if not comment.parent_comment:
            # 递归查找这个根评论下所有子评论
            lis = []
            find_root_sub_comment(comment, lis)
            comment.sub_comment = lis
            comment_list.append(comment)
            continue

    return comment_list
