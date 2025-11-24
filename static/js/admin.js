// Sistema de abas do admin
function openTab(tabName) {
    // Esconder todas as abas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remover active de todos os botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Mostrar aba selecionada
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Modal para produtos
let currentEditingProduct = null;

function showProductForm(product = null) {
    currentEditingProduct = product;
    const modal = document.getElementById('productModal');
    const form = document.getElementById('productForm');
    const title = document.getElementById('modalTitle');
    
    if (product) {
        title.textContent = 'Editar Produto';
        // Preencher formulário com dados do produto
        Object.keys(product).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                if (input.type === 'checkbox') {
                    input.checked = product[key];
                } else {
                    input.value = product[key];
                }
            }
        });
    } else {
        title.textContent = 'Adicionar Produto';
        form.reset();
    }
    
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('productModal').style.display = 'none';
    currentEditingProduct = null;
}

// Fechar modal ao clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('productModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Gerenciar produtos
async function saveProduct(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    data.price = parseFloat(data.price);
    data.stock = parseInt(data.stock);
    data.featured = data.featured === 'on';
    
    try {
        const url = currentEditingProduct 
            ? `/admin/api/products/${currentEditingProduct.id}`
            : '/admin/api/products';
            
        const method = currentEditingProduct ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification(currentEditingProduct ? '✅ Produto atualizado!' : '✅ Produto adicionado!');
            closeModal();
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification('❌ ' + result.message, 'error');
        }
    } catch (error) {
        showNotification('❌ Erro de conexão', 'error');
        console.error('Error:', error);
    }
}

async function editProduct(productId) {
    try {
        const response = await fetch(`/admin/api/products/${productId}`);
        const product = await response.json();
        showProductForm(product);
    } catch (error) {
        showNotification('❌ Erro ao carregar produto', 'error');
        console.error('Error:', error);
    }
}

async function deleteProduct(productId) {
    if (!confirm('🗑️ Tem certeza que deseja excluir este produto?')) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/api/products/${productId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('✅ Produto excluído!');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification('❌ ' + result.message, 'error');
        }
    } catch (error) {
        showNotification('❌ Erro ao excluir produto', 'error');
        console.error('Error:', error);
    }
}

// Gerenciar usuários
async function deleteUser(userId) {
    if (!confirm('🗑️ Tem certeza que deseja excluir este usuário?')) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/api/users/${userId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('✅ Usuário excluído!');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification('❌ ' + result.message, 'error');
        }
    } catch (error) {
        showNotification('❌ Erro ao excluir usuário', 'error');
        console.error('Error:', error);
    }
}

// Gráficos de analytics
function renderBrandChart(brandPreferences) {
    const chartContainer = document.getElementById('brandChart');
    if (!chartContainer) return;
    
    let chartHTML = '';
    Object.entries(brandPreferences).forEach(([brand, percentage]) => {
        const width = Math.max(percentage, 10); // Mínimo de 10% para visualização
        chartHTML += `
            <div class="brand-chart-item">
                <div class="brand-label">${brand}</div>
                <div class="brand-bar">
                    <div class="brand-fill" style="width: ${width}%; background: ${getBrandColor(brand)};"></div>
                    <span class="brand-percentage">${percentage}%</span>
                </div>
            </div>
        `;
    });
    
    chartContainer.innerHTML = chartHTML;
}

function getBrandColor(brand) {
    const colors = {
        'Nike': '#ff6b6b',
        'Adidas': '#4ecdc4',
        'Puma': '#45b7d1',
        'New Balance': '#96ceb4',
        'Mizuno': '#feca57',
        'Jordan': '#ff9ff3',
        'Vans': '#54a0ff'
    };
    return colors[brand] || '#6366f1';
}

// Inicializar admin
document.addEventListener('DOMContentLoaded', function() {
    // Renderizar gráfico de marcas se existir
    const brandDataElement = document.getElementById('brandData');
    if (brandDataElement) {
        const brandPreferences = JSON.parse(brandDataElement.textContent);
        renderBrandChart(brandPreferences);
    }
    
    // Adicionar estilos para o gráfico
    const chartStyles = document.createElement('style');
    chartStyles.textContent = `
        .brand-chart-item {
            margin-bottom: 1rem;
        }
        
        .brand-label {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }
        
        .brand-bar {
            background: var(--bg-secondary);
            border-radius: 1rem;
            height: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .brand-fill {
            height: 100%;
            border-radius: 1rem;
            transition: width 1s ease;
            position: relative;
        }
        
        .brand-percentage {
            position: absolute;
            right: 1rem;
            top: 50%;
            transform: translateY(-50%);
            font-weight: 700;
            color: var(--text-primary);
            z-index: 2;
        }
    `;
    document.head.appendChild(chartStyles);
});