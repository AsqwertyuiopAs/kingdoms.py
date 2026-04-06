from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Ana HTML şablonu
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <meta name="description" content="BarbieCraft - The Ultimate Barbie Mod for Minecraft. Transform your game with pink aesthetics, fashion items, dream houses, and mini-games.">
    <meta name="keywords" content="Barbie, Minecraft, Mod, BarbieCraft, Game Mod, Minecraft Mod">
    <title>BarbieCraft | Ultimate Barbie Mod for Minecraft</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
            overflow-x: hidden;
            color: #fff;
            position: relative;
            min-height: 100vh;
        }

        /* Premium Blurred Background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            background-image: url('https://assets.xboxservices.com/assets/0e/f8/0ef8df5c-a7dd-4eb3-b11a-743058d93953.jpg?n=Minecraft_GLP-Page-Hero-1084_Titan-Update_1920x1080_01.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            filter: blur(12px) brightness(0.55);
            transform: scale(1.05);
        }

        /* Pink Neon Overlay - Reduced Brightness */
        .pink-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: radial-gradient(circle at center, rgba(255,20,147,0.12), rgba(0,0,0,0.4));
            pointer-events: none;
        }

        /* Floating Hearts Animation */
        .heart {
            position: fixed;
            font-size: 18px;
            pointer-events: none;
            animation: floatHeart linear forwards;
            z-index: 9999;
            color: #ff69b4;
            text-shadow: 0 0 8px #ff1493, 0 0 12px rgba(255,20,147,0.5);
            opacity: 0.6;
        }

        @keyframes floatHeart {
            0% {
                transform: translateY(100vh) rotate(0deg) scale(1);
                opacity: 0;
            }
            10% {
                opacity: 0.7;
            }
            90% {
                opacity: 0.7;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg) scale(0.5);
                opacity: 0;
            }
        }

        /* Professional Neon Text Effect */
        .neon-text {
            text-shadow: 
                0 0 5px #fff,
                0 0 10px #fff,
                0 0 15px #ff1493,
                0 0 20px #ff1493,
                0 0 25px #ff69b4;
            animation: neonPulse 2s ease-in-out infinite;
        }

        @keyframes neonPulse {
            0%, 100% {
                text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #ff1493, 0 0 20px #ff1493;
            }
            50% {
                text-shadow: 0 0 8px #fff, 0 0 15px #fff, 0 0 20px #ff69b4, 0 0 30px #ff69b4;
            }
        }

        /* Premium Navbar */
        .navbar {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            padding: 1.2rem 2rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid rgba(255, 105, 180, 0.2);
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        }

        .navbar.scrolled {
            padding: 0.8rem 2rem;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(25px);
            border-bottom: 1px solid rgba(255, 105, 180, 0.3);
        }

        .nav-container {
            max-width: 1300px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        .logo {
            font-size: 2rem;
            font-weight: 700;
            color: #fff;
            text-decoration: none;
            letter-spacing: -0.5px;
            transition: all 0.3s ease;
            background: linear-gradient(135deg, #fff, #ff69b4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .logo:hover {
            transform: scale(1.05);
            background: linear-gradient(135deg, #ff69b4, #fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-menu {
            display: flex;
            gap: 2.5rem;
            list-style: none;
            align-items: center;
        }

        .nav-menu a {
            color: #fff;
            text-decoration: none;
            font-weight: 500;
            font-size: 1rem;
            transition: all 0.3s ease;
            padding: 0.5rem 0;
            position: relative;
        }

        .nav-menu a::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 2px;
            background: linear-gradient(90deg, #ff69b4, #fff);
            transition: width 0.3s ease;
        }

        .nav-menu a:hover::after {
            width: 100%;
        }

        .nav-menu a:hover {
            color: #ff69b4;
        }

        /* Main Container */
        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 120px 2rem 2rem;
        }

        /* Premium Hero Banner */
        .hero-banner {
            width: 100%;
            height: 550px;
            border-radius: 30px;
            overflow: hidden;
            margin-bottom: 4rem;
            position: relative;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            animation: fadeInUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
            border: 1px solid rgba(255, 105, 180, 0.3);
        }

        .hero-banner img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
        }

        .hero-banner:hover img {
            transform: scale(1.08);
        }

        .banner-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
            padding: 3rem;
            color: white;
        }

        .banner-overlay h2 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        /* Hero Section */
        .hero {
            min-height: 70vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            animation: fadeInUp 1s cubic-bezier(0.165, 0.84, 0.44, 1);
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

        .hero-content h1 {
            font-size: 5.5rem;
            margin-bottom: 1rem;
            letter-spacing: -1px;
            font-weight: 800;
        }

        .hero-content p {
            font-size: 1.4rem;
            margin-bottom: 2rem;
            opacity: 0.95;
            font-weight: 400;
        }

        /* Premium Buttons */
        .btn {
            display: inline-block;
            padding: 1rem 2.5rem;
            background: linear-gradient(135deg, #ff1493, #ff69b4);
            color: #fff;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
            border: none;
            cursor: pointer;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s ease;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(255, 20, 147, 0.4);
            background: linear-gradient(135deg, #ff69b4, #ff1493);
        }

        /* Download Section Premium */
        .download-section {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 4rem;
            text-align: center;
            margin: 4rem 0;
            border: 1px solid rgba(255, 105, 180, 0.2);
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        }

        .download-section:hover {
            border-color: rgba(255, 105, 180, 0.5);
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
            transform: translateY(-5px);
        }

        .download-section h2 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        .download-btn {
            font-size: 1.3rem;
            padding: 1.2rem 3rem;
            margin-top: 1.5rem;
        }

        /* Sections */
        .section {
            padding: 5rem 0;
            animation: fadeInUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
        }

        .section-title {
            text-align: center;
            font-size: 3rem;
            margin-bottom: 3rem;
            position: relative;
            display: inline-block;
            width: 100%;
            font-weight: 700;
            background: linear-gradient(135deg, #fff, #ff69b4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 3px;
            background: linear-gradient(90deg, #ff69b4, #fff);
            border-radius: 3px;
        }

        /* Professional Features Grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2.5rem;
            margin-top: 2rem;
        }

        .feature-card {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 2.5rem;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            border: 1px solid rgba(255, 105, 180, 0.2);
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 105, 180, 0.5);
            background: rgba(0, 0, 0, 0.6);
        }

        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 1.5rem;
            display: inline-block;
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        .feature-card h3 {
            margin-bottom: 1rem;
            font-size: 1.6rem;
            font-weight: 600;
            color: #ff69b4;
        }

        .feature-card p {
            line-height: 1.7;
            opacity: 0.9;
        }

        /* Stats Section Premium */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        .stat-card {
            text-align: center;
            padding: 2rem;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            border: 1px solid rgba(255, 105, 180, 0.2);
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            transform: scale(1.05);
            border-color: #ff69b4;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .stat-number {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #fff, #ff69b4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            font-size: 1rem;
            opacity: 0.9;
            letter-spacing: 1px;
        }

        /* Footer Premium */
        .footer {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            text-align: center;
            padding: 3rem;
            margin-top: 4rem;
            border-top: 1px solid rgba(255, 105, 180, 0.2);
        }

        .footer p {
            margin: 0.5rem 0;
            opacity: 0.8;
        }

        .social-links {
            margin-top: 1rem;
            display: flex;
            justify-content: center;
            gap: 1.5rem;
        }

        .social-links a {
            color: #fff;
            text-decoration: none;
            font-size: 1.5rem;
            transition: all 0.3s ease;
            opacity: 0.7;
        }

        .social-links a:hover {
            opacity: 1;
            transform: translateY(-3px);
            color: #ff69b4;
        }

        /* Responsive Design */
        @media (max-width: 968px) {
            .hero-content h1 {
                font-size: 3.5rem;
            }
            
            .hero-content p {
                font-size: 1.1rem;
            }
            
            .container {
                padding: 100px 1.5rem 1.5rem;
            }
            
            .section-title {
                font-size: 2.2rem;
            }

            .hero-banner {
                height: 350px;
            }

            .download-btn {
                font-size: 1.1rem;
                padding: 1rem 2rem;
            }

            .nav-menu {
                gap: 1.5rem;
            }
        }

        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                gap: 1rem;
            }
            
            .nav-menu {
                gap: 1rem;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .hero-content h1 {
                font-size: 2.5rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        /* Scroll Animation */
        .fade-in {
            opacity: 0;
            transform: translateY(40px);
            transition: all 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
        }

        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #ff1493, #ff69b4);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #ff69b4, #ff1493);
        }
    </style>
</head>
<body>
    <div class="pink-overlay"></div>
    
    <!-- Premium Navbar -->
    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <a href="#home" class="logo">BarbieCraft</a>
            <ul class="nav-menu">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#stats">Statistics</a></li>
                <li><a href="#download">Download</a></li>
            </ul>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container">
        <!-- Hero Banner - Updated with new image -->
        <div class="hero-banner">
            <img src="https://i.ytimg.com/vi/-yTx3jWRdRI/maxresdefault.jpg" alt="BarbieCraft Banner">
            <div class="banner-overlay">
                <h2 class="neon-text">BarbieCraft</h2>
                <p>The Ultimate Barbie Experience in Minecraft</p>
            </div>
        </div>

        <!-- Hero Section -->
        <section id="home" class="hero">
            <div class="hero-content">
                <h1 class="neon-text">BarbieCraft</h1>
                <p>Transform Your Minecraft World into a Magical Pink Paradise</p>
                <a href="#download" class="btn">✨ Download Now ✨</a>
            </div>
        </section>

        <!-- Features Section -->
        <section id="features" class="section fade-in">
            <h2 class="section-title">Premium Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">👗</div>
                    <h3>Luxury Fashion System</h3>
                    <p>Discover over 75+ exclusive Barbie outfits, sparkling accessories, and premium hairstyles. Each piece features stunning pink aesthetics and unique animations that bring your character to life.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🏰</div>
                    <h3>Dreamhouse Architecture</h3>
                    <p>Construct your perfect Barbie Dreamhouse using 100+ custom pink-themed blocks, magical furniture sets, and interactive decorations. Every detail is designed for the ultimate luxury experience.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h3>Interactive Mini-Games</h3>
                    <p>Experience 20+ unique Barbie-themed challenges including fashion runway shows, dance competitions, treasure hunts, and magical quests. Each game offers exclusive rewards and achievements.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🦄</div>
                    <h3>Magical Companions</h3>
                    <p>Adopt enchanting pets including unicorns, glittery ponies, and adorable kittens. Each companion has special abilities and can accompany you on epic adventures through magical dimensions.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">✨</div>
                    <h3>Special Effects & Magic</h3>
                    <p>Unlock stunning particle effects, sparkling trails, and magical transformations. Cast spells, create rainbow bridges, and leave trails of glitter wherever you go.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">👥</div>
                    <h3>Multiplayer Paradise</h3>
                    <p>Join friends in cooperative gameplay, host fashion parties, build together, and compete in friendly competitions. Visit other players' Dreamhouses and share your creativity with the community.</p>
                </div>
            </div>
        </section>

        <!-- Statistics Section -->
        <section id="stats" class="section fade-in">
            <h2 class="section-title">Community Impact</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">750K+</div>
                    <div class="stat-label">Total Downloads</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">75+</div>
                    <div class="stat-label">Premium Items</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">20+</div>
                    <div class="stat-label">Mini-Games</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">4.9★</div>
                    <div class="stat-label">Community Rating</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">150K+</div>
                    <div class="stat-label">Active Players</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">50+</div>
                    <div class="stat-label">Countries</div>
                </div>
            </div>
        </section>

        <!-- Download Section -->
        <section id="download" class="section fade-in">
            <div class="download-section">
                <h2>🎮 Download BarbieCraft Premium Mod 🎮</h2>
                <p style="margin: 1.5rem 0; font-size: 1.1rem; line-height: 1.7;">
                    Experience the most comprehensive and professionally crafted Barbie mod for Minecraft. 
                    Transform your gameplay with stunning pink aesthetics, exclusive features, and endless creative possibilities. 
                    Whether you're designing your dream house, collecting rare fashion items, or embarking on magical quests, 
                    BarbieCraft brings the enchanting Barbie universe to life in your Minecraft world like never before.
                </p>
                <p style="margin: 1rem 0; font-size: 1rem; color: #ff69b4; font-weight: 500;">
                    ✨ Version 3.0.0 - Premium Edition | Fully compatible with Minecraft 1.20.4+ ✨
                </p>
                <a href="https://www.mediafire.com/file/shd379a32ec53c8/BarbieCraft.rar/file" class="btn download-btn" target="_blank">
                    ⬇️ Download BarbieCraft Mod (Premium) ⬇️
                </a>
                <p style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.7;">
                    File Size: 20 MB | Requires Minecraft Forge 1.20.4+ | Free Lifetime Updates
                </p>
            </div>
        </section>
    </div>

    <!-- Premium Footer -->
    <footer class="footer">
        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">BarbieCraft</p>
        <p>© 2024 BarbieCraft Mod. All rights reserved. 💖</p>
        <p style="font-size: 0.9rem;">Created with passion for the global Minecraft community</p>
        <div class="social-links">
            <a href="#" target="_blank">📘</a>
            <a href="#" target="_blank">🐦</a>
            <a href="#" target="_blank">📷</a>
            <a href="#" target="_blank">🎮</a>
        </div>
        <p style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.6;">
            
        </p>
    </footer>

    <script>
        // Floating Hearts Animation System
        function createHeart() {
            const heart = document.createElement('div');
            const hearts = ['💖', '💗', '💓', '💕', '💝', '✨', '🌸', '🎀', '👗', '💄', '🦄', '⭐'];
            heart.innerHTML = hearts[Math.floor(Math.random() * hearts.length)];
            heart.classList.add('heart');
            heart.style.left = Math.random() * 100 + '%';
            heart.style.fontSize = Math.random() * 20 + 15 + 'px';
            heart.style.animationDuration = Math.random() * 5 + 6 + 's';
            heart.style.animationDelay = Math.random() * 3 + 's';
            document.body.appendChild(heart);
            
            setTimeout(() => {
                heart.remove();
            }, 11000);
        }

        setInterval(createHeart, 300);

        // Navbar Scroll Effect
        window.addEventListener('scroll', () => {
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Scroll Animation Observer
        const fadeElements = document.querySelectorAll('.fade-in');
        
        const observerOptions = {
            threshold: 0.15,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);
        
        fadeElements.forEach(el => observer.observe(el));

        // Smooth Scroll for Navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Initial Animation
        window.addEventListener('load', () => {
            document.querySelector('.hero').style.animation = 'fadeInUp 1s cubic-bezier(0.165, 0.84, 0.44, 1)';
            
            // Add floating animation to feature icons
            document.querySelectorAll('.feature-icon').forEach(icon => {
                icon.style.animation = 'float 3s ease-in-out infinite';
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
