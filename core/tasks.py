import requests
from bs4 import BeautifulSoup

from core.models import Word, Meaning
from django_dict.celery import app
from django_dict.settings import PARSER_SETTINGS


class CAMParser:
    def __init__(self, word: Word):
        self.word = word
        self.user_agent = PARSER_SETTINGS.get('user_agent')

    def get_page(self):
        url = f'https://dictionary.cambridge.org/dictionary/english-russian/{self.word.word}'
        response = requests.get(url, headers={'User-Agent': self.user_agent})
        return response.text

    @staticmethod
    def parse_meaning_block(block):
        b_tag = block.find('b')
        examples = [example.get_text() for example in block.find_all('div', class_='examp')]
        return {
            'meaning': b_tag.get_text(),
            'examples': examples,
        }

    def parse_page(self, page):
        soup = BeautifulSoup(page, 'lxml')
        data_div = soup.find('div', class_='entry-body__el')
        title = data_div.find('div', class_='di-title').get_text()
        meaning_blocks = data_div.find_all('div', class_='sense-block')
        meanings = [self.parse_meaning_block(block) for block in meaning_blocks]
        part_of_speech = soup.find('span', class_='posgram').get_text()
        return {
            'title': title,
            'meanings': meanings,
            'part_of_speech': part_of_speech,
        }
    
    def get_result(self):
        page = self.get_page()
        return self.parse_page(page)


@app.task
def update_meaning_cam(word_id):
    word = Word.objects.get(id=word_id)
    parsed_data = CAMParser(word).get_result()
    word.part_of_speech = parsed_data.get('part_of_speech')
    meaning_instances = [Meaning(**meaning, word=word) for meaning in parsed_data.get('meanings')]
    meaning_instances = Meaning.objects.bulk_create(meaning_instances)
    word.meanings.add(*meaning_instances)
    word.save()
