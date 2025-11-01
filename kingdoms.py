from flask import Flask, render_template_string, request, session, jsonify, redirect, url_for
import requests
import json

app = Flask(__name__)
app.secret_key = 'modd17checker_secret_key_2025'

VALID_KEYS = {
    'hahatv44': {'name': 'Admin User', 'plan': 'Premium', 'avatar': 'https://i.pinimg.com/736x/9c/64/58/9c6458d2e6ffb0c5e43d46541c6d97f2.jpg'},
    'admin123': {'name': 'Moderator', 'plan': 'Standard', 'avatar': 'https://i.pinimg.com/736x/9c/64/58/9c6458d2e6ffb0c5e43d46541c6d97f2.jpg'},
    'checkerkey': {'name': 'Basic User', 'plan': 'Basic', 'avatar': 'https://i.pinimg.com/736x/9c/64/58/9c6458d2e6ffb0c5e43d46541c6d97f2.jpg'}
}

API_URLS = {
    'tc': 'https://apiservices.alwaysdata.net/diger/tc.php?tc={tc}',
    'tcpro': 'https://apiservices.alwaysdata.net/diger/tcpro.php?tc={tc}',
    'adsoyad': 'https://apiservices.alwaysdata.net/diger/adsoyad.php?ad={ad}&soyad={soyad}',
    'adsoyadpro': 'https://apiservices.alwaysdata.net/diger/adsoyadpro.php?ad={ad}&soyad={soyad}&il={il}&ilce={ilce}',
    'tapu': 'https://apiservices.alwaysdata.net/diger/tapu.php?tc={tc}',
    'tcgsm': 'https://apiservices.alwaysdata.net/diger/tcgsm.php?tc={tc}',
    'gsmtc': 'https://apiservices.alwaysdata.net/diger/gsmtc.php?gsm={gsm}',
    'adres': 'https://apiservices.alwaysdata.net/diger/adres.php?tc={tc}',
    'hane': 'https://apiservices.alwaysdata.net/diger/hane.php?tc={tc}',
    'aile': 'https://apiservices.alwaysdata.net/diger/aile.php?tc={tc}',
    'sulale': 'https://apiservices.alwaysdata.net/diger/sulale.php?tc={tc}'
}

LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modd17 Checker | Giriş</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        :root {
            --primary-color: #0a0a0a; --secondary-color: #111111; --accent-color: #7c3aed;
            --accent-gradient: linear-gradient(135deg, #7c3aed, #6366f1); --text-color: #f8fafc;
            --text-secondary: #94a3b8; --border-color: #1e293b; --card-bg: rgba(15, 23, 42, 0.8);
            --glow: 0 0 25px rgba(124, 58, 237, 0.4); --glass: rgba(255,255,255,0.05);
        }
        body {
            background-color: var(--primary-color); color: var(--text-color); line-height: 1.7;
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(124, 58, 237, 0.1) 0%, transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(99, 102, 241, 0.1) 0%, transparent 25%),
                linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #16213e 100%);
            position: relative; overflow: hidden;
        }
        body::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2072&q=80') center/cover;
            opacity: 0.1; z-index: -1;
        }
        .login-container {
            background: var(--card-bg); padding: 50px 40px; border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.4), var(--glow); backdrop-filter: blur(20px); 
            border: 1px solid var(--glass); width: 90%; max-width: 450px; text-align: center;
            position: relative; overflow: hidden;
        }
        .login-container::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: var(--accent-gradient);
        }
        .logo { text-align: center; margin-bottom: 35px; position: relative; }
        .logo-icon { width: 80px; height: 80px; margin: 0 auto 20px; background: var(--accent-gradient); 
                   border-radius: 20px; display: flex; align-items: center; justify-content: center;
                   box-shadow: var(--glow); }
        .logo-icon i { font-size: 36px; color: white; }
        .logo h1 { background: var(--accent-gradient); -webkit-background-clip: text; background-clip: text; color: transparent; 
                  font-size: 32px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 8px; }
        .logo span { color: var(--text-secondary); font-size: 14px; font-weight: 500; }
        .form-group { margin-bottom: 25px; text-align: left; position: relative; }
        .form-group label { display: block; margin-bottom: 10px; color: var(--text-color); font-weight: 600; font-size: 14px; }
        .form-group input { width: 100%; padding: 16px 20px; background: rgba(15, 23, 42, 0.6); 
                          border: 1px solid var(--border-color); border-radius: 12px; 
                          color: var(--text-color); font-size: 16px; transition: all 0.3s ease;
                          backdrop-filter: blur(10px); }
        .form-group input:focus { outline: none; border-color: #7c3aed; box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2); }
        .form-group input::placeholder { color: #64748b; }
        .btn { padding: 16px 20px; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; 
              width: 100%; background: var(--accent-gradient); color: white; font-size: 16px;
              transition: all 0.3s ease; position: relative; overflow: hidden; }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none !important; box-shadow: none !important; }
        .btn:hover:not(:disabled) { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(124, 58, 237, 0.4); }
        .btn::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
                     background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                     transition: left 0.5s; }
        .btn:hover::before { left: 100%; }
        .error { background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 14px; border-radius: 10px; 
                margin-top: 20px; border-left: 4px solid #ef4444; font-size: 14px; text-align: left; }
        .turnstile-container { margin: 25px 0; }
        .theme-toggle { position: absolute; top: 20px; right: 20px; background: var(--glass); 
                      width: 40px; height: 40px; border-radius: 50%; display: flex; 
                      align-items: center; justify-content: center; cursor: pointer;
                      border: 1px solid var(--border-color); color: var(--text-secondary); }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="theme-toggle">
            <i class="fas fa-moon"></i>
        </div>
        <div class="logo">
            <div class="logo-icon">
                <i class="fas fa-shield-check"></i>
            </div>
            <h1>Modd17 Checker</h1>
            <span>Profesyonel Sorgu Sistemi</span>
        </div>
        <form method="POST" action="/login" id="loginForm">
            <div class="form-group">
                <label for="api_key"><i class="fas fa-key"></i> API Anahtarı</label>
                <input type="password" id="api_key" name="api_key" placeholder="API anahtarınızı girin" required>
            </div>
            
            <div class="turnstile-container">
                <div class="cf-turnstile" data-sitekey="1x00000000000000000000AA" data-theme="dark" data-callback="enableLogin"></div>
            </div>
            
            {% if error %}
            <div class="error"><i class="fas fa-exclamation-triangle"></i> {{ error }}</div>
            {% endif %}
            
            <button type="submit" class="btn" id="loginBtn" disabled>
                <i class="fas fa-sign-in-alt"></i> Giriş Yap
            </button>
        </form>
    </div>

    <script>
        function enableLogin() {
            document.getElementById('loginBtn').disabled = false;
        }
        
        // Tema değiştirme
        document.querySelector('.theme-toggle').addEventListener('click', function() {
            const icon = this.querySelector('i');
            if (icon.classList.contains('fa-moon')) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
                document.documentElement.style.setProperty('--primary-color', '#f8fafc');
                document.documentElement.style.setProperty('--secondary-color', '#e2e8f0');
                document.documentElement.style.setProperty('--text-color', '#0f172a');
                document.documentElement.style.setProperty('--text-secondary', '#475569');
                document.documentElement.style.setProperty('--border-color', '#cbd5e1');
                document.documentElement.style.setProperty('--card-bg', 'rgba(255, 255, 255, 0.9)');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
                document.documentElement.style.setProperty('--primary-color', '#0a0a0a');
                document.documentElement.style.setProperty('--secondary-color', '#111111');
                document.documentElement.style.setProperty('--text-color', '#f8fafc');
                document.documentElement.style.setProperty('--text-secondary', '#94a3b8');
                document.documentElement.style.setProperty('--border-color', '#1e293b');
                document.documentElement.style.setProperty('--card-bg', 'rgba(15, 23, 42, 0.8)');
            }
        });
    </script>
