from discord import AutocompleteContext
from discord import Option, OptionChoice

_school_list = {
    "hb": "Högskolan i Borås",
    "hig": "Högskolan i Gävle",
    "hkr": "Högskolan i Kristianstad",
    "hv": "Högskolan Väst",
    "ltu": "Luleå tekniska universitet",
    "mau": "Malmö universitet",
    "mdu": "Högskolan i Mälardalen",
    "sh": "Södertörns Högskola",
    "oru": "Örebro universitet",
}


async def _get_schools(ctx: AutocompleteContext):
    user_input = ctx.value.lower()
    locale = ctx.interaction.locale

    return [acronym.upper() for acronym in _school_list.keys() if acronym.find(user_input) != -1] or \
           [school for school in [
               choice.name_localizations[locale] for choice in choices
           ] if school.lower().find(user_input) != -1]

    # return [name for name in _school_list.values() if name.lower().find(user_input) != -1] or \
    #        [acronym.upper() for acronym in _school_list.keys() if acronym.find(user_input) != -1]


_hb = OptionChoice(
    name='Högskolan i Borås',
    value='HB',
    name_localizations={
        'da': 'Universitetet i Borås',
        'de': 'Universität Borås',
        'en-GB': 'University of Borås',
        'en-US': 'University of Borås',
        'es-ES': 'Universidad de Borås',
        'fr': 'Université de Borås',
        'hr': 'Sveučilište u Boråsu',
        'it': 'Università di Borås',
        'lt': 'Boråso universitetas',
        'hu': 'Borås Egyetem',
        'nl': 'Universiteit van Borås',
        'no': 'Universitetet i Borås',
        'pl': 'Uniwersytet Borås',
        'pt-BR': 'Universidade de Borås',
        'ro': 'Universitatea din Borås',
        'fi': 'Boråsin yliopisto',
        'sv-SE': 'Högskolan i Borås',
        'vi': 'Đại học Borås',
        'tr': 'Borås Üniversitesi',
        'cs': 'Univerzita Borås',
        'el': 'Πανεπιστήμιο του Borås',
        'bg': 'Университет в Борос',
        'ru': 'Университет Бурос',
        'uk': 'Університет Бороса',
        'zh-CN': '博尔斯大学',
        'ja': 'ボワス大学',
        'zh-TW': '博爾斯大學',
        'ko': 'Borås 대학교'
    }
)

_hig = OptionChoice(
    name='Högskolan i Gävle',
    value='HIG',
    name_localizations={
        'da': 'Universitetet i Gävle',
        'de': 'Universität Gävle',
        'en-GB': 'University of Gävle',
        'en-US': 'University of Gävle',
        'es-ES': 'Universidad de Gävle',
        'fr': 'Université de Gävle',
        'hr': 'Sveučilište u Gävleu',
        'it': 'Università di Gävle',
        'lt': 'Gevlės universitetas',
        'hu': 'Gävle Egyetem',
        'nl': 'Universiteit van Gävle',
        'no': 'Universitetet i Gävle',
        'pl': 'Uniwersytet w Gävle',
        'pt-BR': 'Universidade de Gävle',
        'ro': 'Universitatea din Gävle',
        'fi': 'Gävlen yliopisto',
        'sv-SE': 'Högskolan i Gävle',
        'vi': 'Đại học Gävle',
        'tr': 'Gävle Üniversitesi',
        'cs': 'Univerzita v Gävle',
        'el': 'Πανεπιστήμιο του Gävle',
        'bg': 'Университет в Евле',
        'ru': 'Университет Евле',
        'uk': 'Університет Євле',
        'zh-CN': '戈尔大学',
        'ja': 'ガブレ大学',
        'zh-TW': '戈爾大學',
        'ko': '게블 대학교'
    }
)

