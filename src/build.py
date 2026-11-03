"""Builds the deployable site (../dist/) from template.html in English and Turkish.

Usage: python3 src/build.py
"""
import html, json, os, re, shutil, time

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(os.path.dirname(ROOT), 'dist')
LI = 'https://www.linkedin.com/in/eray-u-163bb5373'
RAW = {'h1_b', 'quote', 'contact_t', 'jsonld', 'brief_lines', 'en_current', 'tr_current'}

EN = dict(
    lang='en', url='https://erayulusoy.com/', og_locale='en_US', og_locale_alt='tr_TR',
    meta_title='Eray Ulusoy | Web Design, Business Apps & Cloud',
    meta_desc='Eray Ulusoy builds professional, secure websites and business applications for companies and sets up reliable cloud infrastructure on AWS.',
    og_desc='Professional websites, business applications and cloud solutions for companies.',
    skip='Skip to content', nav_label='Main', accepting='Accepting new projects', consulting='Web &amp; Software',
    n_services='Services', n_approach='Approach', n_engagements='Engagements', n_about='About', n_contact='Contact',
    lang_label='Language', cta_consult='Request a consultation', menu_open='Open menu',
    other_label='Türkçe', other_lang='tr',
    hero_eyebrow='Eray Ulusoy · Websites, Business Applications & Cloud',
    h1_a='Professional websites.', h1_b='<em>Reliable</em> applications.',
    hero_sub='I design and build websites and applications for businesses, secure by design and running on reliable cloud infrastructure, so your company looks right online and works better behind the scenes.',
    li_connect='Connect on LinkedIn',
    brief_label='Project summary', brief_title='Project brief', brief_status='in progress',
    brief_lines=[['s', 'client     '], ['', 'Retail company\n'], ['s', 'scope      '], ['', 'Website · Order app\n'], ['s', 'hosting    '], ['', 'AWS · Cloudflare\n\n'],
                 ['g', '› '], ['', 'design ................. '], ['g', 'approved\n'], ['g', '› '], ['', 'website ................ '], ['g', 'live\n'],
                 ['g', '› '], ['', 'mobile app ............. '], ['', 'in testing\n'], ['g', '› '], ['', 'cloud setup ............ '], ['s', 'deploying']],
    f1='Years in software and security', f2='Services under one roof', f3='You work directly with me', f4='Certification track in progress',
    s1_label='01 — Perspective',
    quote='I help companies look professional online and work more efficiently, <em>with websites and applications built to last.</em>',
    role='Web Designer &amp; Software Engineer',
    s2_label='I — Services', s2_title='Websites, applications and cloud',
    s2_lead='Everything a business needs to run online, from one person. Your website, your app and the cloud they run on are planned together and built with security in mind from day one, backed by my background in cybersecurity.',
    web_t='Corporate Websites', web_p='Fast, elegant websites designed around your brand. Built to load quickly on every device, be easy to find on Google and turn visitors into customers.',
    web_1='Corporate and brand websites', web_2='Landing pages and redesigns', web_3='SEO, SSL and security hardening',
    dev_t='Business Applications', dev_p='Web and mobile applications that simplify how your company works: customer portals, booking and order systems, dashboards and internal tools.',
    dev_1='Web and mobile apps', dev_2='Admin panels and dashboards', dev_3='Secure login, data protection and integrations',
    cl_t='Cloud Computing', cl_p='Reliable infrastructure on AWS and Cloudflare. I host, migrate and maintain your sites and apps so they stay fast, backed up and available.',
    cl_1='Hosting and cloud setup', cl_2='Migration to the cloud', cl_3='Backups, monitoring and maintenance',
    discuss='Discuss →',
    s3_label='II — Approach', s3_title='A clear method, from first call to handover',
    s3_lead='Every project follows the same four stages, so you always know where the work stands and what comes next.',
    st1_t='Understand', st1_p='Your business, your customers and what the website or application needs to achieve.',
    st2_t='Design', st2_p='Page layouts, screens and a clear plan, agreed with you before development starts.',
    st3_t='Build &amp; Test', st3_p='Development with regular previews, tested on real devices and checked for security vulnerabilities before launch.',
    st4_t='Launch &amp; Support', st4_p='Go-live on reliable cloud hosting, a handover you can manage and ongoing support.',
    s4_label='III — Engagements', s4_title='Ways to work together',
    s4_lead='Clear scope, a fixed price and a defined delivery date. Everything is agreed in writing after a short introductory call.',
    len='Typical length', receive='You receive',
    e1_tag='Website', e1_t='Corporate website', e1_p='A professional website for your company, from design to launch, including domain, hosting and business email setup.',
    e1_len='2 – 6 weeks', e1_rec='Live website, SEO setup and a short guide to manage it',
    e2_tag='Application', e2_t='Business application', e2_p='A web or mobile application built around how your business actually works, for your team or your customers.',
    e2_len='6 – 14 weeks', e2_rec='Working application, deployment and documentation',
    e3_tag='Cloud', e3_t='Cloud setup &amp; care', e3_p='Moving your website or systems to the cloud, or setting them up there from scratch, with backups and monitoring.',
    e3_len='1 – 4 weeks', e3_rec='Cloud setup, backups and an optional monthly care plan',
    s5_label='IV — About',
    about_t='Built to look good. Built to be secure.',
    about_lead='For the past four years I have been building software and working in cybersecurity. Today I help businesses with their whole online presence: the website customers see, the applications teams use every day and the cloud infrastructure behind them. My security background means every project is protected against common attacks from the start, not patched afterwards.',
    about_p='I work independently under my own name, which means every client works with me directly, from the first conversation to launch and beyond. I am currently deepening my cloud expertise through the AWS certification track.',
    li_view='View my LinkedIn profile', cert_track='Certification track',
    c1='Cloud concepts, core services, pricing', c2='Reliable and scalable architecture design',
    inprog='In progress', planned='Planned',
    s6_label='V — Principles', s6_title='How I work',
    p1_t='Security by design', p1_p='Every website and application is built with security best practices from the first line of code: encrypted connections, protected data and safe logins.',
    p2_t='Quality', p2_p='Clean design, fast pages, a clear scope and well-built code that keeps working long after launch.',
    p3_t='Accountability', p3_p='One person responsible for the work from start to finish. Nothing is passed on to subcontractors.',
    s7_label='VI — Contact', contact_t='Let&#39;s discuss <em>your project.</em>',
    contact_lede='Tell me briefly what you need using the form, or write to contact@erayulusoy.com. I reply to every enquiry within two working days, and the first call is free of charge.',
    email='Email', copy='Copy', copied='Copied', location='Location', location_v='Remote · Working with clients internationally',
    li_card_t='Connect with me on LinkedIn',
    f_name='Full name', f_company='Company', f_service='Service of interest', f_msg='Project summary',
    ph_name='Your name', ph_company='Company name', ph_email='you@company.com', ph_msg='What would you like to build, and roughly when do you need it?',
    ch_web='Website', ch_dev='Application', ch_cloud='Cloud', ch_unsure='Not sure yet',
    form_note='Your details are used only to reply to your enquiry.', send='Send enquiry',
    m_name='Please enter your name.', m_email='Please enter a valid email address so I can reply.',
    m_offline='Thank you, {name}. Online sending is not connected yet, so please email contact@erayulusoy.com directly.',
    m_sending='Sending…', m_sent='Thank you, {name}. Your enquiry has been sent and I will reply within two working days.',
    m_error='Your enquiry could not be sent. Please try again or email contact@erayulusoy.com.',
    footer_tag='Websites · Applications · Cloud',
)

