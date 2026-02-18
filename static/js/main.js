// Exproperty - Main JS

// Track enquiry clicks (phone/WhatsApp)
function trackEnquiry(propertyId, action) {
    fetch('/api/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ property_id: propertyId, action: action })
    }).catch(() => {});
}

// WhatsApp click
document.addEventListener('click', function(e) {
    const wa = e.target.closest('.btn-whatsapp');
    if (wa && wa.dataset.propertyId) {
        trackEnquiry(wa.dataset.propertyId, 'whatsapp_click');
    }
    const ph = e.target.closest('.btn-phone');
    if (ph && ph.dataset.propertyId) {
        trackEnquiry(ph.dataset.propertyId, 'phone_click');
    }
});

// Image upload preview
function previewImages(input) {
    const container = document.getElementById('imagePreviewContainer');
    if (!container) return;
    container.innerHTML = '';
    if (input.files) {
        Array.from(input.files).forEach((file, i) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.className = 'd-inline-block position-relative me-2 mb-2';
                div.innerHTML = `<img src="${e.target.result}" class="img-upload-preview" alt="Preview ${i+1}">`;
                container.appendChild(div);
            };
            reader.readAsDataURL(file);
        });
    }
}

// Share button
function shareProperty(url, title) {
    if (navigator.share) {
        navigator.share({ title: title, url: url }).catch(() => {});
    } else {
        navigator.clipboard.writeText(url).then(() => {
            const btn = document.getElementById('shareBtn');
            if (btn) {
                const orig = btn.innerHTML;
                btn.innerHTML = '<i class="bi bi-check"></i> Link Copied!';
                setTimeout(() => { btn.innerHTML = orig; }, 2000);
            }
        });
    }
}

// Lazy load images
document.addEventListener('DOMContentLoaded', function() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        }, { rootMargin: '100px' });
        lazyImages.forEach(img => observer.observe(img));
    } else {
        lazyImages.forEach(img => { img.src = img.dataset.src; });
    }
});

// Price range display
function updatePriceLabel(val, id) {
    const el = document.getElementById(id);
    if (el) {
        if (val >= 100) {
            el.textContent = (val / 100).toFixed(val % 100 === 0 ? 0 : 2) + ' Cr';
        } else {
            el.textContent = val + ' Lakhs';
        }
    }
}

// Mobile filter toggle
function toggleFilter() {
    const sidebar = document.getElementById('filterSidebar');
    if (sidebar) {
        sidebar.classList.toggle('d-none');
        sidebar.classList.toggle('d-block');
    }
}