_hkr = OptionChoice(
    name='Högskolan i Kristianstad',
    value='HKR',
    name_localizations={
        'da': 'Universitetet i Kristianstad',
        'de': 'Universität Kristianstad',
        'en-GB': 'University of Kristianstad',
        'en-US': 'University of Kristianstad',
        'es-ES': 'Universidad de Kristianstad',
        'fr': 'Université de Kristianstad',
        'hr': 'Sveučilište u Kristianstadu',
        'it': 'Università di Kristianstad',
        'lt': 'Kristianstadas universitetas',
        'hu': 'Kristianstad Egyetem',
        'nl': 'Universiteit van Kristianstad',
        'no': 'Universitetet i Kristianstad',
        'pl': 'Uniwersytet w Kristianstadzie',
        'pt-BR': 'Universidade de Kristianstad',
        'ro': 'Universitatea din Kristianstad',
        'fi': 'Kristianstads yliopisto',
        'sv-SE': 'Högskolan i Kristianstad',
        'vi': 'Đại học Kristianstad',
        'tr': 'Kristianstad Üniversitesi',
        'cs': 'Univerzita v Kristianstadu',
        'el': 'Πανεπιστήμιο του Kristianstad',
        'bg': 'Университет в Кристианстад',
        'ru': 'Университет Кристианстад',
        'uk': 'Крістіанстадський університет',
        'zh-CN': '克里斯蒂安斯塔德学院',
        'ja': 'クリスチャンスタッドの大学',
        'zh-TW': '克里斯蒂安斯塔德學',
        'ko': '크리스티안스타드 대학교'
    }
)

_hv = OptionChoice(
    name='Högskolan Väst',
    value='HV',
    name_localizations={
        'da': 'Højskole Vest',
        'de': 'Universität Westen',
        'en-GB': 'University Western',
        'en-US': 'University Western',
        'fr': 'Université Ouest',
        'hr': 'Sveučilište Zapad',
        'it': 'Università Ovest',
        'lt': 'Universitetas Į Vakarus',
        'hu': 'Egyetemi Nyugat',
        'nl': 'Universiteit West',
        'no': 'Universitet Vest',
        'pl': 'Uniwersytet Zachód',
        'pt-BR': 'Universidade Oeste',
        'ro': 'Universitate Vest',
        'fi': 'Yliopisto Länsi',
        'sv-SE': 'Högskolan Väst',
        'vi': 'Đại học hướng Tây',
        'tr': 'Üniversite Batı',
        'cs': 'Univerzita Západ',
        'el': 'Πανεπιστήμιο δυτικά',
        'bg': 'университет Уест',
        'ru': 'Университет Запад',
        'uk': 'Університет Західний',
        'zh-CN': '大学西',
        'ja': '大学西',
        'zh-TW': '大學西',
        'ko': '대학교서쪽'
    }
)

_ltu = OptionChoice(
    name='Luleå Tekniska Universitet',
    value='LTU',
    name_localizations={
        'da': 'Luleå Tekniske Universitet',
        'de': 'Luleå Universität',
        'en-GB': 'Luleå University of Technology',
        'en-US': 'Luleå University of Technology',
        'es-ES': 'Universidad de Luleå',
        'fr': 'Université de Luleå',
        'hr': 'Luleå Tekničko-Poljoprivredna Fakultet',
        'it': 'Università di Luleå',
        'lt': 'Luleo akademija',
        'hu': 'Lulea Egyetem',
        'nl': 'Universiteit Luleå',
        'no': 'Universitetet i Luleå',
        'pl': 'Uniwersytet w Luleå',
        'pt-BR': 'Universidade de Luleå',
        'ro': 'Universitatea din Luleå',
        'fi': 'Lulea yliopisto',
        'sv-SE': 'Högskolan i Luleå',
        'vi': 'Đại học Luleå',
        'tr': 'Luleå Üniversitesi',
        'cs': 'Univerzita v Luleå',
        'el': 'Πανεπιστήμιο του Luleå',
        'bg': 'Университет в Луле',
        'ru': 'Университет Луле',
        'uk': 'Університет Луле',
        'zh-CN': '鲁爾林大学',
        'ja': 'ルーレ大学',
        'zh-TW': '魯爾林大學',
        'ko': '루레 대학교'
    }
)

