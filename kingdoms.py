from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import time
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'orender_professional_secret_2024')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orender Service - Profesyonel YouTube Büyüme Platformu</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --dark-bg: #0a0a0a;
            --darker-bg: #050505;
            --card-bg: #111111;
            --border-color: #222222;
            --text-primary: #ffffff;
            --text-secondary: #888888;
            --youtube-red: #ff0000;
            --youtube-dark-red: #cc0000;
            --accent: #ff3333;
            --success: #00d26a;
            --warning: #ffaa00;
            --discord-purple: #5865F2;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', 'Roboto', 'Arial', sans-serif;
        }

        body {
            background: var(--dark-bg);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
            font-weight: 400;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Auth Wall */
        .auth-wall {
            display: {% if not session.user_id %}flex{% else %}none{% endif %};
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(rgba(5, 5, 5, 0.85), rgba(5, 5, 5, 0.92)),
                url('https://images.squarespace-cdn.com/content/v1/558d57a4e4b047b6f98af00b/1436932289461-Q5VZ13046Y0AP6QHHOWT/Reception+01_2.jpg?format=1500w');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            z-index: 9999;
            align-items: center;
            justify-content: center;
        }

        .auth-container {
            background: rgba(17, 17, 17, 0.95);
            padding: 3rem;
            border-radius: 20px;
            border: 1px solid var(--border-color);
            box-shadow: 0 25px 50px rgba(0,0,0,0.7);
            width: 100%;
            max-width: 450px;
            text-align: center;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }

        .auth-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, var(--youtube-red) 0%, var(--accent) 100%);
        }

        .auth-logo {
            font-size: 2.8rem;
            font-weight: 800;
            color: var(--youtube-red);
            margin-bottom: 1rem;
            letter-spacing: -1px;
        }

        .auth-logo i {
            margin-right: 12px;
        }

        .auth-subtitle {
            color: var(--text-secondary);
            margin-bottom: 2.5rem;
            font-size: 1.1rem;
            font-weight: 400;
        }

        .form-group {
            margin-bottom: 1.8rem;
            text-align: left;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.8rem;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.95rem;
        }

        .form-group input {
            width: 100%;
            padding: 16px 18px;
            background: rgba(10, 10, 10, 0.8);
            border: 1.5px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
            font-weight: 400;
            backdrop-filter: blur(10px);
        }

        .form-group input:focus {
            outline: none;
            border-color: var(--youtube-red);
            box-shadow: 0 0 0 3px rgba(255,0,0,0.15);
            background: rgba(15, 15, 15, 0.9);
        }

        .btn {
            padding: 16px 32px;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            display: inline-block;
            width: 100%;
            letter-spacing: 0.5px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--youtube-red) 0%, var(--youtube-dark-red) 100%);
            color: white;
            position: relative;
            overflow: hidden;
        }

        .btn-primary::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .btn-primary:hover::before {
            left: 100%;
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(255,0,0,0.3);
        }

        .btn-discord {
            background: linear-gradient(135deg, var(--discord-purple) 0%, #4752c4 100%);
            color: white;
        }

        .btn-discord:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(88, 101, 242, 0.3);
        }

        .auth-switch {
            margin-top: 2rem;
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .auth-switch a {
            color: var(--youtube-red);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }

        .auth-switch a:hover {
            color: var(--accent);
        }

        /* Main Content */
        .main-content {
            display: {% if session.user_id %}block{% else %}none{% endif %};
        }

        /* Header */
        header {
            background: rgba(5, 5, 5, 0.95);
            backdrop-filter: blur(20px);
            padding: 1.2rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid var(--border-color);
        }

        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 2rem;
            font-weight: 800;
            color: var(--youtube-red);
            text-decoration: none;
            display: flex;
            align-items: center;
            letter-spacing: -1px;
        }

        .logo i {
            margin-right: 12px;
            font-size: 2.2rem;
        }

        .nav-links {
            display: flex;
            gap: 2.5rem;
            align-items: center;
        }

        .nav-links a {
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            font-size: 0.95rem;
            position: relative;
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--youtube-red);
            transition: width 0.3s ease;
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        .nav-links a:hover {
            color: var(--youtube-red);
        }

        .user-menu {
            display: flex;
            align-items: center;
            gap: 1.2rem;
        }

        .user-email {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
        }

        .logout-btn {
            background: transparent;
            border: 1.5px solid var(--border-color);
            color: var(--text-secondary);
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            font-size: 0.9rem;
            text-decoration: none;
        }

        .logout-btn:hover {
            border-color: var(--youtube-red);
            color: var(--youtube-red);
            transform: translateY(-2px);
        }

        /* Hero Section */
        .hero {
            margin-top: 80px;
            padding: 8rem 0;
            background: 
                linear-gradient(rgba(5, 5, 5, 0.92), rgba(5, 5, 5, 0.96)),
                url('https://images.unsplash.com/photo-1611162617474-5b21e879e113?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2140&q=80');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(255, 0, 0, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 0, 0, 0.06) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(255, 0, 0, 0.04) 0%, transparent 50%);
            pointer-events: none;
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 900px;
            margin: 0 auto;
        }

        .hero h1 {
            font-size: 4rem;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, #ffffff 0%, var(--youtube-red) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            letter-spacing: -2px;
            line-height: 1.1;
        }

        .hero p {
            font-size: 1.4rem;
            color: var(--text-secondary);
            margin-bottom: 3rem;
            line-height: 1.8;
            font-weight: 400;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }

        .hero-buttons {
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 3rem;
        }

        .hero-btn {
            padding: 18px 35px;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }

        .hero-btn.primary {
            background: linear-gradient(135deg, var(--youtube-red) 0%, var(--youtube-dark-red) 100%);
            color: white;
        }

        .hero-btn.primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(255,0,0,0.3);
        }

        .hero-btn.secondary {
            background: transparent;
            border: 2px solid var(--youtube-red);
            color: var(--youtube-red);
        }

        .hero-btn.secondary:hover {
            background: var(--youtube-red);
            color: white;
            transform: translateY(-3px);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 2.5rem;
            margin-top: 4rem;
            padding: 0 2rem;
        }

        .stat-item {
            text-align: center;
            position: relative;
        }

        .stat-item::before {
            content: '';
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 3px;
            background: var(--youtube-red);
            border-radius: 2px;
        }

        .stat-number {
            font-size: 3rem;
            font-weight: 800;
            color: var(--youtube-red);
            margin-bottom: 0.5rem;
            line-height: 1;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Services Section */
        .services {
            padding: 6rem 0;
            background: var(--darker-bg);
            position: relative;
        }

        .services::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        }

        .section-title {
            text-align: center;
            font-size: 3rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
            font-weight: 800;
            letter-spacing: -1.5px;
        }

        .section-subtitle {
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: 4rem;
            font-size: 1.2rem;
            font-weight: 400;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 2.5rem;
            margin-top: 3rem;
        }

        .service-card {
            background: var(--card-bg);
            padding: 3rem 2.5rem;
            border-radius: 20px;
            border: 1px solid var(--border-color);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            text-align: center;
        }

        .service-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, var(--youtube-red) 0%, var(--accent) 100%);
        }

        .service-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 0, 0, 0.03), transparent);
            transition: left 0.6s;
        }

        .service-card:hover::after {
            left: 100%;
        }

        .service-card:hover {
            transform: translateY(-12px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
            border-color: rgba(255, 0, 0, 0.3);
        }

        .service-icon {
            font-size: 3.5rem;
            color: var(--youtube-red);
            margin-bottom: 2rem;
        }

        .service-card h3 {
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            color: var(--text-primary);
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .service-card p {
            color: var(--text-secondary);
            margin-bottom: 2rem;
            line-height: 1.7;
        }

        .service-features {
            list-style: none;
            margin: 2rem 0;
            text-align: left;
        }

        .service-features li {
            padding: 1rem 0;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border-color);
            font-weight: 400;
            display: flex;
            align-items: center;
        }

        .service-features li:last-child {
            border-bottom: none;
        }

        .service-features li i {
            color: var(--success);
            margin-right: 12px;
            font-size: 1.1rem;
            min-width: 20px;
        }

        .discord-cta {
            background: linear-gradient(135deg, var(--discord-purple) 0%, #4752c4 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }

        .discord-cta:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(88, 101, 242, 0.3);
        }

        /* Dashboard */
        .dashboard {
            padding: 4rem 0;
            background: var(--dark-bg);
            min-height: 60vh;
        }

        .dashboard-welcome {
            background: var(--card-bg);
            padding: 3rem;
            border-radius: 20px;
            border-left: 5px solid var(--youtube-red);
            margin-bottom: 3rem;
            position: relative;
            overflow: hidden;
        }

        .dashboard-welcome::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255,0,0,0.1) 0%, transparent 70%);
            pointer-events: none;
        }

        .dashboard-welcome h2 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            font-weight: 800;
            letter-spacing: -1px;
        }

        .dashboard-welcome p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            line-height: 1.7;
            font-weight: 400;
        }

        .dashboard-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .stat-card {
            background: var(--card-bg);
            padding: 2.5rem 2rem;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            text-align: center;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            border-color: var(--youtube-red);
        }

        .stat-card h3 {
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-bottom: 1rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-card .number {
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--youtube-red);
            line-height: 1;
        }

        /* Flash Messages */
        .flash-messages {
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 1000;
        }

        .flash {
            padding: 1.2rem 1.8rem;
            margin-bottom: 1rem;
            border-radius: 12px;
            color: white;
            animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            min-width: 320px;
            font-weight: 500;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border-left: 4px solid rgba(255,255,255,0.3);
        }

        .flash.success {
            background: linear-gradient(135deg, var(--success) 0%, #00b359 100%);
        }

        .flash.error {
            background: linear-gradient(135deg, var(--youtube-red) 0%, var(--youtube-dark-red) 100%);
        }

        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }

        /* Responsive */
        @media (max-width: 968px) {
            .hero h1 {
                font-size: 3rem;
            }
            
            .services-grid {
                grid-template-columns: 1fr;
            }
            
            .section-title {
                font-size: 2.5rem;
            }
            
            .hero-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .hero-btn {
                width: 100%;
                max-width: 300px;
                justify-content: center;
            }
        }

        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .auth-container {
                margin: 1rem;
                padding: 2.5rem 2rem;
            }
            
            .nav-links {
                display: none;
            }
            
            .stats {
                grid-template-columns: repeat(2, 1fr);
                gap: 2rem;
                padding: 0 1rem;
            }
            
            .stat-number {
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body>
    <!-- Auth Wall -->
    <div class="auth-wall">
        <div class="auth-container">
            <div class="auth-logo">
                <i class="fab fa-youtube"></i>
                ORENDER
            </div>
            <p class="auth-subtitle">Profesyonel YouTube Büyüme Platformu</p>

            <!-- Login Form -->
            <form id="loginForm" method="POST" action="{{ url_for('login') }}" style="display: block;">
                <div class="form-group">
                    <label for="loginEmail"><i class="fas fa-envelope"></i> E-posta</label>
                    <input type="email" id="loginEmail" name="email" placeholder="ornek@gmail.com" required>
                </div>
                <div class="form-group">
                    <label for="loginPassword"><i class="fas fa-lock"></i> Şifre</label>
                    <input type="password" id="loginPassword" name="password" placeholder="Şifrenizi girin" required>
                </div>
                <button type="submit" class="btn btn-primary">Giriş Yap</button>
                <div class="auth-switch">
                    Hesabınız yok mu? <a href="#" onclick="showRegister()">Kayıt Olun</a>
                </div>
            </form>

            <!-- Register Form -->
            <form id="registerForm" method="POST" action="{{ url_for('register') }}" style="display: none;">
                <div class="form-group">
                    <label for="registerEmail"><i class="fas fa-envelope"></i> E-posta</label>
                    <input type="email" id="registerEmail" name="email" placeholder="ornek@gmail.com" required>
                </div>
                <div class="form-group">
                    <label for="registerPassword"><i class="fas fa-lock"></i> Şifre</label>
                    <input type="password" id="registerPassword" name="password" placeholder="Minimum 6 karakter" required>
                </div>
                <div class="form-group">
                    <label for="confirmPassword"><i class="fas fa-lock"></i> Şifre Tekrar</label>
                    <input type="password" id="confirmPassword" name="confirm_password" placeholder="Şifrenizi tekrar girin" required>
                </div>
                <button type="submit" class="btn btn-primary">Kayıt Ol</button>
                <div class="auth-switch">
                    Zaten hesabınız var mı? <a href="#" onclick="showLogin()">Giriş Yapın</a>
                </div>
            </form>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <!-- Flash Messages -->
        <div class="flash-messages">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>

        <!-- Header -->
        <header>
            <div class="container nav-container">
                <a href="#" class="logo">
                    <i class="fab fa-youtube"></i>
                    ORENDER
                </a>
                <nav class="nav-links">
                    <a href="#services"><i class="fas fa-rocket"></i> Hizmetler</a>
                    <a href="#dashboard"><i class="fas fa-chart-line"></i> Dashboard</a>
                    <a href="https://discord.gg/gqQGwzrN7t" target="_blank"><i class="fab fa-discord"></i> Discord</a>
                    <div class="user-menu">
                        <span class="user-email">{{ session.email if session.email else '' }}</span>
                        <a href="{{ url_for('logout') }}" class="logout-btn">
                            <i class="fas fa-sign-out-alt"></i> Çıkış
                        </a>
                    </div>
                </nav>
            </div>
        </header>

        <!-- Hero Section -->
        <section class="hero">
            <div class="container hero-content">
                <h1>YouTube Kanalınızı Profesyonelce Büyütün</h1>
                <p>Gerçek kullanıcı etkileşimi, güvenli büyüme stratejileri ve premium hizmetlerle YouTube algoritmasında üst sıralara çıkın</p>
                
                <div class="hero-buttons">
                    <a href="#services" class="hero-btn primary">
                        <i class="fas fa-rocket"></i> Hizmetleri Gör
                    </a>
                    <a href="https://discord.gg/gqQGwzrN7t" target="_blank" class="hero-btn secondary">
                        <i class="fab fa-discord"></i> Discord'a Katıl
                    </a>
                </div>
                
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number">10K+</div>
                        <div class="stat-label">Mutlu Müşteri</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">500K+</div>
                        <div class="stat-label">Başarılı İşlem</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">99.8%</div>
                        <div class="stat-label">Başarı Oranı</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">7/24</div>
                        <div class="stat-label">Destek</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Services Section -->
        <section id="services" class="services">
            <div class="container">
                <h2 class="section-title">Premium Hizmetlerimiz</h2>
                <p class="section-subtitle">YouTube algoritmasına uyumlu, güvenli ve etkili büyüme çözümleri</p>
                
                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <h3>YouTube Abone Paketi</h3>
                        <p>Gerçek ve aktif kullanıcılardan organik abone kazanın</p>
                        <ul class="service-features">
                            <li><i class="fas fa-check"></i> Gerçek kullanıcı etkileşimi</li>
                            <li><i class="fas fa-check"></i> Yavaş ve doğal büyüme</li>
                            <li><i class="fas fa-check"></i> YouTube TOS uyumlu</li>
                            <li><i class="fas fa-check"></i> 30 gün garantili</li>
                        </ul>
                        <a href="https://discord.gg/gqQGwzrN7t" target="_blank" class="discord-cta">
                            <i class="fab fa-discord"></i> Fiyat için Discord
                        </a>
                    </div>

                    <div class="service-card">
                        <div class="service-icon">
                            <i class="fas fa-eye"></i>
                        </div>
                        <h3>YouTube İzlenme Artırma</h3>
                        <p>Videolarınızın önerilere çıkmasını sağlayın</p>
                        <ul class="service-features">
                            <li><i class="fas fa-check"></i> Yüksek tutma oranı</li>
                            <li><i class="fas fa-check"></i> Organik izlenme patterni</li>
                            <li><i class="fas fa-check"></i> SEO optimizasyonu</li>
                            <li><i class="fas fa-check"></i> Anlık başlangıç</li>
                        </ul>
                        <a href="https://discord.gg/gqQGwzrN7t" target="_blank" class="discord-cta">
                            <i class="fab fa-discord"></i> Fiyat için Discord
                        </a>
                    </div>

                    <div class="service-card">
                        <div class="service-icon">
                            <i class="fas fa-comments"></i>
                        </div>
                        <h3>YouTube Yorum Hizmeti</h3>
                        <p>Özgün ve etkileşim artırıcı yorumlar</p>
                        <ul class="service-features">
                            <li><i class="fas fa-check"></i> Özenle yazılmış yorumlar</li>
                            <li><i class="fas fa-check"></i> Türkçe/İngilizce seçenek</li>
                            <li><i class="fas fa-check"></i> Spam filtresine takılmaz</li>
                            <li><i class="fas fa-check"></i> Etkileşim artışı</li>
                        </ul>
                        <a href="https://discord.gg/gqQGwzrN7t" target="_blank" class="discord-cta">
                            <i class="fab fa-discord"></i> Fiyat için Discord
                        </a>
                    </div>

                    <div class="service-card">
                        <div class="service-icon">
                            <i class="fas fa-bolt"></i>
                        </div>
                        <h3>Shorts Görüntülenme</h3>
                        <p>Shorts videolarınızı viral yapın</p>
                        <ul class="service-features">
                            <li><i class="fas fa-check"></i> Hızlı görüntülenme</li>
                            <li><i class="fas fa-check"></i> Explore'a çıkma garantisi</li>
                            <li><i class="fas fa-check"></i> Yüksek etkileşim oranı</li>
                            <li><i class="fas fa-check"></i> Mobil uyumlu</li>
                        </ul>
                        <a href="https://discord.gg/gqQGwzrN7t" target="_blank" class="discord-cta">
                            <i class="fab fa-discord"></i> Fiyat için Discord
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- Dashboard -->
        <section id="dashboard" class="dashboard">
            <div class="container">
                <div class="dashboard-welcome">
                    <h2>Hoş Geldiniz, {{ session.email if session.email else 'Kullanıcı' }}!</h2>
                    <p>YouTube büyüme yolculuğunuzda yanınızdayız. Premium hizmetlerimizle kanalınızı bir üst seviyeye taşıyın ve YouTube algoritmasında öne çıkın. Gerçek etkileşim, güvenli büyüme ve profesyonel destek ile başarıya ulaşın.</p>
                    <div style="margin-top: 2rem;">
                        <a href="https://discord.gg/gqQGwzrN7t" target="_blank" class="btn btn-discord" style="width: auto; padding: 15px 30px;">
                            <i class="fab fa-discord"></i> Discord Topluluğumuza Katıl
                        </a>
                    </div>
                </div>

                <div class="dashboard-stats">
                    <div class="stat-card">
                        <h3>Toplam Harcama</h3>
                        <div class="number">$0.00</div>
                    </div>
                    <div class="stat-card">
                        <h3>Tamamlanan Sipariş</h3>
                        <div class="number">0</div>
                    </div>
                    <div class="stat-card">
                        <h3>Devam Eden Sipariş</h3>
                        <div class="number">0</div>
                    </div>
                    <div class="stat-card">
                        <h3>Kullanıcı Puanı</h3>
                        <div class="number">5.0</div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <script>
        function showRegister() {
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('registerForm').style.display = 'block';
        }

        function showLogin() {
            document.getElementById('registerForm').style.display = 'none';
            document.getElementById('loginForm').style.display = 'block';
        }

        // Auto-hide flash messages
        setTimeout(() => {
            document.querySelectorAll('.flash').forEach(flash => {
                flash.style.animation = 'slideOut 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
                setTimeout(() => flash.remove(), 400);
            });
        }, 5000);

        // Check auth status
        {% if session.user_id %}
            document.querySelector('.auth-wall').style.display = 'none';
            document.querySelector('.main-content').style.display = 'block';
        {% endif %}

        // Smooth scroll for anchor links
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
    </script>
</body>
</html>
'''

def get_db_connection():
    """Get database connection with retry logic"""
    max_retries = 5
    for i in range(max_retries):
        try:
            conn = sqlite3.connect('users.db', timeout=30)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and i < max_retries - 1:
                time.sleep(0.1)
                continue
            else:
                raise e

def init_db():
    """Initialize database"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            flash('Başarıyla giriş yapıldı!', 'success')
            return redirect(url_for('index'))
        else:
            flash('E-posta veya şifre hatalı!', 'error')
            return render_template_string(HTML_TEMPLATE)
    except Exception as e:
        flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'error')
        return render_template_string(HTML_TEMPLATE)

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if len(password) < 6:
        flash('Şifre en az 6 karakter olmalıdır!', 'error')
        return render_template_string(HTML_TEMPLATE)
    
    if password != confirm_password:
        flash('Şifreler eşleşmiyor!', 'error')
        return render_template_string(HTML_TEMPLATE)
    
    hashed_password = generate_password_hash(password)
    
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                 (email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        flash('Bu e-posta zaten kayıtlı!', 'error')
        return render_template_string(HTML_TEMPLATE)
    except Exception as e:
        flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'error')
        return render_template_string(HTML_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    flash('Başarıyla çıkış yapıldı!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
