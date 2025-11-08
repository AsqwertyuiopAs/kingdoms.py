from flask import Flask, render_template_string, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

BASE_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Discord Bot Hizmetleri{% endblock %}</title>
    <style>
        :root {
            --primary: #5865F2;
            --dark: #1e1f22;
            --darker: #111214;
            --light: #f6f6f6;
            --gray: #4e5058;
            --success: #3ba55c;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: var(--darker);
            color: var(--light);
            line-height: 1.6;
        }
        
        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        header {
            background-color: var(--dark);
            padding: 20px 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: var(--light);
            text-decoration: none;
        }
        
        .logo span {
            color: var(--primary);
        }
        
        .nav-links {
            display: flex;
            list-style: none;
        }
        
        .nav-links li {
            margin-left: 30px;
        }
        
        .nav-links a {
            color: var(--light);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: var(--primary);
        }
        
        .hero {
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1633265486064-086b86e124fe?ixlib=rb-4.0.3');
            background-size: cover;
            background-position: center;
            height: 80vh;
            display: flex;
            align-items: center;
            text-align: center;
        }
        
        .hero-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 20px;
            background: linear-gradient(90deg, var(--primary), #9b59b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero p {
            font-size: 1.2rem;
            margin-bottom: 30px;
            color: #b9bbbe;
        }
        
        .btn {
            display: inline-block;
            background-color: var(--primary);
            color: white;
            padding: 12px 30px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s, transform 0.3s;
            margin: 5px;
        }
        
        .btn:hover {
            background-color: #4752c4;
            transform: translateY(-3px);
        }
        
        .btn-secondary {
            background-color: transparent;
            border: 2px solid var(--primary);
        }
        
        .services {
            padding: 80px 0;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .section-title h2 {
            font-size: 2.5rem;
            margin-bottom: 15px;
            color: var(--light);
        }
        
        .section-title p {
            color: var(--gray);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        
        .service-card {
            background-color: var(--dark);
            border-radius: 10px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        }
        
        .service-img {
            height: 200px;
            background: linear-gradient(135deg, var(--primary), #9b59b6);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
        }
        
        .service-content {
            padding: 25px;
        }
        
        .service-content h3 {
            font-size: 1.5rem;
            margin-bottom: 15px;
            color: var(--light);
        }
        
        .service-content p {
            color: var(--gray);
            margin-bottom: 20px;
        }
        
        .price {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 15px;
        }
        
        .features {
            padding: 80px 0;
            background-color: var(--dark);
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }
        
        .feature-card {
            text-align: center;
            padding: 30px 20px;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: var(--primary);
        }
        
        .feature-card h3 {
            font-size: 1.3rem;
            margin-bottom: 15px;
            color: var(--light);
        }
        
        .feature-card p {
            color: var(--gray);
        }
        
        footer {
            background-color: var(--dark);
            padding: 50px 0 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 40px;
            margin-bottom: 40px;
        }
        
        .footer-column h3 {
            font-size: 1.2rem;
            margin-bottom: 20px;
            color: var(--light);
        }
        
        .footer-links {
            list-style: none;
        }
        
        .footer-links li {
            margin-bottom: 10px;
        }
        
        .footer-links a {
            color: var(--gray);
            text-decoration: none;
            transition: color 0.3s;
        }
        
        .footer-links a:hover {
            color: var(--primary);
        }
        
        .copyright {
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--gray);
            font-size: 0.9rem;
        }
        
        .service-detail {
            padding: 80px 0;
        }
        
        .service-header {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .service-header h1 {
            font-size: 2.5rem;
            margin-bottom: 15px;
            color: var(--light);
        }
        
        .service-price {
            font-size: 1.8rem;
            color: var(--primary);
            font-weight: bold;
            margin-bottom: 20px;
        }
        
        .service-description {
            max-width: 800px;
            margin: 0 auto 40px;
            color: var(--gray);
            font-size: 1.1rem;
            line-height: 1.8;
        }
        
        .features-list {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .features-list h2 {
            font-size: 1.8rem;
            margin-bottom: 20px;
            color: var(--light);
        }
        
        .features-list ul {
            list-style: none;
        }
        
        .features-list li {
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--gray);
            position: relative;
            padding-left: 30px;
        }
        
        .features-list li:before {
            content: "✓";
            color: var(--success);
            position: absolute;
            left: 0;
            font-weight: bold;
        }
        
        .cta-section {
            text-align: center;
            margin-top: 50px;
        }
        
        .contact {
            padding: 80px 0;
        }
        
        .contact-form {
            max-width: 600px;
            margin: 0 auto;
            background-color: var(--dark);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: var(--light);
        }
        
        .form-control {
            width: 100%;
            padding: 12px 15px;
            background-color: var(--darker);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            color: var(--light);
            font-size: 1rem;
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--primary);
        }
        
        textarea.form-control {
            min-height: 150px;
            resize: vertical;
        }
        
        .flash-messages {
            max-width: 600px;
            margin: 20px auto;
        }
        
        .flash-success {
            background-color: var(--success);
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
            }
            
            .nav-links {
                margin-top: 20px;
            }
            
            .nav-links li {
                margin: 0 15px;
            }
            
            .hero h1 {
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <nav class="navbar">
                <a href="/" class="logo">Bot<span>Land</span></a>
                <ul class="nav-links">
                    <li><a href="/">Ana Sayfa</a></li>
                    <li><a href="/hizmetler">Hizmetler</a></li>
                    <li><a href="/iletisim">İletişim</a></li>
                    <li><a href="https://discord.gg/botland" target="_blank">Discord</a></li>
                </ul>
            </nav>
        </div>
    </header>

    {% block content %}{% endblock %}

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-column">
                    <h3>BotLand</h3>
                    <p>Profesyonel Discord bot çözümleri sunan lider platform.</p>
                </div>
                <div class="footer-column">
                    <h3>Hızlı Bağlantılar</h3>
                    <ul class="footer-links">
                        <li><a href="/">Ana Sayfa</a></li>
                        <li><a href="/hizmetler">Hizmetler</a></li>
                        <li><a href="/iletisim">İletişim</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Hizmetler</h3>
                    <ul class="footer-links">
                        <li><a href="/hizmet/log-botu-v2">Log Botu V2</a></li>
                        <li><a href="/hizmet/guard-botu-v2">Guard Botu V2</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>İletişim</h3>
                    <ul class="footer-links">
                        <li><a href="https://discord.gg/botland" target="_blank">Discord Sunucumuz</a></li>
                        <li><a href="/iletisim">İletişim Formu</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                <p>&copy; 2024 BotLand. Tüm hakları saklıdır.</p>
            </div>
        </div>
    </footer>
</body>
</html>
'''

INDEX_CONTENT = '''
{% block content %}
<section class="hero">
    <div class="container">
        <div class="hero-content">
            <h1>Profesyonel Discord Bot Çözümleri</h1>
            <p>Sunucunuz için gelişmiş güvenlik ve yönetim botları. 7/24 destek ve en kaliteli hizmet garantisi.</p>
            <a href="/hizmetler" class="btn">Hizmetleri Görüntüle</a>
            <a href="https://discord.gg/botland" class="btn btn-secondary" target="_blank">Discord Sunucumuza Katıl</a>
        </div>
    </div>
</section>

<section class="services">
    <div class="container">
        <div class="section-title">
            <h2>Premium Hizmetlerimiz</h2>
            <p>Sunucunuzun ihtiyaçlarına özel geliştirilmiş profesyonel bot çözümleri</p>
        </div>
        <div class="services-grid">
            <div class="service-card">
                <div class="service-img">📊</div>
                <div class="service-content">
                    <h3>Log Botu V2</h3>
                    <p>Sunucunuzdaki tüm aktiviteleri detaylı bir şekilde kaydeden gelişmiş log botu.</p>
                    <div class="price">200TL</div>
                    <a href="/hizmet/log-botu-v2" class="btn">Detaylı Bilgi</a>
                </div>
            </div>
            <div class="service-card">
                <div class="service-img">🛡️</div>
                <div class="service-content">
                    <h3>Guard Botu V2</h3>
                    <p>Sunucunuzu kötü niyetli saldırılara karşı koruyan gelişmiş güvenlik botu.</p>
                    <div class="price">200TL</div>
                    <a href="/hizmet/guard-botu-v2" class="btn">Detaylı Bilgi</a>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="features">
    <div class="container">
        <div class="section-title">
            <h2>Neden Bizi Seçmelisiniz?</h2>
            <p>Kalite ve güvenilirliğin adresi</p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Hızlı Kurulum</h3>
                <p>5 dakikadan kısa sürede botunuzu sunucunuza entegre edin</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🛡️</div>
                <h3>7/24 Destek</h3>
                <p>Profesyonel destek ekibimiz her zaman yanınızda</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔧</div>
                <h3>Sürekli Güncelleme</h3>
                <p>Botlarımız düzenli olarak güncellenir ve geliştirilir</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💎</div>
                <h3>Premium Kalite</h3>
                <p>En kaliteli kod ve en iyi performans garantisi</p>
            </div>
        </div>
    </div>
</section>
{% endblock %}
'''

SERVICES_CONTENT = '''
{% block content %}
<section class="services" style="padding-top: 120px;">
    <div class="container">
        <div class="section-title">
            <h2>Tüm Hizmetlerimiz</h2>
            <p>İhtiyacınıza en uygun botu seçin ve sunucunuzu güvenle yönetin</p>
        </div>
        <div class="services-grid">
            <div class="service-card">
                <div class="service-img">📊</div>
                <div class="service-content">
                    <h3>Log Botu V2</h3>
                    <p>Sunucunuzdaki tüm aktiviteleri detaylı bir şekilde kaydeden gelişmiş log botu. Üyelerin giriş-çıkışlarını, mesaj silmelerini, kanal ve rol değişikliklerini kaydeder.</p>
                    <div class="price">200TL</div>
                    <a href="/hizmet/log-botu-v2" class="btn">Detaylı Bilgi</a>
                </div>
            </div>
            <div class="service-card">
                <div class="service-img">🛡️</div>
                <div class="service-content">
                    <h3>Guard Botu V2</h3>
                    <p>Sunucunuzu kötü niyetli saldırılara karşı koruyan gelişmiş güvenlik botu. Otomatik anti-raid, anti-spam koruması ve çok daha fazlası.</p>
                    <div class="price">200TL</div>
                    <a href="/hizmet/guard-botu-v2" class="btn">Detaylı Bilgi</a>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
'''

SERVICE_DETAIL_CONTENT = '''
{% block title %}{{ hizmet.ad }} - BotLand{% endblock %}
{% block content %}
<section class="service-detail">
    <div class="container">
        <div class="service-header">
            <h1>{{ hizmet.ad }}</h1>
            <div class="service-price">{{ hizmet.fiyat }}</div>
            <p class="service-description">{{ hizmet.aciklama }}</p>
            <a href="/iletisim" class="btn">Hemen Sipariş Ver</a>
            <a href="https://discord.gg/botland" class="btn btn-secondary" target="_blank">Discord'da Sor</a>
        </div>
        
        <div class="features-list">
            <h2>Özellikler</h2>
            <ul>
                {% for ozellik in hizmet.ozellikler %}
                <li>{{ ozellik }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="cta-section">
            <h2>Hemen Başlayın!</h2>
            <p>Bu premium botu satın almak için hemen iletişime geçin</p>
            <a href="/iletisim" class="btn">İletişime Geç</a>
        </div>
    </div>
</section>
{% endblock %}
'''

CONTACT_CONTENT = '''
{% block content %}
<section class="contact">
    <div class="container">
        <div class="section-title">
            <h2>İletişim</h2>
            <p>Bize ulaşın, en kısa sürede dönüş yapalım</p>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="flash-{{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        <div class="contact-form">
            <form method="POST" action="/iletisim">
                <div class="form-group">
                    <label for="isim">Adınız</label>
                    <input type="text" class="form-control" id="isim" name="isim" required>
                </div>
                <div class="form-group">
                    <label for="email">E-posta Adresiniz</label>
                    <input type="email" class="form-control" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="mesaj">Mesajınız</label>
                    <textarea class="form-control" id="mesaj" name="mesaj" required></textarea>
                </div>
                <button type="submit" class="btn">Gönder</button>
            </form>
        </div>
        
        <div style="text-align: center; margin-top: 40px;">
            <h3>Diğer İletişim Yolları</h3>
            <p>Discord sunucumuza katılarak doğrudan destek alabilirsiniz:</p>
            <a href="https://discord.gg/botland" class="btn" target="_blank">Discord Sunucumuza Katıl</a>
        </div>
    </div>
</section>
{% endblock %}
'''

# Route definitions
@app.route('/')
def index():
    return render_template_string(BASE_HTML + INDEX_CONTENT)

@app.route('/hizmetler')
def hizmetler():
    return render_template_string(BASE_HTML + SERVICES_CONTENT)

@app.route('/iletisim')
def iletisim():
    return render_template_string(BASE_HTML + CONTACT_CONTENT)

@app.route('/hizmet/<hizmet_adi>')
def hizmet_detay(hizmet_adi):
    hizmetler = {
        'log-botu-v2': {
            'ad': 'Log Botu V2',
            'fiyat': '200TL',
            'aciklama': 'Sunucunuzdaki tüm aktiviteleri detaylı bir şekilde kaydeden gelişmiş log botu. Üyelerin giriş-çıkışlarını, mesaj silmelerini, kanal ve rol değişikliklerini, sunucu güncellemelerini ve daha birçok olayı kaydeder. Web paneli ile kolay yönetim imkanı sunar.',
            'ozellikler': [
                'Detaylı üye giriş-çıkış kayıtları',
                'Mesaj silme/düzenleme logları',
                'Kanal ve rol değişiklikleri takibi',
                'Sunucu ayar değişiklikleri kaydı',
                'Özel kanal ve rol logları',
                'Esaslı filtreleme seçenekleri',
                'Web paneli ile kolay yönetim',
                '7/24 aktif kayıt sistemi',
                'Özel raporlama özellikleri'
            ]
        },
        'guard-botu-v2': {
            'ad': 'Guard Botu V2',
            'fiyat': '200TL',
            'aciklama': 'Sunucunuzu kötü niyetli saldırılara karşı koruyan gelişmiş güvenlik botu. Otomatik anti-raid, anti-spam, anti-nuke koruması ve çok daha fazlası. Sunucunuzu 7/24 güvende tutar.',
            'ozellikler': [
                'Gelişmiş anti-raid koruması',
                'Akıllı anti-spam filtresi',
                'Anti-nuke (sunucu sabotajı) önleme',
                'Otomatik şüpheli hesap tespiti',
                'Beyaz liste/karaliste yönetimi',
                '7/24 aktif koruma modu',
                'Anlık bildirim sistemi',
                'Özel güvenlik ayarları',
                'Backup ve restore özellikleri'
            ]
        }
    }
    
    if hizmet_adi in hizmetler:
        return render_template_string(BASE_HTML + SERVICE_DETAIL_CONTENT, hizmet=hizmetler[hizmet_adi])
    else:
        return redirect(url_for('hizmetler'))

@app.route('/iletisim', methods=['POST'])
def iletisim_formu():
    isim = request.form.get('isim')
    email = request.form.get('email')
    mesaj = request.form.get('mesaj')
    
    flash('Mesajınız başarıyla gönderildi! En kısa sürede sizinle iletişime geçeceğiz.', 'success')
    return redirect(url_for('iletisim'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