</body>
</html>
'''

MAIN_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modd17 Checker | TC Sorgu Sistemi</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        :root {
            --primary-color: #0a0a0a; --secondary-color: #111111; --accent-color: #7c3aed;
            --accent-gradient: linear-gradient(135deg, #7c3aed, #6366f1); --text-color: #f8fafc;
            --text-secondary: #94a3b8; --border-color: #1e293b; --card-bg: rgba(15, 23, 42, 0.8);
            --glow: 0 0 25px rgba(124, 58, 237, 0.4); --glass: rgba(255,255,255,0.05);
            --sidebar-width: 300px;
        }
        body {
            background-color: var(--primary-color); color: var(--text-color); line-height: 1.7;
            display: flex; min-height: 100vh; 
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(124, 58, 237, 0.1) 0%, transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(99, 102, 241, 0.1) 0%, transparent 25%),
                linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #16213e 100%);
            position: relative;
        }
        body::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2072&q=80') center/cover;
            opacity: 0.05; z-index: -1;
        }
        .sidebar {
            width: var(--sidebar-width); background: rgba(15, 23, 42, 0.9); padding: 30px 20px;
            position: fixed; height: 100vh; overflow-y: auto; border-right: 1px solid var(--glass);
            backdrop-filter: blur(20px); z-index: 100; transition: all 0.3s ease;
        }
        .logo { text-align: center; margin-bottom: 40px; padding-bottom: 25px; border-bottom: 1px solid var(--glass); position: relative; }
        .logo::after { content: ''; position: absolute; bottom: -1px; left: 25%; width: 50%; height: 2px; background: var(--accent-gradient); }
        .logo-icon { width: 70px; height: 70px; margin: 0 auto 15px; background: var(--accent-gradient); 
                   border-radius: 18px; display: flex; align-items: center; justify-content: center;
                   box-shadow: var(--glow); }
        .logo-icon i { font-size: 28px; color: white; }
        .logo h1 { background: var(--accent-gradient); -webkit-background-clip: text; background-clip: text; color: transparent; 
                  font-size: 26px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 5px; }
        .logo span { color: var(--text-secondary); font-size: 13px; font-weight: 500; }
        .menu { list-style: none; margin-bottom: 30px; }
        .menu li { margin-bottom: 8px; }
        .menu a { display: flex; align-items: center; padding: 14px 18px; color: var(--text-color); 
                 text-decoration: none; border-radius: 12px; transition: all 0.3s ease; font-weight: 500; 
                 cursor: pointer; background: transparent; border: 1px solid transparent; }
        .menu a i { margin-right: 14px; font-size: 16px; width: 20px; text-align: center; }
        .menu a:hover { background: rgba(124, 58, 237, 0.1); border-color: rgba(124, 58, 237, 0.3); transform: translateX(5px); }
        .menu a.active { background: var(--accent-gradient); color: white; box-shadow: var(--glow); border-color: transparent; }
        .main-content { flex: 1; margin-left: var(--sidebar-width); padding: 40px; transition: all 0.3s ease; }
        .section { margin-bottom: 40px; background: var(--card-bg); padding: 35px; border-radius: 20px; 
                  box-shadow: 0 10px 30px rgba(0,0,0,0.3); backdrop-filter: blur(20px); 
                  border: 1px solid var(--glass); position: relative; overflow: hidden; }
        .section::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--accent-gradient); }
        .section h2 { background: var(--accent-gradient); -webkit-background-clip: text; background-clip: text; color: transparent; 
                     margin-bottom: 25px; font-size: 32px; font-weight: 800; letter-spacing: -0.5px; }
        .anasayfa-content { color: var(--text-secondary); font-size: 16px; }
        .anasayfa-content p { margin-bottom: 18px; }
        .anasayfa-content ul { margin: 20px 0; padding-left: 20px; }
        .anasayfa-content li { margin-bottom: 10px; position: relative; padding-left: 15px; }
        .anasayfa-content li::before { content: '▸'; color: #7c3aed; position: absolute; left: 0; }
        .sorgu-form { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 10px; color: var(--text-color); font-weight: 600; font-size: 14px; }
        .form-group input, .form-group select { width: 100%; padding: 14px 18px; background: rgba(15, 23, 42, 0.6); 
                                              border: 1px solid var(--border-color); border-radius: 12px; 
                                              color: var(--text-color); font-size: 15px; transition: all 0.3s ease;
                                              backdrop-filter: blur(10px); }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: #7c3aed; box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2); }
        .btn { padding: 14px 25px; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; 
              background: var(--accent-gradient); color: white; font-size: 15px; transition: all 0.3s ease;
              position: relative; overflow: hidden; display: inline-flex; align-items: center; justify-content: center; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(124, 58, 237, 0.4); }
        .btn i { margin-right: 8px; }
        .btn::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
                     background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                     transition: left 0.5s; }
        .btn:hover::before { left: 100%; }
        .results-container { max-height: 600px; overflow-y: auto; margin-top: 20px; border-radius: 12px; overflow: hidden; }
        .results-table { width: 100%; border-collapse: collapse; background: rgba(15, 23, 42, 0.6); font-size: 14px; }
        .results-table th { background: var(--accent-gradient); color: white; padding: 14px 12px; text-align: left; 
                          font-weight: 600; position: sticky; top: 0; font-size: 12px; text-transform: uppercase; 
                          letter-spacing: 0.5px; }
        .results-table td { padding: 12px; border-bottom: 1px solid var(--glass); color: var(--text-color); font-size: 13px; }
        .results-table tr:hover { background: rgba(124, 58, 237, 0.05); }
        .loading { text-align: center; padding: 40px; color: var(--text-secondary); }
        .loading i { font-size: 32px; margin-bottom: 15px; display: block; }
        .error { background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 18px; border-radius: 12px; 
                margin-top: 20px; border-left: 4px solid #ef4444; font-size: 14px; }
        .success { background: rgba(34, 197, 94, 0.1); color: #22c55e; padding: 18px; border-radius: 12px; 
                  margin-top: 20px; border-left: 4px solid #22c55e; font-size: 14px; }
        .hidden { display: none; }
        .search-info { background: rgba(245, 158, 11, 0.1); color: #f59e0b; padding: 18px; border-radius: 12px; 
                      margin-bottom: 25px; border-left: 4px solid #f59e0b; font-size: 14px; }
        
        /* Kullanıcı Profil ve Çıkış Butonu */
        .user-profile { position: fixed; top: 20px; right: 80px; display: flex; align-items: center; gap: 15px; z-index: 1000; }
        .user-info { background: var(--glass); padding: 10px 15px; border-radius: 12px; border: 1px solid var(--border-color); 
                    backdrop-filter: blur(10px); display: flex; align-items: center; gap: 12px; }
        .user-avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #7c3aed; }
        .user-details { display: flex; flex-direction: column; }
        .user-name { font-weight: 600; font-size: 14px; color: var(--text-color); }
        .user-plan { font-size: 12px; color: var(--text-secondary); }
        .logout-btn { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); 
                     padding: 10px 15px; border-radius: 12px; cursor: pointer; transition: all 0.3s ease;
                     display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 500; }
        .logout-btn:hover { background: rgba(239, 68, 68, 0.3); transform: translateY(-2px); }
        
        .theme-toggle { position: fixed; top: 20px; right: 20px; background: var(--glass); 
                      width: 45px; height: 45px; border-radius: 50%; display: flex; 
                      align-items: center; justify-content: center; cursor: pointer; z-index: 1000;
                      border: 1px solid var(--border-color); color: var(--text-secondary);
                      backdrop-filter: blur(10px); transition: all 0.3s ease; }
        .theme-toggle:hover { background: rgba(124, 58, 237, 0.2); color: #7c3aed; }
        .mobile-menu-toggle { display: none; position: fixed; top: 20px; left: 20px; background: var(--glass); 
                            width: 45px; height: 45px; border-radius: 50%; display: none; align-items: center; 
                            justify-content: center; cursor: pointer; z-index: 1001; border: 1px solid var(--border-color); 
                            color: var(--text-secondary); backdrop-filter: blur(10px); }
        @media (max-width: 1024px) {
            .sidebar { transform: translateX(-100%); }
            .sidebar.active { transform: translateX(0); }
            .main-content { margin-left: 0; }
            .mobile-menu-toggle { display: flex; }
            .user-profile { right: 20px; top: 80px; }
        }
        @media (max-width: 768px) {
            .main-content { padding: 20px; }
            .section { padding: 25px; }
            .sorgu-form { grid-template-columns: 1fr; }
            .sidebar { width: 280px; }
            .user-profile { flex-direction: column; align-items: flex-end; }
            .user-info { flex-direction: column; text-align: center; }
        }
    </style>
</head>
<body>
    <div class="mobile-menu-toggle">
        <i class="fas fa-bars"></i>
    </div>
    
    <!-- Kullanıcı Profil ve Çıkış Butonu -->
    <div class="user-profile">
        <div class="user-info">
            <img src="{{ user_info.avatar }}" alt="Profil" class="user-avatar">
            <div class="user-details">
                <div class="user-name">{{ user_info.name }}</div>
                <div class="user-plan">{{ user_info.plan }} Plan</div>
            </div>
        </div>
        <a href="/logout" class="logout-btn">
            <i class="fas fa-sign-out-alt"></i>
            Çıkış
        </a>
    </div>

    <div class="theme-toggle">
        <i class="fas fa-moon"></i>
    </div>

    <div class="sidebar">
        <div class="logo">
            <div class="logo-icon">
                <i class="fas fa-shield-check"></i>
            </div>
            <h1>Modd17 Checker</h1>
            <span>Profesyonel Sorgu Sistemi</span>
        </div>
        <ul class="menu">
            <li><a class="active" data-page="anasayfa"><i class="fas fa-home"></i> Ana Sayfa</a></li>
            <li><a data-sorgu="tc" data-page="sorgu"><i class="fas fa-id-card"></i> TC Sorgu</a></li>
            <li><a data-sorgu="tcpro" data-page="sorgu"><i class="fas fa-id-card-alt"></i> TC Pro Sorgu</a></li>
            <li><a data-sorgu="adsoyad" data-page="sorgu"><i class="fas fa-user"></i> Ad Soyad Sorgu</a></li>
            <li><a data-sorgu="adsoyadpro" data-page="sorgu"><i class="fas fa-users"></i> Ad Soyad Pro</a></li>
            <li><a data-sorgu="tapu" data-page="sorgu"><i class="fas fa-home"></i> Tapu Sorgu</a></li>
            <li><a data-sorgu="tcgsm" data-page="sorgu"><i class="fas fa-phone"></i> TC GSM Sorgu</a></li>
            <li><a data-sorgu="gsmtc" data-page="sorgu"><i class="fas fa-mobile-alt"></i> GSM TC Sorgu</a></li>
            <li><a data-sorgu="adres" data-page="sorgu"><i class="fas fa-map-marker-alt"></i> Adres Sorgu</a></li>
            <li><a data-sorgu="hane" data-page="sorgu"><i class="fas fa-house-user"></i> Hane Sorgu</a></li>
            <li><a data-sorgu="aile" data-page="sorgu"><i class="fas fa-heart"></i> Aile Sorgu</a></li>
            <li><a data-sorgu="sulale" data-page="sorgu"><i class="fas fa-sitemap"></i> Sülale Sorgu</a></li>
        </ul>
    </div>

    <div class="main-content">
        <!-- Ana Sayfa -->
        <div class="section" id="anasayfa">
            <h2>Hoş Geldiniz</h2>
            <div class="anasayfa-content">
                <p><strong>Modd17 Checker Profesyonel Sorgu Sistemine hoş geldiniz!</strong></p>
                <p>Bu sistem, güvenli ve hızlı bir şekilde TC kimlik numarası sorgulama işlemleri yapmanızı sağlar.</p>
                <p><strong>Özellikler:</strong></p>
                <ul>
                    <li>TC Kimlik Sorgulama</li>
                    <li>Ad-Soyad Sorgulama</li>
                    <li>GSM Numarası Sorgulama</li>
                    <li>Adres ve Tapu Bilgileri</li>
                    <li>Aile ve Sülale Bilgileri</li>
                    <li>Güvenli Cloudflare Doğrulama</li>
                    <li>1000+ satırlık büyük veri setleri</li>
                    <li>Profesyonel Dark/Light Tema</li>
                    <li>Mobil Uyumlu Tasarım</li>
                </ul>
                <p><strong>Kullanım:</strong> Sol menüden sorgu tipini seçin, gerekli bilgileri girin ve sorgulama yapın.</p>
                <p><em>Not: Tüm sorgular güvenli API'ler üzerinden gerçekleştirilmektedir.</em></p>
            </div>
        </div>

        <!-- Sorgu Sayfası -->
        <div class="section hidden" id="sorgu">
            <h2 id="sorgu-baslik">TC Sorgu</h2>
            
            <div class="search-info" id="searchInfo" style="display: none;">
                <i class="fas fa-info-circle"></i> <span id="infoText"></span>
            </div>
            
            <form id="sorguForm" class="sorgu-form">
                <input type="hidden" id="sorguTipi" name="sorgu_tipi" value="tc">
                
                <div class="form-group" id="tcGroup">
                    <label for="tc"><i class="fas fa-id-card"></i> TC Kimlik No</label>
                    <input type="text" id="tc" name="sorgu_degeri" placeholder="TC kimlik numarasını girin" maxlength="11">
                </div>
                
                <div class="form-group" id="adGroup" style="display:none">
                    <label for="ad"><i class="fas fa-user"></i> Ad</label>
                    <input type="text" id="ad" name="ad" placeholder="Adınızı girin">
                </div>
                
                <div class="form-group" id="soyadGroup" style="display:none">
                    <label for="soyad"><i class="fas fa-user"></i> Soyad</label>
                    <input type="text" id="soyad" name="soyad" placeholder="Soyadınızı girin">
                </div>
                
                <div class="form-group" id="ilGroup" style="display:none">
                    <label for="il"><i class="fas fa-city"></i> İl</label>
                    <input type="text" id="il" name="il" placeholder="İl girin">
                </div>
                
                <div class="form-group" id="ilceGroup" style="display:none">
                    <label for="ilce"><i class="fas fa-building"></i> İlçe</label>
                    <input type="text" id="ilce" name="ilce" placeholder="İlçe girin">
                </div>
                
                <div class="form-group" id="gsmGroup" style="display:none">
                    <label for="gsm"><i class="fas fa-phone"></i> GSM No</label>
                    <input type="text" id="gsm" name="sorgu_degeri" placeholder="GSM numarasını girin">
                </div>
                
                <div class="form-group" style="grid-column:1/-1">
                    <div class="cf-turnstile" data-sitekey="1x00000000000000000000AA" data-theme="dark"></div>
                </div>
                
                <div class="form-group" style="grid-column:1/-1;text-align:center">
                    <button type="submit" class="btn"><i class="fas fa-search"></i> Sorgula</button>
                </div>
            </form>
            
            <div id="sonuclar"></div>
        </div>
    </div>

    <script>
        // Tema değiştirme
        document.querySelector('.theme-toggle').addEventListener('click', function() {
            const icon = this.querySelector('i');
            if (icon.classList.contains('fa-moon')) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
                document.documentElement.style.setProperty('--primary-color', '#f8fafc');
                document.documentElement.style.setProperty('--secondary-color', '#e2e8f0');
                document.documentElement.style.setProperty('--text-color', '#0f172a');
                document.documentElement.style.setProperty('--text-secondary', '#475569');
                document.documentElement.style.setProperty('--border-color', '#cbd5e1');
                document.documentElement.style.setProperty('--card-bg', 'rgba(255, 255, 255, 0.9)');
                document.documentElement.style.setProperty('--glass', 'rgba(0,0,0,0.05)');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
                document.documentElement.style.setProperty('--primary-color', '#0a0a0a');
                document.documentElement.style.setProperty('--secondary-color', '#111111');
                document.documentElement.style.setProperty('--text-color', '#f8fafc');
                document.documentElement.style.setProperty('--text-secondary', '#94a3b8');
                document.documentElement.style.setProperty('--border-color', '#1e293b');
                document.documentElement.style.setProperty('--card-bg', 'rgba(15, 23, 42, 0.8)');
                document.documentElement.style.setProperty('--glass', 'rgba(255,255,255,0.05)');
            }
        });

        // Mobil menü toggle
        document.querySelector('.mobile-menu-toggle').addEventListener('click', function() {
            document.querySelector('.sidebar').classList.toggle('active');
        });

        // Sayfa yönlendirme
        function showPage(pageId) {
            document.getElementById('anasayfa').classList.add('hidden');
            document.getElementById('sorgu').classList.add('hidden');
            document.getElementById(pageId).classList.remove('hidden');
            
            // Mobilde menüyü kapat
            if (window.innerWidth <= 1024) {
                document.querySelector('.sidebar').classList.remove('active');
            }
        }

        // Menü tıklama
        document.querySelectorAll('.menu a').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                document.querySelectorAll('.menu a').forEach(item => item.classList.remove('active'));
                this.classList.add('active');
                
                const page = this.getAttribute('data-page');
                if (page === 'sorgu') {
                    const sorguTipi = this.getAttribute('data-sorgu');
                    document.getElementById('sorguTipi').value = sorguTipi;
                    document.getElementById('sorgu-baslik').textContent = this.textContent.trim();
                    updateFormFields(sorguTipi);
                    showPage('sorgu');
                } else {
                    showPage('anasayfa');
                }
            });
        });

        function updateFormFields(sorguTipi) {
            // Tüm alanları gizle
            document.getElementById('tcGroup').style.display = 'none';
            document.getElementById('adGroup').style.display = 'none';
            document.getElementById('soyadGroup').style.display = 'none';
            document.getElementById('ilGroup').style.display = 'none';
            document.getElementById('ilceGroup').style.display = 'none';
            document.getElementById('gsmGroup').style.display = 'none';
            document.getElementById('searchInfo').style.display = 'none';
            
            // Bilgi metnini güncelle
            let infoText = '';
            
            if(['tc','tcpro','tapu','tcgsm','adres','hane','aile','sulale'].includes(sorguTipi)) {
                document.getElementById('tcGroup').style.display = 'block';
                infoText = 'TC kimlik numarası ile sorgulama yapılıyor. 11 haneli numarayı giriniz.';
            } else if(sorguTipi === 'adsoyad') {
                document.getElementById('adGroup').style.display = 'block';
                document.getElementById('soyadGroup').style.display = 'block';
                infoText = 'Ad ve soyad bilgileri ile sorgulama yapılıyor. Örnek: "Ahmet Yılmaz"';
            } else if(sorguTipi === 'adsoyadpro') {
                document.getElementById('adGroup').style.display = 'block';
                document.getElementById('soyadGroup').style.display = 'block';
                document.getElementById('ilGroup').style.display = 'block';
                document.getElementById('ilceGroup').style.display = 'block';
                infoText = 'Ad, soyad, il ve ilçe bilgileri ile detaylı sorgulama yapılıyor.';
            } else if(sorguTipi === 'gsmtc') {
                document.getElementById('gsmGroup').style.display = 'block';
                infoText = 'GSM numarası ile TC kimlik sorgulama yapılıyor.';
            }
            
            // Bilgi metnini göster
            if (infoText) {
                document.getElementById('infoText').textContent = infoText;
                document.getElementById('searchInfo').style.display = 'block';
            }
        }

        // Sorgu formu
        document.getElementById('sorguForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const sorguTipi = document.getElementById('sorguTipi').value;
            
            // Yükleme göster
            document.getElementById('sonuclar').innerHTML = `
                <div class="loading">
                    <i class="fas fa-spinner fa-spin"></i> Sorgu yapılıyor... 
                    <div style="margin-top: 10px; font-size: 14px;">Büyük veri seti yükleniyor, lütfen bekleyin...</div>
                </div>
            `;
            
            fetch('/sorgu', { method: 'POST', body: formData })
            .then(r => {
                if (!r.ok) {
                    throw new Error(`HTTP error! status: ${r.status}`);
                }
                return r.json();
            })
            .then(data => {
                console.log("Ham API Yanıtı:", data);
                const rawData = data.data?.Veri || data.VERI || data.result || data.data || data || [];

                console.log("Çözümlenmiş Veri:", rawData);

                if (data.success && Array.isArray(rawData)) {
                    displayResults(rawData, sorguTipi);
                } else {
                    document.getElementById('sonuclar').innerHTML = `
                        <div class="error">
                            <i class="fas fa-exclamation-triangle"></i> Veri alınamadı veya sonuç boş.
                        </div>`;
                }
            })
            .catch(err => {
                console.error('Fetch Error:', err);
                document.getElementById('sonuclar').innerHTML = '<div class="error"><i class="fas fa-exclamation-triangle"></i> Hata: ' + err.message + '</div>';
            });
        });

        function displayResults(dataArray, sorguTipi) {
            let results = [];
            if (dataArray.VERI && Array.isArray(dataArray.VERI)) {
                results = dataArray.VERI;
            } else if (Array.isArray(dataArray)) {
                results = dataArray;
            } else if (typeof dataArray === 'object' && dataArray !== null) {
                results = [dataArray];
            } else {
                results = [];
            }

            const resultCount = results.length;
            let html = `<div class="success"><i class="fas fa-check-circle"></i> Sorgu başarılı! Sonuçlar aşağıda listelenmiştir.</div>`;
            html += `<div class="search-info"><i class="fas fa-database"></i> Toplam <strong>${resultCount}</strong> kayıt bulundu</div>`;

            if (resultCount > 0) {
                html += `
                    <div class="results-container">
                        <table class="results-table">
                            <thead>
                                <tr>
                                    <th>TC</th>
                                    <th>Adı</th>
                                    <th>Soyadı</th>
                                    <th>Doğum Tarihi</th>
                                    <th>Nüfus İl</th>
                                    <th>Nüfus İlçe</th>
                                    <th>Anne Adı</th>
                                    <th>Anne TC</th>
                                    <th>Baba Adı</th>
                                    <th>Baba TC</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${results.map(item => `
                                    <tr>
                                        <td>${item.TCKN || item.TC || item.tckimlikno || '-'}</td>
                                        <td>${item.Adi || item.ADI || item.ad || item.isim || '-'}</td>
                                        <td>${item.Soyadi || item.SOYADI || item.soyad || item.soyisim || '-'}</td>
                                        <td>${item.DogumTarihi || item.DOGUM_TARIHI || item.dogumtarihi || '-'}</td>
                                        <td>${item.NufusIl || item.NUFUS_IL || item.il || item.sehir || '-'}</td>
                                        <td>${item.NufusIlce || item.NUFUS_ILCE || item.ilce || '-'}</td>
                                        <td>${item.AnneAdi || item.ANNE_ADI || item.anneadi || '-'}</td>
                                        <td>${item.AnneTCKN || item.ANNE_TC || item.annetc || '-'}</td>
                                        <td>${item.BabaAdi || item.BABA_ADI || item.babaadi || '-'}</td>
                                        <td>${item.BabaTCKN || item.BABA_TC || item.babatc || '-'}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            } else {
                html += '<div class="error">Sonuç bulunamadı</div>';
            }

            document.getElementById("sonuclar").innerHTML = html;
        }

        // İlk yüklemede ana sayfayı göster
        showPage('anasayfa');
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    if 'api_key' in session and session['api_key'] in VALID_KEYS:
        user_info = VALID_KEYS[session['api_key']]
        return render_template_string(MAIN_HTML, user_info=user_info)
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    api_key = request.form.get('api_key')
    if api_key in VALID_KEYS:
        session['api_key'] = api_key
        user_info = VALID_KEYS[api_key]
        return render_template_string(MAIN_HTML, user_info=user_info)
    return render_template_string(LOGIN_HTML, error='Geçersiz API anahtarı!')

@app.route('/logout')
def logout():
    session.pop('api_key', None)
    return redirect('/')

@app.route('/sorgu', methods=['POST'])
def sorgu():
    if 'api_key' not in session or session['api_key'] not in VALID_KEYS:
        return jsonify({'error': 'Yetkisiz erişim!'})
    
    sorgu_tipi = request.form.get('sorgu_tipi')
    sorgu_degeri = request.form.get('sorgu_degeri', '').strip()
    
    # TC kimlik numarası gereken sorgular için validasyon
    if sorgu_tipi in ['tc', 'tcpro', 'tapu', 'tcgsm', 'adres', 'hane', 'aile', 'sulale']:
        if len(sorgu_degeri) != 11 or not sorgu_degeri.isdigit():
            return jsonify({'error': 'TC kimlik numarası 11 haneli ve sadece rakamlardan oluşmalıdır.'})
    
    try:
        if sorgu_tipi in ['tc', 'tcpro', 'tapu', 'tcgsm', 'adres', 'hane', 'aile', 'sulale']:
            url = API_URLS[sorgu_tipi].format(tc=sorgu_degeri)
        elif sorgu_tipi == 'adsoyad':
            ad = request.form.get('ad', '').strip()
            soyad = request.form.get('soyad', '').strip()
            if not ad or not soyad:
                return jsonify({'error': 'Ad ve soyad alanları boş olamaz.'})
            url = API_URLS[sorgu_tipi].format(ad=ad, soyad=soyad)
        elif sorgu_tipi == 'adsoyadpro':
            ad = request.form.get('ad', '').strip()
            soyad = request.form.get('soyad', '').strip()
            il = request.form.get('il', '').strip()
            ilce = request.form.get('ilce', '').strip()
            if not ad or not soyad:
                return jsonify({'error': 'Ad ve soyad alanları boş olamaz.'})
            url = API_URLS[sorgu_tipi].format(ad=ad, soyad=soyad, il=il, ilce=ilce)
        elif sorgu_tipi == 'gsmtc':
            if not sorgu_degeri:
                return jsonify({'error': 'GSM numarası boş olamaz.'})
            url = API_URLS[sorgu_tipi].format(gsm=sorgu_degeri)
        else:
            return jsonify({'error': 'Geçersiz sorgu tipi!'})
        
        print(f"Requesting URL: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        print(f"Raw Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Parsed JSON Data: {json.dumps(data, ensure_ascii=False, indent=2)}")
                if not data:
                    return jsonify({'error': 'API boş yanıt döndü. Veri bulunamadı.'})
                return jsonify({'success': True, 'data': data})
            except ValueError as e:
                print(f"JSON Parse Error: {e}")
                return jsonify({'error': 'API yanıtı JSON formatında değil.'})
        else:
            return jsonify({'error': f'API hatası: {response.status_code} - {response.text}'})
    except requests.RequestException as e:
        print(f"Network Error: {str(e)}")
        return jsonify({'error': f'Ağ hatası: {str(e)}'})
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return jsonify({'error': f'Sorgu hatası: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
 
