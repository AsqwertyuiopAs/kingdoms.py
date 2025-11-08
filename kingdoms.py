from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'botland_secret_key_2024'
app.config['DATABASE'] = 'botland.db'

def init_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    # Kullanıcılar tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Siparişler tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service_type TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            admin_response TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Admin kullanıcısını oluştur
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not c.fetchone():
        hashed_password = generate_password_hash('botland1985')
        c.execute('INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)',
                 ('admin', 'admin@botland.com', hashed_password, True))
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Ana template base HTML
BASE_HTML = '''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Bot Hizmetleri</title>
    <style>
        :root {
            --primary: #5865F2;
            --dark: #1e1f22;
            --darker: #111214;
            --light: #f6f6f6;
            --gray: #4e5058;
            --success: #3ba55c;
            --warning: #faa81a;
            --danger: #ed4245;
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
            align-items: center;
        }
        
        .nav-links li {
            margin-left: 20px;
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
        
        .user-menu {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .user-info {
            color: var(--gray);
            font-size: 0.9rem;
        }
        
        .btn {
            display: inline-block;
            background-color: var(--primary);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s, transform 0.3s;
            margin: 5px;
            border: none;
            cursor: pointer;
            font-size: 14px;
        }
        
        .btn:hover {
            background-color: #4752c4;
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background-color: transparent;
            border: 2px solid var(--primary);
        }
        
        .btn-success {
            background-color: var(--success);
        }
        
        .btn-warning {
            background-color: var(--warning);
        }
        
        .btn-danger {
            background-color: var(--danger);
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
        
        .flash-error {
            background-color: var(--danger);
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .auth-forms {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 0;
        }
        
        .auth-form {
            background-color: var(--dark);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .auth-form h2 {
            margin-bottom: 20px;
            color: var(--light);
            text-align: center;
        }
        
        .admin-panel {
            padding: 40px 0;
        }
        
        .orders-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: var(--dark);
            border-radius: 10px;
            overflow: hidden;
        }
        
        .orders-table th,
        .orders-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .orders-table th {
            background-color: var(--primary);
            color: white;
        }
        
        .status-pending {
            color: var(--warning);
            font-weight: bold;
        }
        
        .status-completed {
            color: var(--success);
            font-weight: bold;
        }
        
        .status-cancelled {
            color: var(--danger);
            font-weight: bold;
        }
        
        .user-orders {
            padding: 40px 0;
        }
        
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
            }
            
            .nav-links {
                margin-top: 20px;
                flex-direction: column;
                gap: 10px;
            }
            
            .nav-links li {
                margin: 0;
            }
            
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .auth-forms {
                grid-template-columns: 1fr;
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
                    {% if 'user_id' in session %}
                        <li class="user-menu">
                            <span class="user-info">Hoş geldin, {{ session.username }}</span>
                            <a href="/siparislerim" class="btn">Siparişlerim</a>
                            {% if session.get('is_admin') %}
                                <a href="/admin" class="btn btn-warning">Admin Panel</a>
                            {% endif %}
                            <a href="/cikis" class="btn btn-secondary">Çıkış</a>
                        </li>
                    {% else %}
                        <li class="user-menu">
                            <a href="/giris" class="btn btn-secondary">Giriş Yap</a>
                            <a href="/kayit" class="btn">Kayıt Ol</a>
                        </li>
                    {% endif %}
                </ul>
            </nav>
        </div>
    </header>

    <main>
        {{ content|safe }}
    </main>

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
</html>'''

# Sayfa içerikleri
INDEX_CONTENT = '''
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
'''

SERVICES_CONTENT = '''
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
'''

CONTACT_CONTENT = '''
<section class="contact">
    <div class="container">
        <div class="section-title">
            <h2>İletişim</h2>
            <p>Bize ulaşın, en kısa sürede dönüş yapalım</p>
        </div>
        
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
'''

# Route definitions
@app.route('/')
def index():
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', INDEX_CONTENT))

@app.route('/hizmetler')
def hizmetler():
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', SERVICES_CONTENT))

@app.route('/iletisim')
def iletisim():
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', CONTACT_CONTENT))

@app.route('/kayit')
def kayit():
    kayit_content = '''
    <section class="contact">
        <div class="container">
            <div class="auth-forms">
                <div class="auth-form">
                    <h2>Kayıt Ol</h2>
                    <form method="POST" action="/kayit">
                        <div class="form-group">
                            <label for="username">Kullanıcı Adı</label>
                            <input type="text" class="form-control" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="email">E-posta</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Şifre</label>
                            <input type="password" class="form-control" id="password" name="password" required>
                        </div>
                        <button type="submit" class="btn">Kayıt Ol</button>
                    </form>
                </div>
                <div class="auth-form">
                    <h2>Zaten Hesabınız Var mı?</h2>
                    <p>Hesabınız varsa giriş yaparak sipariş verebilir ve siparişlerinizi takip edebilirsiniz.</p>
                    <a href="/giris" class="btn btn-secondary">Giriş Yap</a>
                </div>
            </div>
        </div>
    </section>
    '''
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', kayit_content))

