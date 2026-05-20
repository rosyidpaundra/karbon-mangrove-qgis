#!/bin/bash
# =============================================================
#  setup_github.sh — Upload karbon-mangrove-qgis ke GitHub
#  Jalankan: bash setup_github.sh
# =============================================================

# ── Konfigurasi — EDIT BAGIAN INI ────────────────────────────
GITHUB_USERNAME="USERNAME_GITHUB_ANDA"
REPO_NAME="karbon-mangrove-qgis"
# ─────────────────────────────────────────────────────────────

echo ""
echo "🌿 Setup Repository: $REPO_NAME"
echo "=================================================="

# 1. Inisialisasi git
git init
git branch -M main

# 2. Tambahkan semua file
git add .
git commit -m "🌿 Initial commit: AGC Mangrove RF Plugin for QGIS"

# 3. Hubungkan ke GitHub
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

# 4. Push
echo ""
echo "📤 Mendorong ke GitHub..."
git push -u origin main

echo ""
echo "✅ Selesai! Repository tersedia di:"
echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
