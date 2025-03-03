document.addEventListener('DOMContentLoaded', () => {
    const assistantIcon = document.getElementById('assistant-icon');
    const assistantBox = document.getElementById('assistant-box');
    const faqList = document.getElementById('faq-list');
    const responseBox = document.getElementById('response-box');
    const responseText = document.getElementById('response-text');
    const closeResponse = document.getElementById('close-response');

    // Base de perguntas frequentes
    const faqData = [
        "Como faço para emprestar um livro?",
        "Como renovar um empréstimo?",
        "Onde vejo meus livros emprestados?",
        "Como faço login no sistema?",
        "Como fazer logout?",
        "Como adicionar um livro?",
        "Como gerenciar tags?",
        "Como fazer backup?",
        "Para que serve o botão de vídeo?",
        "O que posso fazer como administrador?",
        "Como pesquisar livros?"
    ];

    // Abrir/Fechar o balão de perguntas
assistantIcon.addEventListener('click', () => {
    if (assistantBox.classList.contains('hidden')) {
        // Exibe temporariamente a caixa para calcular sua altura
        assistantBox.style.display = 'flex';
        assistantBox.style.visibility = 'hidden'; // Torna invisível enquanto calculamos
        const boxHeight = assistantBox.offsetHeight; // Obtém a altura real da caixa

        // Calcula a posição da caixa de perguntas com base na posição do ícone
        const iconRect = assistantIcon.getBoundingClientRect();

        // Posiciona a caixa à esquerda do ícone
        assistantBox.style.bottom = `${window.innerHeight - iconRect.bottom}px`; // Alinha a parte inferior da caixa com o ícone
        assistantBox.style.left = `${iconRect.left - assistantBox.offsetWidth - 10}px`; // À esquerda do ícone, com um pequeno espaçamento

        // Remove a invisibilidade e exibe a caixa
        assistantBox.style.visibility = 'visible';
        assistantBox.classList.remove('hidden');

        // Carrega as perguntas
        loadFAQ();
    } else {
        // Oculta a caixa de perguntas
        assistantBox.classList.add('hidden');
        assistantBox.style.display = 'none';
    }
});
    // Carregar perguntas frequentes
function loadFAQ() {
    faqList.innerHTML = ''; // Limpar lista anterior
    faqData.forEach(question => {
        const li = document.createElement('li');
        li.textContent = question;
        li.style.cursor = 'pointer';
        li.addEventListener('click', () => handleQuestionClick(question));
        faqList.appendChild(li);
    });
}
    // Lidar com o clique em uma pergunta
    function handleQuestionClick(question) {
        const knowledgeBase = {
            "como faço para emprestar um livro": "Para emprestar um livro, navegue até a página do livro desejado, clique no botão 'Emprestar' e confirme a operação. O prazo padrão é de 14 dias.",
            "como renovar um empréstimo": "Para renovar um empréstimo, acesse a seção 'Livros Emprestados' e clique no botão 'Renovar' ao lado do livro que deseja renovar. Só é possível renovar se não houver reservas para o livro.",
            "onde vejo meus livros emprestados": "Seus livros emprestados podem ser visualizados na seção 'Livros Emprestados', acessível no menu superior (para administradores).",
            "como faço login no sistema": "Para fazer login, clique no botão 'Login' no canto superior direito e insira seu nome de usuário e senha.",
            "como fazer logout": "Para sair do sistema, clique no link 'Logout' no menu superior direito.",
            "como adicionar um livro": "Para adicionar um novo livro, você precisa ser administrador. Clique em 'Adicionar Livro' no menu superior e preencha o formulário com os detalhes do livro.",
            "como gerenciar tags": "Para gerenciar as tags (categorias) dos livros, você deve ser administrador. Acesse 'Gerenciar Tags' no menu superior para adicionar, editar ou remover tags.",
            "como fazer backup": "Para fazer backup do sistema, você deve ser administrador. Acesse 'Backup' no menu superior para iniciar o processo.",
            "para que serve o botão de vídeo": "O botão de vídeo com ícone de gato leva a um vídeo no YouTube que pode conter informações adicionais ou tutoriais sobre o sistema.",
            "o que posso fazer como administrador": "Como administrador, você pode adicionar livros, gerenciar tags, fazer backup do sistema, ver todos os livros emprestados e acessar o painel administrativo.",
            "como pesquisar livros": "Você pode pesquisar livros usando a barra de busca na página principal, filtrando por título, autor ou tags."
        };

        const response = knowledgeBase[question.toLowerCase().replace(/\?/g, '')] || "Desculpe, não tenho informações sobre isso.";
        responseText.textContent = response; // Exibe a resposta no balão
        responseBox.classList.remove('hidden'); // Mostra a caixa de resposta
        responseBox.style.display = 'block';
    }

    // Fechar a caixa de resposta
    closeResponse.addEventListener('click', () => {
        responseBox.classList.add('hidden');
        responseBox.style.display = 'none';
    });

    // Tornar o ícone arrastável
    let isDragging = false;
    let offsetX, offsetY;

    assistantIcon.addEventListener('mousedown', (e) => {
        isDragging = true;
        offsetX = e.clientX - assistantIcon.getBoundingClientRect().left;
        offsetY = e.clientY - assistantIcon.getBoundingClientRect().top;
        assistantIcon.style.cursor = 'grabbing';
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            let x = e.clientX - offsetX;
            let y = e.clientY - offsetY;

            // Limita o ícone dentro dos limites da janela
            const windowWidth = window.innerWidth;
            const windowHeight = window.innerHeight;
            const iconSize = 40; // Tamanho do ícone

            x = Math.max(0, Math.min(x, windowWidth - iconSize)); // Impede que saia da borda direita
            y = Math.max(0, Math.min(y, windowHeight - iconSize)); // Impede que saia da borda inferior

            assistantIcon.style.left = `${x}px`;
            assistantIcon.style.top = `${y}px`;
        }
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
        assistantIcon.style.cursor = 'grab';
    });
});