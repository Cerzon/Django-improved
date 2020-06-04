# Generated by Django 3.0.5 on 2020-05-18 20:12

from django.db import migrations


def forwards_func(apps, schema_editor):
    UserQuote = apps.get_model('quotesapp', 'UserQuote')
    HoHooUser = apps.get_model('authapp', 'HoHooUser')
    Product = apps.get_model('mainapp', 'Product')
    UserQuote.objects.bulk_create([
        UserQuote(
            author=HoHooUser.objects.get(username='ilf_petrov'),
            text='В нашей обширной стране обыкновенный автомобиль, предназначенный, по мысли пешеходов, для мирной перевозки людей и грузов, принял грозные очертания братоубийственного снаряда.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Финансовя пропасть &mdash; самая глубокая из всех пропастей, в неё можно падать всю жизнь.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='ilf_petrov'),
            text='Пиво отпускается только членам профсоюза',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Надо мыслить. Меня, например, кормят идеи. Я не протягиваю лапу за кислым исполкомовским рублём. Моя наметка пошире.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Раз в стране бродят какие-то денежные знаки, то должны же быть люди, у которых их много.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='balag_s'),
            text='Хорошо жить на свете! Вот мы едем, мы сыты. Может быть, нас ожидает счастье...',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='ilf_petrov'),
            text='Настоящая жизнь пролетела мимо, радостно трубя и сверкая лаковыми крыльями',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='ilf_petrov'),
            text='Параллельно большому миру, в котором живут большие люди и большие вещи, существует маленький мир с маленькими людьми и маленькими вещами. В большом мире людьми двигает стремление облагодетельствовать человечество. Маленький мир далёк от таких высоких материй. У его обитателей стремление одно &mdash; как-нибудь прожить, не испытывая чувства голода.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Самое главное &mdash; это внести смятение в лагерь противника. Враг должен потерять душевное равновесие. Сделать это не так трудно. В конце концов люди больше всего пугаются непонятного.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='balag_s'),
            text='Что же вы меня бьёте? Я же только спросил, который час!..',
            header=False
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Вы не в церкви, вас не обманут. Будет и задаток. С течением времени.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='panik_m'),
            text='Отдайте мне мои деньги, я совсем бедный! Я год не был в бане. Я старый. Меня девушки не любят.',
            header=False
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='panik_m'),
            text='Я всех вас переживу. Вы не знаете Паниковского. Паниковский вас всех ещё продаст и купит. Отдайте мои деньги.',
            header=False
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Вот послал бог дурака уполномоченного по копытам! Ничего поручить нельзя. Купил машинку с турецким акцентом. Значит, я начальник отдэлэния? Свинья вы, Шура, после этого!',
            header=False,
            product=Product.objects.get(slug='turkish_typewriter')
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='panik_m'),
            text='Может быть, уйдём? Всё-таки храм божий. Неудобно.',
            header=False
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Где нет любви, там о деньгах говорить не принято.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='panik_m'),
            text='А меня не посылают в командировку. И отпуска не дают. Мне нужно ехать в Ессентуки, лечиться. И выходных дней у меня нету, и спецодежды не дают.',
            header=False
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Полное спокойствие может дать человеку только страховой полис. Так вам скажет любой агент по страхованию жизни. Лично мне вы больше не нужны. Вот государство, оно, вероятно, вами скоро заинтересуется.',
            header=True
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='panik_m'),
            text='Не верю! Паниковский не обязан всему верить!',
            header=False
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='panik_m'),
            text='Это золотые гири! Понимаете? Гири из чистого золота. Я стал перед этими гирями и бешено хохотал.',
            header=False,
            product=Product.objects.get(slug='kettlebell')
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='balag_s'),
            text='Три часа уже пилю, а оно всё ещё не золотое.',
            header=False
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Я не только трудился. Я даже пострадал. Я потерял веру в человечество. Разве это не стоит миллиона рублей, вера в человечество?',
            header=False
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Что это за шутки? Гражданин подзащитный, призываю вас к порядку.',
            header=False,
            product=Product.objects.get(slug='gasmask')
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='balag_s'),
            text='Паниковский сказал, что они золотые.',
            header=False,
            product=Product.objects.get(slug='kettlebell')
        ),
        UserQuote(
            author=HoHooUser.objects.get(username='bender_o'),
            text='Запятые ставят перед &quot;что&quot;, &quot;который&quot; и &quot;если&quot;. Многоточия, восклиц. знаки и кавычки &mdash; где только возможно.',
            header=False,
            product=Product.objects.get(slug='solemnset')
        ),
    ])


def reverse_func(apps, schema_editor):
    UserQuote = apps.get_model('quotesapp', 'UserQuote')
    UserQuote.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('quotesapp', '0001_initial'),
        ('authapp', '0002_fill_staff'),
        ('mainapp', '0002_fill_products'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
