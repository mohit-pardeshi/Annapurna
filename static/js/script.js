document.addEventListener("DOMContentLoaded", () => {
    /* ═══════════════════════════════════════════
       PAGE LOADER — side-loading transition
       ═══════════════════════════════════════════ */

    const loader = document.getElementById("pageLoader");

    if (loader) {
        // Exit animation — slide loader out to the left
        window.requestAnimationFrame(() => {
            window.setTimeout(() => {
                loader.classList.add("loader-exit");
            }, 350);
        });

        // Remove from DOM after transition
        loader.addEventListener("transitionend", function onExit(e) {
            if (e.propertyName === "transform" && loader.classList.contains("loader-exit")) {
                loader.style.display = "none";
                loader.removeEventListener("transitionend", onExit);
            }
        });

        // Intercept internal link clicks for a smooth transition
        document.addEventListener("click", (e) => {
            const link = e.target.closest("a[href]");
            if (!link) return;

            const href = link.getAttribute("href");

            // Skip external links, anchors, mailto, tel, and JS links
            if (!href ||
                href.startsWith("#") ||
                href.startsWith("mailto:") ||
                href.startsWith("tel:") ||
                href.startsWith("javascript:") ||
                link.target === "_blank" ||
                link.hasAttribute("download")) {
                return;
            }

            // Only intercept same-origin links
            try {
                const url = new URL(href, window.location.origin);
                if (url.origin !== window.location.origin) return;
            } catch {
                return;
            }

            e.preventDefault();

            // Show loader sliding in from right
            loader.style.display = "flex";
            loader.classList.remove("loader-exit");
            loader.classList.add("loader-enter-right");

            window.requestAnimationFrame(() => {
                window.requestAnimationFrame(() => {
                    loader.classList.remove("loader-enter-right");
                    loader.classList.add("loader-slide-in");
                });
            });

            // Navigate after the slide-in completes
            window.setTimeout(() => {
                window.location.href = href;
            }, 520);
        });
    }

    /* ═══════════════════════════════════════════
       HERO SLIDER (Text + Dynamic Background Images)
       ═══════════════════════════════════════════ */

    const heroContent = document.getElementById("heroContent");
    const heroTitle = document.querySelector(".hero-content h1");
    const heroEyebrow = document.querySelector(".hero-content .eyebrow");
    const heroSubtitle = document.querySelector(".hero-subtitle");
    const dots = document.querySelectorAll(".hero-dots button");
    const previousButton = document.querySelector(".hero-arrow-left");
    const nextButton = document.querySelector(".hero-arrow-right");
    const bgSlides = document.querySelectorAll(".hero-bg-slide");

    const slides = [
        {
            eyebrow: "THE TASTE OF TRADITION",
            title: "Made with Purity,<br>Made for You",
            subtitle: "Premium Quality <span>•</span> Authentic Recipes <span>•</span> Irresistible Taste",
        },
        {
            eyebrow: "FESTIVE FAVOURITES",
            title: "Share the Joy<br>of Every Celebration",
            subtitle: "Thoughtful Gift Boxes <span>•</span> Traditional Sweets <span>•</span> Made with Love",
        },
        {
            eyebrow: "AUTHENTIC IN EVERY BITE",
            title: "Flavours That Feel<br>Like Home",
            subtitle: "Fresh Ingredients <span>•</span> Time-Honoured Recipes <span>•</span> Delivered with Care",
        },
    ];

    let currentSlide = 0;
    let sliderTimer;

    function showSlide(index) {
        currentSlide = (index + slides.length) % slides.length;
        const slide = slides[currentSlide];

        // 1. Cross-fade background images in sync
        if (bgSlides.length > 0) {
            bgSlides.forEach((bgSlide, slideIndex) => {
                bgSlide.classList.toggle("active", slideIndex === currentSlide);
            });
        }

        // 2. Animate text transition
        if (heroContent) {
            heroContent.style.opacity = "0";
            heroContent.style.transform = "translateY(12px)";

            window.setTimeout(() => {
                heroEyebrow.textContent = slide.eyebrow;
                heroTitle.innerHTML = slide.title;
                heroSubtitle.innerHTML = slide.subtitle;

                dots.forEach((dot, dotIndex) => {
                    dot.classList.toggle("active", dotIndex === currentSlide);
                });

                heroContent.style.opacity = "1";
                heroContent.style.transform = "translateY(0)";
            }, 220);
        }
    }

    function restartSlider() {
        window.clearInterval(sliderTimer);
        sliderTimer = window.setInterval(() => {
            showSlide(currentSlide + 1);
        }, 6000);
    }

    if (heroContent && heroTitle && heroEyebrow && heroSubtitle) {
        heroContent.style.transition = "opacity 0.35s ease, transform 0.35s ease";

        nextButton?.addEventListener("click", () => {
            showSlide(currentSlide + 1);
            restartSlider();
        });

        previousButton?.addEventListener("click", () => {
            showSlide(currentSlide - 1);
            restartSlider();
        });

        dots.forEach((dot, index) => {
            dot.addEventListener("click", () => {
                showSlide(index);
                restartSlider();
            });
        });

        restartSlider();
    }

    /* ═══════════════════════════════════════════
       3D HERO PARALLAX — mouse-reactive layers
       ═══════════════════════════════════════════ */

    const heroSection = document.getElementById("heroSection");
    const heroBgSlider = document.getElementById("heroBgSlider");
    const hero3dLayer = document.getElementById("hero3dLayer");
    const heroParticles = document.getElementById("heroParticles");

    if (heroSection && (heroBgSlider || hero3dLayer)) {
        heroSection.addEventListener("mousemove", (e) => {
            const rect = heroSection.getBoundingClientRect();
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            // Normalised offset from center (-1 to 1)
            const offsetX = (e.clientX - rect.left - centerX) / centerX;
            const offsetY = (e.clientY - rect.top - centerY) / centerY;

            // Subtle 3D parallax on active background image slider
            if (heroBgSlider) {
                heroBgSlider.style.transform = `scale(1.03) translate(${offsetX * -10}px, ${offsetY * -6}px)`;
            }

            // 3D rotation on shape layer
            if (hero3dLayer) {
                hero3dLayer.style.transform = `rotateY(${offsetX * 6}deg) rotateX(${offsetY * -4}deg) translateZ(20px)`;
            }

            // Content layer slight shift for depth
            if (heroContent) {
                heroContent.style.transform = `translate(${offsetX * 5}px, ${offsetY * 3}px)`;
            }

            // Particles drift
            if (heroParticles) {
                heroParticles.style.transform = `translate(${offsetX * 12}px, ${offsetY * 8}px)`;
            }
        });

        heroSection.addEventListener("mouseleave", () => {
            if (heroBgSlider) heroBgSlider.style.transform = "";
            if (hero3dLayer) hero3dLayer.style.transform = "";
            if (heroContent) heroContent.style.transform = "";
            if (heroParticles) heroParticles.style.transform = "";
        });
    }

    /* ═══════════════════════════════════════════
       ABOUT SECTION — 3D Tilt & Scroll Parallax
       ═══════════════════════════════════════════ */

    const aboutSection = document.getElementById("aboutSection");
    const about3dWrapper = document.getElementById("about3dWrapper");
    const about3dCard = document.getElementById("about3dCard");
    const aboutFloatingBadge = document.getElementById("aboutFloatingBadge");
    const aboutFloatingStat = document.getElementById("aboutFloatingStat");
    const aboutMediaImg = document.getElementById("aboutMediaImg");
    const aboutCardContent = document.getElementById("aboutCardContent");

    if (about3dWrapper && about3dCard) {
        // 1. Mouse-Move 3D Gyroscopic Tilt on Hover
        about3dWrapper.addEventListener("mousemove", (e) => {
            const rect = about3dWrapper.getBoundingClientRect();
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const offsetX = (e.clientX - rect.left - centerX) / centerX;
            const offsetY = (e.clientY - rect.top - centerY) / centerY;

            // Card 3D rotation
            const rotateY = offsetX * 16;
            const rotateX = offsetY * -12;
            about3dCard.style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg) translateZ(10px)`;

            // Depth pop on floating badge
            if (aboutFloatingBadge) {
                aboutFloatingBadge.style.transform = `translateZ(65px) translate(${offsetX * -14}px, ${offsetY * -12}px)`;
            }

            // Depth pop on floating stat pill
            if (aboutFloatingStat) {
                aboutFloatingStat.style.transform = `translateZ(70px) translate(${offsetX * -12}px, ${offsetY * -10}px)`;
            }

            // Background media inverse shift for realistic depth
            if (aboutMediaImg) {
                aboutMediaImg.style.transform = `scale(1.08) translate(${offsetX * -8}px, ${offsetY * -6}px)`;
            }

            // Inner quote text shift
            if (aboutCardContent) {
                aboutCardContent.style.transform = `translateZ(40px) translate(${offsetX * 6}px, ${offsetY * 4}px)`;
            }
        });

        about3dWrapper.addEventListener("mouseleave", () => {
            about3dCard.style.transform = "";
            if (aboutFloatingBadge) aboutFloatingBadge.style.transform = "";
            if (aboutFloatingStat) aboutFloatingStat.style.transform = "";
            if (aboutMediaImg) aboutMediaImg.style.transform = "";
            if (aboutCardContent) aboutCardContent.style.transform = "";
        });

        // 2. 3D Scroll Effect on Window Scroll
        let scrollTicking = false;
        window.addEventListener("scroll", () => {
            if (!scrollTicking) {
                window.requestAnimationFrame(() => {
                    if (aboutSection) {
                        const rect = aboutSection.getBoundingClientRect();
                        const windowHeight = window.innerHeight;

                        // Only apply when in or near viewport
                        if (rect.top < windowHeight && rect.bottom > 0) {
                            const scrollFactor = (rect.top + rect.height / 2 - windowHeight / 2) / (windowHeight / 2);
                            
                            if (!about3dWrapper.matches(":hover")) {
                                const tiltY = -5 + scrollFactor * 4;
                                const tiltX = 3 + scrollFactor * -3;
                                const floatY = scrollFactor * 14;

                                about3dCard.style.transform = `rotateY(${tiltY}deg) rotateX(${tiltX}deg) translateY(${floatY}px)`;
                                
                                if (aboutFloatingBadge) {
                                    aboutFloatingBadge.style.transform = `translateZ(55px) translateY(${scrollFactor * -8}px)`;
                                }
                                if (aboutFloatingStat) {
                                    aboutFloatingStat.style.transform = `translateZ(60px) translateY(${scrollFactor * -10}px)`;
                                }
                            }
                        }
                    }
                    scrollTicking = false;
                });
                scrollTicking = true;
            }
        });
    }

    /* ═══════════════════════════════════════════
       SCROLL REVEAL — with staggered delays
       ═══════════════════════════════════════════ */

    const revealItems = document.querySelectorAll("[data-reveal]");

    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("revealed");
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );

    revealItems.forEach((item) => revealObserver.observe(item));

    /* ═══════════════════════════════════════════
       NAVBAR SCROLL EFFECT
       ═══════════════════════════════════════════ */

    const navbar = document.querySelector(".main-navbar");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 30) {
            navbar?.classList.add("navbar-scrolled");
        } else {
            navbar?.classList.remove("navbar-scrolled");
        }
    });

    /* ═══════════════════════════════════════════
       ADD TO CART button feedback
       ═══════════════════════════════════════════ */

    document.querySelectorAll(".product-card .btn").forEach((button) => {
        button.addEventListener("click", () => {
            const originalText = button.textContent;
            button.textContent = "Added!";
            button.classList.remove("btn-outline-maroon");
            button.classList.add("btn-gold");

            window.setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove("btn-gold");
                button.classList.add("btn-outline-maroon");
            }, 1200);
        });
    });

    /* ═══════════════════════════════════════════
       AJAX CART QUANTITY INCREASE / DECREASE / REMOVE
       (Zero full-page reload, zero loading screen)
       ═══════════════════════════════════════════ */

    document.addEventListener("submit", (e) => {
        const form = e.target.closest(".cart-action-form");
        if (!form) return;

        e.preventDefault();

        const formData = new FormData(form);
        const actionUrl = form.getAttribute("action");
        const productId = formData.get("product_id");
        const actionType = formData.get("action");

        const submitBtn = form.querySelector("button");
        if (submitBtn) submitBtn.disabled = true;

        fetch(actionUrl, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json"
            }
        })
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Update navbar cart badges immediately
                const cartBadges = document.querySelectorAll(".cart-count");
                cartBadges.forEach(badge => {
                    badge.textContent = data.total_items;
                    badge.classList.add("badge-pop");
                    setTimeout(() => badge.classList.remove("badge-pop"), 300);
                });

                // Update cart page quantities and totals
                const itemArticle = document.getElementById(`cart-item-${productId}`);
                const qtyValEl = document.getElementById(`qty-val-${productId}`);
                const itemTotalEl = document.getElementById(`item-total-${productId}`);
                const cartSubtotal = document.getElementById("cartSubtotal");
                const cartTotal = document.getElementById("cartTotal");

                if (data.is_empty) {
                    const cartRow = document.getElementById("cartContentRow");
                    const emptyMsg = document.getElementById("emptyCartMessage");
                    if (cartRow) cartRow.remove();
                    if (emptyMsg) emptyMsg.classList.remove("d-none");
                } else if (data.action === "remove" || data.quantity <= 0) {
                    if (itemArticle) {
                        itemArticle.style.transition = "all 0.3s ease";
                        itemArticle.style.opacity = "0";
                        itemArticle.style.transform = "translateX(-20px)";
                        setTimeout(() => itemArticle.remove(), 300);
                    }
                    if (cartSubtotal) cartSubtotal.textContent = `₹${data.cart_total}`;
                    if (cartTotal) cartTotal.textContent = `₹${data.cart_total}`;
                } else {
                    if (qtyValEl) {
                        qtyValEl.textContent = data.quantity;
                        qtyValEl.classList.add("qty-bump");
                        setTimeout(() => qtyValEl.classList.remove("qty-bump"), 250);
                    }
                    if (itemTotalEl) itemTotalEl.textContent = `₹${data.item_total}`;
                    if (cartSubtotal) cartSubtotal.textContent = `₹${data.cart_total}`;
                    if (cartTotal) cartTotal.textContent = `₹${data.cart_total}`;
                }
            }
        })
        .catch(err => {
            console.error("Cart update error, falling back to form submit:", err);
            form.submit();
        })
        .finally(() => {
            if (submitBtn) submitBtn.disabled = false;
        });
    });

    /* ═══════════════════════════════════════════
       NEWSLETTER FORM
       ═══════════════════════════════════════════ */

    const newsletterForm = document.querySelector(".newsletter-form");

    newsletterForm?.addEventListener("submit", (event) => {
        event.preventDefault();

        const emailInput = newsletterForm.querySelector("input[type='email']");
        const subscribeButton = newsletterForm.querySelector("button");

        if (!emailInput.value.trim()) {
            return;
        }

        subscribeButton.textContent = "Subscribed!";
        emailInput.value = "";

        window.setTimeout(() => {
            subscribeButton.textContent = "Subscribe";
        }, 1800);
    });

    /* ═══════════════════════════════════════════
       CONTACT FORM (if present)
       ═══════════════════════════════════════════ */

    const contactForm = document.querySelector(".contact-form");

    contactForm?.addEventListener("submit", (event) => {
        event.preventDefault();

        const submitButton = contactForm.querySelector("button[type='submit']");
        const originalText = submitButton.textContent;

        submitButton.textContent = "Message Sent!";
        submitButton.classList.remove("btn-outline-maroon");
        submitButton.classList.add("btn-gold");

        contactForm.reset();

        window.setTimeout(() => {
            submitButton.textContent = originalText;
            submitButton.classList.remove("btn-gold");
            submitButton.classList.add("btn-outline-maroon");
        }, 2500);
    });

    /* ═══════════════════════════════════════════
       ANIMATED STAT COUNTER (About page)
       ═══════════════════════════════════════════ */

    const statNumbers = document.querySelectorAll(".stat-number[data-target]");

    if (statNumbers.length > 0) {
        const counterObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        counterObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.4 }
        );

        statNumbers.forEach((el) => counterObserver.observe(el));
    }

    function animateCounter(element) {
        const target = parseInt(element.getAttribute("data-target"), 10);
        const suffix = element.getAttribute("data-suffix") || "";
        const duration = 2000;
        const start = performance.now();

        function tick(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const ease = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(ease * target);

            element.textContent = current.toLocaleString("en-IN") + suffix;

            if (progress < 1) {
                window.requestAnimationFrame(tick);
            }
        }

        window.requestAnimationFrame(tick);
    }

    /* ═══════════════════════════════════════════
       CHECKOUT PAGE INTERACTIVITY
       ═══════════════════════════════════════════ */

    const checkoutForm = document.getElementById("checkoutOrderForm");

    if (checkoutForm) {
        // 1. Payment subpanel toggling
        const payRadios = checkoutForm.querySelectorAll("input[name='payment_method']");
        const panelUpi = document.getElementById("panelUpi");
        const panelCard = document.getElementById("panelCard");

        function updatePaymentPanels() {
            const selected = checkoutForm.querySelector("input[name='payment_method']:checked")?.value;
            if (panelUpi) {
                panelUpi.classList.toggle("d-none", selected !== "upi");
            }
            if (panelCard) {
                panelCard.classList.toggle("d-none", selected !== "card");
            }
        }

        payRadios.forEach(radio => {
            radio.addEventListener("change", updatePaymentPanels);
        });
        updatePaymentPanels();

        // 2. Coupon Chips Click to Autofill & Apply
        const promoChips = document.querySelectorAll(".promo-chip");
        const couponInput = document.getElementById("couponCodeInput");
        const btnApplyCoupon = document.getElementById("btnApplyCoupon");
        const btnRemoveCoupon = document.getElementById("btnRemoveCoupon");

        promoChips.forEach(chip => {
            chip.addEventListener("click", () => {
                const code = chip.getAttribute("data-code");
                if (couponInput && code) {
                    couponInput.value = code;
                    applyCouponAjax(code, "apply");
                }
            });
        });

        if (btnApplyCoupon) {
            btnApplyCoupon.addEventListener("click", () => {
                const code = couponInput?.value.trim();
                if (code) {
                    applyCouponAjax(code, "apply");
                }
            });
        }

        if (btnRemoveCoupon) {
            btnRemoveCoupon.addEventListener("click", () => {
                applyCouponAjax("", "remove");
            });
        }

        function applyCouponAjax(code, action) {
            const csrfToken = checkoutForm.querySelector("input[name='csrfmiddlewaretoken']")?.value;
            const formData = new FormData();
            formData.append("coupon_code", code);
            formData.append("action", action);
            formData.append("csrfmiddlewaretoken", csrfToken);

            fetch("/checkout/apply-coupon/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json"
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const discountRow = document.getElementById("rowDiscount");
                    const summaryDiscount = document.getElementById("summaryDiscount");
                    const summaryTax = document.getElementById("summaryTax");
                    const summaryGrandTotal = document.getElementById("summaryGrandTotal");
                    const btnTotalDisplay = document.getElementById("btnTotalDisplay");
                    const feedback = document.getElementById("couponFeedback");

                    if (action === "apply") {
                        if (discountRow) discountRow.classList.remove("d-none");
                        if (summaryDiscount) summaryDiscount.textContent = `- ₹${data.discount_amount}`;
                        if (summaryTax) summaryTax.textContent = `₹${data.tax_amount}`;
                        if (summaryGrandTotal) summaryGrandTotal.textContent = `₹${data.total_amount}`;
                        if (btnTotalDisplay) btnTotalDisplay.textContent = data.total_amount;

                        if (feedback) {
                            feedback.innerHTML = `
                                <div class="alert alert-success py-1 px-2 mb-0 small d-flex align-items-center justify-content-between">
                                    <span><i class="bi bi-check-circle-fill me-1"></i> ${data.message}</span>
                                    <strong>- ₹${data.discount_amount}</strong>
                                </div>`;
                        }

                        if (btnApplyCoupon) {
                            btnApplyCoupon.outerHTML = `<button type="button" class="btn btn-outline-danger" id="btnRemoveCoupon">Remove</button>`;
                            const newRemoveBtn = document.getElementById("btnRemoveCoupon");
                            newRemoveBtn?.addEventListener("click", () => applyCouponAjax("", "remove"));
                        }
                        if (couponInput) couponInput.setAttribute("readonly", "true");
                    } else {
                        window.location.reload();
                    }
                } else {
                    const feedback = document.getElementById("couponFeedback");
                    if (feedback) {
                        feedback.innerHTML = `
                            <div class="alert alert-danger py-1 px-2 mb-0 small">
                                <i class="bi bi-exclamation-triangle-fill me-1"></i> ${data.message}
                            </div>`;
                    }
                }
            })
            .catch(err => {
                console.error("Coupon error:", err);
            });
        }

        // 3. Form submit feedback
        checkoutForm.addEventListener("submit", (e) => {
            const formValid = checkoutForm.checkValidity();
            if (formValid) {
                const btn = document.getElementById("placeOrderBtn");
                if (btn) {
                    btn.disabled = true;
                    btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Placing Your Order...`;
                }
            }
        });
    }
});