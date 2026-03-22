import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Mascot = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [visible, setVisible] = useState(false);
    const [bubbleVisible, setBubbleVisible] = useState(true);
    const [currentOffer, setCurrentOffer] = useState(null);
    const [availableOffers, setAvailableOffers] = useState([]);
    const [pos, setPos] = useState({ bottom: '30px', right: '30px', side: 'right' });

    const offers = [
        {
            title: "Flash Offer! 🔥",
            name: "Ariel Matic",
            image: "/static/images/ariel matic liquid detergent.jpg",
            discount: "50% OFF TODAY",
            tagline: "Save Big! Tap to add this offer to your cart 🛒✨",
            color: '#22c55e'
        },
        {
            title: "Limited Deal! ⚡",
            name: "Oreo Biscuits",
            image: "/static/images/oreo.jpeg",
            discount: "BUY 1 GET 1 FREE",
            tagline: "Snack time just got better! Limited stock 🍪",
            color: '#3b82f6'
        },
        {
            title: "Daily Special! ✨",
            name: "Maaza Juice",
            image: "/static/images/slice.jpeg",
            discount: "FLAT 30% OFF",
            tagline: "Refresh your day with some mango magic! 🥭",
            color: '#f59e0b'
        },
        {
            title: "Mega Sale! 📦",
            name: "Surf Excel",
            image: "/static/images/surf excel washing powder.jpg",
            discount: "EXTRA ₹100 OFF",
            tagline: "Best time to stock up on essentials! 🧺",
            color: '#0ea5e9'
        },
        {
            title: "Quick Snack! 🍟",
            name: "Lays Classic",
            image: "/static/images/lays.jpeg",
            discount: "FREE GIFT",
            tagline: "Free pack on orders above ₹499! 😋",
            color: '#ef4444'
        }
    ];

    const positions = [
        { bottom: '30px', right: '30px', top: 'auto', left: 'auto', side: 'right' },
        { bottom: '30px', left: '30px', top: 'auto', right: 'auto', side: 'left' },
        { top: '30px', right: '20px', bottom: 'auto', left: 'auto', side: 'right' },
        { top: '100px', left: '20px', bottom: 'auto', right: 'auto', side: 'left' },
    ];

    // Only show on dashboard/customer pages
    const dashboardPages = ['/home', '/scanner', '/search', '/history', '/product'];
    const shouldShow = dashboardPages.some(path => location.pathname.startsWith(path));

    useEffect(() => {
        if (shouldShow) {
            const fetchAndFilterOffers = async () => {
                try {
                    // Fetch offers from backend
                    const offersRes = await axios.get('/api/offers');
                    const dynamicOffers = offersRes.data.map(o => ({
                        title: o.title,
                        name: o.product_name,
                        image: o.image,
                        discount: o.discount_label,
                        tagline: o.tagline,
                        color: o.color
                    }));

                    const res = await axios.get('/api/stock');
                    const stock = res.data;

                    // Filter dynamic offers against actual stock
                    const filtered = dynamicOffers.filter(offer => {
                        const product = stock.find(p =>
                            (p.product_name || p.name || "").toLowerCase().includes(offer.name.toLowerCase()) &&
                            (p.quantity > 0)
                        );
                        return !!product;
                    });

                    let finalOffers = filtered;

                    // If no dynamic offers are in stock, pick any 5 available products
                    if (filtered.length === 0) {
                        const inStock = stock.filter(p => p.quantity > 0);
                        finalOffers = inStock.slice(0, 5).map(p => ({
                            title: "Smart Pick! ✨",
                            name: p.product_name || p.name,
                            image: p.image || "/static/images/placeholder.svg",
                            discount: "FRESH STOCK",
                            tagline: `Only ${p.quantity} left in stock! Grab yours now 🛍️`,
                            color: '#6366f1'
                        }));
                    }

                    setAvailableOffers(finalOffers);

                    if (finalOffers.length > 0) {
                        const initialOffer = finalOffers[Math.floor(Math.random() * finalOffers.length)];
                        setCurrentOffer(initialOffer);
                        const initialPos = positions[Math.floor(Math.random() * positions.length)];
                        setPos(initialPos);
                        const timer = setTimeout(() => setVisible(true), 2000);
                        return () => clearTimeout(timer);
                    }
                } catch (err) {
                    console.error("Mascot failed to fetch data:", err);
                    // Minimal fallback
                    setVisible(false);
                }
            };

            fetchAndFilterOffers();

            const interval = setInterval(() => {
                if (availableOffers.length > 0) {
                    const randomOffer = availableOffers[Math.floor(Math.random() * availableOffers.length)];
                    const randomPos = positions[Math.floor(Math.random() * positions.length)];
                    setCurrentOffer(randomOffer);
                    setPos(randomPos);
                }
            }, 5000); // 5 seconds between roams to be less distracting

            return () => clearInterval(interval);
        } else {
            setVisible(false);
        }
    }, [shouldShow, location.pathname, availableOffers.length]);

    if (!visible || !currentOffer) return null;

    const emojis = ['🛒', '✨', '🔥', '🍎', '🍫', '🛍️', '💰', '🏷️', '📦', '🎁', '🚀'];

    return (
        <div style={{
            position: 'fixed',
            bottom: pos.bottom,
            right: pos.right,
            top: pos.top,
            left: pos.left,
            zIndex: 10000,
            display: 'flex',
            flexDirection: 'column',
            alignItems: pos.side === 'right' ? 'flex-end' : 'flex-start',
            pointerEvents: 'none',
            transition: 'all 2.5s cubic-bezier(0.4, 0, 0.2, 1)',
            animation: 'roam 15s linear infinite'
        }}>
            {/* Continuous Floating Emojis Effect */}
            <div style={{ position: 'absolute', bottom: '60px', left: '50%', transform: 'translateX(-50%)' }}>
                {[...Array(6)].map((_, i) => (
                    <span key={i} style={{
                        position: 'absolute',
                        fontSize: '1.2rem',
                        animation: `floatParticle ${2 + i}s linear infinite`,
                        animationDelay: `${i * 0.5}s`,
                        opacity: 0,
                        zIndex: -1
                    }}>
                        {emojis[Math.floor(Math.random() * emojis.length)]}
                    </span>
                ))}
            </div>

            {/* Speech Bubble */}
            {bubbleVisible && (
                <div
                    key={`${currentOffer.name}-${pos.side}`}
                    className="bubble-premium fade-in"
                    onClick={() => navigate('/search', { state: { query: currentOffer.name } })}
                    style={{
                        background: `linear-gradient(135deg, ${currentOffer.color} 0%, ${currentOffer.color}dd 100%)`,
                        backdropFilter: 'blur(16px) saturate(180%)',
                        padding: '24px',
                        borderRadius: pos.side === 'right' ? '32px 32px 4px 32px' : '32px 32px 32px 4px',
                        boxShadow: `0 25px 50px -12px ${currentOffer.color}44, inset 0 0 0 1px rgba(255, 255, 255, 0.3)`,
                        marginBottom: '20px',
                        width: '260px',
                        pointerEvents: 'auto',
                        cursor: 'pointer',
                        animation: 'floatBubble 3.1s ease-in-out infinite'
                    }}
                >
                    <div style={{
                        fontWeight: '900',
                        letterSpacing: '-0.02em',
                        color: 'white',
                        fontSize: '1.1rem',
                        marginBottom: '16px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                        textShadow: '0 2px 4px rgba(0,0,0,0.1)'
                    }}>
                        <span style={{ fontSize: '1.4rem' }}>✨</span>
                        {currentOffer.title}
                    </div>

                    <div style={{
                        background: 'rgba(255,255,255,0.95)',
                        borderRadius: '20px',
                        padding: '16px',
                        marginBottom: '16px',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '16px',
                        position: 'relative',
                        overflow: 'hidden'
                    }}>
                        <div style={{
                            position: 'absolute',
                            top: '-20%',
                            right: '-20%',
                            width: '60%',
                            height: '60%',
                            background: currentOffer.color,
                            opacity: '0.08',
                            borderRadius: '50%',
                            filter: 'blur(30px)'
                        }} />

                        <div style={{
                            width: '60px',
                            height: '60px',
                            background: 'white',
                            borderRadius: '12px',
                            padding: '6px',
                            border: '1px solid #f1f5f9',
                            zIndex: 1,
                            flexShrink: 0
                        }}>
                            <img 
                                src={currentOffer.image || 'https://placehold.co/100'} 
                                onError={(e) => { e.target.onerror = null; e.target.src = `https://placehold.co/400x400/f1f5f9/94a3b8.png?text=${encodeURIComponent(currentOffer.name)}` }}
                                style={{ width: '100%', height: '100%', objectFit: 'contain' }} 
                                alt="" 
                            />
                        </div>
                        <div style={{ flex: 1, zIndex: 1 }}>
                            <div style={{ fontSize: '0.85rem', fontWeight: '800', color: '#1e293b', lineHeight: '1.2' }}>{currentOffer.name}</div>
                            <div style={{
                                fontSize: '0.8rem',
                                fontWeight: '900',
                                color: currentOffer.color,
                                marginTop: '4px',
                                animation: 'pulseDiscount 1.5s ease-in-out infinite'
                            }}>
                                {currentOffer.discount}
                            </div>
                        </div>
                    </div>

                    <div style={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.9)', fontWeight: '600', lineHeight: '1.5', padding: '0 4px', textShadow: '0 1px 2px rgba(0,0,0,0.1)' }}>
                        {currentOffer.tagline}
                    </div>
                </div>
            )}

            {/* 3D Mascot Image */}
            <div style={{
                width: '140px',
                height: '140px',
                cursor: 'pointer',
                pointerEvents: 'auto',
                animation: 'floatMascot 4s ease-in-out infinite',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }} onClick={() => setBubbleVisible(!bubbleVisible)}>
                <img
                    src="/mascot-removebg-preview.png"
                    alt="Assistant Mascot"
                    style={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'contain',
                        filter: 'drop-shadow(0 20px 40px rgba(0, 0, 0, 0.15))'
                    }}
                />
            </div>

            <style>{`
                @keyframes floatMascot {
                    0%, 100% { transform: translateY(0) rotate(0); }
                    50% { transform: translateY(-12px) rotate(4deg); }
                }
                @keyframes floatBubble {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-8px); }
                }
                @keyframes pulseDiscount {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.05); opacity: 0.8; }
                }
                @keyframes slideInUp {
                    from { transform: translateY(30px) scale(0.9); opacity: 0; }
                    to { transform: translateY(0) scale(1); opacity: 1; }
                }
                .fade-in {
                    animation: slideInUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
                }
                @keyframes floatParticle {
                    0% { transform: translateY(0) scale(0.5); opacity: 0; }
                    20% { opacity: 1; }
                    80% { opacity: 0.8; }
                    100% { transform: translateY(-120px) scale(1.2); opacity: 0; }
                }
                @keyframes roam {
                    0% { transform: translate(0, 0); }
                    25% { transform: translate(-20px, -20px); }
                    50% { transform: translate(20px, -10px); }
                    75% { transform: translate(-10px, 20px); }
                    100% { transform: translate(0, 0); }
                }
                .bubble-premium {
                    transition: all 0.5s ease;
                }
            `}</style>
        </div>
    );
};

export default Mascot;
