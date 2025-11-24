// Função para atualizar quantidade no carrinho
async function updateQuantity(itemId, newQuantity) {
    try {
        const response = await fetch(`/update_cart/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: newQuantity })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Recarregar a página para atualizar os totais
            location.reload();
        } else {
            showNotification('❌ Erro ao atualizar carrinho', 'error');
        }
    } catch (error) {
        showNotification('❌ Erro de conexão', 'error');
        console.error('Error:', error);
    }
}

// Animações para o carrinho
document.addEventListener('DOMContentLoaded', function() {
    const cartItems = document.querySelectorAll('.cart-item');
    
    cartItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('fade-in-up');
    });
});

// Adicionar estilos de animação
const cartStyles = document.createElement('style');
cartStyles.textContent = `
    .cart-item {
        opacity: 0;
        transform: translateY(20px);
        animation: fadeInUp 0.5s ease forwards;
    }
    
    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .empty-cart {
        text-align: center;
        padding: 4rem 2rem;
    }
    
    .empty-cart i {
        font-size: 4rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
    }
    
    .empty-cart h3 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .empty-cart p {
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
`;
document.head.appendChild(cartStyles);