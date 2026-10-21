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
    meta_title='Eray Ulusoy | Web Design, Software Development & Cybersecurity',
    meta_desc='Eray Ulusoy is an independent web designer, software developer and cybersecurity consultant. Secure websites, custom software, penetration testing and AWS cloud.',
    og_desc='Independent web design, software development, cybersecurity and AWS cloud consulting.',
    skip='Skip to content', nav_label='Main', accepting='Accepting new projects', consulting='Consulting',
    n_services='Services', n_approach='Approach', n_engagements='Engagements', n_about='About', n_contact='Contact',
    lang_label='Language', cta_consult='Request a consultation', menu_open='Open menu',
    other_label='Türkçe', other_lang='tr',
    hero_eyebrow='Eray Ulusoy · Web Design, Software, Security & Cloud',
    h1_a='Secure software.', h1_b='<em>Considered</em> architecture.',
    hero_sub='I design websites, build software, test it the way an attacker would, and help businesses move to AWS with security in place from the first day.',
    li_connect='Connect on LinkedIn',
    brief_label='Assessment summary', brief_title='Assessment brief', brief_status='in session',
    brief_lines=[['s', 'client     '], ['', 'Confidential\n'], ['s', 'scope      '], ['', 'Website · AWS account\n'], ['s', 'method     '], ['', 'OWASP testing guide\n\n'],
                 ['g', '› '], ['', 'recon .................. '], ['g', 'done\n'], ['g', '› '], ['', 'access review .......... '], ['g', 'done\n'],
                 ['g', '› '], ['', 'findings ............... '], ['', '3 medium\n'], ['g', '› '], ['', 'report ................. '], ['s', 'drafting']],
    f1='Years in software and security', f2='Disciplines under one engagement', f3='You work directly with me', f4='Certification track in progress',
    s1_label='01 — Perspective',
    quote='I help businesses build reliable websites and software and protect what matters, <em>from the first line of code to the cloud.</em>',
    role='Web Designer, Software Engineer &amp; Security Consultant',
    s2_label='I — Services', s2_title='Design, engineering and defensive security',
    s2_lead='Four disciplines that usually sit with four different vendors. Keeping them together means security decisions are made while the site or system is designed, not after it ships.',
    web_t='Web Design &amp; Websites', web_p='Fast, elegant business websites designed around your brand and built to be secure, accessible and easy to find on Google.',
    web_1='Corporate and personal websites', web_2='Landing pages and redesigns', web_3='SEO basics, hosting and domain setup',
    dev_t='Software Development', dev_p='Custom web applications, APIs and internal tools. Clear structure, tested code and documentation your team can work with after handover.',
    dev_1='Web applications and dashboards', dev_2='REST APIs and integrations', dev_3='Process automation',
    sec_t='Cybersecurity', sec_p='Penetration testing and vulnerability assessments for websites, applications and networks. Each finding is rated by severity and explained with a clear fix.',
    sec_1='Web application penetration testing', sec_2='Vulnerability assessment', sec_3='Code and configuration review',
    cl_t='Cloud &amp; AWS', cl_p='Secure foundations on AWS: access control with least privilege, sensible network design and storage that is private by default.',
    cl_1='IAM and access design', cl_2='VPC and network setup', cl_3='S3 and configuration reviews',
    discuss='Discuss →',
    s3_label='II — Approach', s3_title='A clear method, from first call to handover',
    s3_lead='Every engagement follows the same four stages, so you always know where the work stands and what comes next.',
    st1_t='Understand', st1_p='Your goals, your current systems and the risks that matter most to your business.',
    st2_t='Design', st2_p='A written plan for the design, architecture and security controls, agreed before any build starts.',
    st3_t='Build &amp; Test', st3_p='Implementation with automated tests, followed by my own attacker-style review.',
    st4_t='Secure &amp; Support', st4_p='Hardened deployment, documentation and a handover your team can maintain.',
    s4_label='III — Engagements', s4_title='Ways to work together',
    s4_lead='Fixed-scope engagements with a clear deliverable. Scope and price are agreed in writing after a short introductory call.',
    len='Typical length', receive='You receive',
    e1_tag='Build', e1_t='Website or application build', e1_p='A new website, web application or API, designed and built with security reviewed at every stage.',
    e1_len='2 – 10 weeks', e1_rec='Live site or source code, deployment and documentation',
    e2_tag='Assess', e2_t='Security assessment', e2_p='A structured test of an existing website, application or network to find weaknesses before someone else does.',
    e2_len='1 – 3 weeks', e2_rec='Written report with severity ratings and fixes, plus a retest',
    e3_tag='Cloud', e3_t='AWS readiness review', e3_p='A review of how your AWS account is set up, focused on access, exposure and the basics that prevent most incidents.',
    e3_len='1 – 2 weeks', e3_rec='Findings, priorities and a step-by-step remediation plan',
    s5_label='IV — About', portrait_alt='Portrait of Eray Ulusoy',
    about_t='An engineer who also thinks like an attacker.',
    about_lead='I have spent the past four years building websites and software and testing systems for security weaknesses. That combination shapes how I work: I build expecting it to be attacked, and I test systems knowing how they are built.',
    about_p='I now work independently under my own name, which means every client works with me directly, from the first conversation to the final handover. I am currently extending my work into cloud infrastructure through the AWS certification track.',
    li_view='View my LinkedIn profile', cert_track='Certification track',
    c1='Cloud concepts, security, core services', c2='Secure and resilient architecture design', c3='Detection, incident response, data protection',
    inprog='In progress', planned='Planned',
    s6_label='V — Principles', s6_title='How I work',
    p1_t='Discretion', p1_p='Your code, your systems and anything I find in them stay confidential. Findings go only to the people you name.',
    p2_t='Precision', p2_p='Clear scope, clear reports and no unnecessary complexity. Every recommendation comes with the reason behind it.',
    p3_t='Accountability', p3_p='One person responsible for the work from start to finish. Nothing is passed on to subcontractors.',
    s7_label='VI — Contact', contact_t='Let&#39;s discuss <em>your project.</em>',
    contact_lede='Tell me briefly what you need using the form, or write to contact@erayulusoy.com. I reply to every enquiry within two working days, and the first call is free of charge.',
    email='Email', copy='Copy', copied='Copied', location='Location', location_v='Remote · Working with clients internationally',
    li_card_t='Connect with me on LinkedIn',
    f_name='Full name', f_company='Company', f_service='Service of interest', f_msg='Project summary',
    ph_name='Your name', ph_company='Company name', ph_email='you@company.com', ph_msg='What are you building or protecting, and roughly when do you need it?',
    ch_web='Website', ch_dev='Software', ch_sec='Security', ch_cloud='Cloud &amp; AWS',
    form_note='Your details are used only to reply to your enquiry.', send='Send enquiry',
    m_name='Please enter your name.', m_email='Please enter a valid email address so I can reply.',
    m_offline='Thank you, {name}. Online sending is not connected yet, so please email contact@erayulusoy.com directly.',
    m_sending='Sending…', m_sent='Thank you, {name}. Your enquiry has been sent and I will reply within two working days.',
    m_error='Your enquiry could not be sent. Please try again or email contact@erayulusoy.com.',
    footer_tag='Web Design · Software · Security · Cloud',
)