TR = dict(EN)
TR.update(
    lang='tr', url='https://erayulusoy.com/tr/', og_locale='tr_TR', og_locale_alt='en_US',
    meta_title='Eray Ulusoy | Web Sitesi Tasarımı, Uygulama Geliştirme ve Bulut',
    meta_desc='Eray Ulusoy; işletmelere ve şirketlere güvenli ve profesyonel web sitesi tasarımı, web ve mobil uygulama geliştirme ve AWS bulut bilişim hizmetleri sunar.',
    og_desc='Şirketler için profesyonel web siteleri, iş uygulamaları ve bulut çözümleri.',
    skip='İçeriğe geç', nav_label='Ana menü', accepting='Yeni projelere açığım', consulting='Web ve Yazılım',
    n_services='Hizmetler', n_approach='Yaklaşım', n_engagements='Çalışma şekli', n_about='Hakkımda', n_contact='İletişim',
    lang_label='Dil', cta_consult='Görüşme talep et', menu_open='Menüyü aç',
    other_label='English', other_lang='en',
    hero_eyebrow='Eray Ulusoy · Web Sitesi, İş Uygulamaları ve Bulut',
    h1_a='Profesyonel web siteleri.', h1_b='<em>Güvenilir</em> uygulamalar.',
    hero_sub='İşletmeler için baştan güvenli tasarlanmış web siteleri ve uygulamalar geliştiriyor, bunları güvenilir bulut altyapısında çalıştırıyorum. Şirketiniz internette doğru görünsün, arka planda da daha verimli çalışsın.',
    li_connect='LinkedIn’de bağlantı kur',
    brief_label='Proje özeti', brief_title='Proje özeti', brief_status='devam ediyor',
    brief_lines=[['s', 'müşteri    '], ['', 'Perakende şirketi\n'], ['s', 'kapsam     '], ['', 'Web sitesi · Sipariş uygulaması\n'], ['s', 'altyapı    '], ['', 'AWS · Cloudflare\n\n'],
                 ['g', '› '], ['', 'tasarım ................ '], ['g', 'onaylandı\n'], ['g', '› '], ['', 'web sitesi ............. '], ['g', 'yayında\n'],
                 ['g', '› '], ['', 'mobil uygulama ......... '], ['', 'testte\n'], ['g', '› '], ['', 'bulut kurulumu ......... '], ['s', 'yükleniyor']],
    f1='Yıllık yazılım ve güvenlik deneyimi', f2='Tek çatı altında üç hizmet', f3='Doğrudan benimle çalışırsınız', f4='Sertifika süreci devam ediyor',
    s1_label='01 — Bakış açısı',
    quote='Şirketlerin internette profesyonel görünmesine ve daha verimli çalışmasına yardımcı oluyorum, <em>uzun ömürlü web siteleri ve uygulamalarla.</em>',
    role='Web Tasarımcı ve Yazılım Mühendisi',
    s2_label='I — Hizmetler', s2_title='Web siteleri, uygulamalar ve bulut',
    s2_lead='Bir işletmenin internette ihtiyaç duyduğu her şey, tek bir kişiden. Web siteniz, uygulamanız ve bunların çalıştığı bulut altyapısı birlikte planlanır ve siber güvenlik deneyimimle ilk günden güvenli şekilde geliştirilir.',
    web_t='Kurumsal Web Siteleri', web_p='Markanıza özel tasarlanan hızlı ve şık web siteleri. Her cihazda hızlı açılan, Google’da kolay bulunan ve ziyaretçiyi müşteriye dönüştüren siteler.',
    web_1='Kurumsal web sitesi yapımı', web_2='Tanıtım sayfaları ve site yenileme', web_3='SEO, SSL ve güvenlik sıkılaştırması',
    dev_t='İş Uygulamaları', dev_p='Şirketinizin işlerini kolaylaştıran web ve mobil uygulamalar: müşteri panelleri, randevu ve sipariş sistemleri, raporlama ekranları ve şirket içi araçlar.',
    dev_1='Web ve mobil uygulama geliştirme', dev_2='Yönetim panelleri ve raporlama ekranları', dev_3='Güvenli giriş, veri koruma ve entegrasyonlar',
    cl_t='Bulut Bilişim', cl_p='AWS ve Cloudflare üzerinde güvenilir altyapı. Sitelerinizi ve uygulamalarınızı barındırır, buluta taşır ve bakımını yaparım; hızlı, yedekli ve her zaman erişilebilir kalırlar.',
    cl_1='Barındırma ve bulut kurulumu', cl_2='Buluta taşıma', cl_3='Yedekleme, izleme ve bakım',
    discuss='Görüşelim →',
    s3_label='II — Yaklaşım', s3_title='İlk görüşmeden teslime kadar net bir yöntem',
    s3_lead='Her proje aynı dört aşamadan geçer; böylece işin nerede olduğunu ve sırada ne olduğunu her zaman bilirsiniz.',
    st1_t='Anlama', st1_p='İşiniz, müşterileriniz ve web sitesinin ya da uygulamanın neyi başarması gerektiği.',
    st2_t='Tasarım', st2_p='Sayfa düzenleri, ekranlar ve net bir plan; geliştirme başlamadan önce sizinle birlikte onaylanır.',
    st3_t='Geliştirme ve Test', st3_p='Düzenli ön izlemelerle geliştirme; gerçek cihazlarda test ve yayından önce güvenlik açığı kontrolü.',
    st4_t='Yayın ve Destek', st4_p='Güvenilir bulut altyapısında yayına alma, kolayca yönetebileceğiniz bir teslim ve sürekli destek.',
    s4_label='III — Çalışma şekli', s4_title='Birlikte nasıl çalışabiliriz',
    s4_lead='Net kapsam, sabit fiyat ve belirli bir teslim tarihi. Her şey kısa bir tanışma görüşmesinin ardından yazılı olarak belirlenir.',
    len='Tipik süre', receive='Teslim edilenler',
    e1_tag='Web sitesi', e1_t='Kurumsal web sitesi', e1_p='Tasarımdan yayına kadar şirketinize özel profesyonel bir web sitesi; alan adı, barındırma ve kurumsal e-posta kurulumu dahil.',
    e1_len='2 – 6 hafta', e1_rec='Yayında web sitesi, SEO kurulumu ve kısa bir kullanım rehberi',
    e2_tag='Uygulama', e2_t='İş uygulaması', e2_p='İşletmenizin gerçek çalışma şekline göre ekibiniz ya da müşterileriniz için geliştirilen bir web veya mobil uygulama.',
    e2_len='6 – 14 hafta', e2_rec='Çalışan uygulama, kurulum ve dokümantasyon',
    e3_tag='Bulut', e3_t='Bulut kurulumu ve bakımı', e3_p='Web sitenizi ya da sistemlerinizi buluta taşıma veya sıfırdan kurma; yedekleme ve izleme dahil.',
    e3_len='1 – 4 hafta', e3_rec='Bulut kurulumu, yedekleme ve isteğe bağlı aylık bakım planı',
    s5_label='IV — Hakkımda',
    about_t='Hem şık hem güvenli.',
    about_lead='Son dört yıldır yazılım geliştiriyor ve siber güvenlik alanında çalışıyorum. Bugün işletmelerin internetteki varlığının tamamında yardımcı oluyorum: müşterilerin gördüğü web sitesi, ekiplerin her gün kullandığı uygulamalar ve bunların arkasındaki bulut altyapısı. Güvenlik geçmişim sayesinde her proje yaygın saldırılara karşı en baştan korunur, sonradan yamanmaz.',
    about_p='Kendi adımla bağımsız çalışıyorum; yani her müşteri ilk görüşmeden yayına ve sonrasına kadar doğrudan benimle çalışıyor. Şu anda AWS sertifika süreciyle bulut alanındaki uzmanlığımı derinleştiriyorum.',
    li_view='LinkedIn profilimi görüntüle', cert_track='Sertifika süreci',
    c1='Bulut kavramları, temel servisler, fiyatlandırma', c2='Güvenilir ve ölçeklenebilir mimari tasarımı',
    inprog='Devam ediyor', planned='Planlandı',
    s6_label='V — İlkeler', s6_title='Nasıl çalışırım',
    p1_t='Baştan güvenli', p1_p='Her web sitesi ve uygulama ilk satır koddan itibaren güvenlik standartlarına göre geliştirilir: şifreli bağlantılar, korunan veriler ve güvenli girişler.',
    p2_t='Kalite', p2_p='Temiz tasarım, hızlı sayfalar, net kapsam ve yayından çok sonra da sorunsuz çalışan, özenle yazılmış kod.',
    p3_t='Sorumluluk', p3_p='İşin başından sonuna kadar sorumlu tek kişi. Hiçbir iş taşerona devredilmez.',
    s7_label='VI — İletişim', contact_t='Projenizi <em>konuşalım.</em>',
    contact_lede='Neye ihtiyacınız olduğunu formdan kısaca yazın ya da contact@erayulusoy.com adresine e-posta gönderin. Her mesaja iki iş günü içinde dönüyorum; ilk görüşme ücretsizdir.',
    email='E-posta', copy='Kopyala', copied='Kopyalandı', location='Konum', location_v='Uzaktan · Yurt içi ve yurt dışı müşterilerle çalışıyorum',
    li_card_t='LinkedIn’de benimle bağlantı kurun',
    f_name='Ad soyad', f_company='Şirket', f_service='İlgilendiğiniz hizmet', f_msg='Proje özeti',
    ph_name='Adınız', ph_company='Şirket adı', ph_email='siz@sirket.com', ph_msg='Ne yaptırmak istiyorsunuz, yaklaşık ne zaman lazım?',
    ch_web='Web sitesi', ch_dev='Uygulama', ch_cloud='Bulut', ch_unsure='Henüz emin değilim',
    form_note='Bilgileriniz yalnızca mesajınıza dönüş yapmak için kullanılır.', send='Mesajı gönder',
    m_name='Lütfen adınızı yazın.', m_email='Size dönebilmem için lütfen geçerli bir e-posta adresi yazın.',
    m_offline='Teşekkürler {name}. Çevrim içi gönderim henüz bağlı değil, lütfen doğrudan contact@erayulusoy.com adresine yazın.',
    m_sending='Gönderiliyor…', m_sent='Teşekkürler {name}. Mesajınız iletildi, iki iş günü içinde dönüş yapacağım.',
    m_error='Mesajınız gönderilemedi. Lütfen tekrar deneyin ya da contact@erayulusoy.com adresine yazın.',
    footer_tag='Web Siteleri · Uygulamalar · Bulut',
)


