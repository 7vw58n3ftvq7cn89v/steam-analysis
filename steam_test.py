import unittest
from steam_get_info import review_all, gameprice, clean_price
from bs4 import BeautifulSoup


class TestReviewAll(unittest.TestCase):

    def setUp(self):
        # 创建一个包含测试HTML的BeautifulSoup对象
        self.sample_html = """
        <div id="userReviews">
            <div class="user_reviews_summary_row">
                <span class="game_review_summary">多半好评</span>
                <span class="responsive_hidden">(1,234)</span>
                <span class="nonresponsive_hidden responsive_reviewdesc">3132312有 73% 好评</span>
            </div>
            <div class="user_reviews_summary_row" itemprop="aggregateRating">
                <span class="game_review_summary">Very Positive</span>
                <span class="responsive_hidden">(23,456)</span>
                <span class="nonresponsive_hidden responsive_reviewdesc">此游戏的 809,516 篇用户评测中有 78% 为好评。</span>
            </div>
        </div>
        """
        self.soup = BeautifulSoup(self.sample_html, 'html.parser')

    def test_review_all(self):
        # 调用函数
        result = review_all(self.soup)

        # 断言结果是正确的
        self.assertEqual(result[0], "多半好评")
        self.assertEqual(result[1], 1234)
        self.assertAlmostEqual(result[2], 73.0)
        self.assertEqual(result[3], "Very Positive")
        self.assertEqual(result[4], 23456)
        self.assertAlmostEqual(result[5], 78.0)


class TestGamePrice(unittest.TestCase):

    def setUp(self):
        # 定义一个帮助方法，创建测试用的BeautifulSoup对象
        def create_test_soup(content):
            return BeautifulSoup(content, 'html.parser')
        
        # 定义几种价格情况的HTML片段
        self.price_html_with_yuan = create_test_soup('<span class="discount_original_price">¥68</span>')
        self.price_html_with_free = create_test_soup('<span class="discount_original_price">免费开玩</span>')
        self.price_html_with_error = create_test_soup('<span class="discount_original_price">错误价格</span>')
        self.price_html_no_price = create_test_soup('<div class="game_purchase_price price">free</div>')
        self.price_html_backup = create_test_soup('<span class="game_purchase_price price">¥48</span>')

    def test_gameprice_with_yuan(self):
        # 测试价格为¥的情况
        price = gameprice(self.price_html_with_yuan)
        self.assertEqual(price, 68.0)

    def test_gameprice_with_free(self):
        # 测试免费的情况
        price = gameprice(self.price_html_with_free)
        self.assertEqual(price, 0.0)

    def test_gameprice_with_error(self):
        # 测试无法识别价格的情况
        price = gameprice(self.price_html_with_error)
        self.assertEqual(price, 0.0)

    def test_gameprice_no_price(self):
        # 测试没有价格的情况
        price = gameprice(self.price_html_no_price)
        self.assertEqual(price, 0.0)

    def test_gameprice_backup_price(self):
        # 测试备选价格的情况
        price = gameprice(self.price_html_backup)
        self.assertEqual(price, 48.0)

    def test_gameprice_clean_price(self):
        # 测试clean_price函数能否正确处理异常输入
        self.assertEqual(clean_price('¥68'), 68.0)
        self.assertEqual(clean_price('免费开玩'), 0.0)
        self.assertEqual(clean_price('错误价格'), 0.0)
        self.assertEqual(clean_price(None), 0.0)

if __name__ == '__main__':
    unittest.main()