_mau = OptionChoice(
    name='Malmö Universitet',
    value='MAU',
    name_localizations={
        'da': 'Malmö Universitet',
        'de': 'Malmö Universität',
        'en-GB': 'Malmö University',
        'en-US': 'Malmö University',
        'fr': 'Université de Malmö',
        'hr': 'Malmö Fakultet',
        'it': 'Università di Malmö',
        'lt': 'Malmo akademija',
        'hu': 'Malmö Egyetem',
        'nl': 'Universiteit Malmö',
        'no': 'Universitetet i Malmö',
        'pl': 'Uniwersytet w Malmó',
        'pt-BR': 'Universidade de Malmó',
        'ro': 'Universitatea din Malmö',
        'fi': 'Malmo yliopisto',
        'sv-SE': 'Högskolan i Malmö',
        'vi': 'Đại học Malmö',
        'tr': 'Malmö Üniversitesi',
        'cs': 'Univerzita v Malmö',
        'el': 'Πανεπιστήμιο του Malmö',
        'bg': 'Университет в Малмо',
        'ru': 'Университет Малмо',
        'uk': 'Університет Малмо',
        'zh-CN': '马尔默大学',
        'ja': 'マルモ大学',
        'zh-TW': '馬爾默大學',
        'ko': '말로 대학교'
    }
)

_mdu = OptionChoice(
    name='Mälardalens Universitet',
    value='MDU',
    name_localizations={
        'da': 'Mälardalens Universitet',
        'de': 'Mälardalen Universität',
        'en-GB': 'Mälardalen University',
        'en-US': 'Mälardalen University',
        'fr': 'Université de Malardalen',
        'hr': 'Mälardalen Fakultet',
        'it': 'Università di Malardalen',
        'lt': 'Malardalė akademija',
        'hu': 'Málardalen Egyetem',
        'nl': 'Universiteit Mälardalen',
        'no': 'Universitetet i Mälardalen',
        'pl': 'Uniwersytet w Malardalen',
        'pt-BR': 'Universidade de Malardalen',
        'ro': 'Universitatea din Malardalen',
        'fi': 'Mälardalen yliopisto',
        'sv-SE': 'Mälardalen Universitet',
        'vi': 'Đại học Mälardalen',
        'tr': 'Mälardalen Üniversitesi',
        'cs': 'Univerzita v Mälardalen',
        'el': 'Πανεπιστήμιο του Mälardalen',
        'bg': 'Университет в Маларден',
        'ru': 'Университет Маларден',
        'uk': 'Університет Маларден',
        'zh-CN': '马尔阿尔达纳大学',
        'ja': 'マルア',
        'zh-TW': '馬爾阿爾达納大學',
        'ko': '말라드라네 대학교'
    }
)

_sh = OptionChoice(
    name='Södertörns Universitet',
    value='SH',
    name_localizations={
        'da': 'Södertörns Universitet',
        'de': 'Södertörns Universität',
        'en-GB': 'Södertörns University',
        'en-US': 'Södertörns University',
        'fr': 'Université de Södertörns',
        'hr': 'Södertörns Fakultet',
        'it': 'Università di Södertörns',
        'lt': 'Södertörno akademija',
        'hu': 'Södertörn Egyetem',
        'nl': 'Universiteit Södertörns',
        'no': 'Universitetet i Södertörns',
        'pl': 'Uniwersytet w Södertörns',
        'pt-BR': 'Universidade de Södertörns',
        'ro': 'Universitatea din Södertörns',
        'fi': 'Södertörns yliopisto',
        'sv-SE': 'Högskolan i Södertörns',
        'vi': 'Đại học Södertörns',
        'tr': 'Södertörns Üniversitesi',
        'cs': 'Univerzita v Södertörns',
        'el': 'Πανεπιστήμιο του Södertörns',
        'bg': 'Университет в София',
        'ru': 'Университет София',
        'uk': 'Університет Софія',
        'zh-CN': '索尔托纳大学',
        'ja': 'ソートルナ大学',
        'zh-TW': '索爾托納大學',
        'ko': '소데토르네 대학교'
    }
)

