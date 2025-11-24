// Sistema de Modo Escuro/Claro
function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const button = document.querySelector('.theme-toggle i');
    
    if (document.body.classList.contains('dark-mode')) {
        button.className = 'fas fa-sun';
        localStorage.setItem('theme', 'dark');
    } else {
        button.className = 'fas fa-moon';
        localStorage.setItem('theme', 'light');
    }
}

// Carregar tema salvo
document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        const button = document.querySelector('.theme-toggle i');
        if (button) button.className = 'fas fa-sun';
    }
});

// Sistema de notificação
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check' : 'exclamation'}-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Estilos da notificação
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        font-weight: 500;
        min-width: 300px;
        border-left: 4px solid ${type === 'success' ? '#059669' : '#dc2626'};
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 4 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Adicionar animações CSS
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .notification-content i {
        font-size: 1.25rem;
    }
`;
document.head.appendChild(notificationStyles);

// Função para adicionar ao carrinho
async function addToCart(productId) {
    try {
        const response = await fetch(`/add_to_cart/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('✅ Produto adicionado ao carrinho!');
            updateCartCounter();
        } else {
            showNotification('❌ ' + result.message, 'error');
        }
    } catch (error) {
        showNotification('❌ Erro de conexão', 'error');
        console.error('Error:', error);
    }
}

// Atualizar contador do carrinho
async function updateCartCounter() {
    try {
        const response = await fetch('/cart/count');
        const data = await response.json();
        
        const cartCounter = document.querySelector('.cart-counter');
        if (cartCounter) {
            cartCounter.textContent = data.count;
            cartCounter.style.display = data.count > 0 ? 'flex' : 'none';
        }
    } catch (error) {
        console.error('Error updating cart counter:', error);
    }
}

// Efeitos de hover para os cards de produto
document.addEventListener('DOMContentLoaded', function() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Inicializar contador do carrinho
    updateCartCounter();
});