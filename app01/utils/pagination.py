import math
from urllib.parse import urlencode

class Pagination:
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11, position='pos'):
        """
        :param current_page: 当前页码
        :param all_count: 数据库中的总条数
        :param base_url: 原始url
        :param query_params: 保留原始搜索条件
        :param per_page: 一页展示多少条
        :param pager_page_count: 最多展示多少个页码
        """
        self.all_count = all_count
        self.per_page = per_page
        self.position = position

        # 计算一共有多少页
        self.current_count = math.ceil(all_count / per_page)

        # 异常处理 页数只能是从1开始的数字 防止用户乱输入
        try:
            self.current_page = int(current_page)
            if not 0 < self.current_page <= self.current_count:
                self.current_page = 1
        except Exception:  # 出现异常的话 当前文章页面设置为1
            self.current_page = 1

        self.base_url = base_url
        self.query_params = query_params

        self.pager_page_count = pager_page_count

        # 分页的中值
        self.half_pager_count = int(self.pager_page_count / 2)
        if self.current_count < self.pager_page_count:
            # 如果可以分页的页码小于最大显示页码 就让最大显示页码变成可分页页码
            self.pager_page_count = self.current_count

    # 分页的html样式
    def page_html(self):
        # 计算页码的起始和结束：分类讨论情况
        start = self.current_page - self.half_pager_count + 1
        end = self.current_page + self.half_pager_count
        if self.current_page <= self.half_pager_count:
            # 左侧页数范围
            start = 1
            end = self.pager_page_count
        if self.current_page + self.half_pager_count >= self.current_count:
            # 右侧页数范围
            start = self.current_count - self.pager_page_count + 1
            end = self.current_count

        # 生成分页 <li>标签中的<a>标签
        page_list = []

        # 上一页 在第一页时没有上一页
        if self.current_page > 1:
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li class="last_page"><a href="{self.base_url}?{self.query_encode}#{self.position}">Last</a></li>')

        # 页数数字部分
        for i in range(start, end + 1):
            self.query_params['page'] = i
            if self.current_page == i:  # 当前选中的页面有active的css样式
                li = f'<li class="active"><a href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            page_list.append(li)

        # 下一页 在最后一页时没有下一页
        if self.current_page < self.current_count:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li class="next_page"><a href="{self.base_url}?{self.query_encode}#{self.position}">Next</a></li>')
        # 如果页面为1则不显示分页器
        if len(page_list) == 1:
            page_list = []
        return ''.join(page_list)  # 转化为字符串以给前端进行调用

    # 编码的方法
    @property
    def query_encode(self):
        return urlencode(self.query_params)

    @property
    def start(self):  # 每一页的分页开始文章索引值
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page

if __name__ == '__main__':
    pager = Pagination(
        current_page=18,
        all_count=100,
        base_url='/article',
        query_params={'tag': 'python'},
        per_page=5
    )
    print(pager.page_html())
