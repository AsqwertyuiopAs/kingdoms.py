from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SalvoMotivation | Professional Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* PRELOADER - Yükleme Ekranı */
        .preloader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000000;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: opacity 0.5s ease, visibility 0.5s ease;
        }
        
        .preloader.hide {
            opacity: 0;
            visibility: hidden;
        }
        
        .preloader-logo {
            margin-bottom: 3rem;
            animation: fadeInUp 0.6s ease;
        }
        
        .preloader-logo-img {
            height: 80px;
            width: auto;
            object-fit: contain;
            filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.1));
        }
        
        .loader-container {
            width: 280px;
            text-align: center;
        }
        
        .loader-bar-wrapper {
            width: 100%;
            height: 2px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        
        .loader-bar {
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, #ffffff, #888888);
            border-radius: 2px;
            transition: width 0.1s linear;
        }
        
        .loader-percent {
            font-size: 0.9rem;
            color: #888888;
            letter-spacing: 2px;
            font-weight: 500;
            font-family: 'Space Grotesk', monospace;
        }
        
        .loader-text {
            margin-top: 1rem;
            font-size: 0.7rem;
            color: #555555;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* ANA SAYFA - Normal Site İçeriği */
        body {
            background: #000000;
            font-family: 'Space Grotesk', sans-serif;
            color: #e8e8e8;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .main-content-wrapper {
            opacity: 0;
            transition: opacity 0.8s ease;
        }
        
        .main-content-wrapper.show {
            opacity: 1;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0a0a0a;
        }
        ::-webkit-scrollbar-thumb {
            background: #2a2a2a;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #3a3a3a;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: rgba(0, 0, 0, 0.96);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 1.2rem 2rem;
            transition: all 0.4s ease;
        }
        
        .header.scrolled {
            padding: 0.8rem 2rem;
            background: rgba(0, 0, 0, 0.98);
        }
        
        .nav-container {
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo-left {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logo-img {
            height: 48px;
            width: auto;
            object-fit: contain;
            filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.08));
            transition: all 0.4s ease;
        }
        
        .logo-img:hover {
            transform: scale(1.05);
        }
        
        .logo-text {
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 0%, #999999 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .nav-menu {
            display: flex;
            gap: 2.5rem;
            list-style: none;
        }
        
        .nav-menu a {
            color: #e0e0e0;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .nav-menu a::before {
            content: '';
            position: absolute;
            bottom: -6px;
            left: 0;
            right: 0;
            height: 1px;
            background: #ffffff;
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }
        
        .nav-menu a:hover::before {
            transform: scaleX(1);
        }
        
        .hero-banner {
            margin-top: 80px;
            position: relative;
            width: 100%;
            background: #000000;
        }
        
        .banner-wrapper {
            width: 100%;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #000000;
        }
        
        .banner-img {
            width: 100%;
            height: auto;
            max-height: 700px;
            object-fit: contain;
            display: block;
            background: #000000;
        }
        
        .main-content {
            max-width: 1600px;
            margin: 0 auto;
            padding: 6rem 2rem;
        }
        
        .about-section {
            background: linear-gradient(135deg, #0a0a0a 0%, #030303 100%);
            border-radius: 40px;
            padding: 5rem 4rem;
            border: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 0 30px 60px -20px rgba(0, 0, 0, 0.8);
            position: relative;
        }
        
        .about-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
        }
        
        .about-header {
            margin-bottom: 4rem;
            text-align: center;
        }
        
        .about-subtitle {
            color: #888888;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin-bottom: 1.5rem;
            display: inline-block;
        }
        
        .about-title {
            font-size: 4.5rem;
            font-weight: 700;
            letter-spacing: -2px;
            line-height: 1.1;
            background: linear-gradient(135deg, #ffffff 0%, #cccccc 50%, #999999 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 1.5rem;
            font-family: 'Playfair Display', serif;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 3rem;
            margin: 4rem 0;
            padding: 3rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        .stat-item {
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-item:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff, #aaaaaa);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 0.5rem;
            font-family: 'Playfair Display', serif;
        }
        
        .stat-label {
            font-size: 0.85rem;
            color: #888888;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 500;
        }
        
        .motivation-content {
            margin: 3rem 0;
        }
        
        .motivation-text {
            font-size: 1.2rem;
            line-height: 1.8;
            color: #c8c8c8;
            margin-bottom: 2rem;
            text-align: center;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .highlight-white {
            color: #ffffff;
            font-weight: 600;
        }
        
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2.5rem;
            margin-top: 5rem;
        }
        
        .motivation-card {
            background: linear-gradient(135deg, rgba(15, 15, 15, 0.9) 0%, rgba(5, 5, 5, 0.95) 100%);
            backdrop-filter: blur(10px);
            border-radius: 32px;
            padding: 3rem 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            position: relative;
        }
        
        .motivation-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s ease;
        }
        
        .motivation-card:hover::before {
            transform: translateX(100%);
        }
        
        .motivation-card:hover {
            transform: translateY(-12px);
            border-color: rgba(255, 255, 255, 0.15);
            background: linear-gradient(135deg, rgba(20, 20, 20, 0.95) 0%, rgba(10, 10, 10, 0.98) 100%);
            box-shadow: 0 30px 50px -20px rgba(0, 0, 0, 0.8);
        }
        
        .card-icon {
            font-size: 3.5rem;
            margin-bottom: 1.8rem;
            filter: grayscale(0.3);
            transition: all 0.4s ease;
        }
        
        .motivation-card:hover .card-icon {
            transform: scale(1.05);
            filter: grayscale(0);
        }
        
        .card-title {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            color: #ffffff;
            letter-spacing: -0.5px;
            font-family: 'Playfair Display', serif;
        }
        
        .card-description {
            color: #a0a0a0;
            line-height: 1.7;
            font-size: 0.95rem;
        }
        
        .quote-section {
            margin-top: 6rem;
            padding: 4rem;
            background: linear-gradient(135deg, rgba(10, 10, 10, 0.6) 0%, rgba(5, 5, 5, 0.8) 100%);
            border-radius: 32px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .quote-icon {
            font-size: 2.5rem;
            color: #555555;
            margin-bottom: 1.5rem;
            opacity: 0.6;
        }
        
        .quote-text {
            font-size: 1.6rem;
            font-style: italic;
            color: #e0e0e0;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.5;
            font-family: 'Playfair Display', serif;
        }
        
        .quote-author {
            margin-top: 2rem;
            color: #888888;
            font-size: 0.9rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .footer {
            background: linear-gradient(135deg, #000000 0%, #050505 100%);
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            padding: 5rem 2rem 2rem;
            margin-top: 5rem;
        }
        
        .footer-content {
            max-width: 1600px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 4rem;
        }
        
        .footer-section h4 {
            color: #ffffff;
            margin-bottom: 1.2rem;
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .footer-section p {
            color: #777777;
            font-size: 0.9rem;
        }
        
        .social-links {
            display: flex;
            gap: 1.2rem;
            margin-top: 1.5rem;
        }
        
        .social-links a {
            color: #777777;
            font-size: 1.2rem;
            transition: all 0.3s ease;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.03);
        }
        
        .social-links a:hover {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-3px);
        }
        
        .footer-bottom {
            text-align: center;
            padding-top: 4rem;
            margin-top: 4rem;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            color: #666666;
            font-size: 0.85rem;
        }
        
        @media (max-width: 968px) {
            .nav-menu {
                display: none;
            }
            .about-title {
                font-size: 2.8rem;
            }
            .stats-grid {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            .about-section {
                padding: 2.5rem;
            }
            .cards-grid {
                grid-template-columns: 1fr;
            }
            .quote-text {
                font-size: 1.1rem;
            }
        }
        
        @media (max-width: 768px) {
            .header {
                padding: 0.8rem 1rem;
            }
            .logo-img {
                height: 36px;
            }
            .logo-text {
                font-size: 1.1rem;
            }
            .hero-banner {
                margin-top: 70px;
            }
            .banner-img {
                max-height: 350px;
            }
            .main-content {
                padding: 2rem 1rem;
            }
            .about-title {
                font-size: 2rem;
            }
            .motivation-text {
                font-size: 0.95rem;
            }
            .preloader-logo-img {
                height: 60px;
            }
            .loader-container {
                width: 220px;
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-fade-in-up {
            animation: fadeInUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
        }
        
        .motivation-card {
            animation: fadeInUp 0.6s cubic-bezier(0.165, 0.84, 0.44, 1) backwards;
        }
        
        .motivation-card:nth-child(1) { animation-delay: 0.1s; }
        .motivation-card:nth-child(2) { animation-delay: 0.2s; }
        .motivation-card:nth-child(3) { animation-delay: 0.3s; }
        
        ::selection {
            background: #2a2a2a;
            color: #ffffff;
        }
    </style>
</head>
<body>

    <!-- PRELOADER - Yükleme Ekranı -->
    <div class="preloader" id="preloader">
        <div class="preloader-logo">
            <img src="https://raw.githubusercontent.com/AsqwertyuiopAs/kingdoms.py/main/statik/logo.jpg" class="preloader-logo-img" alt="SalvoMotivation Logo">
        </div>
        <div class="loader-container">
            <div class="loader-bar-wrapper">
                <div class="loader-bar" id="loaderBar"></div>
            </div>
            <div class="loader-percent" id="loaderPercent">0%</div>
            <div class="loader-text">LOADING</div>
        </div>
    </div>

    <!-- ANA SAYFA İÇERİĞİ -->
    <div class="main-content-wrapper" id="mainContent">
        <div class="header" id="header">
            <div class="nav-container">
                <div class="logo-left">
                    <img src="https://raw.githubusercontent.com/AsqwertyuiopAs/kingdoms.py/main/statik/logo.jpg" class="logo-img" alt="SalvoMotivation Logo">
                    <span class="logo-text">SALVOMOTIVATION</span>
                </div>
                <ul class="nav-menu">
                    <li><a href="#home">HOME</a></li>
                    <li><a href="#about">ABOUT</a></li>
                    <li><a href="#services">SERVICES</a></li>
                    <li><a href="#contact">CONTACT</a></li>
                </ul>
            </div>
        </div>
        
        <div class="hero-banner" id="home">
            <div class="banner-wrapper">
                <img src="https://raw.githubusercontent.com/AsqwertyuiopAs/kingdoms.py/main/statik/banner.webp" class="banner-img" alt="Motivation Banner">
            </div>
        </div>
        
        <div class="main-content" id="about">
            <div class="about-section animate-fade-in-up">
                <div class="about-header">
                    <div class="about-subtitle">WHO I AM</div>
                    <h1 class="about-title">SalvoMotivation</h1>
                    <div class="motivation-text">
                        Merhaba, ben <span class="highlight-white">Salvo</span>. İçsel gücü keşfetmek, 
                        zihinsel dayanıklılığı artırmak ve duygusal dengeyi sağlamak için buradayım.
                    </div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number">500+</div>
                        <div class="stat-label">HAPPY CLIENTS</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">1000+</div>
                        <div class="stat-label">SUCCESS SESSIONS</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">50+</div>
                        <div class="stat-label">WORKSHOPS</div>
                    </div>
                </div>
                
                <div class="motivation-content">
                    <div class="motivation-text">
                        <strong>Motivasyon</strong> sadece bir kelime değil, her gün daha iyiye gitme sanatıdır.<br><br>
                        <strong>Zihinsel güç</strong> zorluklar karşısında dimdik ayakta kalma yeteneğidir.<br><br>
                        <strong>Duygusallık</strong> ise hislerimizin rehberliğinde, onları kontrol altına alarak 
                        gerçek potansiyelimize ulaşmamızı sağlar.
                    </div>
                </div>
                
                <div class="cards-grid" id="services">
                    <div class="motivation-card">
                        <div class="card-icon">⚡</div>
                        <h3 class="card-title">Motivasyon</h3>
                        <p class="card-description">
                            Her sabah yeni bir başlangıç. Hedeflerine odaklan, harekete geç ve asla vazgeçme. 
                            Gerçek motivasyon içten gelir ve sürdürülebilirdir. Başarıya giden yolda en büyük itici güçtür.
                        </p>
                    </div>
                    
                    <div class="motivation-card">
                        <div class="card-icon">🧠</div>
                        <h3 class="card-title">Zihinsel Güç</h3>
                        <p class="card-description">
                            Zorluklar seni güçlendirir. Her engel, karakterini inşa eden bir tuğladır. 
                            Zihnini kontrol et, hayatını yönet. Mental dayanıklılık, modern dünyanın en önemli yetkinliklerindendir.
                        </p>
                    </div>
                    
                    <div class="motivation-card">
                        <div class="card-icon">❤️</div>
                        <h3 class="card-title">Duygusallık</h3>
                        <p class="card-description">
                            Duygularını tanı, kabullen ve dönüştür. Duygusal zeka, modern dünyanın en büyük süper gücüdür. 
                            Hislerin seni yönlendirmesin, sen onları yönlendir. Duygusal denge ile hayatın kontrolü sende.
                        </p>
                    </div>
                </div>
                
                <div class="quote-section">
                    <div class="quote-icon">
                        <i class="fas fa-quote-left"></i>
                    </div>
                    <div class="quote-text">
                        "The only limit is the one you set in your mind. Break it, and you'll find infinite possibilities."
                    </div>
                    <div class="quote-author">— SALVOMOTIVATION</div>
                </div>
            </div>
        </div>
        
        <div class="footer" id="contact">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>SalvoMotivation</h4>
                    <p>Premium portfolio for motivation, mental strength and emotional intelligence.</p>
                </div>
                <div class="footer-section">
                    <h4>Connect</h4>
                    <p>hello@salvomotivation.com</p>
                    <div class="social-links">
                        <a href="#"><i class="fab fa-linkedin-in"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                        <a href="#"><i class="fab fa-x-twitter"></i></a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 SalvoMotivation. All rights reserved. | Every moment is a new beginning ✨</p>
            </div>
        </div>
    </div>

    <script>
        // Yükleme animasyonu: 0'dan 100'e kadar ilerle
        let percent = 0;
        const loaderBar = document.getElementById('loaderBar');
        const loaderPercent = document.getElementById('loaderPercent');
        const preloader = document.getElementById('preloader');
        const mainContent = document.getElementById('mainContent');
        
        const interval = setInterval(() => {
            percent += Math.floor(Math.random() * 10) + 1;
            if (percent >= 100) {
                percent = 100;
                clearInterval(interval);
                
                // Yükleme tamamlandı, ana sayfayı göster
                setTimeout(() => {
                    preloader.classList.add('hide');
                    mainContent.classList.add('show');
                }, 200);
            }
            loaderBar.style.width = percent + '%';
            loaderPercent.innerText = percent + '%';
        }, 80);
        
        // Header scroll efekti
        window.addEventListener('scroll', function() {
            const header = document.getElementById('header');
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
        
        // Kart tıklama efekti
        document.querySelectorAll('.motivation-card').forEach(card => {
            card.addEventListener('click', () => {
                card.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    card.style.transform = '';
                }, 200);
            });
        });
        
        // Sayfa tamamen yüklendiğinde (yedek)
        window.addEventListener('load', function() {
            setTimeout(() => {
                if (percent < 100) {
                    percent = 100;
                    loaderBar.style.width = '100%';
                    loaderPercent.innerText = '100%';
                    clearInterval(interval);
                    setTimeout(() => {
                        preloader.classList.add('hide');
                        mainContent.classList.add('show');
                    }, 200);
                }
            }, 1000);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
