<template>
  <main class="page">
    <nav class="navbar">
      <div class="logo">NST Studio</div>

      <div class="nav-links">
        <a href="#upload">Yükle</a>
        <span></span>
        <a href="#styles">Stiller</a>
        <span></span>
        <a href="#result">Sonuç</a>
      </div>
    </nav>

    <section class="hero">
      <div class="hero-badge">Fotoğraf ve sanat stilini yapay zekâ ile buluştur.</div>
      <h1>Görselinizi sanatsal bir esere dönüştürmek için stilimiz hazır!</h1>
      <p>
        Content image yapısını koruyarak seçtiğin style image dokusunu, renklerini ve
        atmosferini fotoğrafına uygular.
      </p>
    </section>

    <section
      class="workflow"
      id="upload"
    >
      <div class="panel">
        <div class="step-label">01 / Content Image</div>
        <h2>Fotoğrafını yükle</h2>
        <p class="muted">
          Portre, manzara, şehir veya ürün fotoğrafı yükleyebilirsin. Sistem bu görselin
          ana yapısını koruyup seçtiğin sanat stilini üzerine uygular.
        </p>

        <label class="upload-box">
          <input
            type="file"
            accept="image/*"
            @change="handleContentUpload"
          />
          <span v-if="!contentPreview">Görsel seç veya buraya yükle</span>
          <img
            v-else
            :src="contentPreview"
            alt="Content Preview"
          />
        </label>
      </div>

      <div
        class="panel"
        id="styles"
      >
        <div class="step-label">02 / Style Image</div>
        <h2>Sanat stilini seç</h2>
        <p class="muted">
          Seçtiğin style image, fotoğrafın renklerini, fırça dokusunu ve sanatsal
          atmosferini belirler.
        </p>

        <div class="style-grid">
          <button
            v-for="style in styles"
            :key="style.name"
            class="style-card"
            :class="{ active: selectedStyle === style.name }"
            @click="selectedStyle = style.name"
          >
            <img
              :src="style.url"
              :alt="style.name"
            />
            <span>{{ cleanStyleName(style.name) }}</span>
          </button>
        </div>
      </div>
    </section>

    <section class="action-section">
      <button
        class="generate-btn"
        :disabled="loading"
        @click="generateImage"
      >
        {{ loading ? "Görsel oluşturuluyor..." : "Style Transfer Başlat" }}
      </button>

      <div
        v-if="loading"
        class="loading-card"
      >
        <div class="spinner"></div>
        <div>
          <h3>AI görseli işliyor...</h3>
          <p>Content image analiz ediliyor, seçilen style image dokusu görsele uygulanıyor.</p>
        </div>
      </div>
    </section>

    <section
      v-if="resultImage"
      class="result-section"
      id="result"
    >
      <div class="result-header">
        <div>
          <div class="step-label">03 / Output Result</div>
          <h2>Sanatsal Dönüşüm Sonucu</h2>
          <p class="muted">
            Fotoğrafın ana kompozisyonu korunarak seçilen stilin renk, doku ve atmosfer
            bilgisi görsele aktarıldı.
          </p>
        </div>

        <div class="result-actions">
          <button
            class="download-btn"
            @click="downloadImage"
          >Görseli İndir</button>
          <button
            class="mockup-btn"
            @click="showMockup = true"
          >
            Sanatsal Tişört Baskısı Olarak Gör
          </button>
        </div>
      </div>

      <div class="comparison-grid">
        <div class="compare-card">
          <span>Original Content</span>
          <img
            :src="contentPreview"
            alt="Original Content"
          />
        </div>

        <div class="compare-card">
          <span>Generated Artwork</span>
          <img
            :src="resultImage"
            alt="Generated Result"
          />
        </div>
      </div>

      <div class="info-strip">
        <div>
          <strong>Content</strong>
          <span>Kullanıcı görseli</span>
        </div>
        <div>
          <strong>Style</strong>
          <span>{{ cleanStyleName(selectedStyle) }}</span>
        </div>
        <div>
          <strong>Model</strong>
          <span>VGG19 Neural Style Transfer</span>
        </div>
      </div>
    </section>

    <section
      v-if="showMockup && resultImage"
      class="mockup-section"
    >
      <div class="mockup-header">
        <div class="step-label">04 / Product Mockup</div>
        <h2>Tişört Baskı Önizlemesi</h2>
        <p class="muted">
          Oluşturulan yapay zekâ görseli ön yüzde sol göğüs alanına, arka yüzde ise büyük
          sırt baskısı olarak yerleştirildi.
        </p>
      </div>

      <div class="color-selector">
        <button
          :class="{ active: selectedTshirtColor === 'white' }"
          @click="selectedTshirtColor = 'white'"
        >
          Beyaz Tişört
        </button>

        <button
          :class="{ active: selectedTshirtColor === 'black' }"
          @click="selectedTshirtColor = 'black'"
        >
          Siyah Tişört
        </button>
      </div>

      <div class="mockup-grid">
        <div class="tshirt-card">
          <span>Ön Baskı</span>

          <div class="tshirt-canvas">
            <img
              class="tshirt-base"
              :src="tshirtMockups[selectedTshirtColor].front"
              alt="Tshirt Front"
            />
            <img
              class="print-image front-print"
              :src="resultImage"
              alt="Front Print"
            />
          </div>
        </div>

        <div class="tshirt-card">
          <span>Arka Baskı</span>

          <div class="tshirt-canvas">
            <img
              class="tshirt-base"
              :src="tshirtMockups[selectedTshirtColor].back"
              alt="Tshirt Back"
            />
            <img
              class="print-image back-print"
              :src="resultImage"
              alt="Back Print"
            />
          </div>
        </div>
      </div>
    </section>
    <button
      v-if="showScrollTop"
      class="scroll-top-btn"
      @click="scrollToTop"
    >
      ↑
    </button>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import api from "./services/api";

