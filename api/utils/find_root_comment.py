def find_root_comment(comment):
    # 找到comment的最终根评论
    if comment.parent_comment:
        # 如果还不是根评论 则递归去寻找它的根评论
        return find_root_comment(comment.parent_comment)
    return comment
