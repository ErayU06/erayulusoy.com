"""Text of the legal pages: KVKK information notice and privacy policy, in Turkish and English.

build.py renders these through legal.html into:
  /privacy/  /kvkk/            (English)
  /tr/gizlilik/  /tr/kvkk/     (Turkish)

Fill in CONTROLLER before publishing. Values in [BRACKETS] are placeholders and
build.py prints a warning while any are left.
"""
import html

# Data controller (veri sorumlusu). These details appear on every legal page.
CONTROLLER = dict(
    name='Eray Ulusoy',                       # full legal name, as on ID
    trade='',                                 # registered trade name, if any (şahıs şirketi unvanı); leave '' if none
    address='[POSTA ADRESİ / POSTAL ADDRESS]',  # address for KVKK applications
    email='contact@erayulusoy.com',
    mail_host='[E-POSTA SAĞLAYICISI / EMAIL PROVIDER]',  # who hosts contact@erayulusoy.com, e.g. "Google LLC (Google Workspace, ABD)"
)
UPDATED = dict(tr='3 Kasım 2026', en='3 November 2026')

PATHS = dict(
    en=dict(privacy='/privacy/', kvkk='/kvkk/'),
    tr=dict(privacy='/tr/gizlilik/', kvkk='/tr/kvkk/'),
)


def _c():
    c = {k: html.escape(v) for k, v in CONTROLLER.items()}
    c['who'] = c['name'] + (f' ({c["trade"]})' if c['trade'] else '')
    c['mail'] = f'<a href="mailto:{c["email"]}">{c["email"]}</a>'
    return c


def placeholders_left():
    return [k for k, v in CONTROLLER.items() if '[' in v]