NOT_FOUND = dict(
    en_title='This page could not be found.',
    en_body='The link may be out of date, or the address may have a typo. Everything on this site is on the homepage.',
    en_home='Go to the homepage',
    tr_title='Aradığınız sayfa bulunamadı.',
    tr_body='Bağlantı eskimiş ya da adreste bir yazım hatası olabilir. Sitedeki her şey ana sayfada.',
    tr_home='Türkçe ana sayfaya dön',
)


def jsonld(d):
    data = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'Person', '@id': 'https://erayulusoy.com/#person', 'name': 'Eray Ulusoy',
             'url': 'https://erayulusoy.com/', 'image': 'https://erayulusoy.com/og-image.jpg',
             'jobTitle': 'Web Designer & Software Engineer' if d['lang'] == 'en' else 'Web Tasarımcı ve Yazılım Mühendisi',
             'email': 'mailto:contact@erayulusoy.com', 'sameAs': [LI],
             'knowsAbout': ['Web design', 'Web development', 'Mobile app development', 'Business applications', 'Cloud computing', 'AWS', 'SEO'],
             'knowsLanguage': ['tr', 'en']},
            {'@type': 'ProfessionalService', '@id': 'https://erayulusoy.com/#business', 'name': 'Eray Ulusoy',
             'url': d['url'], 'image': 'https://erayulusoy.com/og-image.jpg', 'email': 'contact@erayulusoy.com',
             'founder': {'@id': 'https://erayulusoy.com/#person'}, 'sameAs': [LI], 'areaServed': 'Worldwide',
             'description': d['meta_desc'],
             'knowsAbout': ['Web sitesi tasarımı', 'Web sitesi yapımı', 'Mobil uygulama geliştirme', 'Kurumsal yazılım', 'Bulut bilişim'] if d['lang'] == 'tr' else ['Website design', 'Website development', 'Mobile app development', 'Business software', 'Cloud computing']},
            {'@type': 'WebSite', '@id': 'https://erayulusoy.com/#website', 'url': 'https://erayulusoy.com/', 'name': 'Eray Ulusoy',
             'inLanguage': ['en', 'tr'], 'publisher': {'@id': 'https://erayulusoy.com/#person'}},
        ],
    }
    return json.dumps(data, ensure_ascii=False).replace('</', '<\\/')


