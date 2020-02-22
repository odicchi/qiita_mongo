import requests
import logging
import json

formatter = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.WARNING, format=formatter)
logger = logging.getLogger(__name__)

class GetQiitaInfo(object):

    def __init__(self):
        self.token = '97af110488fb1f040507f8d56f54e6b28676c888'        

    def get_next_url(self, response):
        """次のページがある場合は'rel="next"'としてurlが含まれるので、urlを抽出して返す。
        ない場合はNoneを返す。

        link: <https://qiita.com/api/v2/authenticated_user/items?page=1>;
        rel="first", <https://qiita.com/api/v2/authenticated_user/items?page=2>;
        rel="next", <https://qiita.com/api/v2/authenticated_user/items?page=4>;
        rel="last"

        :param response:
        :return: 次のurl
        """
        link = response.headers['link']
        if link is None:
            return None

        links = link.split(',')

        for link in links:

            if 'rel="next"' in link:
                return link[link.find('<') + 1:link.find('>')]
        return None
      
    def get_items(self):
        
        """ページネーションして全ての記事を取得し、
        ストック数とビュー数は一覧に含まれないので、それらの情報も追加して返す。

        :param token:
        :return: 記事のリスト
        """
        
        url = 'https://qiita.com/api/v2/authenticated_user/items'
        headers = {'Authorization': 'Bearer {}'.format(self.token)}

        items = []
        while True:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            items.extend(json.loads(response.text))
            logger.info('GET {}'.format(url))
            # 次のurlがあるかを確認する
            url = self.get_next_url(response)
            if url is None:
                break

        # 各記事についてビュー数とストック数の情報を取得して追加する
        # page_views_countは一覧APIにもフィールドはあるがnullが返ってくる
        for item in items:

            # ビュー数
            url = 'https://qiita.com/api/v2/items/{}'.format(item['id'])
            logger.info('GET {}'.format(url))
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            itemJson = json.loads(response.text)
            item['page_views_count'] = itemJson['page_views_count']
            item['tag1'] = itemJson['tags'][0]['name']
            item['tag2'] = itemJson['tags'][1]['name'] if len(itemJson['tags']) >= 2 else ''
            item['tag3'] = itemJson['tags'][2]['name'] if len(itemJson['tags']) >= 3 else ''
            item['tag4'] = itemJson['tags'][3]['name'] if len(itemJson['tags']) >= 4 else ''
            item['tag5'] = itemJson['tags'][4]['name'] if len(itemJson['tags']) >= 5 else ''

            tag_list = []
            for i in range(len(itemJson['tags'])):
                tag_list.append(itemJson['tags'][i]['name'])
            item['tag_list'] = tag_list

            # ストック数
            url = 'https://qiita.com/api/v2/items/{}/stockers'.format(item['id'])
            logger.info('GET {}'.format(url))
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            users = json.loads(response.text)
            for user in users:
                logger.info({
                    'id': user['id'],
                    'name': user['name']
                    })
            item['stocks_count'] = len(users)

        return items