def pages():
    c = _c()
    P = PATHS
    return {
        # ------------------------------------------------------------------ TR · KVKK
        ('tr', 'kvkk'): dict(
            title='KVKK Aydınlatma Metni',
            meta_title='KVKK Aydınlatma Metni | Eray Ulusoy',
            meta_desc='erayulusoy.com iletişim formu ve e-posta yoluyla paylaşılan kişisel verilerin 6698 sayılı KVKK kapsamında işlenmesine ilişkin aydınlatma metni.',
            lead=f'Bu metin, 6698 sayılı Kişisel Verilerin Korunması Kanunu’nun (“KVKK”) 10. maddesi ve Aydınlatma Yükümlülüğünün Yerine Getirilmesinde Uyulacak Usul ve Esaslar Hakkında Tebliğ uyarınca, erayulusoy.com üzerinden veya e-posta ile benimle iletişime geçtiğinizde kişisel verilerinizin nasıl işlendiğini açıklar.',
            body=f'''
<h2>1. Veri sorumlusu</h2>
<p>Kişisel verileriniz, veri sorumlusu sıfatıyla <strong>{c["who"]}</strong> tarafından işlenir.</p>
<ul class="kv">
<li><span>Adres</span>{c["address"]}</li>
<li><span>E-posta</span>{c["mail"]}</li>
</ul>

<h2>2. İşlenen kişisel veriler</h2>
<ul>
<li><strong>Kimlik:</strong> ad soyad.</li>
<li><strong>İletişim:</strong> e-posta adresi; e-postayla yazarsanız e-posta imzanızda yer alan bilgiler.</li>
<li><strong>Mesleki bilgi:</strong> çalıştığınız şirketin adı (isteğe bağlı).</li>
<li><strong>Talep bilgisi:</strong> ilgilendiğiniz hizmet ve mesajınızın içeriği.</li>
<li><strong>İşlem güvenliği:</strong> IP adresi, tarayıcı bilgisi ve gönderim zamanı. Bunlar, siteyi barındıran ve formu ileten hizmet sağlayıcılar tarafından teknik olarak işlenir.</li>
</ul>
<p>Lütfen mesajınızda sağlık, din, etnik köken gibi özel nitelikli kişisel veri paylaşmayın.</p>

<h2>3. İşleme amaçları</h2>
<ul>
<li>Talebinize ve sorularınıza dönüş yapmak,</li>
<li>Teklif hazırlamak ve sözleşme öncesi görüşmeleri yürütmek,</li>
<li>Bir iş ilişkisi kurulursa sözleşmenin kurulması ve ifası,</li>
<li>Site ve formun güvenliğini sağlamak, spam ve kötüye kullanımı önlemek,</li>
<li>Hukuki yükümlülükleri yerine getirmek ve olası uyuşmazlıklarda hakları korumak.</li>
</ul>

<h2>4. Toplama yöntemi ve hukuki sebepler</h2>
<p>Verileriniz, sitedeki iletişim formu veya doğrudan gönderdiğiniz e-posta aracılığıyla elektronik ortamda, kısmen otomatik yollarla toplanır. Hukuki sebepler KVKK madde 5/2 kapsamında şunlardır:</p>
<ul>
<li><strong>(c)</strong> Bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması (teklif ve sözleşme öncesi görüşmeler),</li>
<li><strong>(f)</strong> Temel hak ve özgürlüklerinize zarar vermemek kaydıyla meşru menfaatim (talebinize yanıt vermek, site güvenliği ve spam önleme),</li>
<li><strong>(ç)</strong> Hukuki yükümlülüğümü yerine getirebilmem için zorunlu olması,</li>
<li><strong>(e)</strong> Bir hakkın tesisi, kullanılması veya korunması için zorunlu olması.</li>
</ul>

<h2>5. Aktarım ve yurt dışına aktarım</h2>
<p>Verileriniz satılmaz ve pazarlama amacıyla kimseyle paylaşılmaz. Yalnızca yukarıdaki amaçlar için gerekli olduğu ölçüde şu hizmet sağlayıcılara aktarılır:</p>
<ul>
<li><strong>Formspree, Inc. (ABD):</strong> iletişim formundaki bilgilerin bana e-posta ile iletilmesi.</li>
<li><strong>Cloudflare, Inc. (ABD, küresel sunucu ağı):</strong> sitenin barındırılması ve saldırılara karşı korunması.</li>
<li><strong>{c["mail_host"]}:</strong> {c["email"]} adresine gelen e-postaların barındırılması.</li>
</ul>
<p>Bu hizmet sağlayıcıların sunucuları Türkiye dışında bulunduğundan, verileriniz KVKK madde 9 kapsamında yurt dışına aktarılır. Formdaki bilgilerin Formspree aracılığıyla aktarılması, form gönderilmeden önce ayrıca verdiğiniz <strong>açık rızaya</strong> (madde 9/6-a) dayanır. Bu ülkeler için Kişisel Verileri Koruma Kurulu’nun verdiği bir yeterlilik kararı bulunmamaktadır; bu nedenle verileriniz Türkiye’deki ile aynı düzeyde korunmayabilir ve bulunduğu ülkenin makamlarınca erişilebilir olabilir. Açık rıza vermek istemezseniz formu kullanmadan doğrudan {c["mail"]} adresine yazabilirsiniz.</p>
<p>Ayrıca, kanunen yetkili kamu kurum ve kuruluşlarına yalnızca hukuki bir yükümlülük olduğunda ve gerekli ölçüde aktarım yapılabilir.</p>

<h2>6. Saklama süresi</h2>
<p>Verileriniz, talebiniz sonuçlanana kadar ve sonrasında en fazla <strong>2 yıl</strong> saklanır. Bir iş ilişkisi kurulursa, sözleşme ve fatura kayıtları ilgili mevzuatın (ör. Türk Ticaret Kanunu, Vergi Usul Kanunu) öngördüğü süre boyunca saklanır. Formspree hesabında tutulan form kopyaları en geç 6 ayda bir silinir. Süresi dolan veriler silinir veya anonim hâle getirilir.</p>

<h2>7. KVKK madde 11 kapsamındaki haklarınız</h2>
<p>Veri sorumlusuna başvurarak:</p>
<ul>
<li>Kişisel verilerinizin işlenip işlenmediğini öğrenme,</li>
<li>İşlenmişse buna ilişkin bilgi talep etme,</li>
<li>İşlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme,</li>
<li>Yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme,</li>
<li>Eksik veya yanlış işlenmişse düzeltilmesini isteme,</li>
<li>KVKK madde 7’de öngörülen şartlar çerçevesinde silinmesini veya yok edilmesini isteme,</li>
<li>Düzeltme, silme ve yok etme işlemlerinin, verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme,</li>
<li>İşlenen verilerin münhasıran otomatik sistemler vasıtasıyla analiz edilmesi suretiyle aleyhinize bir sonucun ortaya çıkmasına itiraz etme,</li>
<li>Kanuna aykırı işleme sebebiyle zarara uğramanız hâlinde zararın giderilmesini talep etme</li>
</ul>
<p>haklarına sahipsiniz. Açık rızanızı dilediğiniz zaman geri alabilirsiniz; bu, geri alma öncesindeki işlemlerin hukuka uygunluğunu etkilemez.</p>

<h2>8. Başvuru</h2>
<p>Haklarınıza ilişkin taleplerinizi, Veri Sorumlusuna Başvuru Usul ve Esasları Hakkında Tebliğ’e uygun olarak; yukarıdaki adrese yazılı olarak, kayıtlı elektronik posta (KEP) adresi, güvenli elektronik imza veya mobil imza ile ya da daha önce bana bildirdiğiniz ve sistemimde kayıtlı e-posta adresinizden {c["mail"]} adresine iletebilirsiniz. Başvurunuzda adınızı soyadınızı, T.C. kimlik numaranızı (yabancılar için uyruk ve pasaport/kimlik numarası), tebligat adresinizi, varsa e-posta adresinizi ve talebinizi belirtmeniz gerekir.</p>
<p>Talebiniz en geç <strong>30 gün</strong> içinde ücretsiz olarak sonuçlandırılır; işlemin ayrıca bir maliyet gerektirmesi hâlinde Kurul’un belirlediği tarifedeki ücret alınabilir. Başvurunuzun reddedilmesi, cevabı yetersiz bulmanız veya süresinde cevap verilmemesi hâlinde Kişisel Verileri Koruma Kurulu’na şikâyette bulunabilirsiniz.</p>

<p class="see">Sitenin genel veri uygulamaları için <a href="{P["tr"]["privacy"]}">Gizlilik Politikası</a>’na bakabilirsiniz.</p>
''',
        ),
        # ------------------------------------------------------------------ TR · Gizlilik
        ('tr', 'privacy'): dict(
            title='Gizlilik Politikası',
            meta_title='Gizlilik Politikası | Eray Ulusoy',
            meta_desc='erayulusoy.com gizlilik politikası: çerez ve analitik kullanılmaz, iletişim formu verileri yalnızca talebinize dönüş için işlenir.',
            lead='Bu site mümkün olan en az veriyle çalışacak şekilde tasarlandı. Çerez, reklam veya ziyaretçi takibi yoktur; üçüncü taraf script yüklenmez.',
            body=f'''
<h2>Kısaca</h2>
<ul>
<li>Çerez, analitik, reklam ya da sosyal medya takip kodu kullanılmaz.</li>
<li>Yazı tipleri dahil tüm dosyalar bu siteden yüklenir; ziyaretiniz Google Fonts gibi üçüncü taraflara bildirilmez.</li>
<li>Yalnızca iletişim formunu doldurursanız veya e-posta gönderirseniz verdiğiniz bilgiler işlenir; ayrıntılar <a href="{P["tr"]["kvkk"]}">KVKK Aydınlatma Metni</a>’ndedir.</li>
</ul>

<h2>Veri sorumlusu</h2>
<p><strong>{c["who"]}</strong>, {c["address"]} · {c["mail"]}</p>

<h2>Siteyi ziyaret ettiğinizde</h2>
<p>Site, Cloudflare, Inc. (ABD) altyapısında barındırılır. Sayfaları size ulaştırmak ve siteyi saldırılara karşı korumak için Cloudflare, IP adresiniz, tarayıcı bilgisi ve istek zamanı gibi teknik verileri kısa süreli olarak işler. Bu kayıtlar bana kişisel bir ziyaretçi profili olarak sunulmaz ve tarafımdan takip amacıyla kullanılmaz.</p>
<p>Dil tercihiniz (EN / TR), siz dil değiştirdiğinizde yalnızca kendi tarayıcınızın yerel depolamasında (localStorage) saklanır ve hiçbir sunucuya gönderilmez. Tarayıcı ayarlarınızdan dilediğiniz zaman silebilirsiniz.</p>

<h2>İletişim formu ve e-posta</h2>
<p>Formdaki ad, e-posta, şirket, hizmet ve mesaj bilgileri Formspree, Inc. (ABD) aracılığıyla bana e-posta olarak iletilir ve yalnızca talebinize dönüş yapmak için kullanılır. Form, gönderilmeden önce yurt dışına aktarım için açık rızanızı ister; istemezseniz doğrudan {c["mail"]} adresine yazabilirsiniz. Saklama süreleri, aktarımlar ve haklarınız <a href="{P["tr"]["kvkk"]}">KVKK Aydınlatma Metni</a>’nde açıklanmıştır.</p>

<h2>Dış bağlantılar</h2>
<p>LinkedIn gibi başka sitelere verilen bağlantılara tıkladığınızda o sitenin kendi gizlilik politikası geçerli olur.</p>

<h2>Avrupa Birliği’nden ziyaretçiler</h2>
<p>AB veya AEA’da bulunuyorsanız Genel Veri Koruma Tüzüğü (GDPR) kapsamındaki haklarınız da saklıdır. Form verileri; talebinize yanıt vermek ve sözleşme öncesi adımlar (GDPR m.6/1-b), meşru menfaat (m.6/1-f) ve yurt dışı aktarım için verdiğiniz rıza (m.49/1-a) temelinde işlenir. Bulunduğunuz ülkedeki veri koruma otoritesine şikâyette bulunabilirsiniz.</p>

<h2>Güvenlik</h2>
<p>Site yalnızca şifreli bağlantı (HTTPS) üzerinden sunulur ve sıkı güvenlik başlıklarıyla korunur. Hiçbir aktarım yöntemi tamamen risksiz değildir; lütfen formda hassas bilgi paylaşmayın.</p>

<h2>Değişiklikler</h2>
<p>Bu politika gerektiğinde güncellenir; güncel sürüm her zaman bu sayfadadır ve son güncelleme tarihi aşağıda yer alır.</p>

<h2>İletişim</h2>
<p>Gizlilikle ilgili her soru için: {c["mail"]}</p>
''',
        ),
        # ------------------------------------------------------------------ EN · KVKK
        ('en', 'kvkk'): dict(
            title='KVKK Information Notice',
            meta_title='KVKK Information Notice | Eray Ulusoy',
            meta_desc='Information notice under the Turkish Personal Data Protection Law (KVKK) for personal data shared through the erayulusoy.com contact form or by email.',
            lead=f'This notice explains, under Article 10 of the Turkish Personal Data Protection Law No. 6698 (“KVKK”), how your personal data is processed when you contact me through erayulusoy.com or by email. It is a translation; if it differs from the <a href="{P["tr"]["kvkk"]}">Turkish version</a>, the Turkish version prevails.',
            body=f'''
<h2>1. Data controller</h2>
<p>Your personal data is processed by <strong>{c["who"]}</strong> as data controller.</p>
<ul class="kv">
<li><span>Address</span>{c["address"]}</li>
<li><span>Email</span>{c["mail"]}</li>
</ul>

<h2>2. Personal data processed</h2>
<ul>
<li><strong>Identity:</strong> full name.</li>
<li><strong>Contact:</strong> email address; if you write by email, anything in your email signature.</li>
<li><strong>Professional:</strong> your company name (optional).</li>
<li><strong>Enquiry:</strong> the service you are interested in and the content of your message.</li>
<li><strong>Transaction security:</strong> IP address, browser details and time of sending, processed technically by the providers that host the site and deliver the form.</li>
</ul>
<p>Please do not include special categories of data (such as health, religion or ethnic origin) in your message.</p>

<h2>3. Purposes</h2>
<ul>
<li>Replying to your enquiry and questions,</li>
<li>Preparing a proposal and holding pre-contract discussions,</li>
<li>Entering into and performing a contract if we start working together,</li>
<li>Keeping the site and form secure and preventing spam and abuse,</li>
<li>Meeting legal obligations and protecting rights in any dispute.</li>
</ul>

<h2>4. How data is collected and legal grounds</h2>
<p>Data is collected electronically, partly by automated means, through the contact form on this site or the emails you send. The legal grounds under KVKK Article 5(2) are:</p>
<ul>
<li><strong>(c)</strong> processing is directly related to entering into or performing a contract (proposals and pre-contract discussions),</li>
<li><strong>(f)</strong> my legitimate interest, provided it does not harm your fundamental rights and freedoms (answering you, site security, spam prevention),</li>
<li><strong>(ç)</strong> it is necessary to meet a legal obligation,</li>
<li><strong>(e)</strong> it is necessary to establish, exercise or protect a right.</li>
</ul>

<h2>5. Recipients and transfers abroad</h2>
<p>Your data is never sold or shared for marketing. It is passed only to these service providers, and only as far as the purposes above require:</p>
<ul>
<li><strong>Formspree, Inc. (USA):</strong> delivers the contact form to me by email.</li>
<li><strong>Cloudflare, Inc. (USA, global network):</strong> hosts the site and protects it from attacks.</li>
<li><strong>{c["mail_host"]}:</strong> hosts the mailbox for {c["email"]}.</li>
</ul>
<p>Because these providers’ servers are outside Turkey, your data is transferred abroad under KVKK Article 9. Sending the form through Formspree relies on the <strong>explicit consent</strong> (Article 9(6)(a)) you give separately before the form is sent. The Turkish Personal Data Protection Board has not issued an adequacy decision for these countries, so your data may not be protected to the same standard as in Turkey and may be accessible to authorities there. If you would rather not consent, you can skip the form and write directly to {c["mail"]}.</p>
<p>Data may also be disclosed to authorised public bodies, only where the law requires it and only as far as necessary.</p>

<h2>6. Retention</h2>
<p>Your data is kept until your enquiry is concluded and for at most <strong>2 years</strong> after that. If we work together, contract and invoice records are kept for the periods set by Turkish law (for example the Commercial Code and the Tax Procedure Law). Copies held in the Formspree account are deleted at least every 6 months. Data past its retention period is deleted or anonymised.</p>

<h2>7. Your rights under KVKK Article 11</h2>
<p>You may apply to the data controller to:</p>
<ul>
<li>learn whether your personal data is processed,</li>
<li>request information about the processing,</li>
<li>learn the purpose of processing and whether data is used accordingly,</li>
<li>know the third parties in Turkey or abroad to whom data is transferred,</li>
<li>request correction of incomplete or inaccurate data,</li>
<li>request deletion or destruction under the conditions in KVKK Article 7,</li>
<li>request that third parties who received the data are notified of any correction, deletion or destruction,</li>
<li>object to a result against you arising solely from automated analysis,</li>
<li>claim compensation for damage caused by unlawful processing.</li>
</ul>
<p>You can withdraw your explicit consent at any time; this does not affect processing carried out before withdrawal.</p>

<h2>8. How to apply</h2>
<p>Send your request, in line with the Communiqué on the Procedures and Principles of Application to the Data Controller, in writing to the address above, by registered electronic mail (KEP), secure electronic or mobile signature, or by email to {c["mail"]} from an email address you have previously given me. Please include your full name, Turkish ID number (or nationality and passport/ID number for foreign nationals), postal address, email address if any, and your request.</p>
<p>Requests are answered free of charge within <strong>30 days</strong>; if the request involves an additional cost, the fee set by the Board may be charged. If your request is refused, you find the answer insufficient, or it is not answered in time, you may complain to the Turkish Personal Data Protection Board.</p>

<p class="see">For how the site handles data in general, see the <a href="{P["en"]["privacy"]}">Privacy Policy</a>.</p>
''',
        ),
        # ------------------------------------------------------------------ EN · Privacy
        ('en', 'privacy'): dict(
            title='Privacy Policy',
            meta_title='Privacy Policy | Eray Ulusoy',
            meta_desc='Privacy policy for erayulusoy.com: no cookies or analytics; contact form details are used only to reply to your enquiry.',
            lead='This site is built to work with as little data as possible. There are no cookies, ads or visitor tracking, and no third-party scripts are loaded.',
            body=f'''
<h2>In short</h2>
<ul>
<li>No cookies, analytics, advertising or social media tracking code.</li>
<li>Everything, including fonts, is served from this site, so your visit is not reported to third parties such as Google Fonts.</li>
<li>Your details are processed only if you fill in the contact form or send an email; see the <a href="{P["en"]["kvkk"]}">KVKK Information Notice</a> for the details.</li>
</ul>

<h2>Data controller</h2>
<p><strong>{c["who"]}</strong>, {c["address"]} · {c["mail"]}</p>

<h2>When you visit the site</h2>
<p>The site is hosted on the infrastructure of Cloudflare, Inc. (USA). To deliver pages to you and protect the site from attacks, Cloudflare briefly processes technical data such as your IP address, browser details and the time of the request. These records are not given to me as a visitor profile and I do not use them to track anyone.</p>
<p>When you switch language (EN / TR), your choice is saved only in your own browser’s local storage and is never sent to a server. You can clear it at any time in your browser settings.</p>

<h2>Contact form and email</h2>
<p>The name, email, company, service and message you enter in the form are delivered to me by email through Formspree, Inc. (USA) and used only to reply to your enquiry. Before sending, the form asks for your consent to this transfer abroad; if you would rather not give it, write directly to {c["mail"]}. Retention, recipients and your rights are explained in the <a href="{P["en"]["kvkk"]}">KVKK Information Notice</a>.</p>

<h2>Links to other sites</h2>
<p>When you follow a link to another site, such as LinkedIn, that site’s own privacy policy applies.</p>

<h2>Visitors from the European Union</h2>
<p>If you are in the EU or EEA, your rights under the General Data Protection Regulation (GDPR) also apply. Form data is processed to answer you and take pre-contract steps (GDPR Art. 6(1)(b)), on the basis of legitimate interest (Art. 6(1)(f)), and transferred abroad on the basis of your consent (Art. 49(1)(a)). You may complain to the data protection authority in your country.</p>

<h2>Security</h2>
<p>The site is served only over encrypted connections (HTTPS) and protected by strict security headers. No method of transmission is entirely without risk, so please do not send sensitive information through the form.</p>

<h2>Changes</h2>
<p>This policy is updated when needed. The current version is always on this page, with the date of the last update below.</p>

<h2>Contact</h2>
<p>For any privacy question: {c["mail"]}</p>
''',
        ),
    }