def fill(tpl, v, raw=()):
    def sub(m):
        k = m.group(1)
        val = v[k]
        if k in raw:
            return str(val)
        # values may contain pre-escaped entities (&amp;, &#39;); escape only bare < > "
        return str(val).replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    out = re.sub(r'\{\{(\w+)\}\}', sub, tpl)
    assert '{{' not in out
    return out


def read(name):
    return open(os.path.join(ROOT, name), encoding='utf-8').read()


def render(d, base, home, en_href, tr_href, ver):
    v = dict(d)
    v['brief_lines'] = json.dumps(d['brief_lines'], ensure_ascii=False).replace('&', '&amp;').replace("'", '&#39;').replace('<', '&lt;')
    v['jsonld'] = jsonld(d)
    v.update(base=base, home=home, en_href=en_href, tr_href=tr_href, ver=ver,
             other_href=tr_href if d['lang'] == 'en' else en_href,
             en_current=' aria-current="true"' if d['lang'] == 'en' else '',
             tr_current=' aria-current="true"' if d['lang'] == 'tr' else '')
    return fill(read('template.html'), v, RAW)


def build():
    ver = time.strftime('%Y%m%d%H%M')
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, 'tr'))
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(DIST, 'assets'))
    for f in ['favicon.svg', 'favicon.ico', 'favicon-192.png', 'apple-touch-icon.png', 'og-image.jpg', 'robots.txt', 'sitemap.xml', '_headers', 'site.webmanifest']:
        shutil.copy(os.path.join(ROOT, f), DIST)
    os.makedirs(os.path.join(DIST, '.well-known'))
    shutil.copy(os.path.join(ROOT, 'security.txt'), os.path.join(DIST, '.well-known', 'security.txt'))
    open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8').write(render(EN, '', '/', '/', '/tr/', ver))
    open(os.path.join(DIST, 'tr', 'index.html'), 'w', encoding='utf-8').write(render(TR, '../', '/tr/', '/', '/tr/', ver))
    # served by Cloudflare for any unknown URL (assets.not_found_handling = "404-page" in wrangler.jsonc)
    open(os.path.join(DIST, '404.html'), 'w', encoding='utf-8').write(fill(read('404.html'), dict(NOT_FOUND, ver=ver)))
    print('built', ver)


if __name__ == '__main__':
    build()