@app.route('/kayit', methods=['POST'])
def kayit_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = get_db_connection()
    
    # Kullanıcı adı veya email zaten var mı kontrol et
    existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', 
                               (username, email)).fetchone()
    
    if existing_user:
        conn.close()
        flash_content = '''
        <div class="flash-messages">
            <div class="flash-error">Bu kullanıcı adı veya e-posta zaten kullanılıyor!</div>
        </div>
        '''
        kayit_with_flash = kayit_content.replace('<h2>Kayıt Ol</h2>', f'{flash_content}<h2>Kayıt Ol</h2>')
        return render_template_string(BASE_HTML.replace('{{ content|safe }}', kayit_with_flash))
    
    # Yeni kullanıcı oluştur
    hashed_password = generate_password_hash(password)
    conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, hashed_password))
    conn.commit()
    conn.close()
    
    flash_content = '''
    <div class="flash-messages">
        <div class="flash-success">Kayıt başarılı! Giriş yapabilirsiniz.</div>
    </div>
    '''
    kayit_with_flash = kayit_content.replace('<h2>Kayıt Ol</h2>', f'{flash_content}<h2>Kayıt Ol</h2>')
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', kayit_with_flash))

@app.route('/giris')
def giris():
    giris_content = '''
    <section class="contact">
        <div class="container">
            <div class="auth-forms">
                <div class="auth-form">
                    <h2>Giriş Yap</h2>
                    <form method="POST" action="/giris">
                        <div class="form-group">
                            <label for="username">Kullanıcı Adı</label>
                            <input type="text" class="form-control" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Şifre</label>
                            <input type="password" class="form-control" id="password" name="password" required>
                        </div>
                        <button type="submit" class="btn">Giriş Yap</button>
                    </form>
                </div>
                <div class="auth-form">
                    <h2>Hesabınız Yok mu?</h2>
                    <p>Hesap oluşturarak sipariş verebilir ve siparişlerinizi takip edebilirsiniz.</p>
                    <a href="/kayit" class="btn btn-secondary">Kayıt Ol</a>
                </div>
            </div>
        </div>
    </section>
    '''
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', giris_content))

@app.route('/giris', methods=['POST'])
def giris_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = user['is_admin']
        return redirect('/')
    else:
        flash_content = '''
        <div class="flash-messages">
            <div class="flash-error">Kullanıcı adı veya şifre hatalı!</div>
        </div>
        '''
        giris_with_flash = giris_content.replace('<h2>Giriş Yap</h2>', f'{flash_content}<h2>Giriş Yap</h2>')
        return render_template_string(BASE_HTML.replace('{{ content|safe }}', giris_with_flash))

@app.route('/cikis')
def cikis():
    session.clear()
    return redirect('/')

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
        hizmet = hizmetler[hizmet_adi]
        
        # Sipariş butonu - giriş yapmış kullanıcılar için
        siparis_butonu = '''
        <div style="text-align: center; margin-top: 30px;">
            <h3>Bu hizmeti satın almak istiyor musunuz?</h3>
            <form method="POST" action="/siparis-ver" style="display: inline-block;">
                <input type="hidden" name="service_type" value="''' + hizmet['ad'] + '''">
                <textarea name="description" placeholder="Özel isteklerinizi buraya yazın..." style="width: 100%; margin: 10px 0; padding: 10px; background: var(--darker); border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 5px;"></textarea>
                <button type="submit" class="btn btn-success">Sipariş Ver</button>
            </form>
        </div>
        ''' if 'user_id' in session else '''
        <div style="text-align: center; margin-top: 30px;">
            <h3>Bu hizmeti satın almak için giriş yapın</h3>
            <a href="/giris" class="btn">Giriş Yap</a>
            <a href="/kayit" class="btn btn-secondary">Kayıt Ol</a>
        </div>
        '''
        
        service_detail_content = f'''
        <section class="service-detail">
            <div class="container">
                <div class="service-header">
                    <h1>{hizmet['ad']}</h1>
                    <div class="service-price">{hizmet['fiyat']}</div>
                    <p class="service-description">{hizmet['aciklama']}</p>
                    <a href="/iletisim" class="btn">İletişime Geç</a>
                    <a href="https://discord.gg/botland" class="btn btn-secondary" target="_blank">Discord'da Sor</a>
                </div>
                
                <div class="features-list">
                    <h2>Özellikler</h2>
                    <ul>
                        {"".join([f'<li>{ozellik}</li>' for ozellik in hizmet['ozellikler']])}
                    </ul>
                </div>
                
                {siparis_butonu}
            </div>
        </section>
        '''
        return render_template_string(BASE_HTML.replace('{{ content|safe }}', service_detail_content))
    else:
        return redirect(url_for('hizmetler'))

@app.route('/siparis-ver', methods=['POST'])
def siparis_ver():
    if 'user_id' not in session:
        return redirect('/giris')
    
    service_type = request.form.get('service_type')
    description = request.form.get('description', '')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO orders (user_id, service_type, description) VALUES (?, ?, ?)',
                (session['user_id'], service_type, description))
    conn.commit()
    conn.close()
    
    return redirect('/siparislerim')

