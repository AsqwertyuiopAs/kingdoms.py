from flask import Flask, render_template_string

app = Flask(__name__)

# Ana sayfa HTML
index_html = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enes & Ceren ❤️ | Özel Soru</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: #f8fafc;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            position: relative;
        }
        
        .header {
            text-align: center;
            padding: 60px 0;
        }
        
        .main-title {
            font-size: 3.5em;
            font-weight: 800;
            background: linear-gradient(45deg, #60a5fa, #3b82f6);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 20px;
        }
        
        .couple-names {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 30px;
            margin: 40px 0;
            flex-wrap: wrap;
        }
        
        .name {
            font-size: 2.5em;
            font-weight: 700;
            padding: 20px 40px;
            background: rgba(30, 58, 138, 0.4);
            border-radius: 15px;
            border: 2px solid #3b82f6;
        }
        
        .heart {
            font-size: 3em;
            color: #ef4444;
            animation: heartbeat 1.5s infinite;
        }
        
        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }
        
        .video-container {
            margin: 40px auto;
            max-width: 800px;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            border: 3px solid #3b82f6;
        }
        
        .video-wrapper {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
        }
        
        .video-wrapper iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        
        .proposal-box {
            background: rgba(15, 23, 42, 0.9);
            border-radius: 25px;
            padding: 60px 40px;
            margin: 60px auto;
            max-width: 900px;
            border: 2px solid #3b82f6;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .question {
            font-size: 2.8em;
            line-height: 1.4;
            color: #ffffff;
            margin-bottom: 40px;
        }
        
        .highlight {
            color: #60a5fa;
            font-weight: 800;
        }
        
        .buttons {
            display: flex;
            justify-content: center;
            gap: 25px;
            margin-top: 50px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 20px 50px;
            font-size: 1.3em;
            font-weight: 600;
            border-radius: 50px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
        }
        
        .yes-btn {
            background: linear-gradient(45deg, #3b82f6, #1d4ed8);
            color: white;
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
        }
        
        .yes-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(59, 130, 246, 0.6);
        }
        
        .settings-btn {
            background: rgba(30, 41, 59, 0.9);
            color: #93c5fd;
            border: 2px solid #3b82f6;
        }
        
        .settings-btn:hover {
            background: rgba(59, 130, 246, 0.2);
        }
        
        .water-effect {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            opacity: 0.1;
        }
        
        .water-drop {
            position: absolute;
            background: #3b82f6;
            border-radius: 50%;
            animation: drop 15s infinite linear;
        }
        
        @keyframes drop {
            0% {
                transform: translateY(-100px) scale(0.5);
                opacity: 0;
            }
            10% {
                opacity: 0.3;
            }
            90% {
                opacity: 0.3;
            }
            100% {
                transform: translateY(100vh) scale(1.5);
                opacity: 0;
            }
        }
        
        @media (max-width: 768px) {
            .main-title {
                font-size: 2.5em;
            }
            
            .question {
                font-size: 2em;
            }
            
            .name {
                font-size: 1.8em;
                padding: 15px 30px;
            }
            
            .btn {
                padding: 18px 40px;
                font-size: 1.1em;
                width: 100%;
                max-width: 300px;
            }
            
            .buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .video-container {
                margin: 20px;
            }
        }
        
        @media (max-width: 480px) {
            .main-title {
                font-size: 2em;
            }
            
            .question {
                font-size: 1.6em;
            }
            
            .proposal-box {
                padding: 40px 20px;
                margin: 30px 15px;
            }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="water-effect" id="waterEffect"></div>
    
    <div class="container">
        <header class="header">
            <h1 class="main-title">Özel Bir Teklif</h1>
            <p style="font-size: 1.2em; color: #94a3b8; max-width: 700px; margin: 0 auto;">
                Sadece bizim için hazırlanmış bu özel anda...
            </p>
            
            <div class="couple-names">
                <div class="name">Enes</div>
                <div class="heart">❤️</div>
                <div class="name">Ceren</div>
            </div>
        </header>
        
        <div class="video-container">
            <div class="video-wrapper">
                <iframe 
                    src="https://www.youtube.com/embed/g3dKcRJCP8U?autoplay=1&mute=0&loop=1&playlist=g3dKcRJCP8U&controls=1&rel=0"
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen
                    title="i hate u, i love u - Glimpse of Us">
                </iframe>
            </div>
        </div>
        
        <div class="proposal-box">
            <div class="question">
                İlerde <span class="highlight">eşim olarak</span> ortak 
                <span class="highlight">havuzumuzda</span> yüzmeye 
                <span class="highlight">benler misin?</span>
            </div>
            
            <p style="font-size: 1.3em; line-height: 1.6; color: #cbd5e1; margin-bottom: 40px;">
                Ceren, hayatımın en güzel sürprizisin. Seninle geçen her an, 
                geleceğe dair hayallerimi daha da anlamlı kılıyor...
            </p>
            
            <div class="buttons">
                <a href="#" class="btn yes-btn" onclick="handleYes()">
                    <i class="fas fa-heart"></i>
                    EVET! Kabul Ediyorum
                </a>
                <a href="/ayar" class="btn settings-btn">
                    <i class="fas fa-cog"></i>
                    Ayarlar
                </a>
            </div>
        </div>
        
        <footer style="text-align: center; margin-top: 60px; padding: 30px; color: #64748b;">
            <p>Enes'ten Ceren'e, tüm kalbimle ❤️</p>
            <p style="margin-top: 10px; font-size: 0.9em;">© 2024 - Özel teklif sitesi</p>
        </footer>
    </div>
    
    <script>
        // Su damlacıkları efekti
        function createWaterDrops() {
            const waterEffect = document.getElementById('waterEffect');
            for (let i = 0; i < 25; i++) {
                const drop = document.createElement('div');
                drop.className = 'water-drop';
                
                const size = 3 + Math.random() * 8;
                const left = Math.random() * 100;
                const delay = Math.random() * 15;
                const duration = 10 + Math.random() * 10;
                
                drop.style.width = `${size}px`;
                drop.style.height = `${size}px`;
                drop.style.left = `${left}vw`;
                drop.style.animationDelay = `${delay}s`;
                drop.style.animationDuration = `${duration}s`;
                
                waterEffect.appendChild(drop);
            }
        }
        
        // Evet butonu efekti
        function handleYes() {
            // Konfeti efekti
            for(let i = 0; i < 150; i++) {
                setTimeout(() => {
                    const confetti = document.createElement('div');
                    confetti.innerHTML = ['🎉', '🎊', '❤️', '🥰'][Math.floor(Math.random() * 4)];
                    confetti.style.position = 'fixed';
                    confetti.style.left = Math.random() * 100 + 'vw';
                    confetti.style.top = '-50px';
                    confetti.style.fontSize = (20 + Math.random() * 25) + 'px';
                    confetti.style.zIndex = '9999';
                    confetti.style.pointerEvents = 'none';
                    confetti.style.animation = `fall ${2 + Math.random() * 3}s linear forwards`;
                    
                    document.body.appendChild(confetti);
                    
                    setTimeout(() => confetti.remove(), 3000);
                }, i * 20);
            }
            
            // Konfeti animasyonu
            const style = document.createElement('style');
            style.textContent = `
                @keyframes fall {
                    0% {
                        transform: translateY(0) rotate(0deg);
                        opacity: 1;
                    }
                    100% {
                        transform: translateY(100vh) rotate(360deg);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
            
            // Mesaj
            setTimeout(() => {
                alert('🎉 HARİKA! 🎉\n\nCeren, bu harika haber için çok teşekkür ederim!\nSeni çok seviyorum! ❤️\n\nİlk iş ortak havuzumuzu planlayalım!');
            }, 1000);
        }
        
        // Sayfa yüklendiğinde
        document.addEventListener('DOMContentLoaded', function() {
            createWaterDrops();
            
            // Video hazır olduğunda
            const iframe = document.querySelector('iframe');
            iframe.onload = function() {
                console.log('Video hazır!');
            };
        });
        
        // Video ses kontrolü
        function toggleMute() {
            const iframe = document.querySelector('iframe');
            iframe.contentWindow.postMessage('{"event":"command","func":"mute","args":""}', '*');
        }
        
        // Video oynat/durdur
        function togglePlay() {
            const iframe = document.querySelector('iframe');
            iframe.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
        }
    </script>
</body>
</html>
'''

# Ayarlar sayfası HTML
ayar_html = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ayarlar | Enes & Ceren</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: #f8fafc;
            min-height: 100vh;
            padding: 20px;
        }
        
        .settings-container {
            max-width: 800px;
            margin: 50px auto;
            padding: 40px;
            background: rgba(15, 23, 42, 0.95);
            border-radius: 25px;
            border: 2px solid #3b82f6;
        }
        
        .settings-title {
            text-align: center;
            font-size: 2.5em;
            color: #60a5fa;
            margin-bottom: 40px;
        }
        
        .setting-section {
            background: rgba(30, 41, 59, 0.8);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            border-left: 5px solid #3b82f6;
        }
        
        .setting-section h3 {
            color: #93c5fd;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .setting-list {
            list-style: none;
            padding: 0;
        }
        
        .setting-list li {
            padding: 10px 0;
            border-bottom: 1px solid rgba(96, 165, 250, 0.2);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .setting-list li:last-child {
            border-bottom: none;
        }
        
        .back-btn {
            display: block;
            width: 200px;
            margin: 40px auto 0;
            padding: 18px 40px;
            background: linear-gradient(45deg, #3b82f6, #1d4ed8);
            color: white;
            text-decoration: none;
            text-align: center;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .back-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
        }
        
        @media (max-width: 768px) {
            .settings-container {
                padding: 20px;
                margin: 20px;
            }
            
            .settings-title {
                font-size: 2em;
            }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="settings-container">
        <h1 class="settings-title"><i class="fas fa-cog"></i> Site Ayarları</h1>
        
        <div class="setting-section">
            <h3><i class="fas fa-video"></i> Video Ayarları</h3>
            <ul class="setting-list">
                <li><i class="fas fa-check" style="color: #10b981;"></i> YouTube video gömülü</li>
                <li><i class="fas fa-check" style="color: #10b981;"></i> Otomatik oynatma: Aktif</li>
                <li><i class="fas fa-check" style="color: #10b981;"></i> Sürekli döngü: Aktif</li>
                <li><i class="fas fa-link" style="color: #3b82f6;"></i> <a href="https://www.youtube.com/watch?v=g3dKcRJCP8U" target="_blank" style="color: #60a5fa;">YouTube Linki</a></li>
            </ul>
        </div>
        
        <div class="setting-section">
            <h3><i class="fas fa-heart"></i> Özel Mesaj</h3>
            <ul class="setting-list">
                <li><i class="fas fa-user" style="color: #3b82f6;"></i> Gönderen: Enes</li>
                <li><i class="fas fa-user" style="color: #3b82f6;"></i> Alıcı: Ceren</li>
                <li><i class="fas fa-quote-left" style="color: #60a5fa;"></i> "İlerde eşim olarak ortak havuzumuzda yüzmeye benler misin?"</li>
                <li><i class="fas fa-palette" style="color: #8b5cf6;"></i> Tema: Lacivert & Su efekti</li>
            </ul>
        </div>
        
        <div class="setting-section">
            <h3><i class="fas fa-info-circle"></i> Site Bilgileri</h3>
            <ul class="setting-list">
                <li><i class="fas fa-code" style="color: #f59e0b;"></i> Framework: Flask Python</li>
                <li><i class="fas fa-mobile-alt" style="color: #10b981;"></i> Responsive: Evet</li>
                <li><i class="fas fa-server" style="color: #8b5cf6;"></i> Hosting: Render.com</li>
                <li><i class="fas fa-calendar" style="color: #ef4444;"></i> Tarih: 2024</li>
            </ul>
        </div>
        
        <div class="setting-section">
            <h3><i class="fas fa-wrench"></i> Kontroller</h3>
            <ul class="setting-list">
                <li><button onclick="window.location.href='/'" style="background: #3b82f6; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Ana Sayfaya Dön</button></li>
                <li><button onclick="if(confirm('Siteyi yenilemek istediğinize emin misiniz?')) location.reload()" style="background: #10b981; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Siteyi Yenile</button></li>
                <li><button onclick="alert('Video linki: https://www.youtube.com/watch?v=g3dKcRJCP8U')" style="background: #f59e0b; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Video Linkini Göster</button></li>
            </ul>
        </div>
        
        <a href="/" class="back-btn">
            <i class="fas fa-arrow-left"></i> Ana Sayfaya Dön
        </a>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/ayar')
def ayar():
    return render_template_string(ayar_html)

# Render için gerekli konfigürasyon
if __name__ == '__main__':
    # Render.com'da çalışırken
    # app.run(host='0.0.0.0', port=10000, debug=False)
    
    # Lokal test için
    app.run(debug=True, port=5000)
