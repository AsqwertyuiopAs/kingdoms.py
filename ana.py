import os
import json
import uuid
import base64
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.secret_key = '8.04.2026-secret-key'

# ==================== DİSK KALICI VERİ ====================
DATA_DIR = os.environ.get('DATA_DIR', '.')
DATA_FILE = os.path.join(DATA_DIR, 'anilar.json')

def load_anilar():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_anilar(anilar):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(anilar, f, ensure_ascii=False, indent=2)

HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>8.04.2026 | Anı Kutusu</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Cormorant+Garamond:wght@300;400;500;600&family=Sora:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #000000; color: #ffffff; font-family: 'Inter', sans-serif; font-weight: 300; }
        .loading-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000000; display: flex; justify-content: center; align-items: center; z-index: 10000; transition: opacity 0.6s ease; }
        .loading-content { text-align: center; }
        .loading-spinner { width: 48px; height: 48px; border: 1px solid #222; border-top: 1px solid #fff; border-radius: 50%; margin: 0 auto 2rem; animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .progress-bar-bg { width: 300px; max-width: 70vw; background: #111; height: 1px; margin: 1rem auto; }
        .progress-bar-fill { background: #fff; height: 1px; width: 0%; transition: width 0.03s linear; }
        .progress-text { margin-top: 1rem; font-family: 'Sora', monospace; font-size: 2rem; letter-spacing: 6px; }
        .site-wrapper { opacity: 0; transition: opacity 0.6s ease; }
        .site-wrapper.visible { opacity: 1; }
        .container { max-width: 1280px; margin: 0 auto; padding: 3rem 2rem; }
        .header { text-align: center; padding: 2rem 0 3rem; border-bottom: 1px solid #111; margin-bottom: 3rem; }
        .header h1 { font-family: 'Cormorant Garamond', serif; font-size: 4.5rem; font-weight: 400; letter-spacing: 8px; }
        .header p { font-size: 0.7rem; letter-spacing: 4px; color: #666; margin-top: 0.5rem; }
        .upload-panel { background: #050505; border: 1px solid #151515; padding: 2rem; margin-bottom: 3rem; }
        .upload-panel h3 { font-size: 0.7rem; letter-spacing: 4px; color: #888; margin-bottom: 1.5rem; text-transform: uppercase; }
        .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
        .form-field { display: flex; flex-direction: column; gap: 0.5rem; }
        .form-field.full { grid-column: span 2; }
        .form-field label { font-size: 0.55rem; letter-spacing: 2px; color: #555; text-transform: uppercase; }
        .form-field input, .form-field select { background: #000; border: 1px solid #222; padding: 0.8rem; color: #fff; font-size: 0.85rem; }
        .form-field input:focus, .form-field select:focus { outline: none; border-color: #444; }
        .color-row { display: flex; gap: 0.75rem; align-items: center; }
        .color-preview { width: 44px; height: 44px; border: 1px solid #222; }
        .btn-submit { background: #fff; color: #000; border: none; padding: 1rem; font-size: 0.7rem; letter-spacing: 4px; font-weight: 600; cursor: pointer; transition: all 0.3s; width: 100%; margin-top: 1rem; text-transform: uppercase; }
        .btn-submit:hover { background: #1a1a1a; color: #fff; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 2rem; margin-top: 2rem; }
        .memory-card { background: #0a0a0a; border: 1px solid #151515; transition: transform 0.3s ease; }
        .memory-card:hover { transform: translateY(-5px); border-color: #2a2a2a; }
        .memory-card img { width: 100%; height: 380px; object-fit: cover; display: block; }
        .memory-content { padding: 1.5rem; }
        .memory-title { font-size: 1.1rem; font-weight: 500; letter-spacing: 1px; margin-bottom: 0.5rem; }
        .memory-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #151515; }
        .memory-date { font-size: 0.55rem; color: #555; }
        .delete-btn { background: none; border: 1px solid #2a2a2a; color: #666; padding: 0.3rem 0.9rem; font-size: 0.55rem; cursor: pointer; transition: all 0.2s; }
        .delete-btn:hover { border-color: #ff4444; color: #ff4444; }
        .empty { text-align: center; padding: 4rem; color: #333; font-size: 0.7rem; letter-spacing: 3px; border: 1px dashed #1a1a1a; }
        .footer { text-align: center; margin-top: 4rem; padding: 2rem; border-top: 1px solid #111; font-size: 0.55rem; color: #2a2a2a; letter-spacing: 3px; }
        @media (max-width: 768px) {
            .container { padding: 1.5rem; }
            .header h1 { font-size: 2.5rem; }
            .form-grid { grid-template-columns: 1fr; }
            .gallery { grid-template-columns: 1fr; }
            .memory-card img { height: 280px; }
        }
        ::selection { background: #222; color: #fff; }
    </style>
</head>
<body>
<div class="loading-screen" id="loadingScreen">
    <div class="loading-content">
        <div class="loading-spinner"></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" id="progressFill"></div></div>
        <div class="progress-text" id="progressPercent">0%</div>
        <div style="font-size:0.6rem; color:#333; margin-top:0.5rem;">8.04.2026</div>
    </div>
</div>
<div class="site-wrapper" id="siteWrapper">
    <div class="container">
        <div class="header">
            <h1>8.04.2026</h1>
            <p>ANI KUTUSU</p>
        </div>
        <div class="upload-panel">
            <h3>✦ YENİ ANI EKLE ✦</h3>
            <form id="memoryForm" enctype="multipart/form-data">
                <div class="form-grid">
                    <div class="form-field full">
                        <label>GÖRSEL YÜKLE</label>
                        <input type="file" name="image" accept="image/*" required>
                    </div>
                    <div class="form-field">
                        <label>BAŞLIK</label>
                        <input type="text" name="title" placeholder="Anı başlığı..." required>
                    </div>
                    <div class="form-field">
                        <label>BAŞLIK RENGİ</label>
                        <div class="color-row">
                            <input type="color" name="titleColor" value="#ffffff" id="colorInput">
                            <div class="color-preview" id="colorPreview" style="background:#ffffff;"></div>
                        </div>
                    </div>
                    <div class="form-field">
                        <label>BAŞLIK FONTU</label>
                        <select name="titleFont">
                            <option value="'Inter', sans-serif">Modern (Inter)</option>
                            <option value="'Cormorant Garamond', serif">Elegant (Cormorant)</option>
                            <option value="'Sora', sans-serif">Premium (Sora)</option>
                        </select>
                    </div>
                </div>
                <button type="submit" class="btn-submit">✦ ANIYI EKLE ✦</button>
            </form>
        </div>
        <div class="gallery" id="gallery"></div>
        <div class="footer"><span>8.04.2026 · PREMIUM MEMORY ARCHIVE</span></div>
    </div>
</div>
<script>
    let memories = [];
    let progress = 0;
    const fill = document.getElementById('progressFill');
    const percent = document.getElementById('progressPercent');
    const loadingScreen = document.getElementById('loadingScreen');
    const siteWrapper = document.getElementById('siteWrapper');
    const timer = setInterval(() => {
        progress += 2.86;
        if (progress >= 100) {
            progress = 100;
            clearInterval(timer);
            setTimeout(() => {
                loadingScreen.style.opacity = '0';
                setTimeout(() => {
                    loadingScreen.style.display = 'none';
                    siteWrapper.classList.add('visible');
                }, 500);
            }, 200);
        }
        if (fill) fill.style.width = progress + '%';
        if (percent) percent.innerText = Math.floor(progress) + '%';
    }, 100);
    function renderGallery() {
        const gallery = document.getElementById('gallery');
        if (!gallery) return;
        if (memories.length === 0) {
            gallery.innerHTML = '<div class="empty">📭 HENÜZ HİÇ ANI YOK</div>';
            return;
        }
        gallery.innerHTML = memories.map(m => `
            <div class="memory-card" data-id="${m.id}">
                <img src="${m.imageData}" alt="${m.title}">
                <div class="memory-content">
                    <div class="memory-title" style="color: ${m.titleColor}; font-family: ${m.titleFont};">${escapeHtml(m.title)}</div>
                    <div class="memory-footer">
                        <span class="memory-date">${m.date}</span>
                        <button class="delete-btn" onclick="deleteMemory('${m.id}')">SİL</button>
                    </div>
                </div>
            </div>
        `).join('');
    }
    async function loadMemories() {
        try {
            const res = await fetch('/api/anilar');
            memories = await res.json();
            renderGallery();
        } catch(e) { console.error(e); }
    }
    document.getElementById('memoryForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const btn = e.target.querySelector('.btn-submit');
        btn.textContent = '✦ YÜKLENİYOR ✦';
        btn.disabled = true;
        try {
            const res = await fetch('/api/ekle', { method: 'POST', body: formData });
            const data = await res.json();
            if (data.success) {
                await loadMemories();
                e.target.reset();
                showToast('✓ Anı eklendi');
                document.getElementById('colorPreview').style.background = '#ffffff';
            } else {
                showToast('✗ Hata: ' + data.error);
            }
        } catch(e) { showToast('✗ Bağlantı hatası'); }
        finally { btn.textContent = '✦ ANIYI EKLE ✦'; btn.disabled = false; }
    });
    async function deleteMemory(id) {
        if (!confirm('Bu anıyı silmek istediğinize emin misiniz?')) return;
        try {
            const res = await fetch(`/api/sil/${id}`, { method: 'DELETE' });
            const data = await res.json();
            if (data.success) { await loadMemories(); showToast('✓ Anı silindi'); }
            else { showToast('✗ Silme hatası'); }
        } catch(e) { showToast('✗ Hata oluştu'); }
    }
    function showToast(msg) {
        const toast = document.createElement('div');
        toast.textContent = msg;
        toast.style.cssText = 'position:fixed; bottom:25px; right:25px; background:#0a0a0a; color:#fff; padding:0.8rem 1.5rem; font-size:0.65rem; letter-spacing:2px; z-index:10001; border-left:2px solid #fff; font-family:monospace;';
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
    function escapeHtml(str) { if (!str) return ''; return String(str).replace(/[&<>]/g, function(m) { if (m === '&') return '&amp;'; if (m === '<') return '&lt;'; if (m === '>') return '&gt;'; return m; }); }
    document.getElementById('colorInput')?.addEventListener('input', (e) => { document.getElementById('colorPreview').style.background = e.target.value; });
    loadMemories();
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/anilar')
def get_anilar():
    return jsonify(load_anilar())

@app.route('/api/ekle', methods=['POST'])
def add_ani():
    try:
        title = request.form.get('title', 'İsimsiz')
        title_color = request.form.get('titleColor', '#ffffff')
        title_font = request.form.get('titleFont', "'Inter', sans-serif")
        image_file = request.files.get('image')
        if not image_file:
            return jsonify({'success': False, 'error': 'Görsel gerekli'})
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        image_src = f'data:{image_file.content_type};base64,{image_data}'
        ani = {
            'id': str(uuid.uuid4())[:8],
            'title': title,
            'titleColor': title_color,
            'titleFont': title_font,
            'imageData': image_src,
            'date': datetime.now().strftime('%d.%m.%Y · %H:%M')
        }
        anilar = load_anilar()
        anilar.insert(0, ani)
        save_anilar(anilar)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sil/<ani_id>', methods=['DELETE'])
def delete_ani(ani_id):
    try:
        anilar = load_anilar()
        anilar = [a for a in anilar if a['id'] != ani_id]
        save_anilar(anilar)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
