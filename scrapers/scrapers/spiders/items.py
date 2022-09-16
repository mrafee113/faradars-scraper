from datetime import timedelta
from scrapy.item import Item, Field
from utils.itemloader import TFCompose, ItemLoader
from utils.scrapy_handler import ScrapyHandler as H
from validators import url
from utils import fa_to_en


class MainItem(Item):
    title: str = Field()
    link: str = Field()
    number_of_students: int = Field()
    tutor: str = Field()
    duration: timedelta = Field()


def parse_duration(d: str) -> timedelta:
    hour = minute = 0
    if 'ساعت' in d:
        hour = int(fa_to_en(d[:d.find('ساعت')].strip()))
    if 'دقیقه' in d:
        h = d.find('ساعت')
        start = h + len('ساعت') if h != -1 else 0
        minute = int(fa_to_en(d[start:].replace('و', '').replace('دقیقه', '').strip()))

    return timedelta(minutes=minute, hours=hour)


class MainLoader(ItemLoader):
    default_item_class = MainItem

    title_in = TFCompose(H.pvalidate(tipe=str, value_exc=str()), str.strip)
    link_in = TFCompose(H.pvalidate(tipe=str, validation=url), str.strip)
    number_of_students_in = TFCompose(
        H.pvalidate(
            tipe=str, value_exc=str(),
            validation=lambda x: ':' in x and isinstance(int(fa_to_en(x.split(':')[1].strip().replace(",", ""))), int)
        ),
        lambda x: x.split(':')[1].strip().replace(",", ""),
        fa_to_en, int,
    )
    tutor_in = TFCompose(
        H.pvalidate(tipe=str, value_exc=str(), validation=lambda x: ':' in x),
        lambda x: x.split(':')[1].strip()
    )
    duration_in = TFCompose(
        H.pvalidate(
            tipe=str, value_exc=str(),
            validation=lambda x: ':' in x and isinstance(parse_duration(x.split(':')[1].strip()), timedelta)
        ),
        lambda x: parse_duration(x.split(':')[1].strip())
    )