TR = dict(EN)
TR.update(
    lang='tr', url='https://erayulusoy.com/tr/', og_locale='tr_TR', og_locale_alt='en_US',
    meta_title='Eray Ulusoy | Web Sitesi Tasarımı, Yazılım ve Siber Güvenlik',
    meta_desc='Eray Ulusoy; web sitesi tasarımı, web sitesi yapımı, yazılım geliştirme, siber güvenlik ve sızma testi hizmetleri sunan bağımsız danışman. Güvenli web siteleri ve AWS.',
    og_desc='Web sitesi tasarımı, yazılım geliştirme, siber güvenlik ve AWS bulut danışmanlığı.',
    skip='İçeriğe geç', nav_label='Ana menü', accepting='Yeni projelere açığım', consulting='Danışmanlık',
    n_services='Hizmetler', n_approach='Yaklaşım', n_engagements='Çalışma şekli', n_about='Hakkımda', n_contact='İletişim',
    lang_label='Dil', cta_consult='Görüşme talep et', menu_open='Menüyü aç',
    other_label='English', other_lang='en',
    hero_eyebrow='Eray Ulusoy · Web Tasarım, Yazılım, Güvenlik ve Bulut',
    h1_a='Güvenli yazılım.', h1_b='<em>Özenli</em> mimari.',
    hero_sub='Web siteleri tasarlıyor, yazılım geliştiriyor, bunları bir saldırgan gözüyle test ediyor ve işletmelerin AWS’e ilk günden güvenli şekilde geçmesine yardımcı oluyorum.',
    li_connect='LinkedIn’de bağlantı kur',
    brief_label='Değerlendirme özeti', brief_title='Değerlendirme özeti', brief_status='devam ediyor',
    brief_lines=[['s', 'müşteri    '], ['', 'Gizli\n'], ['s', 'kapsam     '], ['', 'Web sitesi · AWS hesabı\n'], ['s', 'yöntem     '], ['', 'OWASP test rehberi\n\n'],
                 ['g', '› '], ['', 'keşif .................. '], ['g', 'tamam\n'], ['g', '› '], ['', 'erişim incelemesi ...... '], ['g', 'tamam\n'],
                 ['g', '› '], ['', 'bulgular ............... '], ['', '3 orta\n'], ['g', '› '], ['', 'rapor .................. '], ['s', 'hazırlanıyor']],
    f1='Yıllık yazılım ve güvenlik deneyimi', f2='Tek çatı altında dört uzmanlık', f3='Doğrudan benimle çalışırsınız', f4='Sertifika süreci devam ediyor',
    s1_label='01 — Bakış açısı',
    quote='İşletmelerin güvenilir web siteleri ve yazılımlar kurmasına ve değerli olanı korumasına yardımcı oluyorum, <em>ilk satır koddan buluta kadar.</em>',
    role='Web Tasarımcı, Yazılım Mühendisi ve Güvenlik Danışmanı',
    s2_label='I — Hizmetler', s2_title='Tasarım, yazılım ve savunma odaklı güvenlik',
    s2_lead='Genelde dört farklı firmadan alınan dört hizmet. Hepsi bir arada olduğunda güvenlik kararları site ya da sistem tasarlanırken alınır, yayına çıktıktan sonra değil.',
    web_t='Web Sitesi Tasarımı', web_p='Markanıza özel tasarlanan; hızlı, şık, güvenli ve Google’da kolay bulunan kurumsal web siteleri.',
    web_1='Kurumsal ve kişisel web sitesi yapımı', web_2='Tanıtım sayfaları ve site yenileme', web_3='Temel SEO, hosting ve alan adı kurulumu',
    dev_t='Yazılım Geliştirme', dev_p='Özel web uygulamaları, API’ler ve iç araçlar. Teslimden sonra ekibinizin rahatça devam edebileceği düzenli yapı, test edilmiş kod ve dokümantasyon.',
    dev_1='Web uygulamaları ve yönetim panelleri', dev_2='REST API’ler ve entegrasyonlar', dev_3='Süreç otomasyonu',
    sec_t='Siber Güvenlik', sec_p='Web siteleri, uygulamalar ve ağlar için sızma testi ve zafiyet analizi. Her bulgu önem derecesine göre puanlanır ve net bir çözümle açıklanır.',
    sec_1='Web uygulaması sızma testi', sec_2='Zafiyet analizi', sec_3='Kod ve yapılandırma incelemesi',
    cl_t='Bulut ve AWS', cl_p='AWS üzerinde güvenli temeller: en az yetki ilkesiyle erişim kontrolü, doğru ağ tasarımı ve varsayılan olarak gizli depolama.',
    cl_1='IAM ve erişim tasarımı', cl_2='VPC ve ağ kurulumu', cl_3='S3 ve yapılandırma incelemesi',
    discuss='Görüşelim →',
    s3_label='II — Yaklaşım', s3_title='İlk görüşmeden teslime kadar net bir yöntem',
    s3_lead='Her proje aynı dört aşamadan geçer; böylece işin nerede olduğunu ve sırada ne olduğunu her zaman bilirsiniz.',
    st1_t='Anlama', st1_p='Hedefleriniz, mevcut sistemleriniz ve işiniz için en önemli riskler.',
    st2_t='Tasarım', st2_p='Tasarım, mimari ve güvenlik önlemleri için yazılı bir plan; geliştirme başlamadan önce birlikte onaylanır.',
    st3_t='Geliştirme ve Test', st3_p='Otomatik testlerle geliştirme, ardından saldırgan bakış açısıyla kendi incelemem.',
    st4_t='Güvenlik ve Destek', st4_p='Güvenliği sıkılaştırılmış yayın, dokümantasyon ve ekibinizin sürdürebileceği bir teslim.',
    s4_label='III — Çalışma şekli', s4_title='Birlikte nasıl çalışabiliriz',
    s4_lead='Kapsamı belli, teslimatı net projeler. Kapsam ve fiyat, kısa bir tanışma görüşmesinin ardından yazılı olarak belirlenir.',
    len='Tipik süre', receive='Teslim edilenler',
    e1_tag='Geliştirme', e1_t='Web sitesi veya uygulama geliştirme', e1_p='Her aşamasında güvenliği gözden geçirilerek tasarlanan ve geliştirilen yeni bir web sitesi, web uygulaması ya da API.',
    e1_len='2 – 10 hafta', e1_rec='Yayında site veya kaynak kod, kurulum ve dokümantasyon',
    e2_tag='Değerlendirme', e2_t='Güvenlik değerlendirmesi', e2_p='Mevcut web sitenizin, uygulamanızın ya da ağınızın zayıf noktalarını başkasından önce bulmak için yapılandırılmış bir test.',
    e2_len='1 – 3 hafta', e2_rec='Önem derecelendirmeli ve çözümlü yazılı rapor, ardından tekrar test',
    e3_tag='Bulut', e3_t='AWS hazırlık incelemesi', e3_p='AWS hesabınızın kurulumunu; erişim, dışa açıklık ve olayların çoğunu önleyen temel ayarlar açısından inceleme.',
    e3_len='1 – 2 hafta', e3_rec='Bulgular, öncelikler ve adım adım iyileştirme planı',
    s5_label='IV — Hakkımda', portrait_alt='Eray Ulusoy portresi',
    about_t='Saldırgan gibi de düşünen bir mühendis.',
    about_lead='Son dört yıldır web siteleri ve yazılımlar geliştiriyor, sistemlerdeki güvenlik açıklarını test ediyorum. Bu ikisi çalışma şeklimi belirliyor: saldırıya uğrayacağını bilerek geliştiriyor, nasıl kurulduğunu bilerek test ediyorum.',
    about_p='Artık kendi adımla bağımsız çalışıyorum; yani her müşteri ilk görüşmeden son teslime kadar doğrudan benimle çalışıyor. Şu anda AWS sertifika süreciyle çalışmalarımı bulut altyapısına genişletiyorum.',
    li_view='LinkedIn profilimi görüntüle', cert_track='Sertifika süreci',
    c1='Bulut kavramları, güvenlik, temel servisler', c2='Güvenli ve dayanıklı mimari tasarımı', c3='Tespit, olay müdahalesi, veri koruma',
    inprog='Devam ediyor', planned='Planlandı',
    s6_label='V — İlkeler', s6_title='Nasıl çalışırım',
    p1_t='Gizlilik', p1_p='Kodunuz, sistemleriniz ve bunlarda bulduğum her şey gizli kalır. Bulgular yalnızca sizin belirlediğiniz kişilerle paylaşılır.',
    p2_t='Özen', p2_p='Net kapsam, anlaşılır raporlar ve gereksiz karmaşıklık yok. Her önerinin nedeni de açıklanır.',
    p3_t='Sorumluluk', p3_p='İşin başından sonuna kadar sorumlu tek kişi. Hiçbir iş taşerona devredilmez.',
    s7_label='VI — İletişim', contact_t='Projenizi <em>konuşalım.</em>',
    contact_lede='Neye ihtiyacınız olduğunu formdan kısaca yazın ya da contact@erayulusoy.com adresine e-posta gönderin. Her mesaja iki iş günü içinde dönüyorum; ilk görüşme ücretsizdir.',
    email='E-posta', copy='Kopyala', copied='Kopyalandı', location='Konum', location_v='Uzaktan · Yurt içi ve yurt dışı müşterilerle çalışıyorum',
    li_card_t='LinkedIn’de benimle bağlantı kurun',
    f_name='Ad soyad', f_company='Şirket', f_service='İlgilendiğiniz hizmet', f_msg='Proje özeti',
    ph_name='Adınız', ph_company='Şirket adı', ph_email='siz@sirket.com', ph_msg='Ne geliştiriyor ya da neyi korumak istiyorsunuz, yaklaşık ne zaman lazım?',
    ch_web='Web sitesi', ch_dev='Yazılım', ch_sec='Güvenlik', ch_cloud='Bulut ve AWS',
    form_note='Bilgileriniz yalnızca mesajınıza dönüş yapmak için kullanılır.', send='Mesajı gönder',
    m_name='Lütfen adınızı yazın.', m_email='Size dönebilmem için lütfen geçerli bir e-posta adresi yazın.',
    m_offline='Teşekkürler {name}. Çevrim içi gönderim henüz bağlı değil, lütfen doğrudan contact@erayulusoy.com adresine yazın.',
    m_sending='Gönderiliyor…', m_sent='Teşekkürler {name}. Mesajınız iletildi, iki iş günü içinde dönüş yapacağım.',
    m_error='Mesajınız gönderilemedi. Lütfen tekrar deneyin ya da contact@erayulusoy.com adresine yazın.',
    footer_tag='Web Tasarım · Yazılım · Güvenlik · Bulut',
)