import blackBack from "./assets/tshirts/black-back.png";
import blackFront from "./assets/tshirts/black-front.png";
import whiteBack from "./assets/tshirts/white-back.png";
import whiteFront from "./assets/tshirts/white-front.png";

const styles = ref([]);
const selectedStyle = ref("");
const contentFile = ref(null);
const contentPreview = ref("");
const resultImage = ref("");
const loading = ref(false);

const showMockup = ref(false);
const selectedTshirtColor = ref("white");
const showScrollTop = ref(false);

const tshirtMockups = {
  white: {
    front: whiteFront,
    back: whiteBack,
  },
  black: {
    front: blackFront,
    back: blackBack,
  },
};

const getStyles = async () => {
  try {
    const { data } = await api.get("/styles");
    styles.value = data;
    selectedStyle.value = data[0]?.name || "";
  } catch (error) {
    console.error("Style listesi alınamadı:", error);
  }
};

const handleContentUpload = (event) => {
  const file = event.target.files?.[0];
  if (!file) return;

  contentFile.value = file;
  contentPreview.value = URL.createObjectURL(file);
  resultImage.value = "";
  showMockup.value = false;
};

const generateImage = async () => {
  if (!contentFile.value) {
    alert("Lütfen önce bir fotoğraf yükle.");
    return;
  }

  if (!selectedStyle.value) {
    alert("Lütfen bir style image seç.");
    return;
  }

  loading.value = true;
  resultImage.value = "";
  showMockup.value = false;

  try {
    const formData = new FormData();
    formData.append("content", contentFile.value);
    formData.append("style_name", selectedStyle.value);

    const response = await api.post("/style-transfer", formData, {
      responseType: "blob",
    });

    resultImage.value = URL.createObjectURL(response.data);
  } catch (error) {
    console.error("Style transfer hatası:", error);
    alert("Görsel oluşturulurken hata oluştu.");
  } finally {
    loading.value = false;
  }
};

const downloadImage = () => {
  if (!resultImage.value) return;

  const link = document.createElement("a");
  link.href = resultImage.value;
  link.download = "neural-style-transfer-result.jpg";
  link.click();
};

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
};