@app.route('/siparislerim')
def siparislerim():
    if 'user_id' not in session:
        return redirect('/giris')
    
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT o.*, u.username 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        WHERE o.user_id = ? 
        ORDER BY o.created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    orders_html = ''
    for order in orders:
        status_class = f"status-{order['status']}"
        orders_html += f'''
        <tr>
            <td>{order['id']}</td>
            <td>{order['service_type']}</td>
            <td>{order['description'] or '-'}</td>
            <td class="{status_class}">{order['status'].title()}</td>
            <td>{order['created_at']}</td>
            <td>{order['admin_response'] or '-'}</td>
        </tr>
        '''
    
    siparislerim_content = f'''
    <section class="user-orders">
        <div class="container">
            <h2>Siparişlerim</h2>
            <table class="orders-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Hizmet</th>
                        <th>Açıklama</th>
                        <th>Durum</th>
                        <th>Tarih</th>
                        <th>Admin Yanıtı</th>
                    </tr>
                </thead>
                <tbody>
                    {orders_html if orders_html else '<tr><td colspan="6" style="text-align: center;">Henüz siparişiniz bulunmuyor.</td></tr>'}
                </tbody>
            </table>
        </div>
    </section>
    '''
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', siparislerim_content))

@app.route('/admin')
def admin_panel():
    if not session.get('is_admin'):
        return redirect('/')
    
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT o.*, u.username 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        ORDER BY o.created_at DESC
    ''').fetchall()
    conn.close()
    
    orders_html = ''
    for order in orders:
        status_class = f"status-{order['status']}"
        
        # Durum değiştirme butonları
        status_buttons = f'''
        <form method="POST" action="/admin/siparis-durum" style="display: inline;">
            <input type="hidden" name="order_id" value="{order['id']}">
            <button type="submit" name="status" value="completed" class="btn btn-success">Tamamlandı</button>
            <button type="submit" name="status" value="cancelled" class="btn btn-danger">İptal</button>
        </form>
        ''' if order['status'] == 'pending' else f'<span class="{status_class}">{order["status"].title()}</span>'
        
        # Admin yanıtı formu
        response_form = f'''
        <form method="POST" action="/admin/yanit-ver">
            <input type="hidden" name="order_id" value="{order['id']}">
            <textarea name="response" placeholder="Yanıtınızı yazın..." style="width: 100%; margin: 5px 0; padding: 5px; background: var(--darker); border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 3px; font-size: 12px;"></textarea>
            <button type="submit" class="btn" style="padding: 5px 10px; font-size: 12px;">Yanıt Ver</button>
        </form>
        '''
        
        orders_html += f'''
        <tr>
            <td>{order['id']}</td>
            <td>{order['username']}</td>
            <td>{order['service_type']}</td>
            <td>{order['description'] or '-'}</td>
            <td>{status_buttons}</td>
            <td>{order['created_at']}</td>
            <td>
                {order['admin_response'] or '-'}
                {response_form}
            </td>
        </tr>
        '''
    
    admin_content = f'''
    <section class="admin-panel">
        <div class="container">
            <h2>Admin Panel - Sipariş Yönetimi</h2>
            <table class="orders-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Kullanıcı</th>
                        <th>Hizmet</th>
                        <th>Açıklama</th>
                        <th>Durum</th>
                        <th>Tarih</th>
                        <th>Yanıt</th>
                    </tr>
                </thead>
                <tbody>
                    {orders_html if orders_html else '<tr><td colspan="7" style="text-align: center;">Henüz sipariş bulunmuyor.</td></tr>'}
                </tbody>
            </table>
        </div>
    </section>
    '''
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', admin_content))

@app.route('/admin/siparis-durum', methods=['POST'])
def admin_siparis_durum():
    if not session.get('is_admin'):
        return redirect('/')
    
    order_id = request.form.get('order_id')
    status = request.form.get('status')
    
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()
    
    return redirect('/admin')

@app.route('/admin/yanit-ver', methods=['POST'])
def admin_yanit_ver():
    if not session.get('is_admin'):
        return redirect('/')
    
    order_id = request.form.get('order_id')
    response = request.form.get('response')
    
    conn = get_db_connection()
    conn.execute('UPDATE orders SET admin_response = ? WHERE id = ?', (response, order_id))
    conn.commit()
    conn.close()
    
    return redirect('/admin')

@app.route('/iletisim', methods=['POST'])
def iletisim_formu():
    isim = request.form.get('isim')
    email = request.form.get('email')
    mesaj = request.form.get('mesaj')
    
    flash_content = '''
    <div class="flash-messages">
        <div class="flash-success">Mesajınız başarıyla gönderildi! En kısa sürede sizinle iletişime geçeceğiz.</div>
    </div>
    '''
    
    contact_with_flash = CONTACT_CONTENT.replace('</div>\n        \n        <div class="contact-form">', f'</div>\n        {flash_content}\n        <div class="contact-form">')
    return render_template_string(BASE_HTML.replace('{{ content|safe }}', contact_with_flash))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