# ---- Repositioning: websites, business applications and cloud (no cybersecurity service) ----
EN.update(
    consulting='Web &amp; Software',
    meta_title='Eray Ulusoy | Web Design, Business Apps & Cloud',
    meta_desc='Eray Ulusoy builds professional, secure websites and business applications for companies and sets up reliable cloud infrastructure on AWS.',
    og_desc='Professional websites, business applications and cloud solutions for companies.',
    hero_eyebrow='Eray Ulusoy · Websites, Business Applications & Cloud',
    h1_a='Professional websites.', h1_b='<em>Reliable</em> applications.',
    hero_sub='I design and build websites and applications for businesses, secure by design and running on reliable cloud infrastructure, so your company looks right online and works better behind the scenes.',
    brief_label='Project summary', brief_title='Project brief', brief_status='in progress',
    brief_lines=[['s', 'client     '], ['', 'Retail company\n'], ['s', 'scope      '], ['', 'Website · Order app\n'], ['s', 'hosting    '], ['', 'AWS · Cloudflare\n\n'],
                 ['g', '› '], ['', 'design ................. '], ['g', 'approved\n'], ['g', '› '], ['', 'website ................ '], ['g', 'live\n'],
                 ['g', '› '], ['', 'mobile app ............. '], ['', 'in testing\n'], ['g', '› '], ['', 'cloud setup ............ '], ['s', 'deploying']],
    f1='Years in software and security', f2='Services under one roof', f3='You work directly with me', f4='Certification track in progress',
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
    s3_lead='Every project follows the same four stages, so you always know where the work stands and what comes next.',
    st1_t='Understand', st1_p='Your business, your customers and what the website or application needs to achieve.',
    st2_t='Design', st2_p='Page layouts, screens and a clear plan, agreed with you before development starts.',
    st3_t='Build &amp; Test', st3_p='Development with regular previews, tested on real devices and checked for security vulnerabilities before launch.',
    st4_t='Launch &amp; Support', st4_p='Go-live on reliable cloud hosting, a handover you can manage and ongoing support.',
    s4_lead='Clear scope, a fixed price and a defined delivery date. Everything is agreed in writing after a short introductory call.',
    e1_tag='Website', e1_t='Corporate website', e1_p='A professional website for your company, from design to launch, including domain, hosting and business email setup.',
    e1_len='2 – 6 weeks', e1_rec='Live website, SEO setup and a short guide to manage it',
    e2_tag='Application', e2_t='Business application', e2_p='A web or mobile application built around how your business actually works, for your team or your customers.',
    e2_len='6 – 14 weeks', e2_rec='Working application, deployment and documentation',
    e3_tag='Cloud', e3_t='Cloud setup &amp; care', e3_p='Moving your website or systems to the cloud, or setting them up there from scratch, with backups and monitoring.',
    e3_len='1 – 4 weeks', e3_rec='Cloud setup, backups and an optional monthly care plan',
    about_t='Built to look good. Built to be secure.',
    about_lead='For the past four years I have been building software and working in cybersecurity. Today I help businesses with their whole online presence: the website customers see, the applications teams use every day and the cloud infrastructure behind them. My security background means every project is protected against common attacks from the start, not patched afterwards.',
    about_p='I work independently under my own name, which means every client works with me directly, from the first conversation to launch and beyond. I am currently deepening my cloud expertise through the AWS certification track.',
    c1='Cloud concepts, core services, pricing', c2='Reliable and scalable architecture design',
    p1_t='Security by design', p1_p='Every website and application is built with security best practices from the first line of code: encrypted connections, protected data and safe logins.',
    p2_t='Quality', p2_p='Clean design, fast pages, a clear scope and well-built code that keeps working long after launch.',
    p3_t='Accountability', p3_p='One person responsible for the work from start to finish. Nothing is passed on to subcontractors.',
    ph_msg='What would you like to build, and roughly when do you need it?',
    ch_web='Website', ch_dev='Application', ch_cloud='Cloud', ch_unsure='Not sure yet',
    footer_tag='Websites · Applications · Cloud',
)
TR.update(
    consulting='Web ve Yazılım',
    meta_title='Eray Ulusoy | Web Sitesi Tasarımı, Uygulama Geliştirme ve Bulut',
    meta_desc='Eray Ulusoy; işletmelere ve şirketlere güvenli ve profesyonel web sitesi tasarımı, web ve mobil uygulama geliştirme ve AWS bulut bilişim hizmetleri sunar.',
    og_desc='Şirketler için profesyonel web siteleri, iş uygulamaları ve bulut çözümleri.',
    hero_eyebrow='Eray Ulusoy · Web Sitesi, İş Uygulamaları ve Bulut',
    h1_a='Profesyonel web siteleri.', h1_b='<em>Güvenilir</em> uygulamalar.',
    hero_sub='İşletmeler için baştan güvenli tasarlanmış web siteleri ve uygulamalar geliştiriyor, bunları güvenilir bulut altyapısında çalıştırıyorum. Şirketiniz internette doğru görünsün, arka planda da daha verimli çalışsın.',
    brief_label='Proje özeti', brief_title='Proje özeti', brief_status='devam ediyor',
    brief_lines=[['s', 'müşteri    '], ['', 'Perakende şirketi\n'], ['s', 'kapsam     '], ['', 'Web sitesi · Sipariş uygulaması\n'], ['s', 'altyapı    '], ['', 'AWS · Cloudflare\n\n'],
                 ['g', '› '], ['', 'tasarım ................ '], ['g', 'onaylandı\n'], ['g', '› '], ['', 'web sitesi ............. '], ['g', 'yayında\n'],
                 ['g', '› '], ['', 'mobil uygulama ......... '], ['', 'testte\n'], ['g', '› '], ['', 'bulut kurulumu ......... '], ['s', 'yükleniyor']],
    f1='Yıllık yazılım ve güvenlik deneyimi', f2='Tek çatı altında üç hizmet', f3='Doğrudan benimle çalışırsınız', f4='Sertifika süreci devam ediyor',
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
    s3_lead='Her proje aynı dört aşamadan geçer; böylece işin nerede olduğunu ve sırada ne olduğunu her zaman bilirsiniz.',
    st1_t='Anlama', st1_p='İşiniz, müşterileriniz ve web sitesinin ya da uygulamanın neyi başarması gerektiği.',
    st2_t='Tasarım', st2_p='Sayfa düzenleri, ekranlar ve net bir plan; geliştirme başlamadan önce sizinle birlikte onaylanır.',
    st3_t='Geliştirme ve Test', st3_p='Düzenli ön izlemelerle geliştirme; gerçek cihazlarda test ve yayından önce güvenlik açığı kontrolü.',
    st4_t='Yayın ve Destek', st4_p='Güvenilir bulut altyapısında yayına alma, kolayca yönetebileceğiniz bir teslim ve sürekli destek.',
    s4_lead='Net kapsam, sabit fiyat ve belirli bir teslim tarihi. Her şey kısa bir tanışma görüşmesinin ardından yazılı olarak belirlenir.',
    e1_tag='Web sitesi', e1_t='Kurumsal web sitesi', e1_p='Tasarımdan yayına kadar şirketinize özel profesyonel bir web sitesi; alan adı, barındırma ve kurumsal e-posta kurulumu dahil.',
    e1_len='2 – 6 hafta', e1_rec='Yayında web sitesi, SEO kurulumu ve kısa bir kullanım rehberi',
    e2_tag='Uygulama', e2_t='İş uygulaması', e2_p='İşletmenizin gerçek çalışma şekline göre ekibiniz ya da müşterileriniz için geliştirilen bir web veya mobil uygulama.',
    e2_len='6 – 14 hafta', e2_rec='Çalışan uygulama, kurulum ve dokümantasyon',
    e3_tag='Bulut', e3_t='Bulut kurulumu ve bakımı', e3_p='Web sitenizi ya da sistemlerinizi buluta taşıma veya sıfırdan kurma; yedekleme ve izleme dahil.',
    e3_len='1 – 4 hafta', e3_rec='Bulut kurulumu, yedekleme ve isteğe bağlı aylık bakım planı',
    about_t='Hem şık hem güvenli.',
    about_lead='Son dört yıldır yazılım geliştiriyor ve siber güvenlik alanında çalışıyorum. Bugün işletmelerin internetteki varlığının tamamında yardımcı oluyorum: müşterilerin gördüğü web sitesi, ekiplerin her gün kullandığı uygulamalar ve bunların arkasındaki bulut altyapısı. Güvenlik geçmişim sayesinde her proje yaygın saldırılara karşı en baştan korunur, sonradan yamanmaz.',
    about_p='Kendi adımla bağımsız çalışıyorum; yani her müşteri ilk görüşmeden yayına ve sonrasına kadar doğrudan benimle çalışıyor. Şu anda AWS sertifika süreciyle bulut alanındaki uzmanlığımı derinleştiriyorum.',
    c1='Bulut kavramları, temel servisler, fiyatlandırma', c2='Güvenilir ve ölçeklenebilir mimari tasarımı',
    p1_t='Baştan güvenli', p1_p='Her web sitesi ve uygulama ilk satır koddan itibaren güvenlik standartlarına göre geliştirilir: şifreli bağlantılar, korunan veriler ve güvenli girişler.',
    p2_t='Kalite', p2_p='Temiz tasarım, hızlı sayfalar, net kapsam ve yayından çok sonra da sorunsuz çalışan, özenle yazılmış kod.',
    p3_t='Sorumluluk', p3_p='İşin başından sonuna kadar sorumlu tek kişi. Hiçbir iş taşerona devredilmez.',
    ph_msg='Ne yaptırmak istiyorsunuz, yaklaşık ne zaman lazım?',
    ch_web='Web sitesi', ch_dev='Uygulama', ch_cloud='Bulut', ch_unsure='Henüz emin değilim',
    footer_tag='Web Siteleri · Uygulamalar · Bulut',
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


def render(d, base, home, en_href, tr_href, ver):
    tpl = open(os.path.join(ROOT, 'template.html'), encoding='utf-8').read()
    v = dict(d)
    v['brief_lines'] = json.dumps(d['brief_lines'], ensure_ascii=False).replace('&', '&amp;').replace("'", '&#39;').replace('<', '&lt;')
    v['jsonld'] = jsonld(d)
    v.update(base=base, home=home, en_href=en_href, tr_href=tr_href, ver=ver,
             other_href=tr_href if d['lang'] == 'en' else en_href,
             en_current=' aria-current="true"' if d['lang'] == 'en' else '',
             tr_current=' aria-current="true"' if d['lang'] == 'tr' else '')

    def sub(m):
        k = m.group(1)
        val = v[k]
        if k in RAW:
            return str(val)
        # values may contain pre-escaped entities (&amp;, &#39;); escape only bare < > "
        return str(val).replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    out = re.sub(r'\{\{(\w+)\}\}', sub, tpl)
    assert '{{' not in out
    return out


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
    print('built', ver)


if __name__ == '__main__':
    build()