const cleanStyleName = (name) => {
  return name
    .replace(/\.[^/.]+$/, "")
    .replace(/[-_]/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

onMounted(() => {
  getStyles();

  window.addEventListener("scroll", () => {
    showScrollTop.value = window.scrollY > 500;
  });
});
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.page {
  width: 100%;
  min-height: 100vh;
  padding: 0 72px 80px;
  background: #ffffff;
  color: #111111;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Navbar */
.navbar {
  width: 100%;
  height: 92px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  color: #111111;
  font-size: 30px;
  font-weight: 900;
  letter-spacing: -1px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav-links a {
  color: #111111;
  text-decoration: none;
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}

.nav-links span {
  width: 28px;
  height: 1px;
  background: #cfcfcf;
}

.nav-links a:hover {
  color: #777777;
}

/* Hero */
.hero {
  max-width: 900px;
  margin: 0 auto 90px;
  padding-top: 80px;
  text-align: center;
}

.hero-badge {
  margin-bottom: 22px;
  color: #666666;
  font-size: 15px;
}

.hero h1 {
  max-width: 760px;
  margin: 0 auto;
  color: #111111;
  font-size: clamp(42px, 5vw, 68px);
  line-height: 1.18;
  letter-spacing: -2.5px;
  font-weight: 800;
}

.hero p {
  max-width: 680px;
  margin: 28px auto 0;
  color: #555555;
  font-size: 17px;
  line-height: 1.8;
}

/* Shared */
.workflow,
.action-section,
.result-section,
.mockup-section {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.workflow,
.action-section {
  max-width: 1500px;
}

.step-label {
  margin-bottom: 14px;
  color: #777777;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1.6px;
  text-transform: uppercase;
}

h2 {
  margin: 0 0 12px;
  color: #111111;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.8px;
}

.muted {
  max-width: 620px;
  margin-bottom: 26px;
  color: #555555;
  font-size: 15px;
  line-height: 1.8;
}

button {
  cursor: pointer;
  font-weight: 800;
  transition: 0.25s ease;
}

/* Workflow */
.workflow {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 54px;
  align-items: start;
}

.panel {
  padding: 0;
  background: transparent;
  border: none;
}

.upload-box {
  width: 100%;
  min-height: 520px;
  padding: 24px;
  background: #f3f3f3;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
  transition: 0.25s ease;
}

.upload-box:hover {
  background: #e9e9e9;
}

.upload-box input {
  display: none;
}

.upload-box span {
  color: #8b8b8b;
  font-size: 17px;
  font-weight: 700;
}

.upload-box img {
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 620px;
  object-fit: contain;
  display: block;
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 26px;
  margin-top: 34px;
}

.style-card {
  padding: 0;
  background: transparent;
  border: none;
  color: #111111;
  text-align: center;
}

.style-card:hover {
  transform: translateY(-5px);
}

.style-card.active img {
  outline: 4px solid #111111;
  outline-offset: -4px;
}

.style-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
  background: #eeeeee;
}

.style-card span {
  display: block;
  margin-top: 12px;
  color: #111111;
  font-size: 18px;
  font-weight: 800;
}

/* Actions */
.action-section {
  margin-top: 70px;
  margin-bottom: 70px;
  text-align: center;
}

.generate-btn,
.download-btn {
  border: none;
  background: #111111;
  color: #ffffff;
}

.generate-btn {
  min-width: 320px;
  padding: 18px 40px;
  font-size: 16px;
  letter-spacing: 0.3px;
}

.generate-btn:hover:not(:disabled),
.download-btn:hover {
  background: #444444;
}

.generate-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.loading-card {
  max-width: 620px;
  margin: 28px auto 0;
  padding: 24px;
  background: #f4f4f4;
  display: flex;
  gap: 18px;
  align-items: center;
  text-align: left;
}

.spinner {
  width: 42px;
  height: 42px;
  border: 3px solid #d6d6d6;
  border-top-color: #111111;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
  flex-shrink: 0;
}

.loading-card h3 {
  margin: 0 0 6px;
  color: #111111;
  font-size: 18px;
}

.loading-card p {
  margin: 0;
  color: #8f8f8f;
  font-size: 14px;
  line-height: 1.6;
}

/* Result */
.result-section {
  max-width: 1200px;
  text-align: center;
}

.result-header {
  margin-bottom: 34px;
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: end;
  text-align: left;
}

.result-actions {
  display: flex;
  gap: 14px;
  align-items: center;
}

.download-btn,
.mockup-btn {
  padding: 14px 30px;
  font-size: 15px;
}

.mockup-btn {
  background: #ffffff;
  color: #111111;
  border: 1px solid #111111;
}

.mockup-btn:hover {
  background: #eeeeee;
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 34px;
  margin-top: 30px;
}

.compare-card {
  padding: 18px;
  background: #f4f4f4;
}

.compare-card span {
  display: block;
  margin-bottom: 14px;
  color: #111111;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.4px;
}

.compare-card img {
  width: 100%;
  height: 520px;
  object-fit: contain;
  display: block;
  background: #ffffff;
}

.info-strip {
  margin-top: 28px;
  border-top: 1px solid #111111;
  border-bottom: 1px solid #111111;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

.info-strip div {
  padding: 22px;
  border-right: 1px solid #111111;
}

.info-strip div:last-child {
  border-right: none;
}

.info-strip strong {
  display: block;
  margin-bottom: 8px;
  color: #111111;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1.4px;
}

.info-strip span {
  color: #555555;
  font-size: 15px;
}

/* Mockup */
.mockup-section {
  max-width: 1400px;
  margin-top: 90px;
}

.mockup-header {
  max-width: 820px;
  margin: 0 auto 34px;
  text-align: center;
}

.mockup-header .muted {
  margin-left: auto;
  margin-right: auto;
}

.color-selector {
  margin-bottom: 42px;
  display: flex;
  justify-content: center;
  gap: 16px;
}

.color-selector button {
  padding: 14px 34px;
  background: #ffffff;
  color: #111111;
  border: 1px solid #111111;
}

.color-selector button.active {
  background: #111111;
  color: #ffffff;
}

.mockup-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 46px;
}

.tshirt-card {
  padding: 26px;
  background: #f4f4f4;
  text-align: center;
}

.tshirt-card>span {
  display: block;
  margin-bottom: 20px;
  color: #111111;
  font-size: 22px;
  font-weight: 900;
}

.tshirt-canvas {
  position: relative;
  width: 100%;
  min-height: 640px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.tshirt-base {
  position: relative;
  z-index: 1;
  width: 100%;
  max-height: 640px;
  object-fit: contain;
  display: block;
}

.print-image {
  position: absolute;
  z-index: 2;
  object-fit: contain;
  pointer-events: none;
}

.front-print {
  width: 13%;
  top: 31%;
  left: 52%;
}

.back-print {
  width: 28%;
  top: 29%;
  left: 50%;
  transform: translateX(-50%);
}

/* Responsive */
@media (max-width: 1000px) {
  .page {
    padding: 0 24px 60px;
  }

  .hero {
    padding-top: 90px;
    margin-bottom: 60px;
  }

  .workflow,
  .comparison-grid,
  .mockup-grid {
    grid-template-columns: 1fr;
  }

  .style-grid {
    grid-template-columns: 1fr;
  }

  .upload-box {
    min-height: 420px;
  }

  .result-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .result-actions {
    width: 100%;
    flex-direction: column;
  }

  .mockup-btn,
  .download-btn {
    width: 100%;
  }

  .info-strip {
    grid-template-columns: 1fr;
  }

  .info-strip div {
    border-right: none;
    border-bottom: 1px solid #111111;
  }

  .info-strip div:last-child {
    border-bottom: none;
  }

  .tshirt-canvas {
    min-height: 460px;
  }
}

@media (max-width: 700px) {
  .navbar {
    height: auto;
    padding: 28px 0;
    flex-direction: column;
    gap: 18px;
  }

  .nav-links {
    gap: 16px;
  }

  .nav-links span {
    width: 18px;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.scroll-top-btn {
  position: fixed;
  right: 34px;
  bottom: 34px;
  width: 58px;
  height: 58px;
  border: none;
  background: #111111;
  color: #ffffff;
  font-size: 26px;
  font-weight: 900;
  cursor: pointer;
  z-index: 999;
  transition: 0.25s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

.scroll-top-btn:hover {
  transform: translateY(-4px);
  background: #333333;
}
</style>