_oru = OptionChoice(
    name='Örebro Universitet',
    value='ORU',
    name_localizations={
        'da': 'Örebro Universitet',
        'de': 'Örebro Universität',
        'en-GB': 'Örebro University',
        'en-US': 'Örebro University',
        'es-ES': 'Universidad de Örebro',
        'fr': 'Université Örebro',
        'hr': 'Sveučilište Örebro',
        'it': 'Örebro Università',
        'lt': 'Örebro universitetas',
        'hu': 'Egyetemi Örebro Egyetem',
        'nl': 'Universiteit Örebro',
        'no': 'Örebro Universitet',
        'pl': 'Uniwersytet Örebro',
        'pt-BR': 'Universidade de Örebro ',
        'ro': 'Universitatea Örebro',
        'fi': 'Örebron Yliopisto',
        'sv-SE': 'Örebro Universitet',
        'vi': 'Đại học Örebro',
        'tr': 'Örebro Üniversitesi',
        'cs': 'Univerzita Örebro',
        'el': 'Πανεπιστήμιο Örebro',
        'bg': 'Университет Еребру',
        'ru': 'Университет Эребру',
        'uk': 'Університет Еребру',
        'zh-CN': 'Örebro 大学',
        'ja': 'Örebro 大学',
        'zh-TW': 'Örebro 大學',
        'ko': 'Örebro 대학교 '
    }
)

schools = Option(
    str,
    name='university',
    name_localizations={
        'da': 'universitet',
        'de': 'universiteit',
        'en-GB': 'university',
        'en-US': 'university',
        'es-ES': 'universidad',
        'fr': 'université',
        'hr': 'sveučilište',
        'it': 'università',
        'lt': 'universitetas',
        'hu': 'egyetemi',
        'nl': 'universiteit',
        'no': 'universitet',
        'pl': 'uniwersytet',
        'pt-BR': 'universidade',
        'ro': 'universitate',
        'fi': 'yliopisto',
        'sv-SE': 'universitet',
        'vi': 'đạihọc',
        'tr': 'üniversite',
        'cs': 'univerzita',
        'el': 'πανεπιστήμιο',
        'bg': 'университет',
        'ru': 'университет',
        'uk': 'університет',
        'zh-CN': '大学',
        'ja': '大学',
        'zh-TW': '大學',
        'ko': '대학교'
    },
    description='Choose which university you want to search a schedule from',
    description_localizations={
        'da': 'Vælg hvilket universitet du vil søge efter plan for planlægning fra',
        'de': 'Wählen Sie aus, welche Universität Sie nach Zeitplan suchen möchten',
        'en-GB': 'Choose which university you want to search for schedule from',
        'en-US': 'Choose which university you want to search for schedule from',
        'es-ES': 'Elija qué universidad desea buscar programación de',
        'fr': 'Choisissez quelle université vous souhaitez rechercher le calendrier de',
        'hr': 'Odaberite koje sveučilište želite tražiti raspored',
        'it': 'UnivScegli quale università vuoi cercare il programma daersità',
        'lt': 'Pasirinkite, kurį universitetą norite ieškoti tvarkaraščio',
        'hu': 'Válassza ki, melyik egyetemre szeretné keresni az ütemtervet',
        'nl': 'Kies welke universiteit u zoekt naar schema van',
        'no': 'Velg hvilket universitet du vil søke etter tidsplan fra',
        'pl': 'Wybierz, z którego uniwersytet chcesz wyszukać harmonogram',
        'pt-BR': 'Escolha qual universidade você deseja procurar por programação de',
        'ro': 'Alegeți la care universitate doriți să căutați un program de la',
        'fi': 'Valitse mikä yliopisto haluat etsiä aikataulua',
        'sv-SE': 'Välj vilken universitet du vill söka schema från',
        'vi': 'Chọn trường đại học nào bạn muốn tìm kiếm lịch trình từ',
        'tr': 'Zamanlama için hangi üniversiteyi aramak istediğinizi seçin',
        'cs': 'Vyberte si, která univerzita chcete vyhledat plán',
        'el': 'Επιλέξτε ποιο πανεπιστήμιο θέλετε να αναζητήσετε πρόγραμμα από',
        'bg': 'Изберете кой университет искате да търсите график от',
        'ru': 'Выберите, какой у университета вы хотите найти расписание по расписанию',
        'uk': 'Виберіть, який університет ви хочете шукати графік з',
        'zh-CN': '选择您要搜索的哪所大学',
        'ja': 'スケジュールを検索したい大学を選択する',
        'zh-TW': '選擇您要搜索的哪所大學',
        'ko': '일정을 검색하고자하는 대학을 선택하십시오'
    },
    # choices=[_hb, _hig, _hkr, _hv, _ltu, _mau, _mdu, _sh, _oru],
    autocomplete=_get_schools,
    required=True
)

choices = [_hb, _hig, _hkr, _hv, _ltu, _mau, _mdu, _sh, _oru]
